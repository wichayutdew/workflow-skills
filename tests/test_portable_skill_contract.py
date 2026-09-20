import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
EXPECTED = {
    "work": ("intake", "prepare-workspace.md"),
    "investigate": ("intake", "research.md"),
    "mr-review": ("fetch", "findings.md"),
    "mr-comment": ("fetch", "checkout-source.md"),
    "sprint-triage": ("collect", "collect.md"),
}
REQUIRED_HEADINGS = {
    "work": ("Goal/Acceptance Criteria", "Non Goal", "Implementation Steps and Tests", "Validation", "Risks/Decisions Needed", "Publications Contract/Metadata", "Execution appendix (machine-readable)"),
    "investigate": ("Report destination", "Goal/Acceptance Criteria", "Non Goal", "Investigation Resources", "Questions"),
    "mr-review": ("Reviews", "Publication contract"),
    "mr-comment": ("Comments", "Implementation plan", "Validation", "Execution appendix (machine-readable)"),
    "sprint-triage": ("Knowledge base repository", "Report", "Ledger", "Confluence top append", "Guides", "Publication fragment", "Execution contract"),
}
FORBIDDEN = (
    "{{" + "workflow.",
    "{{" + "restart.",
    "{{" + "reviewed.",
    "." + "workflows/state",
    "invoke" + ".py",
    ".agents" + "/skills",
)
REQUIRED_PI_HERDR_ROUTE = (
    "When running in Pi inside Herdr (`HERDR_ENV=1`), run the bundled adapter",
    "Do not execute the stage prompts inline in that environment.",
)


class PortableSkillContractTests(unittest.TestCase):
    def test_public_skills_are_discoverable_and_self_contained(self):
        self.assertEqual({path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}, set(EXPECTED))
        for name, (start, required_prompt) in EXPECTED.items():
            root = SKILLS / name
            text = (root / "SKILL.md").read_text()
            self.assertIn(f"name: {name}", text)
            self.assertIn("## Portable execution contract", text)
            self.assertIn("## Pi adapter", text)
            self.assertIn("use a fresh subagent whenever the harness supports subagents", text)
            self.assertIn("do not give it or rely on parent conversational context", text)
            self.assertIn(required_prompt, text)
            self.assertTrue((root / "scripts" / "run-pi.py").is_file())
            for heading in REQUIRED_HEADINGS[name]:
                self.assertIn(heading, text)
            self.assertIn("submit the complete artifact to Plannotator", text)
            for required in REQUIRED_PI_HERDR_ROUTE:
                self.assertIn(required, text)
            self.assertNotEqual(start, "")
            adapter_text = (root / "scripts" / "run-pi.py").read_text()
            self.assertNotIn("'" + "limit':", adapter_text)
            self.assertIn('"herdr", "pane", "split"', adapter_text)
            self.assertIn('"--direction", "down"', adapter_text)
            self.assertIn('"herdr", "pane", "close", pane_id', adapter_text)
        readme = README.read_text()
        self.assertIn("When invoked from Pi inside Herdr, the skill directs Pi to launch this adapter automatically.", readme)
        self.assertIn("closes that child pane after its artifact is captured", readme)

    def test_no_extension_placeholders_or_stale_paths_remain(self):
        for path in SKILLS.rglob("*.md"):
            text = path.read_text()
            for forbidden in FORBIDDEN:
                self.assertNotIn(forbidden, text, path)
        self.assertTrue((SKILLS / "work" / "prepare-workspace.md").is_file())
        self.assertFalse((SKILLS / "work" / "publish.md").exists())

    def test_pi_adapters_render_first_command_without_pi(self):
        for name, (start, _) in EXPECTED.items():
            adapter = SKILLS / name / "scripts" / "run-pi.py"
            with tempfile.TemporaryDirectory() as state_dir:
                result = subprocess.run(
                    ["python3", str(adapter), "--dry-run", "example request"],
                    text=True,
                    capture_output=True,
                    env={**os.environ, "WORKFLOW_SKILLS_STATE_DIR": state_dir},
                )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'"stage": "{start}"', result.stdout)
            self.assertIn('"--model"', result.stdout)
            self.assertIn('"--thinking"', result.stdout)

    def test_pi_adapters_open_wait_and_close_herdr_stage_panes(self):
        expected_stage_counts = {
            "work": 2,
            "investigate": 2,
            "mr-review": 3,
            "mr-comment": 3,
            "sprint-triage": 2,
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            bin_directory = temporary_path / "bin"
            bin_directory.mkdir()
            log_path = temporary_path / "herdr.log"
            command_path = temporary_path / "herdr-command.txt"
            output_path = temporary_path / "herdr-output.txt"
            herdr = bin_directory / "herdr"
            herdr.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, subprocess, sys\n"
                "from pathlib import Path\n"
                "args = sys.argv[1:]\n"
                "log = Path(os.environ['FAKE_HERDR_LOG'])\n"
                "if args[:2] == ['pane', 'split']:\n"
                "    log.open('a').write('split\\n')\n"
                "    print(json.dumps({'result': {'pane': {'pane_id': 'fake:pane'}}}))\n"
                "elif args[:2] == ['pane', 'run']:\n"
                "    log.open('a').write('run\\n')\n"
                "    command = args[3]\n"
                "    Path(os.environ['FAKE_HERDR_COMMAND']).write_text(command)\n"
                "    result = subprocess.run(['fish', '-c', command], text=True, capture_output=True)\n"
                "    Path(os.environ['FAKE_HERDR_OUTPUT']).write_text(result.stdout + result.stderr)\n"
                "    result.check_returncode()\n"
                "elif args[:2] == ['pane', 'wait-output']:\n"
                "    marker = args[4]\n"
                "    command = Path(os.environ['FAKE_HERDR_COMMAND']).read_text()\n"
                "    output = Path(os.environ['FAKE_HERDR_OUTPUT']).read_text()\n"
                "    if marker in command or marker not in output:\n"
                "        log.open('a').write(f'wait-failed input={marker in command} output={marker in output} raw={output!r}\\n')\n"
                "        raise SystemExit('completion marker check failed')\n"
                "    log.open('a').write('wait-output\\n')\n"
                "elif args[:2] == ['pane', 'close']:\n"
                "    log.open('a').write('close\\n')\n"
                "else:\n"
                "    raise SystemExit(f'unexpected Herdr command: {args}')\n"
            )
            pi = bin_directory / "pi"
            pi.write_text(
                "#!/usr/bin/env python3\n"
                "print('## Machine-readable handoff')\n"
                "print('```json')\n"
                "print('{\\\"status\\\": \\\"ready\\\", \\\"remaining\\\": []}')\n"
                "print('```')\n"
            )
            herdr.chmod(0o755)
            pi.chmod(0o755)

            for name, stage_count in expected_stage_counts.items():
                log_path.write_text("")
                with tempfile.TemporaryDirectory() as state_directory:
                    result = subprocess.run(
                        [sys.executable, str(SKILLS / name / "scripts" / "run-pi.py"), "example request"],
                        text=True,
                        capture_output=True,
                        env={
                            **os.environ,
                            "PATH": f"{bin_directory}{os.pathsep}{os.environ['PATH']}",
                            "HERDR_ENV": "1",
                            "HERDR_PANE_ID": "fake:parent",
                            "FAKE_HERDR_LOG": str(log_path),
                            "FAKE_HERDR_COMMAND": str(command_path),
                            "FAKE_HERDR_OUTPUT": str(output_path),
                            "WORKFLOW_SKILLS_STATE_DIR": state_directory,
                        },
                    )
                self.assertEqual(result.returncode, 0, result.stderr + log_path.read_text())
                self.assertIn("approval required; resume with:", result.stdout)
                self.assertEqual(
                    log_path.read_text().splitlines(),
                    ["split", "run", "wait-output", "close"] * stage_count,
                )

    def test_pi_adapters_reject_empty_requests(self):
        for name in EXPECTED:
            adapter = SKILLS / name / "scripts" / "run-pi.py"
            result = subprocess.run(["python3", str(adapter)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("natural-language request is required", result.stderr)


if __name__ == "__main__":
    unittest.main()
