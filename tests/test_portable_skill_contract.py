import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
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
            self.assertNotEqual(start, "")
            adapter_text = (root / "scripts" / "run-pi.py").read_text()
            self.assertNotIn("'" + "limit':", adapter_text)
            self.assertIn('"herdr", "pane", "split"', adapter_text)
            self.assertIn('"--direction", "down"', adapter_text)
            self.assertIn('"herdr", "pane", "close", pane_id', adapter_text)

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

    def test_pi_adapters_reject_empty_requests(self):
        for name in EXPECTED:
            adapter = SKILLS / name / "scripts" / "run-pi.py"
            result = subprocess.run(["python3", str(adapter)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("natural-language request is required", result.stderr)


if __name__ == "__main__":
    unittest.main()
