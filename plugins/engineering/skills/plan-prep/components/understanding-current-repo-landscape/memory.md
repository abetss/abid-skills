# Understand the Current Repo Landscape — Memory

Learnings about how to trace and load repository context. Read this before starting repository landscape exploration.

## When to write

When the user points you to files you wouldn't have found on your own. Record the pattern, not the path.

## Entry Format

```markdown
## [Date] -- [One-line summary]
**Area**: [area of the codebase]
**What the user pointed out**: [what they told you to read and why]
**Tracing lesson**: [the pattern to follow next time — e.g., "when working on X, also trace into Y because..."]
```

<!-- Add entries below -->

## 2026-06-16 -- Attendant↔ShiftTemplate links live in 3 places, not just instances
**Area**: platform-api scheduling (schema.zmodel — ShiftTemplate/ShiftInstance/ShiftAssignment)
**What the user pointed out**: pushed back on a claim that "a template has no direct attendant link." It does.
**Tracing lesson**: When reasoning about who/what is attached to a `ShiftTemplate`, check ALL of: (1) `ShiftJobAssignment` rows are XOR template-scoped (`shift_template_id`) vs instance-scoped — template rows are the "still on the template" source of truth; (2) attendants attach via `ShiftTemplateAcceptance` (direct `attendant_id`+`shift_template_id`, accept/decline log) and `PatternBackupPool` (direct, backup attendants); (3) the working MAIN/BACKUP `ShiftAssignment` is materialized PER-INSTANCE (no `template.primary_attendant_id` column). ZenStack employee read on ShiftTemplate traverses `shift_instances?[shift_assignments?[…]]`. Don't trust an Explore-agent summary on relationship existence — read the model's relations + @@allow lines directly.

## 2026-07-09 -- A "materializes a week late" scheduling bug was FRONTEND date-picker, not backend RRULE
**Area**: scheduling shift-create (apps/home create-shift-form.tsx `computed_one_off_dates`) ↔ platform-api materialize-shift-template.ts `expand_rrule`
**What the user pointed out**: reported symptom "recurring shift materializes one week after the date I picked" read like a backend RRULE/WKST bug; an Explore agent's root-cause guess (correctly) pointed at `expand_rrule` anchoring — but was wrong.
**Tracing lesson**: For any "date landed on the wrong day/week" bug, REPRODUCE EACH LAYER IN ISOLATION before assuming which layer is at fault — it's cheap and decisive. (1) Backend: `expand_rrule` is a PURE function of (rrule, start_date, window, tz) — replicate it with the exact reported inputs via a throwaway node script importing the app's `rrule-rust` by absolute path; it returned the picked date correctly, exonerating the backend. (2) Frontend: the date-pill helper built `label` from LOCAL `Date` getters but `date_iso` from `toISOString()` (UTC) — so in the evening (local clock past UTC midnight in a negative-offset tz) the SUBMITTED value was +1 day from the DISPLAYED label; `BYDAY` then snapped it a full week forward. The "one week" was an emergent effect, not the primary bug. Also: the machine clock in this repo is time-warped (2026) and was in the evening — check `date -u` vs local `date`; a `toISOString()`-for-local-date bug only manifests past the UTC rollover, so daytime testing hides it. Grep `toISOString` near any user-facing calendar-date picker.
