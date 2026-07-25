# Eval loop for generating-html-artifacts

Adapted from the `skill-creator` loop in [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator),
trimmed to what this repo can run. The point: every skill change is graded
against `evals/evals.json`, with a baseline, so improvements are measured
deltas instead of vibes.

## Layout

Runs go in a workspace **next to** the skill (git-ignored scratch space):

```
evals-workspace/
  iteration-1/
    0-migration-options-comparison/
      with_skill/outputs/…        grading.json  timing.json
      without_skill/outputs/…     grading.json  timing.json
    1-outage-postmortem/
      …
```

- Configs are directory names — `with_skill`, `without_skill`, `old_skill`,
  or model names (`haiku`, `sonnet`) when A/B-ing models.
- `old_skill` baseline: point the run at the sibling
  `generating-html-artifacts-old` skill — it is the natural pre-component
  baseline.

## Running an iteration

1. **Spawn all runs in the same turn** — with-skill AND baseline per eval, so
   they finish together and see the same conditions. One subagent per run:
   - *with-skill*: "Read the skill at `plugins/meta-skilling/skills/generating-html-artifacts/SKILL.md`
     and follow it to do this task: <prompt>. Save the artifact to `<workspace>/<eval>/with_skill/outputs/`."
   - *baseline*: same prompt, no skill (or the `-old` skill path).
   - Time each run (wall clock) and record `timing.json`:
     `{"duration_s": 123, "total_tokens": 45678}` — tokens only if your harness
     reports them; duration always.
2. **Grade scripted assertions** (while or after runs finish):
   ```bash
   python scripts/grade_artifact.py <run>/outputs/<file>.html --eval <id> --out <run>/grading.json
   ```
   This prints PASS/FAIL per scripted assertion and lists the assertions that
   still need judgment.
3. **Grade the rest with an LLM grader** — one subagent per run:
   "Read the artifact at <path> (and the run summary if saved). For each
   assertion below, decide pass/fail with one line of evidence. Append to
   `grading.json` in the same `{"text","passed","evidence"}` format:
   <pending assertions>." For assertions about the *summary* (component
   inventory), save the run's final summary to the run dir so the grader can
   read it.
4. **Aggregate**:
   ```bash
   python scripts/aggregate_benchmark.py evals-workspace/iteration-N --skill-name generating-html-artifacts
   ```
   Produces `benchmark.json` + `benchmark.md`: pass rate per config, per-eval
   breakdown, failed assertions, delta vs the first config.
5. **Analyst pass** — read benchmark.md and look for:
   - assertions that pass in *every* config including `without_skill`
     (non-discriminating — tighten or drop them),
   - evals with high variance across reruns (flaky prompt or flaky check),
   - time/token tradeoffs (is the skill expensive for what it adds?).
6. **Human review** — open the with-skill artifacts in a browser, both themes.
   The scripted checks read source; they do not render. Note feedback per eval,
   improve the skill, rerun into `iteration-(N+1)`.

## Model A/B (haiku vs sonnet)

Same loop, configs named by model. In Claude Code the skill's frontmatter
`model:` picks the forked model, so run one iteration per frontmatter value.
Compare pass rate, duration, and tokens in benchmark.md — that, not taste,
decides whether the cheaper model is good enough.

## Blind comparison (optional, rigorous)

For "is the new skill actually better than the old one": give an independent
agent the two artifacts for the same eval without saying which is which, ask
it to pick and justify. Repeat per eval; tally. Removes the reviewer's
attachment to either version.

## Trigger-rate evals (optional, after the skill stabilizes)

The frontmatter `description` decides when the skill fires. Build ~20 queries —
8–10 that should trigger (varied phrasings, including ones that never say
"HTML artifact") and 8–10 near-misses that should not (adjacent asks like
"make a React component in my app", "write a markdown report") — then check
the description against them and iterate. Keep the should-not-trigger cases
genuinely tricky; easy negatives test nothing.
