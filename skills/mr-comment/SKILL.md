---
name: mr-comment
description: Use when running the mr-comment pipeline with fresh agent per step.
---

# mr-comment
Master skill. Sub-steps below. Hand-off via .workflows/state/<session-key>/state.json.

## Extension Features Ported
permissions: [read, ls, bash, edit, write, mcp]; mcp: [github/*, gitlab, context7]

## Transition Rules (per original `.pi/agent/workflows/mr-comment.workflow.yaml`)
- mr-comment sub-steps: checkout-source→fetch (ready); $pause (blocked); fetch→implement (ready); checkout-source (gaps); implement→verify (ready); plan (gaps); plan→publish (ready); fetch (gaps); verify→publish (ready); implement (gaps); publish→$done (ready); $pause (blocked)
## Agent Profiles
Embedded per sub-step (`.agents/agents/*.md` profile included in each `.md`).