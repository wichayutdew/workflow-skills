# Stage: plan

Use the invoking request and complete source evidence, inline or through the evidence references defined in SKILL.md.

---

Turn reviewer findings into comments the user can approve.

Input: `the invoking request`
Findings: `{{last.summary}}`
Rejected plan: `{{gate.artifact}}`
Feedback: `{{gate.feedback}}`

Use only actionable, evidence-based findings anchored to the reviewed head. Keep the proposed published text specific, professional, and consistent with its detailed suggestion. Include every user-answerable review decision and its impact in the existing `Reviews` or `Publication contract` sections; do not ask separately. Approval feedback returns to this plan stage and the artifact is re-presented at the same review gate.

Carry each finding's severity, trigger, baseline/contract, impact and verification limits into the proposed comment. Deduplicate existing discussions and root causes. With no findings, this stage is needed only when the user requested a published summary; no ceremonial comment is implied.

Give every publication action a stable marker and capture current review state/head plus confirmed/unconfirmed action IDs for retry reconciliation. Refresh stale evidence instead of publishing obsolete anchors.

For GitLab, construct exact publication actions with the available connector or authenticated host API/CLI before submitting the artifact. Each inline finding needs the native base/start/head SHAs, text position type, old/new paths and changed-line anchor. Preserve the exact body and stable marker; no placeholders. For CLI fallback, prepare commands safe for the active shell and pass multiline bodies through a safely quoted file or structured argument. Use nested multipart position parameters when the selected endpoint requires them; flat fields are not a substitute. Verify the chosen client's encoding before approval. Mark actions inline-comment with paths/line/SHAs. A generic-comment action is allowed only when a valid text position is impossible, with its reason and exact approved mutation. A failed inline action has no silent generic fallback.

`ready`: every intended comment has the required artifact content and is ready for review.
`handoff`: transient read failure.
`refresh`: head/state changed; fetch and revalidate before revising/reusing approval.
`blocked`: required safe evidence or authority cannot be obtained.


## Required ready response
On `ready` or `handoff`, put the complete proposed review-comment and publication-action ledger in `Completed`.

# Completed
<complete review plan ledger>

# Remaining
<exact remaining work, or None.>

When Findings are absent or incomplete, return `gaps` with exact missing fields so the workflow re-enters review.
