# Composing the Plan

> Decide which components to include and how their dependencies shape execution, based on the nature of the work.

## Memory

Read entries below before composing. Look for:
- Past corrections for similar work types (user added or removed components, or revised dependencies)
- Dependency or execution failures (a composition that caused rework)

## Need

Not every piece of work needs every component. A backend-only API change has different planning needs than a full-stack feature with UI. The composition must be tailored to the work, not applied as a fixed template.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute architecture points discovered while composing this work; this component reports only the points it finds and leaves their lifecycle to the shared protocol.

## Process

### Step 1: Read the available components

Read the Components table in `../../SKILL.md`. For each component listed, read its **Need or Problem section** to understand what it achieves and when it's valuable.

### Step 2: Evaluate each component against the work

For each component, based on what you learned in "Understanding What Needs to Be Done," ask:

1. **Does this work need what this component provides?** — Read the component's stated need or problem. Does the work we're doing require that need to be met?
2. **What would we lose by skipping it?** — If we skip this component, what gap does that leave in our planning? Is that gap acceptable?
3. **What would we gain by including it?** — Does it reduce risk, surface unknowns, or prevent implementation problems?

Also factor in architecture points already surfaced during Step 1 — these may inform component selection, dependencies, and the concerns Design the Solution needs to consider. Architecture discovery itself is cross-cutting, not a selectable component.

Be honest about this. Don't include a component "just in case." Include it because the work genuinely needs it.

Apply this coverage check explicitly:

- Existing repository or codebase must be understood → **Understand the Current Repo Landscape**
- Named platform or possibly existing extension/tool/system → **Discover Existing Capabilities and Solutions**
- Broader analogous systems could inform a consequential decision → **Research Solution Precedents**

These needs can coexist. Do not treat local repository inspection as platform/ecosystem discovery, or general precedents as proof that no nearby implementation exists.

### Step 3: Determine dependencies and maximum concurrency

Build a dependency graph from each component's required inputs and outputs. Optional context may improve later work but does not create a blocking edge. At every stage, identify the largest set whose required inputs are ready and schedule that set concurrently up to available concurrency.

Also inspect inside each selected component for independent work units such as repository starting points, capability questions, candidate solutions, precedents, architecture decisions, or task files. A component-level assignment must not hide independent work inside one sequential agent.

When both solution discovery and general precedents are selected, complete the bounded nearby-candidate discovery before fixing the general-precedent shortlist. Candidate verification and independent precedent lanes may then run concurrently.

Determine:

- The critical path and every true input dependency
- The maximum ready set at each stage
- Internal fan-out opportunities within each component
- Where iteration is required because one output changes another
- Which single-writer operations require consolidation
- Why every serialized edge cannot safely run concurrently

### Step 4: Present the composition to the user

Present your reasoning, not just the list:

```
Based on the work we're doing, here's the planning I propose:

**Included:**
- [Component name] — [why it's needed for this specific work]
- [Component name] — [why]
- [Component name] — [why]

**Excluded:**
- [Component name] — [why it's not needed for this work]

**Dependencies and execution:** [Critical path, maximum ready sets, internal fan-out, expected peak concurrency, consolidation points, and required iteration]

Does this composition work? Should I add or remove anything, or revise the dependencies or concurrency?
```

When the composition has parallel branches, convergence, iteration, or approval gates, include a fenced Mermaid flowchart under **Dependencies and execution**. Keep a simple linear composition as prose unless a diagram materially improves understanding.

**Get user approval** before executing any components.

**Note:** The composition isn't locked. If a new need or architecture point emerges during execution, pause and re-evaluate the selection, dependencies, or concern composition.

## Rules

- **Read, don't assume** — Don't hardcode which components exist or what they do. Read from SKILL.md and each component's file.
- **Justify every inclusion and exclusion** — The user should understand WHY each component is or isn't included.
- **Maximize the ready set** — Run all dependency-ready work concurrently up to available capacity. Serialize only true input dependencies, user checkpoints, or single-writer consolidation; justify every serialized edge.
- **The user has final say** — They may include a component you'd skip, or skip one you'd include. Their judgment about the work overrides yours.
- **Stay open** — The user may suggest a component or step not in the table. That's fine.

## Writing to Memory

After the plan-prep is complete, write an entry if:
- The user adjusted the composition (added or removed a component, or revised its dependencies) — capture what they changed and why
- A composition caused rework (a component had to re-run, or a skipped component turned out to be needed) — capture what went wrong

Do NOT write entries for compositions that worked without issues — success doesn't need recording.

Memory is at `./memory.md`

### Entry Format

```markdown
## [Date] -- [One-line summary of the correction or failure]
**Work type**: [e.g., full-stack feature, backend API, service, bug fix]
**What happened**: [what was adjusted or what went wrong]
**Why**: [the user's reason, or the cause of the rework]
**Lesson**: [what to do differently next time for similar work]
```
