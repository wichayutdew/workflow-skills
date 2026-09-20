---
name: work
description: Use when running the full agent work pipeline (intake -> plan -> workspace -> implement -> verify -> publish) with fresh agent per step.
---

# Work Pipeline

Master skill for `/work`. Invokes sub-steps sequentially with handoff via `.workflows/state/<session-key>/state.json`. Each step reads `.agents/agents/<agent>.md` and starts a fresh agent context.

Transition support: verify (and other review steps) can circle back to previous steps (e.g., implement) when `.workflows/state/*.json` status is `gaps`, `back`, or `invalid`. `invoke.py` reads previous state and prints back-circulation.

## Gate (Plan Step — Artifact Contract)
When running `plan.md`, enforce artifactContract:
- maxChars: 30000
- Required headings: Goal/Acceptance Criteria, Non Goal, Implementation Steps and Tests, Validation, Risks/Decisions Needed, Publications Contract/Metadata, Execution appendix (machine-readable JSON)

Sub-steps: `intake.md`, `plan.md`, `implement.md`, `verify.md`, `publish.md`
Agent roles: scout, planner, worker, reviewer, scout.

## Invocation
Run `.workflows/invoke.py <step-file>` (e.g., `.workflows/invoke.py .agents/skills/work/intake.md`).
The script parses `Agent profile:` and `model:` from embedded frontmatter, reads `.agents/agents/<agent>.md`, and passes agent config + step prompt + `.workflows/state/<session-key>/state.json` to a fresh agent session.

## Extension Features Ported
- maxStepVisits: 30
- summaryMaxChars: 30000
- permissions: [read, ls, bash, edit, write, mcp] per step; bash unrestricted
- mcp: [atlassian, context7, sourcegraph, glean, gh_grep, github/*, gitlab] (step-specific)
- gate (plan step only): artifactContract with maxChars 30000; required headings per original YAML
- workspace (prepare-workspace only): bindOn [ready], allowedRoots [~/repositories/worktrees]
