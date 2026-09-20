---
name: mr-review
description: Use when running the mr-review pipeline with fresh agent per step.
---

# mr-review
Master skill. Sub-steps below. Hand-off via .workflows/state/<session-key>/state.json.

## Extension Features Ported
permissions: [read, ls, bash, mcp]; mcp: [github/*, gitlab]

## Transition Rules (per original `.pi/agent/workflows/mr-review.workflow.yaml`)
- mr-review sub-steps: fetch→findings (ready); $pause (blocked); findings→plan (ready); fetch (gaps); plan→publish-approved (ready); findings (gaps); publish-approved→$done (ready); $pause (blocked)
## Agent Profiles
Embedded per sub-step (`.agents/agents/*.md` profile included in each `.md`).