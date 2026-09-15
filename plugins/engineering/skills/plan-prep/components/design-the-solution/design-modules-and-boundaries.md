# Design Modules and Ownership Boundaries

> Define where responsibilities live and how modules may depend on one another.

## Need

Requirements and architecture decisions do not automatically define how modules collaborate. Without explicit boundaries, implementation tasks may place responsibilities inconsistently or create incompatible dependencies.

## Inputs

- Requirements or an equivalent statement of scope
- Access to the relevant codebase and project instructions
- Any available architecture decisions, landscape findings, flow designs, QA scenarios, design artifacts, or precedent research

Available inputs improve fidelity but do not impose an execution order.

## Procedure

1. Map the existing and proposed modules that participate in the work, including each module's responsibilities.
2. Assign ownership for behavior, state, and side effects; define dependency direction and allowed collaboration across boundaries.
3. Account for failure-handling responsibility, compatibility or migration concerns, and testing seams at each boundary.
4. Contribute every architecture point encountered through `../architecture-decision-protocol.md`.
5. Check that every in-scope responsibility has a clear owner and every cross-module dependency is explicit. Return unresolved conflicts to the parent concern for routing or iteration.

## Output

Return a `Modules and Ownership Boundaries` section for the parent to integrate into `technical-design.md`, containing as applicable:

- Module map and responsibilities
- Ownership and dependency boundaries
- Behavior, state, and side-effect ownership
- Failure-handling and compatibility or migration implications
- Testing seams
- Explicit unknowns requiring resolution
