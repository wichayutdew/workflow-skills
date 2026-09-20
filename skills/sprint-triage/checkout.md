# Stage: checkout

## Pi profile

- Role: `scout`
- Model: `gateway/gemini-3.8-flash`
- Thinking: `low`

The Pi adapter supplies the invoking request and previous stage artifact automatically. In a portable session, use the active conversation request and prior artifacts.

---

Create the knowledge-base worktree. Mechanical only.

Input: `the invoking request`
Approved plan: `the approved plan artifact from this run`

Read `~/.pi/agent/workflows/steps/sprint-triage/sprint-triage.yaml`. Dates must be `YYYY-MM-DD YYYY-MM-DD`. Create a linked worktree and add `docs/sprint-triage-<start>-to-<end>`. Missing content dir or index is fine.

`ready`: `workspace: {cwd: "<worktree-path>"}`.
`handoff`: transient mechanical worktree work remains and requires no user input.
`blocked`: bad dates, missing repository information, or an unsafe Git state requiring user input; put the question in `remaining`.
