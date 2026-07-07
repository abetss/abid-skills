## Evaluating a skill's output quality

Triggering tests (see `testing.md`) tell you the skill *loads*. Evals tell you the output is
actually *good* — reliably, across varied prompts, in edge cases, and better than no skill at
all. Evals are opt-in: objectively-verifiable skills (transforms, extraction, code generation,
fixed workflows) benefit most; purely subjective skills (writing voice, visual taste) are
better judged by eye. Offer them; don't force them.

## Contents

- Designing test cases
- Running with a baseline
- Capturing timing
- Writing assertions
- Grading
- Aggregating
- Analyzing patterns
- Human review
- Iterating
- Automating with skill-creator

## Designing test cases

A test case has three parts: a **prompt** (a realistic user message), an **expected output**
(a human-readable description of success), and optional **input files**. Store them in
`evals/evals.json` in the skill directory:

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "prompt": "I have monthly sales in data/sales_2025.csv. Find the top 3 months by revenue and make a bar chart.",
      "expected_output": "A bar chart of the top 3 months by revenue, with labeled axes and values.",
      "files": ["evals/files/sales_2025.csv"]
    }
  ]
}
```

Tips: start with 2–3 cases (don't over-invest before the first results); vary phrasing
(casual and precise, short and long); cover at least one edge case (malformed input, ambiguous
request); be concrete (real paths, column names, context — "process this data" tests nothing).
Hold off on pass/fail checks — you write those after seeing the first run.

## Running with a baseline

Run each case twice: once **with the skill**, once **without** (or against the previous
version, when improving an existing skill). The baseline is what makes the result mean
anything. Organize results in a workspace beside the skill, one `iteration-N/` per pass, each
case its own directory with `with_skill/` and `without_skill/`:

```
my-skill-workspace/
└── iteration-1/
    ├── eval-top-months-chart/
    │   ├── with_skill/outputs/
    │   └── without_skill/outputs/
    └── benchmark.json
```

Each run starts from a **clean context** so it reflects only what the SKILL.md says, not
leftover authoring state — one subagent per run gives that isolation (see `subagents.md`).
When improving a skill, snapshot the old version first (`cp -r <skill> <workspace>/skill-snapshot/`)
and point the baseline at the snapshot.

## Capturing timing

A skill that triples tokens for a 2-point quality gain is a different trade than one that's
better and cheaper. Record tokens and duration per run (`timing.json`):

```json
{ "total_tokens": 84852, "duration_ms": 23332 }
```

In Claude Code these arrive in the subagent's completion notification and aren't persisted
elsewhere — save them as each run finishes.

## Writing assertions

Add these after the first run — you often don't know what "good" means until you've seen
output. Good assertions are objective and specific: "The output file is valid JSON"
(programmatically checkable), "The bar chart has labeled axes" (observable), "The report
includes at least 3 recommendations" (countable). Weak ones: "The output is good" (too vague);
"uses exactly the phrase 'Total Revenue: $X'" (too brittle — correct output worded differently
fails). Reserve assertions for objective checks; leave taste to human review.

## Grading

Evaluate each assertion against the actual output, recording PASS/FAIL with **evidence that
quotes the output**, not an opinion (`grading.json`):

```json
{
  "assertion_results": [
    { "text": "Both axes are labeled", "passed": false, "evidence": "Y-axis reads 'Revenue ($)'; X-axis has no label" }
  ]
}
```

Require concrete evidence for a PASS — a section titled "Summary" with one empty sentence is a
FAIL. For mechanical checks (valid JSON, row counts), write a script; it's more reliable than
eyeballing and reusable across iterations.

## Aggregating

Compute per-configuration stats into `benchmark.json` — pass rate, time, tokens, and the
**delta**. The delta is the point: what the skill costs (time, tokens) versus what it buys
(pass rate).

```json
{
  "run_summary": {
    "with_skill":    { "pass_rate": { "mean": 0.83 }, "tokens": { "mean": 3800 } },
    "without_skill": { "pass_rate": { "mean": 0.33 }, "tokens": { "mean": 2100 } },
    "delta": { "pass_rate": 0.50, "tokens": 1700 }
  }
}
```

## Analyzing patterns

Aggregates hide things. After computing them:

- **Drop assertions that pass in both configs** — the model handles them without the skill;
  they inflate the score without showing value.
- **Investigate assertions that fail in both** — broken assertion, too-hard case, or wrong check.
- **Study assertions that pass with the skill and fail without** — that's where the skill earns
  its keep; understand *why* so you don't later remove the instruction that caused it.
- **Tighten on high variance** — a case passing sometimes and failing others means a flaky eval
  or ambiguous instructions; add an example or sharpen the wording.
- **Read transcripts on time/token outliers** — a case taking 3× the others usually reveals a
  step the skill made the model waste effort on.

## Human review

Assertions only check what you thought to check. A human catches the rest — technically correct
but misses the point, or problems that don't fit pass/fail. Record specific, actionable feedback
per case (`feedback.json`); empty feedback means it looked fine. "Missing axis labels" is
actionable; "looks bad" is not.

## Iterating

Three signals feed the next version: failed assertions (specific gaps), human feedback (broader
quality), and transcripts (*why* it went wrong). Turning them into edits:

- **Generalize.** The skill runs across many prompts, not just these cases. Fix the underlying
  issue broadly; don't patch the specific example.
- **Keep it lean.** Fewer better instructions beat exhaustive rules. If transcripts show wasted
  work, remove the instruction causing it. If pass rate plateaus as you add rules, the skill may
  be over-constrained — cut and see if results hold.
- **Explain why.** "Do X because Y causes Z" outperforms "ALWAYS do X." Models follow reasons.
- **Bundle repeated work.** If every run independently wrote a similar helper script, bundle it
  into `scripts/` so future runs don't reinvent it.

Loop: propose edits → apply → rerun all cases into `iteration-N+1/` → grade → review → repeat.
Stop when you're satisfied, feedback is consistently empty, or improvement stalls.

## Automating with skill-creator

Anthropic's official `skill-creator` skill automates this whole loop — spawning isolated runs,
grading assertions, aggregating benchmarks, blind A/B between versions, description tuning, and
an HTML review viewer. Prefer it over hand-rolling the harness:

```
/plugin install skill-creator@claude-plugins-official
```

References: agentskills.io evaluating-skills (https://agentskills.io/skill-creation/evaluating-skills)
and the skill-creator source (https://github.com/anthropics/skills/tree/main/skills/skill-creator).
