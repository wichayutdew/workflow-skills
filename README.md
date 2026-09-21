# workflow-skills

Portable guided workflows migrated from `pi-workflows`.

## Install

After this repository is pushed, install directly from GitHub; npm publication is not required:

```bash
npx skills add wichayutdew/workflow-skills
npx skills add wichayutdew/workflow-skills --all
npx skills add wichayutdew/workflow-skills --skill work
```

Update or remove installed skills:

```bash
npx skills update
npx skills remove work
npx skills remove --all
```

## Use

Invoke one of the five skills with a natural-language request:

- `work`
- `investigate`
- `mr-review`
- `mr-comment`
- `sprint-triage`

The skill derives workspace, Git, Jira, PR/MR, and integration context from the request and active environment. It asks only for missing business information, authorization, or access. It does not require workflow variables, restart metadata, or a state path. When the harness supports subagents, every stage runs in a fresh subagent that receives only the request, previous stage artifact, and stage prompt; the parent does not pass conversational context between stages.

## Pi adapter

Each installed skill includes `scripts/run-pi.py`. When invoked from Pi inside Herdr, the skill directs Pi to launch this adapter automatically. To launch it directly from a skill directory, run:

```bash
python3 scripts/run-pi.py --stage intake --request "Investigate the failing deployment for PROJ-123"
```

The adapter runs exactly one requested stage in a fresh interactive Pi process with its configured role, model, and thinking level. Inside Herd, it opens an unfocused background horizontal split, waits for the child completion tool to write and signal a JSON handoff, and then closes that child pane. It prints the handoff path and validated contents from `${XDG_STATE_HOME:-$HOME/.local/state}/workflow-skills/`; the invoking main agent decides whether to run another stage, retry, block, or request approval.

If Pi or Herd is unavailable, use a fresh subagent for each stage when the harness supports subagents. If no subagent capability exists, execute the guided stages in the main agent pane. In both fallbacks, use the root `SKILL.md` prompts without Pi model selection or process isolation.
