## Eval-driven skill development

Anthropic's recommended way to build a skill: write the evaluations *before* the documentation, so the skill solves problems you've actually observed instead of ones you imagined. This is opt-in — offer it to the user and follow it only if they choose it. It pays off for **verifiable** skills (transforms, extraction, code generation, fixed workflows) where success is observable. For **subjective** skills (writing voice, visual taste) where there's no baseline to measure against, skip it and use the draft-first process in SKILL.md.

This file is the *methodology* — the order of operations. For the mechanics it leans on (writing assertions, grading, aggregating, computing the delta), use `evaluating.md`.

## Contents

- Why eval-first
- The loop
- The Claude A / Claude B split
- When to choose it vs draft-first
- Handing off to the eval mechanics

## Why eval-first

Writing instructions first tempts you to document an imagined problem — rules for cases that never occur, explanations the model didn't need. Building evals first forces the opposite: you watch the model fail at a real task, and you write only the instructions that fix the observed failures. The result is leaner and demonstrably better than no skill, because you measured it against a baseline.

## The loop

1. **Identify the gaps.** Run the model on 2–3 representative tasks **without any skill**. Capture exactly where it fails or what context it lacks — wrong output, missing domain knowledge, skipped steps, repeated questions you had to answer by hand.
2. **Create evaluations.** Turn each observed gap into a test case in `evals/evals.json` — a realistic prompt, the input files, and a description of success. Cover the failures you actually saw, plus one edge case.
3. **Establish the baseline.** Grade the no-skill runs against those cases. This is the number the skill has to beat; without it, "better" is an opinion.
4. **Write minimal instructions.** Add *just enough* to SKILL.md to close the observed gaps and pass the evals. Resist documenting anything the baseline already handled — the model knows it.
5. **Iterate.** Run the evals with the skill, compare against the baseline, and refine. Add an instruction only when a failing case demands it; cut one when removing it doesn't drop the pass rate. Stop when the delta is solid and feedback is consistently empty.

The discipline is step 4: the baseline tells you what the model can already do, so you write only what it can't.

## The Claude A / Claude B split

The most reliable version of this loop separates two roles:

- **Claude A** — the author you pair with to design and refine the skill. Works from the failures Claude B surfaces.
- **Claude B** — a *fresh* instance with the skill loaded, running real tasks. Its struggles are the data.

You watch Claude B, bring specific observations back to Claude A ("on a regional report it forgot to filter test accounts even though the skill mentions it — make that rule more prominent"), Claude A revises, then you re-test with a fresh Claude B. Each pass is grounded in observed behavior, not assumptions. In this repo, give each run its own subagent for the clean-context isolation (see `subagents.md`); each baseline and each iteration is a separate run.

## When to choose it vs draft-first

Choose **eval-driven** when:

- The output is objectively checkable (a file, a transform, a structured doc, code).
- You can run the task without the skill to get a baseline.
- Correctness matters enough to justify building the harness up front.

Stay with **draft-first** (the SKILL.md process, evals offered at the end) when:

- The skill is subjective — there's no pass/fail, only taste.
- It's a quick or low-stakes skill where the eval harness costs more than it returns.
- You're making a small edit to an existing skill, not building one.

## Handing off to the eval mechanics

Once the user opts in and you've identified gaps, the *how* of each step lives in `evaluating.md`: the `evals.json` shape, running with a baseline in `iteration-N/` workspaces, capturing timing, writing objective assertions, grading with quoted evidence, aggregating into a delta, and the analysis patterns (drop assertions that pass in both configs, study the ones the skill alone passes). `evaluating.md` also points at Anthropic's `skill-creator`, which automates the whole harness — prefer it over hand-rolling once the user is committed to the loop.
