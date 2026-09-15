# Architecture-Decision Protocol

This is the single source of truth for architecture-decision handling in plan-prep. Architecture discovery is cross-cutting: every component surfaces material architecture points encountered during its own work and contributes them through this protocol.

## Contribute architecture points

Return each point to the plan-prep/workflow owner with:

- Title and discovering component
- Decision context, why it is material, and affected areas
- Known constraints, drivers, evidence, and unresolved questions
- Suggested owning component and blocking state

Parallel workers return contributions; they do not edit the architecture table of contents.

## Assign and route ownership

Route a point to another selected component when that component naturally owns it. Otherwise, the discovering component or plan coordinator owns it. If the owning component is skipped or removed, ownership returns to the coordinator. Every point must retain an owner through completion.

The owner invokes the `architect-solution` process in assigned-ADR mode to resolve each material decision and produce its ADR. `Discover Existing Capabilities and Solutions` supplies native-platform and nearby adopt/extend/build evidence when applicable. `Research Solution Precedents` may independently supply broader architectural evidence.

## Consolidate architecture artifacts

Runtime architecture artifacts live at:

```text
{work-folder}/architecture/
  table-of-contents.md
  ADR-NNN-short-title.md
```

The plan-prep/workflow owner is the single writer that consolidates contributions into `table-of-contents.md`, assigns stable `ADR-NNN` IDs, and prevents duplicate entries. The table records each decision's:

- Stable ID and title
- Discovering component and owning component
- Status and blocking state
- ADR link

Create exactly one `ADR-NNN-short-title.md` for each material decision. Each ADR contains:

- Complete decision context
- Constraints and drivers
- Considered approaches
- Research and sources where relevant
- Diagrams where useful
- Selected decision and rationale
- Trade-offs and consequences
- Implementation implications
- Verification considerations
- Unresolved follow-ups

## Build-versus-reuse evidence gate

Before selecting a custom subsystem, the decision owner evaluates relevant native platform capabilities and either compares the closest credible implementation or records a bounded search that found no credible candidate. The owner then names the unmet requirements that justify building rather than adopting or extending. Missing applicable discovery is an evidence gap, not evidence that no suitable solution exists.

Unresolved evidence that could change adopt/extend/build **blocks that decision and its dependent design and tasks**. A nonblocking follow-up must explain why any answer cannot change the decision; unrelated independent work may continue.

Classify each blocker as missing evidence, unresolved user choice, implementation verification, or document correction. Repeat architecture revision/review only when new evidence or a material amendment addresses it; otherwise stop and route the blocker to the action that can resolve it.

## No-orphans gate

Before task breakdown, the plan-prep/workflow owner verifies that every contributed architecture point has been consolidated and every table-of-contents entry has an owner, terminal status, and valid ADR link. Every material decision must have exactly one ADR. An unresolved blocking decision fails the gate and prevents task breakdown.
