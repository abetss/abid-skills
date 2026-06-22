# Interview Brief — Calibration By Level

The interview-brief is the most-read doc in the set. It's the one the user opens the night before. It must match the level of the interview because the same content, told at the wrong altitude, sinks the candidate.

## What stays constant across levels

These sections appear in every interview-brief regardless of level:

1. **30-second elevator pitch** — a single paragraph the candidate memorizes verbatim. Captures the system in one breath: what it does, key tech, scale, key decision class.
2. **Numbers to memorize** — a small table. Polling intervals, concurrency limits, retry counts, retention windows, SKUs, replica counts. Concrete numbers anchor abstract claims.
3. **The 3-minute "tell me about the architecture" walkthrough** — a structured spoken script.
4. **N key decisions, each with a script** — the meat. Number depends on level (see below).
5. **Likely Q&A** — interviewer's likely questions paired with 1-paragraph answers.
6. **"What would you change?"** — never optional. Interviewers ask this. Have an answer.
7. **Night-before checklist** — small set of concrete pre-interview actions.

## What changes by level

### Junior (1-3 YOE)

**The interview tests**: can this person hold a system in their head and explain it cleanly?

The brief leans into:

- **Component naming and roles.** "There's a queue, a worker, a database, an email provider. Each does this." Crisp, no jargon traps.
- **Data flow.** "When the user does X, here's what happens step by step."
- **Surface vocabulary.** Library names, framework names, language-level patterns. The candidate should sound fluent in the codebase's tools.
- **One key decision, deeply explained.** Not 5. The interviewer wants to see the candidate can defend ONE choice and not get lost.

What to cut for junior briefs:

- Tradeoff defense scripts (interviewer won't probe to that depth).
- "What would change our mind" sections (too senior a framing).
- Long Q&A on alternatives (the alternative-set is shorter at this level).

### Senior (3-7 YOE)

**The interview tests**: can this person make a system-level decision and explain its tradeoffs in plain language?

Junior content PLUS:

- **3-5 key decisions** with the alternative named and the tradeoff explained. Not just "we did X" — "we did X over Y because Z."
- **A whiteboard-able mental model.** The candidate can draw a component diagram from memory while talking.
- **Failure mode awareness.** "If Redis is down, here's what happens" — but not a deep dive into recovery RTOs.
- **One "what would you change" answer** with a concrete bug or limitation named.

What to cut for senior briefs:

- Multi-year evolution paths (more principal).
- Cross-team organizational implications (more principal).

### Staff (7+ YOE, the user's level)

**The interview tests**: can this person hold the WHOLE system in context, make tradeoffs that survive scale, and articulate the conditions under which they'd choose differently?

Senior content PLUS:

- **5 key decisions** with the full tradeoff treatment — alternative names, tradeoff axes, "what would change our mind," what we accept.
- **Naming-trap callouts.** If a pattern is commonly miscalled (e.g. "we call it `.emit()` but it's not EDA"), the brief calls out the trap and gives the candidate the disarming script.
- **Migration paths preserved.** Every "we didn't build X" should be paired with "and the migration to X stays open because…"
- **Failure-mode scaling.** "At 1x today, at 10x I'd change A, at 100x B." Shows the candidate can think across time horizons.
- **Defense scripts** for likely pushbacks (3-4 prepared rebuttals).
- **Honest self-criticism.** Known bugs surfaced honestly, prioritized, with the fix path. Hiding bugs reads as immature; surfacing them reads as staff.

### Principal (10+ YOE, architect track)

Staff content PLUS:

- **Cross-system implications.** "This system's choices constrain X system's choices because…"
- **Team-shape fit.** When the team grows from 3 to 30, which decisions break? "When notification ownership splits from timesheet ownership, the function call we used becomes coordination overhead — that's the trigger for moving to a bus."
- **Multi-year evolution path.** "Here's how this system looks at year 1, year 3, year 5 — and what migration we'd execute at each step."
- **Organizational consequences.** Conway's law applied. Build/buy decisions tied to team capacity and headcount trajectory.

## Tone calibration

| Level | Voice | Hedges and confidence |
|---|---|---|
| Junior | "Here's how it works." | Confident on facts, modest on opinions. Acknowledges what they don't yet know. |
| Senior | "Here's what we built and why." | Confident on the choice, names the tradeoff. |
| Staff | "Here's what we built, the alternatives, what we accept, and what would change our mind." | Confident on the choice AND on the conditions under which they'd switch. Self-criticism is a strength signal. |
| Principal | "Here's the choice and its implications across systems and team trajectory." | Frames decisions as load-bearing for years; willing to say "I'd do this differently now." |

## The "what would you change?" answer — by level

Almost-certain interview question. Answer template:

| Level | Answer shape |
|---|---|
| Junior | One concrete bug or limitation. "BUG-1 affects accessibility users — I'd fix that this week." |
| Senior | Two things: a known bug + a small structural improvement. |
| Staff | Three things in categories: (1) known bugs, (2) observability gaps, (3) what changes at 10x scale. |
| Principal | Structural answer: the architecture decisions I'd revisit, the team-shape changes that would force them, and the migration sequence. |

## Calibrating the user's specific brief

The user wrote: "staff level, not great at system design." Two implications:

1. **Use staff-level content** — the alternatives, the "what would change our mind," the defense scripts.
2. **But favor concrete-over-abstract phrasing** — name the file paths, the concrete numbers, the specific bugs. Don't lean on "system design jargon" that the candidate might fumble. The brief becomes a confidence aid as much as a content aid.

Specifically for staff candidates weaker on abstract system design:

- **Anchor every claim in a file path or concrete number.** "The fan-out worker has concurrency 5" is more retrievable under pressure than "we tuned worker concurrency for our throughput profile."
- **Lead each decision section with the verbatim answer.** "If they ask about X, say: ..." Followed by the supporting why. Reverse-order from a tutorial — the candidate gets the line first, the reasoning second.
- **Avoid CS taxonomy unless the candidate can defend it.** If you say "this is a CQRS pattern" the interviewer will probe CQRS. If you say "we split the read path from the write path because…" the interviewer will probe what's actually true. Concrete claims beat taxonomic claims.
- **Pre-emptively name the naming traps.** A staff interviewer will probe ".emit() — isn't that EDA?". The brief should have the disarming script ready: "we use 'emit' for the call but it's not EDA, here's why."

## Anti-patterns

### The "explain everything" brief

12 decisions, 40 pages, no priority. The candidate will retain none of it under stress. **Pick fewer; go deeper.**

### The "show off" brief

Heavy on architectural buzzwords (CQRS, saga, event sourcing) that aren't actually what's in the code. The interviewer probes; the candidate falters. **Use the words that match the code.**

### The "perfect system" brief

No bugs, no limitations, no "what would you change." Reads as either dishonest or shallow. **Surface the bugs. Naming them is the strength signal.**

### The "tutorial" brief

Explains the architecture from first principles. The candidate doesn't need to learn the system at the interview — they need to recall it under pressure. **Optimize for retrieval, not for teaching.**
