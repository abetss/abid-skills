# Resolve Architecture Decisions

> Make informed decisions between material alternatives so the solution serves the product well.

**Conditional:** Select when material architecture points are routed to Design the Solution for resolution. Architecture-point discovery remains cross-cutting rather than a step in this concern.

## Shared Protocol

Read and follow `../architecture-decision-protocol.md`. It is the single source of truth for contributions, ownership, routing, architecture artifacts, and completion gates.

## Need

Choose between alternative approaches so that the solution is:

- **The simplest viable approach**
- Secure
- Performant
- Resilient to future feature and code changes
- Easy to maintain
- Cost-effective (development effort and infrastructure)
- Consistent with the existing system's direction
- Scalable to the product's growth trajectory

## Method

- **Delegate to the `architect-solution` skill** — It routes relevant expertise, chooses direct or multi-perspective resolution according to the decision, synthesizes credible approaches, and drives decisions with the user.

## Procedure

### Step 1: Confirm the resolution set

Read the architecture-point contributions and table-of-contents entries routed to this component. Present the material decisions and why each matters:

```markdown
Here are the architecture decisions routed to Design the Solution:

1. [ADR-NNN — Decision]: [brief description of the choice]
   - Why it matters: [what this affects]

These will be resolved using the architect-solution skill, which will choose the smallest sufficient resolution mode and explore multiple approaches when material trade-offs require them.

Are any ownership or scope corrections needed before resolution?
```

Get user approval. This step is complete when every routed point is either approved for resolution here or returned to the workflow owner for rerouting under the shared protocol.

### Step 2: Delegate to architect-solution

Build the dependency graph between approved decisions. Launch every dependency-ready decision concurrently, with one isolated `architect-solution` assigned-ADR invocation and one exclusive ADR path per decision. Serialize a decision only when it requires another decision's output or a user checkpoint.

For each approved decision, hand off to the `architect-solution` skill:

- Its stable ID, title, context, constraints, drivers, evidence, and blocking state
- Relevant solution-design and current-landscape findings
- The requirements path
- Any design artifacts or independently selected precedent research that informs the decision
- Its assigned `{work-folder}/architecture/ADR-NNN-short-title.md` path

The skill will:

1. Inspect plugin-local expertise first, then consult the global expertise index for uncovered material concerns.
2. Gather only missing evidence, choose direct or multi-perspective resolution, and display any proposed lenses, assignments, and parallelization for approval unless autonomous execution was explicit.
3. Synthesize the evidence and any independent architecture lanes, present a recommendation, and record the user's decision.
4. Produce the ADR required by the shared protocol at the assigned path through exactly one artifact owner.

This step is complete when every approved decision has a protocol-compliant ADR or has been returned for rerouting.

### Step 3: Incorporate decisions

Read the completed ADRs and summarize their key implications in the affected solution-design outputs. Get user approval on the summary, then return each decision's status and ADR link to the workflow owner for consolidation under the shared protocol.

## Output

Return an architecture summary for integration into `plan-prep.md` without duplicating the ADRs:

```markdown
## Architecture Decisions

Full details: `architecture/table-of-contents.md`

**ADR-NNN: [Name]**
- Chosen: [approach]
- Key implication: [how this shapes the solution]
```
