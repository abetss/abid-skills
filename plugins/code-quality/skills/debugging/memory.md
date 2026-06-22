# Debugging Memory

Learnings from past debugging sessions. Read this before starting any debugging work.

<!-- Add entries below as bugs are fixed. Format:
## [Date] -- [One-line summary]
**Bug type**: [functional | flaky | performance | build | production]
**Root cause**: [one sentence]
**What was surprising**: [what we didn't expect]
**Prevention**: [what would prevent this class of bug]
-->

## 2026-04-24 — Signature attribution rendered stale "Signed by …" on admin-reverted timesheets
**Bug type**: functional
**Root cause**: `get-timesheets.ts` derived `approver_signed_by` / `claimant_signed_by` from the latest MANAGER_SIGNED / CLAIMANT_SIGNED workflow row alone. Admin-revert clears `approver_signed_at` / `claimant_signed_at` but intentionally leaves the workflow rows for history — so the attribution union stayed populated after a revert, and the UI's SignatureBlock (keyed on `signed_by` being truthy) rendered a fake green-check "Signed by …" on a DRAFT timesheet with no actual signature timestamp.
**What was surprising**: Two signals (`*_signed_at` timestamp and `*_signed_by` attribution) that SHOULD be a derived pair were populated independently. The sign path sets both; the revert path clears only one. PROD-151's grand QA (25/25 browser cases) didn't catch it because every revert QA case checked the admin list or notifications — none re-opened the same row's sign tab after the revert. The attribution bug only surfaces on the post-revert review page.
**Prevention**: When two fields must co-vary (e.g. a timestamp and its derived attribution), either collapse them at the data layer OR add an integration test asserting the pair. For derived fields, always add a test for the "data cleared but derivation source still exists" transition — it's the invariant everyone forgets.

## 2026-05-10 — Nullable boolean read with `=== false` mis-classified `null` rows; sibling reader used `!== true` correctly
**Bug type**: functional
**Root cause**: A tri-state field (`series_accepted: true | false | null`) was read in one place with `=== false` and in another with `!== true`. The strict `=== false` silently dropped the `null` case (one-off shifts with no series), so the per-card badge fell through to "Unconfirmed" while the alerts list (using `!== true`) correctly classified the same shifts as "Awaiting Acceptance". Same file, same field, two different comparison semantics — only one matches the spec.
**What was surprising**: A test had been written that asserted the buggy `is_awaiting_acceptance: false` for `series_accepted: null`, locking in the bug. The transformer-test convention (one assertion per field, narrow per-case `it()`) made it easy to write a "current behavior" test instead of an "expected behavior" test, because each scenario looked self-contained.
**Prevention**: (a) For nullable booleans, prefer `!== true` / `!== false` over `=== true` / `=== false` — the strict form silently mishandles `null`. (b) When two code paths read the same nullable field, grep all readers together and verify they agree on the null semantics — divergence is almost always a bug. (c) When writing per-case tests against a tri-state, the case for the `null` value especially must encode the spec, not the current output.

## 2026-04-23 — Notification fanout silently dropped one recipient only when prior UNREAD existed on shared dedup_key
**Bug type**: functional
**Root cause**: Admin-revert UNSIGNED emit reused `dedup_action: 'SIGNATURE_TOGGLE'` from the manager-sign-unsign toggle path; fanout's `try_toggle_reversal` then treated the pre-existing UNREAD SIGNED (from the manager's earlier sign) as the SIGNED half of a toggle, deleted it, and skipped creating the new UNSIGNED — but only for the recipient who actually had the prior UNREAD row (the claimant). Manager was self-notify-filtered during the earlier sign, so they had no prior row and their UNSIGNED was created normally.
**What was surprising**: (1) The bug did NOT reproduce in a naive integration test with fresh DB state — needed to pre-seed an UNREAD SIGNED to trigger the toggle-reversal path. (2) Task 02's integration test spied `notification_service.emit` and asserted the payload was correct, which gave false confidence that the whole flow worked. The test passed through the buggy code because it never exercised the fanout downstream of emit.
**Prevention**: (a) Whenever emit payloads go through BullMQ + a fanout processor, pair the payload-shape spy test with an end-to-end test that drives the processor and asserts per-recipient rows. (b) Reusing a `dedup_action` string (e.g. SIGNATURE_TOGGLE) across semantically distinct flows is a footgun — the fanout's toggle-reversal is actor-independent and will cross-cancel the flows. Either give each distinct flow its own dedup_action or don't use dedup_action at all unless the flow is a genuine toggle pair.
