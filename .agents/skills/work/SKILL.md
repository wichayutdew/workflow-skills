---
name: work
description: Use when running the full agent work pipeline (intake -> plan -> workspace -> implement -> verify -> publish) with fresh agent per step.
---

# Work Pipeline

Master skill for `/work`. Invokes sub-steps sequentially with handoff via `.workflows/state/<session-key>/state.json`. Each step reads `.agents/agents/<agent>.md` and starts a fresh agent context.

Sub-steps: `intake.md`, `plan.md`, `implement.md`, `verify.md`, `publish.md`
Agent roles: scout, planner, worker, reviewer, scout.
