# Step: checkout-source.md
Agent: (scout/planner/worker/reviewer — reads .agents/agents/*.md)
Prompt:

Check out the reviewed source branch. Mechanical only.

Input: `{{workflow.input}}`
Evidence: `{{last.summary}}`

Never stash, reset, clean, or delete unrelated files.

`ready`: source branch bound. Include `workspace: {cwd: "<path>"}`.
`handoff`: transient fetch error.
`blocked`: dirty unrelated checkout or missing remote.


## Required ready response
Put the complete prior Evidence payload verbatim in `Completed`, followed by bound workspace cwd, branch, and HEAD.

# Completed
<complete fetched review evidence>
<workspace cwd, branch, and HEAD>

# Remaining
- None.

When Evidence is absent or incomplete, return `gaps` with exact missing fields so the workflow re-enters fetch.

Hand-off: read/write .workflows/state/<session-key>/state.json
