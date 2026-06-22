# Understanding the Current Landscape — Memory

Learnings about how to trace and load codebase context. Read this before starting any landscape exploration.

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
