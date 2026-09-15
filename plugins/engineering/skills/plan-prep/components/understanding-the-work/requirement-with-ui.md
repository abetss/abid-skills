# Understanding What Needs to Be Done

> Know what we're building before anything else.

## Need

Fully understand the scope, intent, and constraints of the work so that every subsequent component is grounded in a clear picture of what we're trying to achieve.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute and return the architecture points encountered while interpreting the requirements and design artifacts; leave their lifecycle to the shared protocol.

## Methods

- **Read requirements.md** — Understand the feature, acceptance criteria, business rules, constraints
- **Read design artifacts** (if they exist) — Scan the work folder for all `design-discovery-result.md` files — each is the manifest for one design area. For each one found: extract referenced component folders and read each one's `view-model-props.md` and `design-result.md`. Also read any `discovery.md` alongside it, and Storybook stories from `final/` subfolders. These are settled facts — do not question or redo design decisions.
- **Ask clarifying questions** — Surface ambiguities, missing information, unclear acceptance criteria
- **Push back on requirements** — Flag requirements that seem problematic, contradictory, or unnecessarily complex
- **Research** — Look into unfamiliar domains, technologies, or patterns mentioned in the requirements
- **Engineer brings knowledge** — Apply technical knowledge to interpret requirements and identify implications
- **Surface architecture points** — For every technical decision implied by the requirements, ask: is there more than one decent way to achieve this? If yes, does it warrant an architectural discussion? If so, contribute it through the shared architecture-decision protocol

## Process

### Step 1: Read everything provided

**Detect and read design artifacts (if this is UI/frontend work):**

1. Scan the work folder for all `design-discovery-result.md` files — a feature can have multiple design folders, each with its own manifest.
   - For each one found: read it fully, extract all referenced component folder paths
   - For each component folder: read `view-model-props.md` and `design-result.md` if they exist
   - Note any `final/` subfolders — they contain Storybook stories (`.stories.tsx`)
   - Read any `discovery.md` in the same folder (captures design questions and decisions)
2. `requirements.md` is always read (engineering requirements)

If no `design-discovery-result.md` files are found → backend/service work, no design context to load. Skip silently.

Take note of:
- What is the feature trying to achieve for the user?
- What are the acceptance criteria?
- What constraints exist (technical, business, compliance)?
- What design artifacts exist? What UI data contracts and component variants do they define?
- What is NOT specified that should be?

### Step 2: Summarize understanding

Present to user:

```
Here's my understanding of what needs to be done:

**Feature:** [one-line summary]
**Goal:** [what this achieves for the user]
**Scope:** [what's in and out of scope]

**Key requirements:**
- [requirement 1]
- [requirement 2]
- ...

**Design artifacts:** (or "none" if no design artifacts found)

**[Sub-feature name]**
- [design-discovery-result.md](./sub-feature/design-discovery-result.md): [one-line description of what it defines]
- [view-model-props.md](./sub-feature/view-model-props.md): [one-line description of UI data contracts]
- [requirements.md](./sub-feature/requirements.md): [one-line description]
- [any other file found](./path): [one-line description]

(repeat for each design folder found)

**Open questions:**
- [anything unclear, ambiguous, or missing]

**Concerns / pushback:**
- [anything that seems problematic]

Does this match your understanding? Anything to correct or add?
```

**Get user approval** before proceeding to Step 3.

## Output

Document in `plan-prep.md`:

```markdown
# Plan Preparation: [Feature Name]

## Understanding What Needs to Be Done

**Feature:** [summary]
**Goal:** [user-facing goal]
**Scope:** [in/out]

**Requirements:**
- [requirement 1]
- [requirement 2]

**Design Artifacts:** (or "none" for backend-only work)

**[Sub-feature name]**
- [design-discovery-result.md](./sub-feature/design-discovery-result.md): [one-line description of what it defines]
- [view-model-props.md](./sub-feature/view-model-props.md): [one-line description of UI data contracts]
- [requirements.md](./sub-feature/requirements.md): [one-line description]
- [any other file found](./path): [one-line description]

(repeat for each design folder found)

**Clarifications Resolved:**
- [question] → [answer]
```
