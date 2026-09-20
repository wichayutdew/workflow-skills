---
name: investigate
description: Use when running the investigate pipeline with fresh agent per step.
---

# investigate
Master skill. Sub-steps below. Hand-off via .workflows/state/<session-key>/state.json.

## Extension Features Ported
permissions: [read, ls, bash, mcp]; mcp: [atlassian, context7, sourcegraph, glean]

## Transition Rules (per original `.pi/agent/workflows/investigate.workflow.yaml`)
- investigate sub-steps: intake→plan (ready); intake (gaps); plan→research (ready); intake (gaps); $pause (blocked); research→validate (ready); plan (gaps); validate→write-report (ready); research (gaps); $pause (blocked); write-report→$done (ready); $pause (blocked)
## Agent Profiles
Embedded per sub-step (`.agents/agents/*.md` profile included in each `.md`).