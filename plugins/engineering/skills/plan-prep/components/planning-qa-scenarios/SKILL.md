# Planning QA Scenarios

> Define what correct behavior looks like before we build — from a product owner's perspective.

## Need

Surface every "when X happens, expect Y" scenario from requirements and any available desired-flow designs, so that:
- Missing requirements are caught before implementation begins
- Edge cases shape the design, not just the testing
- Implementers know exactly what success looks like for every path
- Post-implementation QA has a starting inventory instead of rediscovering everything from scratch

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute and return the architecture points this component finds. Architecture opportunities returned by the delegated QA-writing skill are findings of this component and use the same protocol.

## Method

**Delegate to the `manual-qa-case-writing` skill** with planning-phase adjustments.

The QA writing skill already knows how to systematically think about edge cases, permissions, error states, boundaries, and accessibility. We invoke it with the right context and instructions rather than duplicating that expertise here.

## Process

### Step 1: Invoke the QA writing skill with planning-phase instructions

Pass the QA writing skill:
- The requirements and any available desired flows from Design the Solution in `plan-prep.md` as context
- These adjustments to its normal behavior:

**Instructions to pass to the skill:**

> You are writing QA scenarios during the PLANNING phase, before any code exists.
>
> **Adjustments from your normal mode:**
>
> 1. **Product owner lens** — Write from the perspective of someone who knows what the product should do but nothing about how it's built. No implementation details.
>
> 2. **Every scenario must be verifiable from the consumer's perspective** — The expected outcome must be something the user/consumer can observe (what they see, where they land, what message appears). Never reference internal state. "Expect the shift is created" is NOT verifiable. "Expect the user is redirected to the weekly schedule and sees the new shift displayed" IS verifiable.
>
> 3. **Write autonomously, flag doubts** — Do NOT ask the user to approve every scenario. Write all of them, then present ONLY items needing user input: ambiguous scenarios marked `[NEEDS DECISION]`, missing requirements, and architecture points.
>
> 4. **Surface architecture points** — For every decision, ask: is there more than one decent way to achieve this? If yes, return the point to the invoking Planning QA Scenarios component for contribution through its shared protocol.
>
> 5. **Flag missing requirements** — When a scenario reveals undefined behavior, mark it `[NEEDS DECISION]`.
>
> 6. **Derive from requirements and available desired flows only** — If a scenario can't be derived from what's documented, it doesn't belong here. No guessing about implementation details.
>
> 7. **Output to `plan-prep.md`** under a `## Planning QA Scenarios` section, not to `qa.md`.
>
> 8. **Include cross-flow scenarios** — After individual flows, add scenarios that span multiple flows.

### Step 2: Present items needing user input

Present ONLY:
- Scenarios marked `[NEEDS DECISION]`
- Missing requirements discovered
- Architecture points surfaced

```
I've written [N] QA scenarios across [N] flows.

**Items needing your input:**

**Needs Decision ([N]):**
- [NEEDS DECISION] When [condition], expect [???] — [why this is ambiguous]

**Missing Requirements ([N]):**
- [description of undefined behavior]

**Architecture Points ([N]):**
- [description] — multiple decent approaches exist

Everything else has been written to plan-prep.md.
```

## Key Principles

- **Product owner lens** — No implementation knowledge. "When the user does X, expect Y."
- **Verifiable from the consumer** — Observable outcomes only. If you can't verify it without checking the database, rewrite it.
- **AI-driven** — Write all scenarios autonomously. Only involve the user for genuine ambiguity.
- **Delegate, don't duplicate** — The QA writing skill has the expertise. This component provides the context and adjustments.

## Output

Document in the `## Planning QA Scenarios` section of `plan-prep.md`:

```markdown
## Planning QA Scenarios

### Flow: [Name]

**Happy Path:**
- When [action], expect [observable outcome]

**Edge Cases:**
- When [boundary condition], expect [observable behavior]

**Error States:**
- When [failure condition], expect [what user sees]

**Permissions:**
- When [wrong role does action], expect [what user sees]

**Data States:**
- When [empty collection], expect [what user sees]

**Accessibility:** (if UI work)
- When [keyboard/screen reader action], expect [accessible behavior]

---

(Repeat for each flow)

### Cross-Flow Scenarios
- When [flow A outcome] followed by [flow B action], expect [behavior]

### Decisions Needed
- [NEEDS DECISION] [scenario] — [why ambiguous]

### Architecture Points Surfaced
- [topic] — [brief description]
```
