# workflow-skills

Portable workflows for software work, investigations and hosted code reviews.

## Skills

| Skill | Purpose |
| --- | --- |
| [work](skills/work/SKILL.md) | Implement scoped changes using existing code, meaningful verification and approved delivery. |
| [investigate](skills/investigate/SKILL.md) | Research a question and deliver an evidence-backed report, hosted description or chat answer. |
| [mr-review](skills/mr-review/SKILL.md) | Find introduced regressions and performance degradation; leave business/style nits to the user. |
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

Run stages in the current agent unless the user/runtime authorizes another execution method. Use the runtime's configured model; stage thinking levels express relative reasoning needs, not a requirement to install or switch models. Missing model-routing or subagent support does not block execution.

Read the linked stage instructions and follow their outcome routes automatically. Present complete plans and exact publication actions at the skill's approval gate. Plannotator is optional: use it when available, otherwise save the Markdown artifact and obtain explicit chat approval. Resume valid approval after continuation; revise it when scope or assumptions materially change.

Use available connectors, authenticated public host CLIs/APIs and local tools appropriate to the task. Discover capabilities and access rather than assuming particular tool names or a company environment. Jira and Linear are optional tracker examples. Traffic evidence uses whichever authorized telemetry/analytics source is available.

Keep complete evidence through readable source references and reconcile remote state before retrying mutations. Work and code-changing comment delivery check required CI for the actual source commit, including associated merge-result pipelines. No-findings reviews finish locally unless a published summary was requested.

## Validation

```bash
python3 scripts/validate_skills.py
```
