## Testing a skill

A skill that doesn't trigger is dead weight; a skill that triggers badly is noise. Test both axes before calling the skill done.

## Contents

- Triggering tests (should/should-not queries)
- Functional tests (does the output work)
- Trigger debugging with a fresh session
- The "iterate on a single task first" loop
- Under- vs over-triggering diagnostics

## Triggering tests

**Goal:** the skill loads on relevant queries and stays out of the way on unrelated ones.

Before marking a skill done, write:

- 3 queries that **should** trigger the skill
- 3 queries that **should NOT** trigger the skill

Include paraphrased requests, not just the canonical phrasing. Real users won't use your exact keywords.

Example for a "project-sprint-planning" skill:

```
Should trigger:
- "Help me plan this sprint"
- "Create tasks for Q4 planning in Linear"
- "Set up a new sprint with the mobile team"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Write me a Python function"
- "Summarize this article"
```

## Functional tests

**Goal:** the skill produces correct output.

For verifiable skills (code generation, data transforms, file processing), run a representative task end-to-end and check:

- Valid outputs generated
- External calls (MCP, APIs) succeed
- Error handling fires on bad input
- Edge cases covered

For subjective skills (writing style, visual design), replace this with a few "does this feel right?" comparisons against known-good examples.

## Trigger debugging in a fresh session

Best-practices-documented technique: open a fresh Claude session and ask:

> "When would you use the [skill name] skill?"

Claude will paraphrase the description back. Compare its paraphrase to your intended trigger surface:

- Paraphrase is missing a context you care about → add that context to the description
- Paraphrase includes a context you don't want → add a negative scope clause or tighten the domain
- Paraphrase is generic ("helps with files") → description is too vague; add specific phrases and keywords

## Iterate on a single task first

The most effective skill authors iterate on **one challenging task** until Claude succeeds, then extract the winning approach into the skill. This leverages in-context learning and gives faster feedback than broad testing. Once a single task works, expand to multiple test cases for coverage.

## Under-triggering diagnostics

Symptoms:
- Skill never loads automatically
- Users have to manually invoke it
- Claude "helpfully" handles the task without consulting the skill

Fixes (in order):
1. Add specific keywords and phrases users actually say
2. Add file types if applicable (`.fig`, `.pdf`, `.xlsx`)
3. Add "even when the user doesn't explicitly say ..." clauses
4. Be pushier — the description is the only thing Claude sees before deciding

## Over-triggering diagnostics

Symptoms:
- Skill loads on unrelated queries
- User disables it or tells Claude to ignore it
- Confusion about the skill's purpose

Fixes:
1. Add a negative scope clause: `Do NOT use for [X], use the [other-skill] skill instead.`
2. Narrow the domain — replace "documents" with "PDF legal documents for contract review"
3. Remove over-broad trigger phrases
