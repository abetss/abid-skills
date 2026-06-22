# Product Guide Writer — Lessons Learned

This file captures things past sessions got wrong or that users had to correct. SKILL.md, file-folder-structure.md, and templates/ already cover the design rules — don't duplicate them here.

Add a new entry only when something surprised us, broke, or was explicitly fixed by a user.

---

## Bugs found in older docs (always re-verify before copying)

Past sessions have copied content from older docs and shipped real inaccuracies. Examples found in PROD-124 session:

- **Travel expense rate range was wrong** in the existing product-guide ($15–$50 instead of actual $3.50–$5.00). Caught only because we re-read the source constants.
- **History sort order was wrong** in the existing product-guide (claimed "newest first" — actually oldest first per code).
- **STATUTORY_HOLIDAY multiplier was inconsistent** between two docs (one said 2.0x, the other said 1.5x — actual is database-driven, default 1.5x).

**Lesson:** never copy a numeric value, threshold, sort order, or formula from an existing doc without grepping the current code for the source of truth. Even our own docs from yesterday can be wrong.

---

## Anti-patterns from real mistakes

These are concrete failures past sessions made. Watch for them in your own writing.

- Writing role-specific behavior under one heading when both roles differ (use the Role differences section instead).
- Stating "the system handles X" without giving the specific value, formula, or threshold.
- Documenting what code currently does without explaining WHY (every behavior should link back to a domain rule, ESA section, DF rule, or explicit UX/accessibility decision).
- Skipping a state in the States section because "it's obvious" — loading and empty are the most-skipped and most-asked-about.
- Treating Q&A as a dumping ground for behaviors. Q&A is for actual user-facing questions, not "Q: What does this button do? A: It clicks."

---

## Project-convention overrides (always check the project README first)

The `file-folder-structure.md` in this skill describes the generic pattern (per-feature `q-and-a.md`, flat `pages-and-features/screenshots/`). Individual projects may override this in their `pages-and-features/README.md`. When the project README contradicts the skill, **follow the project README**, not the skill.

Observed in admin-3 (PROD-149 session, 2026-04-19):
- Q&A lives **inline** in each page file's `## Q&A` section. There is **no per-feature `q-and-a.md`**.
- Screenshots live in **per-feature `screenshots/` subfolders** (e.g. `voice-assistant/screenshots/`), not in a single flat root folder.
- Relative screenshot paths are then `screenshots/foo.png` from a page file at the feature root, not `../screenshots/foo.png`.

## Non-route features also belong in pages-and-features

Not every documented "page" is a route. Cross-cutting sidebar features (e.g. Voice Assistant, mounted once in the manager shell for all `/em/*` pages) also get a folder under `pages-and-features/`. Use the feature name as the folder (`voice-assistant/`) and `main.md` as the primary file. Document in the Route field which pages host the panel, e.g. "sidebar panel on all `/em/*` pages".

## Updated by

Append a dated line when adding new lessons.

- 2026-04-06 — Initial creation from PROD-124 product knowledge base session
- 2026-04-19 — PROD-149: captured project-convention override (inline Q&A, per-feature screenshots) and precedent for documenting non-route sidebar features
- 2026-04-23 — PROD-151: when the work-folder already contains authoritative browser-captured QA screenshots from a recent execute-all run (grand-qa/*.png, per-case evidence), prefer reusing them over launching fresh chrome MCP sessions. Note the date and the role (white vs dark theme may vary by who took them). Also: privacy-sensitive role-label attribution ("admin" literal vs admin's real name) may differ between code intent and browser reality due to ZenStack policy scoping — always check the actual rendered string in the authoritative screenshot and the raw-SQL bypass path (`$queryRaw` on `user_role`) before documenting the behavior. Don't copy the context summary verbatim when code + browser disagree.
- 2026-04-23 — PROD-151 hotfixes: when the context summary says "same pattern applies" across admin flows, check the code — the three admin-variant notification flags (`reverted_by_admin`, `signed_by_admin`, `unsigned_by_admin`) produce THREE distinct body suffixes ("reverted to draft by admin" / "signed by admin" / "unsigned by admin") and come from TWO different routes (status PATCH vs signature PATCH). Don't collapse them into one "admin-variant body" in the docs. Also: an attribution "stale value" bug (lingering workflow row after timestamp cleared) is worth documenting as an explicit edge case in the signature-block doc, because the fix is invisible from the UI but the behavior is load-bearing for correctness of reverted-to-draft timesheets.
- 2026-05-10 — PROD-156 followup: when a feature has two roles' weekly views built on a shared card-component tree (manager + attendant), split into ONE doc per role (not "schedule.md" with two role-differences columns) — each role has materially different inline CTAs, default density, privacy gates, and edge cases. The shared component layer goes in Technical notes. Also: when the card-side classification ("Unconfirmed" badge) and the alerts-panel classification ("Awaiting Acceptance" bucket) intentionally diverge for one-off shifts (`series_accepted = null`), document the asymmetry explicitly in Business rules AND in Q&A — managers will hit it and ask. Pre-existing handler bugs flagged in the walkthrough as "out of scope" still belong in `## Known gaps / tech debt` so future maintainers can find them when they reproduce the bug.
- 2026-05-12 — PROD-162/165: Replace-primary UX entry point is NOT on the primary card itself — it's (a) Edit Shift page for non-vacant shifts, and (b) the CoveringCard "Replace" button for cover scenarios. The component comment says "Primary card: only [Replace] action" but the implementation routes replace through the Edit page instead. Always check the actual callback wiring in `ui.tsx` rather than trusting component-level comments. Also: shift-type tint is display-only for attendants (no selector on their side) — document this explicitly to avoid someone looking for a missing attendant control.
- 2026-05-13 — Community redesign docs: the community app (`apps/community`) requires Auth0 env vars to run locally — the dev server starts but all routes redirect to an auth page that 404s because `AUTH0_DOMAIN` is missing. When browser testing is blocked for this reason, write from code (diff + source files) and mark screenshots as pending. Also: the community app may start on a port other than the configured one (Next.js falls back to 3000 if the configured port is taken by another process) — always check `lsof -i` across a range of ports and verify the process CWD before trusting a port is serving the right code.
- 2026-05-13 — Scheduling bug-fix docs (overnight/default/images/chat/labels): when an existing doc's "type-colored outlines" language describes bar label colours that were later unified to `text-foreground`, grep for that exact phrase across ALL scheduling docs — multiple docs (week-manager, week-attendant, shift-detail-manager) can carry stale copies of the same claim. Fix all of them in one pass rather than patching one at a time. Also: `EditAvailabilityDialog` (post-acceptance edit) still has `start < end` validation even though `AcceptSeriesDialog` (initial accept) removed it for overnight support — document both dialogs' differing validation to avoid future confusion about why one allows overnight windows and the other doesn't.
- 2026-06-17 — PROD-178 (Shift Tasks attendant tab): the context summary said the list = "union of two sources" (explicit share ∪ template-attached), but the ZenStack `ShiftJob` read policy actually OR's THREE employee grants — the two named plus a legacy per-shift-INSTANCE grant. Document the as-shipped policy (three grants, template one is the load-bearing one for this tab), not just the two-source summary. Also: the revocation AC ("revoked job drops off") only holds because a `deleted_at == null` guard was added to the PERMISSION read grant during development (Task 11) — without it the tombstoned permission still satisfied the EXISTS and the job lingered. The sibling template/schedule grants still lack that guard (replaced ShiftAssignment may linger) — that's real known tech debt worth flagging in the doc. Manager name on the list is the only personal datum surfaced and falls back to "Unknown" when policy-denied — call this out as the PIPEDA minimization choice. Reused the running admin-3 dev server (home :3003 / api :3203, cwd-verified per CLAUDE.local.md) for the browser pass instead of starting one; the notification drawer still carries pre-renderer "Unknown action: SHIFT_JOB_SHARED" dev rows whose deep-link nonetheless works — documented as a dev-data artifact, not a defect.
- 2026-06-17 — PROD-178 bug-fix followup (re-grant after revoke): the original PROD-178 doc's "Revocation" section + tech-debt note pre-dated the re-grant-handler fix. The fix makes `create-shift-job-permission.ts` reactivate a soft-deleted `ShiftJobPermission` (clear `deleted_at`, refresh `granted_by_id`/`granted_at`) instead of blind-`create()` (which collided on `@@unique([shift_job_id, attendant_id])` → P2002 → 500 → job never reappeared); already-active grant still 409. Doc edits: renamed section "Revocation" → "Revocation and re-grant" and added the reinstate behavior (job reappears + `SHIFT_JOB_SHARED` re-fires); broadened "Notification on share" so re-share re-notifies (only an already-active grant is the 409 no-notify case); added a "Revoked-then-re-granted" edge case + two Q&A. Key subtlety to PRESERVE when editing this doc: the permission READ grant's `deleted_at == null` guard (the original Task-11 fix) is a SEPARATE fix from this re-grant-HANDLER fix — both are now done, but the sibling template/schedule read grants still lack the guard, so that tech-debt bullet stays OPEN. Reworded it to "the same class of soft-delete-blind-EXISTS bug … since been fixed for [permission read grant + re-grant handler]" and added a "Resolved:" bullet for the duplicate-row fix. Backend-only change, no UI delta — grounded against the two changed source files, no dev-server pass needed.
- 2026-06-17 — PROD-177 (Timesheet Excel export): three load-bearing gotchas. (1) The provided context summary's admin-edit surface (`/admin/settings/fiscal-year` page) was a SUPERSEDED intermediate plan — the shipped fiscal-year-start-month editor lives on the Manager Profile (`/em/profile`) as 12 month pills, set by an admin via impersonation; `/admin/settings` is just a stub. Always reconcile the context summary against the FINAL git diff + a browser pass; the walkthrough's early "Task 12" notes can describe abandoned designs. (2) Shipped UI copy diverged from the QA-observed copy: the unsigned-warning dialog is titled "Signed" with a DISABLED checklist of all caregivers + "Download (N)" button — NOT the "X of Y timesheets are signed" enumeration an earlier QA round reported. Browser-verify dialog copy; document the shipped component. (3) The single AND period export buttons share one component with the hardcoded label "Download Period" — even the single-timesheet button reads "Download Period". Don't assume the requirement's "Download Excel" label shipped. (4) Harness guard: the `Write` tool BLOCKS creating any file literally named `report.md` (misreads it as an agent report artifact) — name a route-`/report` page doc `quarterly-report.md` instead and link accordingly.
