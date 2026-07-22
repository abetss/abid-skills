# rung-3 build plan — grammar-feedback judge (holistic)

**Judge design (settled):** a **holistic** LLM-as-judge that grades the evaluator's grammar observations on an essay — *did it catch the real errors (coverage) AND are its corrections right (correctness)?* → **`passed` (binary) + `note`**, per essay. This matches Hamel's critique-shadowing (one holistic pass/fail + critique); decomposing into separate correctness/coverage judges is a *later* step (Hamel Step 7), only if calibration/error-analysis shows we need it.

**Two ordering rules that override the naive sequence:**
1. **Label before you polish the prompt** — "you cannot write a good judge prompt until you've seen the data" (Hamel). Criteria + few-shot examples are an *output* of labelling.
2. **Online comes after calibration** — never deploy an uncalibrated judge.

**Agent file:** `apps/main-api/src/mastra/agents/english-evaluator/evals/grammer-observation-critic.agent.ts` (currently a bare `Agent`; input = `{ input, observations: Observation[] }`, output = `{ passed, note }`).

Legend: `[me]` = companion fetches/runs mechanically · `[you]` = your judgment / your code.

---

## A. Data + labels — FIRST, before any prompt work
1. `[me]` Fetch the calibration set from run `fa5b792a`: per essay, the essay text + its grammar observations (location / problem / suggested fix). Per-essay, because the judge is per-essay.
2. `[you / friend]` Hand-label ~10 essays — holistic **PASS/FAIL + note**. Record class balance (how many fails). **This is the anchor; everything downstream depends on it.**
   - Task instructions for a labeller: **`apps/main-api/src/mastra/features/english-evaluator/evals/progress/label-task-for-friend.md`**. Labeller must be strong at English grammar, one consistent person, no AI assistance, no answer key.

## B. The judge prompt — derived from those labels
3. `[you]` Soften the hard "≥80% match" rule into a holistic call expressed in the `note` (keep the AI re-finding issues as *context* it reasons over; don't gate on a fixed ratio).
4. `[you]` Fold 2–4 of the human labels in as **few-shot examples** (critique-before-verdict) + write the criteria that labelling surfaced.
5. `[you]` Pick the judge model (same Gemini vs a stronger model — self-preference tradeoff).

## C. Wire it as a scorer — unlocks offline + persistence + online
6. `[me+you]` Wrap the agent in a `createScorer` sibling — `passed`→1/0, `note`→reason, distinct `scorerId`. (Template to copy: `observation-a.scorer.ts`.)
7. `[me]` Register on the Mastra instance + configure `storage` so verdicts persist to `mastra.mastra_scorers` (a bare `scorer.run()` does not save).
8. `[me+you]` Add it to the offline eval run (`bun run eval:workflow`) beside Method A; inject the per-essay input via `preprocess`/`createPrompt` (`run.input` is type-dependent, no first-class `groundTruth`).

## D. Calibrate — the rung's actual deliverable
9. `[me]` Run the eval → judge scores the labelled essays.
10. `[you+me]` Build the **calibration table**: judge verdict vs the human label — raw agreement + PASS/FAIL **confusion counts** + **class balance**. (Compare *verdicts* for the metric; use the *notes* to understand disagreements.)
11. `[you]` If agreement `< 8/10`: read the disagreement cells, adjust criteria/few-shot, re-run. Iterate (~3 rounds, per Hamel). If class-imbalanced (e.g. 9 pass / 1 fail), report precision/recall on the minority class, not raw agreement.
12. `[you]` Record generator/judge **lineage + directional self-preference** (generator = Gemini; judge = ___; direction noted, **no magnitude imported** from the GPT-4/Claude figures).

## E. Online — only once D passes
13. `[me+you]` Attach the **same** scorer to the workflow so it runs on live submissions. This is the payoff of reference-free: *one identical scorer* runs offline (calibration) and online (production) — Method A can't, because it needs gold. Plumbing can be wired anytime; don't *trust* its output until calibrated.
14. `[you]` Sanity-check on a few fresh online essays.

## F. Close out (rung-3 is the final rung of Day 3)
15. Coverage evidence `cov-judge-design` + `cov-judge-calibration` → checkpoint `days/day-03/progress.md` + a root `· work ·` line → **end-of-day assessment** (see `guide.md → End-of-day`).

---

## Shortcut worth knowing
You can calibrate **before** wrapping it as a scorer: call the agent directly over the labelled essays and compare in a table (B↔D by hand), iterate the prompt fast, then do C once it's trustworthy. Hamel did exactly this in a spreadsheet.

## Current blocker
**Step 2 (the human labels).** Nothing downstream can start without them. Step 1 (fetch the set) is ready to run on request.

## Known app notes / caveats
- Agent version churned 20→22→20; confirm which evaluator variant (A vs B) is live before pinning calibration lineage.
- Primer `learn/rung-3.md` currently locks the judge to *correctness-only* — that was over-narrowed; this plan supersedes it with the holistic design. Reconcile the primer/brief later (non-blocking).
