# Stage: checkout-source

Use the invoking request and complete source evidence, inline or through the evidence references defined in SKILL.md.

---

Validate and bind the task directory and reviewed source worktrees. Reuse the preceding work run when available; for a standalone review, bind a verified suitable source checkout or prepare an isolated workspace using the review source identity and the cleanup ledger. This stage is read-only for checkout contents and branch/index state.

Input: `the invoking request`
Evidence: `{{last.summary}}`

When continuing work, recover the inherited `workspace` and `repositories[]` per [Task workspace](../generic/task-workspace.md), including the original absolute root, manifest path, cleanup ledger, all source/base/head identities, dirty baselines and confirmed publication IDs. Validate every relevant repository; do not replace an inherited workspace or choose an unrelated existing checkout. Run the helper's `--check` for a helper-managed layout, or validate recorded custom contexts in place. Compare each source origin/branch and local HEAD with that review's fetched source identity, including fork source versus target. Preserve every inherited path and the root's ticket-ID or short-summary name.

Reconcile incoming source evidence before edits. A fetch may retrieve objects/remote refs without changing the bound worktrees, but do not checkout, pull, reset, stash, clean or overwrite files. Preserve another contributor's commits and distinguish our verified local/pushed commits and uncommitted progress from external movement using the checkpoint. Route movement that invalidates assumptions through fetch/plan recovery; do not silently implement an old plan on a newer head. A merged/closed review has no active source-edit delivery for that entry; retain its evidence for the planner’s local report while continuing independent active reviews.

If recorded paths are missing, retain the established root and resource identities. Recover source evidence in a separate read-only inspection location when needed, record exact reconstruction requirements for plan approval, and never silently substitute it as the editable workspace. Only the approved implementation route may recreate missing resources at their recorded paths. An unresolved expected handoff, review identity or an unsafe path/branch collision remains a factual blocker. Existing reused resources are not re-registered for cleanup; carry the inherited ledger path.

`ready`: verified workspace is safely bound with current source evidence, or precisely identified missing-resource reconstruction is documented for the plan using separate read-only evidence.
`gaps`: source/evidence changed or is incomplete; refresh through fetch.
`handoff`: transient mechanical/fetch failure.
`blocked`: no safe checkout or reconciliation is possible.

## Required response

# Completed
<prior evidence references, inherited workspace/root/manifest/ledger, per-repository cwd/origin/role/branch/base and fetched/local HEAD, dirty baseline, incoming-commit assessment, confirmed publication IDs and any exact missing-resource recovery proposal>

# Remaining
<exact mechanical work, or None.>
