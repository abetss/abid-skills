# Composing the Plan

> Decide which components to include and in what order, based on the nature of the work.

## Memory

Read entries below before composing. Look for:
- Past corrections for similar work types (user added/removed/reordered components)
- Ordering failures (a composition that caused rework)

## Need

Not every piece of work needs every component. A backend-only API change has different planning needs than a full-stack feature with UI. The composition must be tailored to the work, not applied as a fixed template.

## Process

### Step 1: Read the available components

Read the Components table in `SKILL.md` (this skill's main file). For each component listed, read its **Need section** to understand what it achieves and when it's valuable.

### Step 2: Evaluate each component against the work

For each component, based on what you learned in "Understanding What Needs to Be Done," ask:

1. **Does this work need what this component provides?** — Read the component's Need. Does the work we're doing require that need to be met?
2. **What would we lose by skipping it?** — If we skip this component, what gap does that leave in our planning? Is that gap acceptable?
3. **What would we gain by including it?** — Does it reduce risk, surface unknowns, or prevent implementation problems?

Also factor in any architecture questions already surfaced during Step 1 — these may inform whether the architecture component is needed.

Be honest about this. Don't include a component "just in case." Include it because the work genuinely needs it.

### Step 3: Determine the order

The order depends on what each component needs as input and what it produces as output. Think about:

- What does each included component need to know before it can start?
- Which components produce information that other components need?
- What ordering minimizes rework (doing something, then discovering you need to redo it because of later findings)?

### Step 4: Present the composition to the user

Present your reasoning, not just the list:

```
Based on the work we're doing, here's the planning I propose:

**Included:**
1. [Component name] — [why it's needed for this specific work]
2. [Component name] — [why, and why in this position]
3. [Component name] — [why]

**Excluded:**
- [Component name] — [why it's not needed for this work]

**Order rationale:** [Brief explanation of why this sequence — what feeds into what]

Does this composition work? Should I add, remove, or reorder anything?
```

**Get user approval** before executing any components.

**Note:** The composition isn't locked. If a new need emerges during execution (e.g., an architecture question surfaces during flow design), pause and re-evaluate whether the composition needs adjustment.

## Rules

- **Read, don't assume** — Don't hardcode which components exist or what they do. Read from SKILL.md and each component's file.
- **Justify every inclusion and exclusion** — The user should understand WHY each component is or isn't included.
- **Order matters** — A component placed too early may lack context; placed too late may cause rework.
- **The user has final say** — They may include a component you'd skip, or skip one you'd include. Their judgment about the work overrides yours.
- **Stay open** — The user may suggest a component or step not in the table. That's fine.

## Writing to Memory

After the plan-prep is complete, write an entry if:
- The user adjusted the composition (added, removed, or reordered a component) — capture what they changed and why
- A composition caused rework (a component had to re-run, or a skipped component turned out to be needed) — capture what went wrong

Do NOT write entries for compositions that worked without issues — success doesn't need recording.

### Entry Format

```markdown
## [Date] -- [One-line summary of the correction or failure]
**Work type**: [e.g., full-stack feature, backend API, service, bug fix]
**What happened**: [what was adjusted or what went wrong]
**Why**: [the user's reason, or the cause of the rework]
**Lesson**: [what to do differently next time for similar work]
```

<!-- Memory entries below -->
