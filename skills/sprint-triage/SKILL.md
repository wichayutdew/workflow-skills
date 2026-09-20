---
name: sprint-triage
description: Use when running the sprint-triage pipeline with fresh agent per step.
---

# sprint-triage
Master skill. Sub-steps below. Hand-off via .workflows/state/<session-key>/state.json.

## Extension Features Ported
permissions: [read, ls, bash, mcp]; mcp: [atlassian, context7]

## Transition Rules (per original original workflow `sprint-triage.workflow.yaml`)
- sprint-triage sub-steps: checkout→collect (ready); $pause (blocked); collect→plan (ready); checkout (gaps); plan→implement (ready); collect (gaps); implement→publish (ready); plan (gaps); publish→$done (ready); $pause (blocked)
## Agent Profiles
Embedded per sub-step (`.agents/agents/*.md` profile included in each `.md`).