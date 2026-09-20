---
name: work
description: Use when running the full agent work pipeline (intake -> plan -> workspace -> implement -> verify -> publish) with fresh agent per step.
---

# Work Pipeline

Master skill for `/work`. Invokes sub-steps sequentially with handoff via `.workflows/state/<session-key>/state.json`. Each step reads `.agents/agents/<agent>.md` and starts a fresh agent context.

Sub-steps: `intake.md`, `plan.md`, `implement.md`, `verify.md`, `publish.md`
Agent roles: scout, planner, worker, reviewer, scout.

## Invocation
Run `.workflows/invoke.py <step-file>` (e.g., `.workflows/invoke.py .agents/skills/work/intake.md`).
The script parses `Agent profile:` and `model:` from embedded frontmatter, reads `.agents/agents/<agent>.md`, and passes agent config + step prompt + `.workflows/state/<session-key>/state.json` to a fresh agent session.
