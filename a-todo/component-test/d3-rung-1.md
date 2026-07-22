# Rung rung-1 — Error-analyze the current run

**Requirement:** From the current comparable workflow baseline, read the failing observations trace by trace, turn them into a small **counted** failure taxonomy, and choose exactly one next target justified by frequency and impact.

---

## Primer

> You are about to do the single highest-leverage thing in applied AI: **look at your data**. Not a dashboard, not a summary — the actual gold-vs-candidate rows of a real eval run, one essay at a time. This rung is not about making F1 go up. It is about turning a number (F1 0.371) into a *named, counted list of failure modes* and one justified next target. Everything after today (the prompt change in rung-2, the judge in rung-3) is only as good as this reading.

### Sources you're assembling from (bibliography)

Everything below is assembled from six sources read in full, cached under [`../sources-raw/`](../sources-raw/). Body citations point to these:
- **[FG]** Field Guide — [`rung1-field-guide.md`](../sources-raw/rung1-field-guide.md) (Hamel & Shreya, Mar 2025)
- **[FAQ]** Evals-FAQ error-analysis — [`rung1-evals-faq-error-analysis.md`](../sources-raw/rung1-evals-faq-error-analysis.md) (near-verbatim on-page capture)
- **[YAN]** Yan, "…Fixing Your Process Will" — [`rung1-yan-eval-process.md`](../sources-raw/rung1-yan-eval-process.md) (Apr 2025)
- **[L123]** Hamel, "Your AI Product Needs Evals" — [`rung1-hamel-your-ai-product-needs-evals.md`](../sources-raw/rung1-hamel-your-ai-product-needs-evals.md) (optional; L1/L2/L3 ladder)
- **[ALL]** applied-llms.org Part I — [`rung1-applied-llms-part1.md`](../sources-raw/rung1-applied-llms-part1.md) (optional)
- **App code/data** — cited to the exact file/run in this repo.

> **Fidelity note (source-level):** [FAQ] is a near-verbatim Readability capture (reliable to quote). [FG], [YAN], [L123], [ALL] are faithful *reconstructions* via WebFetch (a small model rendered them) — quoted phrases are high-confidence but not guaranteed character-exact; the figures were cross-checked. See each raw dump's caveat before quoting.

---

### 1. The mental model: error analysis is a bottom-up, counted process — not a metric and not a tool

The instinct a strong SWE brings — "the F1 is 0.371, let me tweak the prompt" — is exactly the trap. Three of your sources open by naming it:

- Hamel calls skipping error analysis **"the most common mistake,"** and error analysis itself **"the single most valuable activity in AI development"** and **"consistently the highest-ROI activity"** ([FG] §1). The failure it prevents is the **"tools trap"**: adopting a framework/dashboard and getting a "false sense of measurement and progress" while the real, domain-specific failure never appears on a generic metric ([FG] §1).
- Yan's title is the whole argument: **"An LLM-as-Judge Won't Save The Product—Fixing Your Process Will."** Adding "another tool, metric, or LLM-as-judge… sidesteps the core problem and avoids the real work" ([YAN]). Evals are a *process*, not a purchase.
- The Evals-FAQ states it flatly: **"Error analysis is the most important activity in evals. Error analysis helps you decide what evals to write in the first place. It allows you to identify failure modes unique to your application and data"** ([FAQ]).

The method is **bottom-up**, and the contrast with top-down is the load-bearing distinction. Top-down analysis starts from generic, off-the-shelf labels (hallucination, toxicity, a generic F1 dashboard) and "often misses domain-specific issues"; bottom-up "forces you to look at actual data and lets metrics naturally emerge" ([FG] §1). The FAQ's version: error analysis "ensures that the evaluation metrics you develop are supported by real application behaviors instead of counter-productive generic metrics (which most platforms nudge you to use)" ([FAQ]).

> **Why this is exactly your situation (app fact).** You already *have* a top-down metric: Method-A pooled **F1 0.371** on run `7d58b8c2-988b-44b3-8dc0-b06a8b4874cc` ([progress.md → Starting state](../progress.md#starting-state-grounded-2026-07-12)). That number tells you the agent is missing a lot (recall 0.33 < precision 0.42) but tells you *nothing* about **what kind** of miss. Rung-1 is the bottom-up read that turns 0.371 into a list you can act on. The Field Guide's own success story is this exact arc: NurtureBoss read real conversation logs, found a domain-specific failure (date handling, "failing 66% of the time"), built tests for it, and drove it "from 33% to 95%" ([FG] §1) — none of which a generic dashboard would have surfaced.

```
  TOP-DOWN (where you are now)          BOTTOM-UP (where rung-1 takes you)
  ┌───────────────────────┐            ┌───────────────────────────────┐
  │  F1 = 0.371           │            │  read 11 essays' gold-vs-cand │
  │  P 0.42  R 0.33       │   ──vs──►  │  → open notes (first failure) │
  │  COR10 PAR6 MIS23 SPU15│           │  → axial taxonomy (named modes)│
  └───────────────────────┘            │  → COUNT each mode            │
   "something is wrong"                │  → pick ONE target (freq+impact)│
                                       └───────────────────────────────┘
                                        "THIS is wrong, N times, fix it"
```

### 2. The four-step procedure (open → axial → count → prioritize)

The Evals-FAQ gives the tightest procedural spec, and — importantly — it is the source that **names the steps** ([FAQ]; the Field Guide describes the *activity* but does not use the terms "open coding"/"axial coding" — verified absent, [FG] attribution note):

1. **Creating a dataset** — "Gathering representative traces of user interactions with the LLM" ([FAQ]).
   > *App fact:* your dataset already exists — the 11 essays × their gold in [`essays-v1.4.json`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/collections/essays-v1.4.json) (36 gold total), scored against the agent's candidates in run `7d58b8c2`. You don't gather traces; you read the ones the run produced.

2. **Open coding** — "Human annotator(s) (ideally a benevolent dictator) review and write open-ended notes about traces… akin to 'journaling'… adapted from qualitative research methodologies. When beginning, it is recommended to focus on **noting the first failure observed in a trace, as upstream errors can cause downstream issues**, though you can also tag all independent failures if feasible. A domain expert should be performing this step" ([FAQ]). The Field Guide's mechanical version: for each row, write "open-ended notes describing the undesired behavior" ([FG] §1).
   - **The first-failure rule** exists because errors cascade: if step 1 of a trace is wrong, everything downstream is contaminated, so you'd over-count. For a *single-shot* essay eval (no multi-turn cascade), "you can also tag all independent failures if feasible" ([FAQ]) applies — see the local-protocol note in §4 for how this interacts with set-matching.

3. **Axial coding** — "Categorize the open-ended notes into a 'failure taxonomy.' In other words, group similar failures into distinct categories. **This is the most important step.** At the end, count the number of failures in each category. You can use a LLM to help with this step" ([FAQ]).
   > **Two different superlatives — keep them straight (source-attribution).** [FAQ] says *axial coding* "is the most important step" (grouping + counting). [FG] says *error analysis as a whole* is "the single most valuable activity." Both are real; neither says "taxonomy-building is the most important step" in the Field Guide (verified — [FG] note). Cite each superlative to its own page.

4. **Iterative refinement / saturation** — "Keep iterating on more traces until you reach **theoretical saturation**, meaning new traces do not seem to reveal new failure modes… aim to review at least 100 traces. My rough heuristic is if ~20 traces don't turn up a new category, you can stop (but review at least 100 to start)" ([FAQ]). "The goal is to prioritize the failures that actually happen the most, not catch every possible failure (evals are not free, so we need to be pragmatic)" ([FAQ]).

Yan frames the same loop as **the scientific method**: Observation (Look at The Data) → Annotate → Hypothesize → Design & Run Experiments → Measure ([YAN]; *labels reconstructed* — see [YAN] caveat). Rung-1 is the first two boxes: **Observation + Annotate.** rung-2 is Hypothesize → Experiment → Measure. And Yan supplies the discipline that carries into rung-2: **"define success criteria… to ensure alignment and measurability from day one"** — name the pass/fail bar *before* you tune ([YAN]).

```
  Yan's loop (labels reconstructed):
  ┌────────────┐   ┌──────────┐   ┌────────────┐   ┌──────────────┐   ┌─────────┐
  │Observation │──►│ Annotate │──►│ Hypothesize│──►│ Run Experiment│──►│ Measure │──┐
  │(look@data) │   │(label 1st│   │(why fail?  │   │(1 change)    │   │(vs base)│  │
  └────────────┘   │ failure) │   │ prioritize)│   └──────────────┘   └─────────┘  │
        ▲          └──────────┘   └────────────┘                                    │
        └──────────────────────  rung-1 = these two  ─┘   rung-2 = these three ─────┘
```

### 3. Set-metric literacy: reading COR / PAR / MIS / SPU, and why they are not the failure count

This is the second owned concept (`cov-set-metric-literacy`) and it is an **app fact**, grounded entirely in the Method-A scorer code, not in the reading. Method A is a **set-matching** eval (SemEval-style), so its counts are about *matching*, not about *distinct semantic failures* — and the gap between those two is the whole point of the rung.

**How Method A matches** (from [`observation-scorer-a/utils.ts`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/scorers/observation-scorer-a/utils.ts), `match_observations`): a candidate observation matches a gold observation only when **all three gates pass**:

```
  gate 1:  candidate.category    === gold.category          (exact)
  gate 2:  candidate.subcategory === gold.subcategory       (exact string)
  gate 3:  location token-multiset Jaccard ≥ 0.5            (DEFAULT_MATCH_THRESHOLD)
```

Matching is **greedy 1:1** — each gold claims its highest-overlap unclaimed candidate (`claimed` set in the code). The roll-up buckets (SemEval labels, from the `MatchCounts` type):

| bucket | meaning | code |
|---|---|---|
| **COR** (correct) | matched, location Jaccard **== 1** | pair with perfect span |
| **PAR** (partial) | matched, location Jaccard **< 1** | pair with span drift |
| **MIS** (missed) | a **gold** with no matching candidate | false negative |
| **SPU** (spurious) | a **candidate** with no matching gold | false positive |

And the metrics (`compute_metrics`), with **partial credit** (a PAR counts as half):

```
  found      = COR + 0.5·PAR
  precision  = found / (COR + PAR + SPU)      // of what the agent said, how much was right
  recall     = found / (COR + PAR + MIS)      // of the gold, how much the agent found
  F1         = harmonic mean(precision, recall)
```

> **App fact (the baseline, [Starting state](../progress.md#starting-state-grounded-2026-07-12)):** run `7d58b8c2` pooled **COR 10 / PAR 6 / MIS 23 / SPU 15**, P 0.419, R 0.333, F1 0.371. Note the pooled F1 is recomputed from *summed* counts across essays, **not** the mean of per-essay F1s (repo [`CLAUDE.md`](/Users/abtinghods/Ork/code/english-workshop/CLAUDE.md)).

#### The reconciliation that is the crux of the rung

Here is the trap set-metric literacy must defuse. **A single mislabelled prediction can surface as BOTH a MIS and a SPU.** If the agent finds the right span and right category but emits the *wrong subcategory leaf*, gate 2 (`subcategory !== gold.subcategory`) blocks the match. The consequence, in code:
- the **gold** it was trying to name becomes a **MIS** (no candidate matched it), and
- the **candidate** becomes a **SPU** (it matched no gold).

So **one semantic failure ("agent saw the error but named the wrong leaf") = 1 MIS + 1 SPU** in the counts. Therefore **23 MIS + 15 SPU is NOT 38 independent failures.** Some unknown number of them are the same prediction failing gate 2 twice.

> **App fact — this is real in your baseline, not hypothetical.** Pulled from run `7d58b8c2`, essay `corrections-and-improvements-long` (F1 0.182, COR 1 / PAR 0 / MIS 5 / SPU 4), the `by_observation` rows include these **paired** MIS+SPU (same span, same category `grammar`, different subcategory leaf):
>
> | gold (→ MIS) | candidate (→ SPU) | same span? |
> |---|---|---|
> | `grammar/voice_active_passive` "She born in a small village" | `grammar/passive_voice` "She born in a small village" | ✅ identical |
> | `grammar/tense` "she work very hard since she was a child" | `grammar/tense_consistency` "she work very hard…" | ✅ identical |
> | `grammar/possessive` "a person life" | `grammar/possessive_nouns` "a person life" | ✅ identical |
> | `grammar/dependent_preposition` "listen her for hours" | `grammar/prepositional_verbs` "I can listen her for hours" | ≈ overlap (candidate span longer) |
>
> That's **4 MIS + 4 SPU = 8 rows** on this one essay that are really **~4 distinct failures** ("right error, wrong subcategory leaf"). Contrast the genuine miss on the same essay: gold `tone/warmth` (a long sentence) has **no candidate at all** → a pure MIS, a *distinct* recall failure. And essay `corrections-only-short`: gold `grammar/indefinite_article` "My sister is nurse" MIS ↔ candidate `grammar/articles` "My sister is nurse" SPU — again **one** failure, not two.

**Why the subcategory leaf drifts (root-cause app fact).** The agent's `subcategory` field is an **open `z.string()`, not a closed enum** — the ~280-leaf taxonomy blows Gemini's structured-output schema limit, so the *only* thing steering the model to the exact gold leaf is the prompt's SUBCATEGORY guidance ([Starting state](../progress.md#starting-state-grounded-2026-07-12); agent [`english-evaluator.agent.ts`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/agents/english-evaluator.agent.ts)). This is *why* you get near-synonym leaves (`passive_voice` vs the gold `voice_active_passive`). It is a live candidate for the rung-2 hypothesis — but rung-1 only *names and counts*; it does not fix.

> **Do not read past this without internalizing the distinction:** the **unit of analysis** for error analysis is a **distinct semantic failure**, not a scorer row. The scorer counts rows (MIS/SPU); *you* count failures. Reconciling paired rows *before* counting is the difference between "prioritize the subcategory-leaf problem (huge)" and "chase 38 phantom bugs."

### 4. Failure modes & pitfalls to guard against

Four distinct evidence classes are in play in this rung; keep them separate:

- **Source claim** — open/axial/count/saturation/first-failure/prioritize-by-frequency ([FAQ], [FG], [YAN]).
- **App fact** — Method-A gates, COR/PAR/MIS/SPU, the paired-row mechanism, the real `by_observation` examples above, the open-`z.string()` subcategory (cited to code/run/Starting state).
- **Local inference** — e.g. "the 11-essay seed cannot be *saturated*." Entailed by [FAQ]'s "review at least 100 to start," since 11 ≪ 100 — but **the source never mentions our corpus.** Label it ours.
- **Local protocol** — e.g. "reconcile paired MIS+SPU as one failure before counting." This is a *sprint decision* about how to apply open/axial coding to a set-matching metric; it is not stated by Hamel/Yan (their first-failure rule is about *cascading multi-turn traces*, [FAQ]). It's the honest bottom-up reading of *this* scorer.

Specific traps:
- **Counting rows, not failures.** Treating 23 MIS + 15 SPU as 38 independent modes. The paired-row reconciliation above is the antidote. (App-grounded.)
- **Fixing before counting.** The urge to jump to "let me constrain the subcategory" is rung-2. Open→axial→**count** first; the count is what justifies the target ([FAQ] "count the number of failures in each category"; [FG] "counted the frequency of each issue").
- **Calling 11 essays "saturated."** You have not reached saturation; you have a *prioritization seed*. [FAQ]'s heuristic is "≥100 to start." With 11 essays you can *rank* failure modes but not *close* the taxonomy. Say so explicitly. (Local inference on [FAQ].)
- **Prioritizing by raw frequency alone, ignoring impact.** The three `no_feedback_needed` essays score COR=1 (a correct "stay silent" — [`utils.ts` `evaluate`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/scorers/observation-scorer-a/utils.ts), the empty-gold branch). A COR is not a failure to chase. And recall (0.33) < precision (0.42) → you are **recall-bound**: the biggest lever is the failures that *cost recall* (MIS and the MIS-half of paired rows), not the SPU-only noise. Frequency **and** impact ([FG] prioritizes by frequency; the recall-bound impact read is a local inference on the baseline metrics).
- **Goodhart is NOT your rung-1 concept.** [ALL] §1.4.4 invokes Goodhart's Law for *over-optimizing a single eval* (NIAH). That is scoped to over-optimization; do not import it into rung-1's set-metric reading. (Attribution discipline — [ALL] note.)

### Learning coverage

Each owned concept maps to evidence you must *produce* in the Build (not just read here):

| coverage_id | concept | evidence you must produce in the Build |
|---|---|---|
| `cov-error-analysis` | open → axial → count → prioritize; first-failure rule; small-seed ≠ saturation | a persisted report with: per-failing-observation open notes → a **named** axial taxonomy → **per-mode counts** → **exactly one** target justified on frequency **and** impact; an explicit line that 11 essays is prioritization evidence, not theoretical saturation |
| `cov-set-metric-literacy` | read COR/PAR/MIS/SPU → P/R/F1; reconcile a paired MIS+SPU as one failure | in the report, the paired rows (right span+category, wrong subcategory leaf) **explicitly merged into single failures before counting**, with the reason (gate-2 fails → 1 MIS + 1 SPU for one prediction) |

---

## Reading

> **Measured budget (rung-1):** Core ⏱ **39 min** · full list (Core + Optional) ⏱ **131 min (~2h 11m)**. Times measured 2026-07-12 with `estimate-reading-time.mjs` @ 200 wpm on the article body. You do **not** need the optional set before building.

### Core (⏱ 39 min)

- **Hamel Husain & Shreya Shankar — [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/)** (Mar 2025) · ⏱ **32 min** · *Why read:* the canonical account of "look at your data before touching the system" and the tools-trap it prevents; the NurtureBoss 66%→95% arc is the template for what you're about to do. *Extract:* bottom-up vs top-down; "used an LLM to build a taxonomy of common failure modes… counted the frequency of each issue"; prioritize by frequency. (Note: the *terms* open/axial coding and the first-failure rule are NOT here — get those from the FAQ below.)
- **Hamel & Shreya — [Evals-FAQ: "Why is error analysis so important…"](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html)** · ⏱ **2 min** · *Why read:* the tightest procedural spec — this is the one you'll actually follow, step by step. It's short but dense; read it twice. *Extract:* the four named steps (Creating a Dataset → Open Coding → Axial Coding → Iterative Refinement); "note the first failure observed in a trace"; axial coding "is the most important step… count the number of failures in each category"; theoretical saturation ("≥100 to start; ~20 with no new category → stop").
- **Eugene Yan — [An LLM-as-Judge Won't Save The Product—Fixing Your Process Will](https://eugeneyan.com/writing/eval-process/)** (Apr 2025) · ⏱ **5 min** · *Why read:* reframes error analysis as a *process* (the scientific method), and gives the discipline you'll need in rung-2 — define the pass/fail bar before you tune. *Extract:* Observation → Annotate → Hypothesize → Experiment → Measure; "define success criteria… from day one"; "buying or building yet another evaluation tool won't save the product." (No decision tree in this article — it's a loop.)

### Optional / go deeper (adds ⏱ 92 min → 131 min total)

- **Hamel — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)** (Mar 2024) · ⏱ **20 min** · *Marginal benefit — future-rung bridge:* situates today's work in the **L1 (unit tests/assertions) / L2 (human & model eval) / L3 (A/B)** ladder. *Extract:* where code assertions end and an LLM judge begins ("validation that cannot be tested by assertions alone" = start of L2) — your Method-A scorer is L1-family; the rung-3 judge is L2. Bridges forward, not needed to build rung-1.
- **applied-llms.org — [What We Learned from a Year of Building with LLMs, Part I](https://applied-llms.org/)** · ⏱ **70 min** · *Marginal benefit — independent corroboration:* six practitioners on assertion-first eval discipline (§1.4.1) and "Look at samples of LLM inputs and outputs every day" (§2.1.2). *Extract:* the assertion-first habit; the "Intern Test" (§1.4.3) for diagnosing why a generation failed. Long; skim §1.4.
- **DeepLearning.AI (Arize) — [Evaluating AI Agents](https://www.deeplearning.ai/courses/evaluating-ai-agents/)** · ⏱ **2 min** (public outline only) · *Marginal benefit — structured-video on-ramp:* a paced walkthrough of the annotate→experiment cadence if you want video. *Extract:* public outline only (17 lessons; lesson 13 "Improving your LLM-as-a-judge" bridges to rung-3). Gated content not accessed; don't infer lesson content from titles.

---

## Build

### Current app context

You are reading, not changing. The run is already scored and persisted; rung-1 **must not** touch the agent or the scorer (that's rung-2). The surfaces you'll use:

- **The run:** `7d58b8c2-988b-44b3-8dc0-b06a8b4874cc` — target `essay_feedback_workflow`, workflow v2 · agent v4 · corpus v1.4 · Method-A report v1 · `gemini-3.5-flash` · **F1 0.371, COR 10 / PAR 6 / MIS 23 / SPU 15, 13 matched pairs** ([Starting state](../progress.md#starting-state-grounded-2026-07-12)). Confirm it's still the latest workflow run before you start (temp 0 → an unchanged re-run reproduces it near-exactly; the companion can re-run `bun run eval:workflow` to confirm).
- **The viewer:** the admin dashboard's **Gold-vs-candidate** per-essay drill-down — `bun run dev:admin` → `http://localhost:5174/v1/workflows/essay_feedback_workflow?run=7d58b8c2-988b-44b3-8dc0-b06a8b4874cc`. This *is* your data viewer (the Field Guide's "most important investment", [FG] §2 — you already have it; you don't build one).
- **The per-observation data behind it:** each scored row's `analyzeStepResult.report.by_observation` (keyed by observation id; each entry has `status` ∈ correct|partial|missed|spurious, `reference` = gold, `candidate` = agent) and `report.field_summary` (repo [`CLAUDE.md`](/Users/abtinghods/Ork/code/english-workshop/CLAUDE.md)). The companion may fetch these raw rows for you (`GET /api/eval-runs`, or SQL on `mastra.mastra_scorers`) — but **you** read them.

### Exercise — do error analysis on the real run

Go essay by essay through the failing observations of run `7d58b8c2` and produce a counted failure taxonomy with one chosen target. Concretely:

1. **Open code (first pass, no theory).** For each *failing* observation (every MIS, SPU, and PAR row — the COR rows are hits, skip them), write a one-line open note in your own words describing what actually went wrong. Look at the gold and the candidate side by side. Don't categorize yet — just journal ([FAQ] "open-ended notes… akin to journaling"). Note the first/primary failure per row; for these single-shot essays you may tag independent failures too ([FAQ]).
2. **Reconcile the scorer rows into semantic failures.** *Before* counting, merge each paired **MIS+SPU that is the same span + same category with a different subcategory leaf** into ONE failure, and write *why* (gate-2 exact-subcategory fails → the one prediction becomes both a MIS and a SPU). This is `cov-set-metric-literacy`, and it's the step that separates a real taxonomy from 38 phantom bugs. Keep genuine solo-MIS (no candidate) and solo-SPU (no gold) as their own failures.
3. **Axial code (name the taxonomy).** Group your reconciled failures into a small set of **named** modes. Let the names emerge from the data — don't import a generic label set ([FG] bottom-up). Expect a handful, e.g. distinct kinds of "right error / wrong subcategory leaf," span-drift PAR, pure recall miss — but **derive them yourself**; the Starting-state note is your grader's private key, not your answer.
4. **Count.** Tally how many reconciled failures fall in each named mode ([FAQ] "count the number of failures in each category"). A tiny table is enough.
5. **Prioritize — pick exactly ONE target.** Choose the single mode to attack in rung-2, justified on **frequency AND impact** — remember you're recall-bound (R 0.33 < P 0.42), and `no_feedback_needed` CORs are not failures. State the justification in one or two sentences.
6. **Saturation caveat.** Add one explicit line: 11 essays is a prioritization seed, not theoretical saturation ([FAQ] "≥100 to start"); the ranking is directional, not closed.

*(The `/eval-error-analysis` skill can mechanically tally your codebook once you have one — it **counts** against your taxonomy; it does not choose the target or write the notes. Use it to check your arithmetic, not to skip the reading.)*

### Inputs / starting evidence

- The 11 essays and their gold: [`essays-v1.4.json`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/collections/essays-v1.4.json) (per-essay gold counts `3,10,2,3,4,6,0,0,3,5,0`).
- The scored run `7d58b8c2` `by_observation` rows (companion fetches raw on request).
- The Method-A definition: [`observation-scorer-a/utils.ts`](/Users/abtinghods/Ork/code/english-workshop/apps/main-api/src/mastra/scorers/observation-scorer-a/utils.ts) — re-read the three match gates and the COR/PAR/MIS/SPU roll-up if the counts confuse you.

### Artifact to produce

A **persisted error-analysis report** (written to [`../progress.md`](../progress.md) under Rung progress, or a linked file) containing: (a) open notes on the failing observations; (b) the paired-row reconciliations with reasons; (c) a named axial taxonomy; (d) per-mode counts; (e) exactly one chosen target with a frequency+impact justification; (f) the saturation caveat. It must name the exact run identity it read (target, corpus, versions, run id).

### Success criterion

The report lets someone else pick up rung-2 without re-reading the raw run: they can see the named modes, the counts, why the paired rows are one failure each, and which single target was chosen and why. The unit of analysis is a **distinct semantic failure**, never a raw scorer row.

### Hints / rubric

*Hints (only after an attempt — see the guide's hint ladder):*
- Stuck on whether two rows are one failure? Ask: do the gold row and the candidate row describe the **same underlying error at the same span**? If yes and only the subcategory leaf differs, it's one failure (gate 2).
- Stuck on the taxonomy? Group by *what the agent did wrong*, not by grammar topic: "found it but mislabeled the leaf" vs "found a longer span than gold (PAR drift)" vs "missed it entirely (no candidate)."

*Rubric (independent mastery):* a counted taxonomy; paired rows reconciled with the gate-2 reason stated; exactly one target justified on frequency **and** impact (recall-bound read); the saturation caveat present; minimal hints needed. *Partial:* needed prompting to reconcile paired rows or to weigh impact vs raw count. **No answer leakage — the taxonomy is derived by the learner, never supplied.**

---

## Verify

- [ ] The analysis names the exact run identity it read (target `essay_feedback_workflow`, corpus v1.4, workflow v2 · agent v4 · scorer/report v1, run id `7d58b8c2-988b-44b3-8dc0-b06a8b4874cc`).
- [ ] The unit of analysis is a **distinct semantic failure**, not raw MIS+SPU rows; paired rows (same span + category, wrong subcategory leaf) reconciled to one failure **before** counting, with the gate-2 reason stated.
- [ ] The report contains open notes, a small **named** axial taxonomy, per-mode counts, and **exactly one** next target justified by frequency **and** impact.
- [ ] It states that the 11-essay seed is prioritization evidence, not theoretical saturation.
