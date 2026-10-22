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

Work, MR review, and MR comment follow their declared stage routes and approval gates. The parent coordinates bounded workers and checks evidence; where model selection or delegation is unavailable, use the configured model or continue inline. Respect explicit user choices and available runtime capabilities.

Investigation produces a report and repeats the user-feedback loop until it is accepted. It supports RFC and detailed investigation-result templates, plus user-supplied formats. Breakdown reads a report, drafts an epic and stories with descriptions, brief implementation steps and acceptance criteria, then refines the draft until the user explicitly approves creating it in the selected tracker. Report acceptance alone never creates tickets.

Every skill has a plan step. `workflows/plan.md` contains the step prompt; `generic/plan-template.md` contains only the plan structure. Investigation and breakdown use working plans without an extra upfront approval gate. Implementation/review publication and tracker creation keep their own explicit approval requirements. Resume valid approval after interruption; re-review material scope or destination changes.

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

Repository workflows record only newly created clones/worktrees for cleanup. On an explicit “clean everything up” instruction, use the bundled cleanup helper as described in each skill's `generic/cleanup.md`. It removes tracked workflow resources, including dirty temporary checkouts, while preserving reused existing repositories. The default ledger is `~/.local/state/workflow-skills/workspaces.json`; override it with `WORKFLOW_SKILLS_CLEANUP_LEDGER` consistently across workers and resumptions. This namespace is separate from any act-mkt installation. Runtime-managed worktrees use their native cleanup facility before ledger reconciliation.

## Validation

```bash
python3 scripts/validate_skills.py
```
