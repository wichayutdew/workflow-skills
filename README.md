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
python3 scripts/run-pi.py "Investigate the failing deployment for PROJ-123"
```

The adapter runs each stage in a fresh Pi process with its configured role, model, and thinking level. Inside Herdr, it opens an unfocused background horizontal split for that stage, waits for the artifact, and closes that child pane after its artifact is captured. It manages artifacts under `${XDG_STATE_HOME:-$HOME/.local/state}/workflow-skills/` and stops at approval gates. Resume an approved run with the exact command it prints.

If Pi, Herdr, or a configured model is unavailable, use the root `SKILL.md` stages. Other harnesses use a fresh subagent for every stage when supported; otherwise they retain the same guided workflow in the active session, without Pi model selection or process isolation.
