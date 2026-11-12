# workflow-skills

Portable workflows for software work, investigation reports, backlog breakdowns and hosted code reviews.

## Skills

| Skill | Purpose |
| --- | --- |
| [work](skills/work/SKILL.md) | Implement scoped changes using existing code, meaningful verification and approved delivery. |
| [investigate](skills/investigate/SKILL.md) | Investigate an idea, feature, technical or general question; refine an RFC or detailed report until the user is satisfied. |
| [breakdown](skills/breakdown/SKILL.md) | Refine a report into an epic and stories; create tracker items only after explicit approval of the complete backlog and destination. |
| [mr-review](skills/mr-review/SKILL.md) | Propose evidence-backed improvements and identify introduced regressions without waiting for CI. |
| [mr-comment](skills/mr-comment/SKILL.md) | Validate review feedback, apply approved fixes and deliver verified replies incrementally. |

## Install

Install this repository directly; npm publication is not required:

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

Invoke a skill with a natural-language request. The skill derives repository, tracker and review context from the request and active environment; no workflow engine, adapter, state-path argument or private model service is required.

| Workflow | Planning and human decision |
| --- | --- |
| `work` | Review the outcome, observable acceptance criteria, useful diagram and exact actions; explicitly approve before implementation. |
| `investigate` | Refine material scope before research, then produce and refine the Markdown report. No formal plan approval. |
| `breakdown` | Refine the complete backlog and destination; explicitly approve before tracker creation. |
| `mr-comment` | Recover the matching task across conversations or use verified standalone intake; debate interpretation, changes and exact replies before approval. |
| `mr-review` | Show the read-only coverage approach, validate findings and discuss exact comments; approve publication. No-findings results stay local. |

Review plans in the active conversation. Lead with acceptance criteria, a useful diagram and the exact decision; keep implementation detail and machine-readable state in the linked complete artifact. Use host-native Plan mode when available; skills cannot switch host-controlled modes themselves. Conversation approval also works without a separate application or mode-switch tool.

Every skill retains its working plan and resumable task context. Reuse valid approval after interruption and refresh only affected scope when requirements, review heads or publication actions change. Report acceptance does not authorize tracker creation. Preserve existing task paths and confirmed action IDs across later conversations; missing mapped context requires recovery, not a duplicate task.

The parent coordinates bounded workers and checks evidence. When model selection or delegation is unavailable, use the configured model or continue inline. No particular runtime or company service is required.

## Skill layout

```text
<skill>/
  SKILL.md
  workflows/*.md
  generic/*.md
  scripts/*
```

Skills include only the folders they need and work without sibling installations. Markdown links are relative to their document. Run helper commands from the skill root or use absolute paths. Repository helpers require Bash, Python 3, Git and jq; code search uses rg. Hosted-review helpers use authenticated gh/glab for the selected host, with connector fallback when the required CLI is unavailable or unauthenticated.

Use available tools appropriate to the task rather than assuming company services. Jira and Linear are optional tracker examples. Investigation traffic evidence is conditional and uses an authorized telemetry or analytics source available in the current environment.

Only work and code-changing mr-comment delivery wait for required CI on the published source commit, including verified merged-result pipelines where applicable. MR review reads current pipeline status as context and proceeds without polling or requiring green CI. No-action reviews record their plan and finish locally unless a published summary was requested.

Repository workflows register new task roots and newly created clones/worktrees for cleanup. Task artifacts and the task-local cleanup ledger live under `<root>/.artifacts/`; pass `WORKFLOW_SKILLS_CLEANUP_LEDGER` and `WORKFLOW_SKILLS_REGISTER_LEDGER=1` to resource-creating workers. On an explicit “clean everything up” instruction, the bundled helper removes tracked resources and verified owned task roots, preserving reused repositories. It also supports the legacy shared ledger at `~/.local/state/workflow-skills/workspaces.json`. Runtime-managed worktrees use their native cleanup facility before ledger reconciliation.

## Validation

```bash
python3 scripts/validate_skills.py
```
