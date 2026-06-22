# Finding the Right Solution

> Make informed decisions between alternatives so the solution serves the product well.

**Conditional:** Include when architectural decisions need to be made. Skip when the approach is obvious (e.g., follow existing patterns exactly).

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

## Methods

- **Delegate to the `architect-solution` skill** — It dispatches parallel `code-architect` agents with different design lenses, synthesizes approaches, and drives decisions with the user
- **Use `review-db-schema` skill** — When decisions involve database schema changes

## Process

### Step 1: Identify decisions that need resolution

Based on previous components (especially the gap analysis from Understanding the Current Landscape), identify which items have non-obvious approaches.

Present to user:

```
Here are the architectural decisions I've identified that need resolution:

1. [Decision]: [brief description of the choice]
   - Why it matters: [what this affects]

2. [Decision]: [brief description]
   - Why it matters: [what this affects]

These will be resolved using the architect-solution skill, which will explore multiple approaches for each decision.

Are there other decisions to add? Any to remove (approach is obvious)?
```

**Get user approval** on the list.

### Step 2: Delegate to architect-solution skill

Hand off the approved decisions to the `architect-solution` skill. Pass it:

- The decisions list from Step 1
- Relevant sections from `plan-prep.md` (current landscape, gap analysis)
- The `requirements.md` path
- Any design artifacts that inform the decisions

The skill will:
1. Dispatch research agents for codebase context
2. For each decision: propose lenses → user approves → dispatch code-architect agents → synthesize → present comparison → user decides
3. Write resolved decisions to `architecture-decisions.md` in the work folder

### Step 3: Incorporate decisions

After architect-solution completes, read `architecture-decisions.md` and summarize the key implications for the plan.

**Get user approval** on the summary before moving on.

## Output

Document in `plan-prep.md` (append after previous component):

```markdown
## Architecture Decisions

Decisions resolved via architect-solution skill. Full details in `architecture-decisions.md`.

### Summary of decisions and their implications:

**Decision 1: [Name]**
- Chosen: [approach]
- Key implication: [how this shapes the implementation]

**Decision 2: [Name]**
- Chosen: [approach]
- Key implication: [how this shapes the implementation]
```

Note: The full decision context, alternatives explored, and rationale live in `architecture-decisions.md`, not duplicated here.
