# Plan-Prep Component Brainstorming

This is a draft component map, not an execution sequence. Composition selects components and runs them sequentially, in parallel, or iteratively for each problem. Required inputs are the minimum needed to start; optional inputs are used when available and do not block execution.

### Cross-Cutting Architecture Decisions

Architecture-decision discovery is part of every selected component, not a standalone planning component. Each component reports the architecture points found during its own work through `../components/architecture-decision-protocol.md`, the single source of truth for contribution, ownership, routing, artifacts, and the no-orphans gate.

Parallel workers return contributions to the plan-prep/workflow owner rather than racing on the index. Runtime artifacts are `architecture/table-of-contents.md` and one `architecture/ADR-NNN-short-title.md` per material decision. The no-orphans gate must pass before Break Down the Work begins.

### Understand the Work

Problem:
Requirements can be ambiguous, incomplete, or misunderstood.

Intented Outcome:
Confirmed scope, goals, constraints, and open questions.

When to use:
Always except when the requirement is not small and very easy one.

Inputs:
- Required: Requirements or an equivalent statement of work.
- Optional: Design artifacts, saved progress, and unfamiliar-domain research.

Outputs:
`understand-the-work.md` understanding section; resolved and open questions.

### Compose the Plan

Problem:
Different work needs different planning depth and capabilities and potentiall in tailored sequence.

Intented Outcome:
Every component required to design, architect the solution and break up the tasks for the intented quality of the soltuion is planned and its sequential, parallel, or iterative workflow is set.

When to use:
Always

Inputs:
- Required: Confirmed understanding and the component catalog.
- Optional: Prior composition learnings, user preferences, and surfaced risks.

Outputs:
components-graph.md: User-approved component selection, dependencies, concurrency, and model choices.

### Define Planning verifiying Scenarios

Problem:
Understanding how to test and what to test, particularly how a QA person would verify the solution. This helps with understanding the scope of the work, expected behaviour and edge cases better

Intented Outcome:
Consumer-observable scenarios defining correct behavior, edge cases and missing decisions.

When to use:
Always

Inputs:
- Required: Requirements or an agreed behavior scope.
- Optional: Desired-flow outputs from Design the Solution, design artifacts, known risks, and landscape findings, understand-the-work.md.

Outputs:
test-scenarioes.md: Planning QA section in decisions and architecture points.

### Understand the Current Landscape

Problem:
Planning without existing-system context causes incompatible or duplicated work. Understanding the system and its gaps would help plan the work better

Intented Outcome:
Grounded understanding of relevant code, interfaces, patterns, constraints, flow of data and gaps.

When to use:
When work modifies or integrates with an existing system.

Inputs:
- Required: requirements, test-scenarioes.md, Feature scope and access to the codebase and project instructions.
- Optional: Desired-flow outputs from Design the Solution, design artifacts, architecture documentation, test-scenarioes.md; `understand-the-work.md` and user-provided starting points.

Outputs:
landscape.md: Current-landscape and gap findings; relevant-file references.

### Design the Solution

Problem:
Requirements alone may not show end-to-end behavior or data movement, and chosen directions do not automatically define compatible modules, contracts, or material architecture decisions.

Intented Outcome:
A coherent solution composed from the concerns this work needs. The approved outputs of those concerns are the technical design; Define Technical Design is not a separate component.

When to use:
When the work needs one or more of these concerns:
- Desired flows.
- Modules and ownership boundaries.
- Interfaces, types, validation schemas, and data contracts.
- Architecture-decision resolution for material points routed to this component.

Execution:
Select only the applicable concerns. Map their actual dependencies and run them sequentially, in parallel, or iteratively; there is no fixed sequence. Research Solution Precedents may support any concern needing external evidence, but remains independently selectable rather than a required predecessor.

Inputs:
- Required: Requirements or an agreed scope.
- Optional: Landscape findings, QA scenarios, design artifacts, existing contracts, architecture points and ADRs, and precedent research.

Outputs:
- Desired-flow design in `plan-prep.md` when selected.
- Modules, boundaries, interfaces, types, validation schemas, and data contracts in `technical-design.md` when selected.
- Architecture-decision summaries in `plan-prep.md` and protocol-owned ADRs when resolution is selected.

### Research Solution Precedents

Problem:
Local patterns and model knowledge may omit proven approaches and operational lessons.

Intented Outcome:
Cited comparable approaches with context, trade-offs, and transferability.

When to use:
When external evidence would improve an unfamiliar, consequential, or contested decision. This capability is optional and independently selectable; it may support any decision and is not a fixed predecessor.

Inputs:
- Required: A specific research question and known comparison constraints.
- Optional: Decision inventory, requirements, landscape findings, technical targets, and preferred sources.

Outputs:
`solution-research.md`.

### Break Down the Work

Problem:
An approved direction still needs executable, dependency-aware implementation units.

Intented Outcome:
Complete task inventory, dependency waves, and implementation-ready task files.

When to use:
When requirement is large enoug that should be done in more than one task

Inputs:
- Required: Approved implementation scope and sufficient technical direction.
- Optional: Any completed component artifacts, `architecture/table-of-contents.md` and relevant ADRs, conventions, and testing guidance.

Gate:
The architecture-decision protocol's no-orphans gate must pass. Unresolved blocking decisions prevent task breakdown.

Outputs:
`task/task-list.md`; `task/task-NN.md` files.
