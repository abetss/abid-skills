---
name: architect-solution
description: Architect, compare, review, or resolve software, system, solution, data, infrastructure, and API designs. Use for architecture questions, material technical trade-offs, plan-prep architecture decisions, assigned ADRs, or comparisons between credible implementation approaches.
---

# Architect Solution

Use one architecture process for direct advice, multi-perspective comparison, and plan-prep decision resolution. Keep architecture dialogue and synthesis in the main conversation. Delegate bounded evidence gathering or independent design lanes only when they improve the decision.

**Core principle:** Start with the smallest viable architecture. Add alternatives, scale mechanisms, and resilience only when requirements, evidence, or material uncertainty justify them.

## Modes

Select the smallest mode that can resolve the request.

| Mode | Use when | Parallel architecture lanes |
|---|---|---|
| **Direct** | One approach is clearly viable, the decision is bounded, or the user asks a focused architecture question | None required |
| **Comparison** | Two or more credible approaches have material trade-offs | 2–5 lanes |
| **Assigned ADR** | The caller supplies one stable `ADR-NNN` ID and exact ADR path | Direct or comparison, according to decision complexity |
| **Aggregate** | Several related architecture decisions must be resolved together | Dependency-ready decisions may run concurrently |

A bug fix, pure implementation task, or purely visual UI choice belongs to its specialized process unless it exposes a material architecture decision.

## Expertise Routing

Expertise is progressively disclosed and never loaded as one undifferentiated library.

### 1. Read the global expertise router

Always read this router before selecting architecture expertise:

```text
~/.agents/expertise/table-of-content.md
```

Consider every `ACTIVE` entry and its semantic routing trigger. Ignore entries in all other statuses. Load only materially relevant `expertise.md` entry points and the references they require. If the router is unavailable, disclose that global expertise could not be routed and proceed with general architectural reasoning.

### 2. Inspect plugin-local supplements

After global routing, inspect this skill's optional `experts/` directory for `*/expertise.md` entry points. Treat an absent directory as empty because version control does not preserve empty directories.

For every local entry point found:

1. Read its routing trigger.
2. Compare it with the problem, proposed solution, constraints, likely failure modes, and quality attributes.
3. Load the complete entry point and required relative references only when it adds materially relevant plugin-specific guidance.

Global expertise is the mandatory routing baseline. Plugin-local expertise may supplement it but does not replace reading the global router. When both apply, combine nonconflicting guidance and make any conflict and controlling source explicit.

Expertise routing is complete when the global router has been read, every `ACTIVE` global trigger has been considered, and each material global or local match has been loaded or explicitly accounted for.

## Architecture Baseline

Every mode must:

1. Clarify the outcome, scope, assumptions, constraints, and measurable quality attributes.
2. Model responsibilities, ownership boundaries, data flow, state transitions, and failure domains.
3. Identify the simplest viable design before introducing additional infrastructure or abstractions.
4. Compare relevant alternatives across correctness, latency, throughput, consistency, availability, operability, security, complexity, cost, migration, and testability.
5. Apply selected expertise and reconcile overlap according to user requirements and established project conventions.
6. Make the decision explicit: chosen option, rejected alternatives, accepted trade-offs, thresholds, failure handling, observability, migration, and verification.

Use only criteria that can materially change the decision. Project-specific concerns such as accessibility, privacy legislation, or a particular schema technology belong in the analysis only when project evidence makes them relevant.

## Inputs

Gather the available evidence for the selected mode:

- The decision or architecture question
- Requirements and acceptance criteria
- Existing architecture, code, schemas, contracts, tests, and conventions
- Similar implementations and reusable platform capabilities
- Constraints, quality attributes, and unresolved questions
- For assigned ADR mode: stable ID, exact output path, owner, and blocking state
- For aggregate mode: work folder and decision dependency graph

Missing evidence that could change the decision is a blocker or a research assignment. Missing evidence that cannot change the decision should be recorded as a bounded follow-up.

## Exploration Proposal

Before dispatching research or architecture lanes, display:

- Mode and decision scope
- Evidence already available and evidence gaps
- Selected local and global expertise, with a concrete reason for each
- Proposed lenses and what each optimizes
- Agent count, model/effort when selectable, and assignment boundaries
- Parallel and sequential dependencies
- Consolidation owner and artifact writer
- Expected output

Request approval unless the user explicitly requested autonomous execution. Autonomous runs still record the proposal before dispatch.

## Evidence Gathering

Research is conditional rather than automatic. Use bounded assignments for genuinely missing evidence:

| Assignment | Use when | Required return |
|---|---|---|
| Repository context | Existing patterns or boundaries could change the design | File-specific patterns, comparable implementations, constraints, and gaps |
| Contract and policy constraints | Schemas, APIs, authorization, compliance, or compatibility are material | Exact contracts, invariants, policies, and migration constraints |
| External precedent | A platform capability or established solution could avoid custom work | Credible alternatives, source authority, applicability, and unmet requirements |

The main conversation may gather straightforward evidence directly. Research agents return evidence; they do not choose the architecture or write shared artifacts.

## Architecture Exploration

### Direct mode

Analyze the evidence and selected expertise in the main conversation. State the recommendation, why alternatives are not material, trade-offs, implementation implications, and verification.

### Comparison mode

Choose distinct lenses that produce meaningfully different designs. Do not dispatch several unconstrained agents that are likely to converge on the same answer.

| Complexity | Suggested lanes | Signal |
|---|---:|---|
| Simple comparison | 2 | One material trade-off or boundary |
| Standard | 3 | Several interacting concerns with clear dimensions |
| Complex | 4–5 | High uncertainty, broad failure impact, difficult migration, or competing quality attributes |

Each lane receives the same self-contained evidence and selected expertise, plus one explicit lens. It must return:

- Architecture under that lens
- Components and ownership
- Data and control flow
- State transitions and failure recovery
- Implementation and migration implications
- Verification strategy
- Benefits, costs, risks, and what the lens trades away

Use the available orchestration runtime rather than hardcoding a particular agent tool or agent name. Run independent lanes concurrently. Give each shared artifact exactly one writer.

### Assigned ADR mode

Treat the supplied decision as the entire resolution scope. Preserve its stable ID and exact path. Do not discover or write unrelated ADRs. Choose direct or comparison exploration according to the material uncertainty in that decision.

### Aggregate mode

Identify the material decisions and their true dependencies. Run every dependency-ready decision concurrently up to available capacity. Serialize only an input dependency, user checkpoint, or single-writer integration. All decisions converge before implementation task breakdown.

## Synthesis and Decision

The main conversation owns synthesis and recommendation.

1. Validate that every lane addressed the same decision and constraints.
2. Normalize approaches into a comparison whose criteria come from the requirements, quality attributes, and selected expertise.
3. Identify genuine disagreements, hidden assumptions, and combinations that are internally inconsistent.
4. Present each credible approach fairly.
5. Recommend one approach and state the accepted trade-offs.
6. Ask the user to choose, refine, request a hybrid, or add another lens unless autonomous execution was explicit.
7. Re-run only the affected exploration when new evidence or a material scope change justifies it.

A hybrid must be checked as a complete architecture rather than assembled from individually attractive parts.

## Output

### Chat output

When no artifact is requested, return:

- Context and assumptions
- Selected expertise and why it applied
- Considered approaches
- Comparison
- Recommendation and rationale
- Consequences and implementation implications
- Verification
- Unresolved follow-ups


### Assigned ADR output

Write exactly one ADR to the supplied path. It is complete only when it contains:

- Stable ID and title
- Decision context
- Constraints and drivers
- Considered approaches
- Research and sources where relevant
- Diagrams where useful
- Selected decision and rationale
- Trade-offs and consequences
- Implementation implications
- Failure handling and observability
- Verification considerations
- Unresolved follow-ups

Do not also create `architecture-decisions.md`.

### Aggregate output

When the caller requests an aggregate artifact, write `architecture-decisions.md` in the supplied work folder. Give each decision its context, approaches, comparison, chosen option, rationale, consequences, implementation implications, and verification. Keep dedicated ADRs as the source of truth when they already exist; summarize and link rather than duplicating them.

## Completion Criteria

Before finishing, verify that:

- expertise routing read the global table of contents, considered every `ACTIVE` global trigger, and accounted for every material global or plugin-local match;
- the chosen mode was no heavier than the decision required;
- all architecture claims have evidence or visible assumptions;
- ownership, boundaries, state, data flow, and failure paths are explicit;
- credible alternatives and accepted trade-offs are recorded;
- selected expertise materially affected or validated the decision;
- one actor owns each written artifact;
- assigned ADR mode preserved the exact ID and path;
- proposed verification can distinguish a correct architecture from an incorrect one;
- unresolved blocking evidence is routed rather than hidden.
