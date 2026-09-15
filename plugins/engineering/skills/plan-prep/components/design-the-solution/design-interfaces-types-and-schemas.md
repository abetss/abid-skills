# Design Interfaces, Types, and Schemas

> Define the contracts and data shapes through which the solution's parts collaborate.

## Need

Explicit boundaries do not by themselves define compatible interactions. Implementation tasks need shared interfaces, types, validation schemas, and data contracts rather than inventing them independently.

## Inputs

- Requirements or an equivalent statement of scope
- Access to the relevant codebase and project instructions
- Any available architecture decisions, landscape findings, flow designs, module boundaries, QA scenarios, design artifacts, or precedent research

Available inputs improve fidelity but do not impose an execution order.

## Procedure

1. Enumerate each interaction that crosses a system or module boundary.
2. Define its public interface and interaction contract, including applicable commands, events, APIs, and error contracts.
3. Define the complete types, validation schemas, and data models exchanged by each interaction.
4. Record applicable invariants, state transitions, failure handling, and compatibility or migration concerns.
5. Identify testing seams and contract-verification points.
6. Contribute every architecture point encountered through `../architecture-decision-protocol.md`.
7. Check that every interaction has matching producer and consumer contracts and that every in-scope field and outcome is defined. Return conflicts to the parent concern for routing or iteration.

## Output

Return an `Interfaces, Types, Validation Schemas, and Data Contracts` section for the parent to integrate into `technical-design.md`, containing as applicable:

- Public interfaces and interaction contracts
- Commands, events, APIs, and error contracts
- Complete types, validation schemas, and data models
- Invariants and state transitions
- Failure-handling and compatibility or migration implications
- Testing seams and contract-verification points
- Explicit unknowns requiring resolution
