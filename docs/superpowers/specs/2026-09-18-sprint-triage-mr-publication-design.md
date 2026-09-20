# Sprint-triage MR-first publication design

## Purpose

Make GitLab merge requests the review surface for every sprint-triage knowledge-base publication while retaining Confluence publication when the approved plan contains a fragment.

## Scope

The change applies only to `skills/sprint-triage`.

- Keep the existing collection, plan approval, knowledge-base worktree, report, ledger, and index behavior.
- Keep Confluence configuration and the approval-artifact sections.
- Do not modify any ticket, Slack, GitLab, or Confluence content outside a sprint-triage run.

## Publication flow

1. Checkout creates a new linked knowledge-base worktree and a topic branch for the sprint period.
2. Implement writes, verifies, and commits only the approved knowledge-base report, ledger, and index changes in that worktree. It does not push.
3. Publish pushes the committed branch without force and creates a GitLab MR against `gitlab.targetBranch`, following the repository’s verified template rules.
4. Publish updates Confluence only if both conditions hold:
   - the approved plan’s `## Publication fragment` contains a non-empty HTML fragment; and
   - the configured Confluence target is present.
5. When no fragment is approved, publish records an intentional Confluence skip; this is successful publication, not an error.
6. Publish verifies the created MR. When it updated Confluence, it rereads the page and verifies that the approved fragment is its top insertion.

## Plan contract

The plan retains the exact existing heading structure, including `Confluence top append`, `Guides`, and `Publication fragment`.

- A non-empty publication fragment authorizes the corresponding Confluence append.
- An explicitly empty fragment authorizes no Confluence mutation.
- The execution contract records the KB worktree/branch, commit verification, MR target branch, and—when applicable—Confluence page version or content integrity data needed to detect drift.

## Failure handling

- Missing KB commit, branch, MR target, or GitLab access blocks publication.
- A transient push or GitLab API error returns `handoff`.
- A malformed approved publication fragment, missing configured Confluence target for a non-empty fragment, page-version/content drift, or Confluence mutation failure blocks publication.
- A deliberately empty fragment does not block publication.

## Verification

The skill documentation must be checked for consistent MR-first behavior across `SKILL.md`, `plan.md`, `checkout.md`, `implement.md`, `publish.md`, and `sprint-triage.example.yaml`.

Pressure scenarios:

1. A plan with an empty fragment results in a pushed branch and MR, with no Confluence call.
2. A plan with approved HTML results in a pushed branch and MR before the Confluence update, then verifies the top insertion.
3. An implementation agent cannot push before the publish stage.
4. A run cannot reuse the primary checkout in place of a new KB worktree and branch.
