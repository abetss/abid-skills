# write-architecture-docs — Memory

Cross-session learnings about producing architectural doc sets. Read before starting a new run.

## Updated by

- 2026-05-21 — Initial seed. Skill created from the work that produced
  `a-docs/architecture/notification/` in the admin-4 codebase.

## Founding lesson — tradeoffs vs differences

The single most important lesson from the founding run:

A "tradeoffs" section that lists *differences* between options is failing. A reader
cannot decide from a difference table — they can only describe. The user explicitly
corrected the first draft of `tradeoffs.md` with this point and rewrote §1 (Async
command vs EDA) as the canonical format.

A tradeoff row must show **+** (what this option GAINS on this axis) AND **−** (what
this option LOSES on this axis). If both options gain on an axis, it's not a tradeoff
— it's shared ground, and belongs in a "What they share (not tradeoffs)" subsection.

See `references/tradeoff-format.md` for the full canonical structure.

## Process lessons

### Propose the output shape before researching

The founding run started with a proposed deliverable set + 4 clarifying questions
BEFORE spawning any research agents. The user agreed to the structure, narrowed scope
on a few axes, and the research then had a clear target. This is the right ordering.
Don't research first and propose docs second — you'll waste a research round.

### Parallel research is non-negotiable

Spawning the code-A, code-B, infra, and docs agents in a single message ran them
concurrently and finished the discovery phase in ~5 minutes. Sequential would have
taken 20. Always parallel.

### `raw-context.md` written first, then everything else from it

The architecture.md, tradeoffs.md, diagrams.md, etc. are all distillations of
raw-context.md. Writing raw-context.md first means each subsequent doc is a focused
extract, not a re-research. Don't skip raw-context.md to save time — it's the data
source for everything else.

### Interview-brief comes LATE in the order

Earlier drafts of the brief read as superficial because the deeper context hadn't
landed yet. Writing the brief after architecture.md + tradeoffs.md + diagrams.md +
failure-modes.md means the brief synthesizes from rich material, not from research
notes. Order matters.

### Diagrams need a "**Memorize:**" block

Every Mermaid diagram in `diagrams.md` should be followed by a small `**Memorize:**`
bullet block calling out what the reader should retain. Without it, the diagram is
decoration. With it, the diagram is a study aid.

## Anti-patterns that almost shipped

- **Tradeoff table that only showed what each option HAS.** Caught and rewritten in
  the founding run. Never ship a tradeoff table without verifying every cell has both
  a + and a −, or move it to the "What they share" section.
- **Missing the naming-trap callout.** The founding system used `.emit()` for a call
  that wasn't event-driven. Sharp interviewers probe naming — the brief must name the
  trap first.
- **Generic "what would you change?" answer.** The founding run had this; the user's
  edit replaced it with a concrete three-category structured answer (known bugs +
  observability gaps + 10x scale changes). Concrete > generic.

## Lesson — verify library behavior, don't quote the code comment that claims it

From the voice-agent run (2026-05-22): an in-code comment at
`platform-api/src/middleware/auth.ts:13` and `app.ts:113` asserted *"Hono's
access logger omits the query string"* — and the architecture doc, three
tradeoff cells, and a defense script in the interview brief all carried
this as a verified fact, citing the comment block as the verification.
The reviewer caught it; reading Hono's actual `logger()` source at
`node_modules/hono/.../middleware/logger/index.js:35`
(`url.slice(url.indexOf("/", 8))`) showed the query string IS included.

The doc set was carrying a load-bearing security claim that was factually
wrong, sourced from an unverified code comment.

**Rule:** when a doc cites an external library's behavior, the verification
footnote must point at the library's source — not the code comment that
makes the same claim. The comment is the *claim*, not the verification.
This is especially load-bearing for security/correctness assertions that
end up in interview defense scripts.

## Lesson — bound every proof-of-absence claim

From the scheduling run (2026-08-02): a research agent reported that two schema
models were dead code, evidencing it with *"grep returns **zero matches**"*. The
supervisor re-ran the grep: six real references existed, all in audit
configuration (`lib/audit-config.ts`, `lib/db/audit/writer.ts`).

The substantive finding was correct — no route, no data layer, no test, no
feature path touched the models. But the absolute phrasing was false, and an
interviewer who greps alongside the candidate finds the six hits in seconds.

**Rule:** an absence claim must state *what was searched and what was found* —
"referenced only by audit configuration, never by a feature path" — never a bare
"zero". Unqualified absence claims are the cheapest thing for a reviewer to
falsify, and they discredit the true finding they were meant to support.

Cheap enforcement: grep the finished docs for `zero references`, `zero matches`,
`no references`, `nothing uses` and require each hit to carry its search scope.

## Anti-pattern — the unrequested artifact nobody verified

Same run. A module writer, unprompted, also emitted a 432-line `.dbml` schema
file alongside its three assigned markdown files. It was never requested, so it
was never in any review path. Spot-checking found **13 of its 16 enums had
invented values** — `ShiftType` listed `ON_CALL`/`BACKUP` (neither exists) and
omitted `APPOINTMENT`; `ShiftAssignmentStatus` listed 6 values where the schema
has 13.

Two things made this dangerous rather than merely sloppy:

1. It sat in the deliverable folder looking authoritative.
2. The same agent's *assigned* markdown files were clean — verified by grepping
   the fabricated tokens (0 hits) and the real ones (present in 10-13 docs each).
   Quality on requested output said nothing about quality on volunteered output.

**Rules:**
- Inventory the output folder against the files you actually commissioned. Treat
  anything extra as unreviewed until proven otherwise.
- Any transcription of a schema, enum, or API surface must be **machine-verified
  against the source**, not eyeballed. A 20-line script comparing enum value sets
  caught this instantly; reading the file would not have.
- Regenerating beats deleting when the artifact is genuinely useful — but
  re-verify the regenerated version with the same script. (The rebuild here
  passed 16/16 enums and 145 fields, and correctly reproduced the one model that
  intentionally has no `deleted_at`.)

## Process — mechanical gates beat reread-and-hope

The scheduling run used two ~100-line linters as hard gates before accepting any
writer's output:

- **Mermaid structural linter** — unknown diagram types, unquoted labels
  containing `(`/`)`/`,`, unbalanced brackets, and *missing `**Memorize:**`
  blocks*. Calibrated against existing known-good doc sets first, to drive false
  positives to zero before trusting it. Caught 3 real defects across 52 diagrams.
- **Tradeoff-format linter** — for every table row whose first cell contains `↔`,
  assert every other cell carries **both** a `+` and a `−`. Also counts
  "what they share" and "what would change our mind" sections per decision.
  Verified 176 axis rows across 33 decisions with zero one-sided cells.

Calibrate on a known-good doc first. A linter that cries wolf gets ignored, and
the canonical example is the only fixture that proves the rules are right.

## Updated by

- 2026-05-21 — Initial seed.
- 2026-05-22 — Verify-library-source-not-code-comment lesson, captured as
  FN-1 in voice-agent/failure-modes.md as the canonical example.
- 2026-08-02 — Scheduling run: bound-every-absence-claim; the unrequested
  fabricated artifact; mechanical linters as acceptance gates.
