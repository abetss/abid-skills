---
name: write-architecture-docs
description: Produces a folder of deep architectural docs (raw context, deep architecture narrative, Mermaid diagrams, real-tradeoff analysis, interview brief, failure modes) for an existing feature or system. Use whenever the user wants to document an existing system's architecture, prepare for an interview about a feature they built, capture the design decisions and tradeoffs behind a system, write design docs for a system that's already running, hand off an engineering area to a new owner, or explain how a feature works at a deep technical level. Triggers on phrases like "document the architecture", "interview prep", "write architecture docs", "document this system", "capture design decisions", "tradeoffs of X", "architectural documentation", "how does our X work", "prepare me for an interview about", "design doc for X", "explain the architecture of", or whenever the user mentions they need to talk about an existing feature's architecture.
---

# Write Architecture Docs

Produces a set of architectural docs for an existing feature or system. The output is a folder of 4-6 Markdown files that, together, let the reader:

- Recall the system end-to-end (`architecture.md`)
- See it visually (`diagrams.md`)
- Defend the decisions made (`tradeoffs.md`)
- Practice for an interview about it (`interview-brief.md` — optional)
- Know what would break and what to do at 10x scale (`failure-modes.md` — optional)
- Get to the raw evidence behind every claim (`raw-context.md`)

The user might want all six, or only a subset. The first job of this skill is to figure out which.

## Always read these first

1. `memory.md` (in this skill folder) — cross-session learnings, especially the "tradeoffs vs differences" lesson the user explicitly taught the first time this skill ran
2. `references/tradeoff-format.md` — the format for `tradeoffs.md`. This is the hard part of the skill — if you skip the reference, your `tradeoffs.md` will read as a difference table and the user will rewrite it
3. `references/diagram-catalog.md` — when to use each Mermaid diagram type
4. `references/interview-brief-by-level.md` — only when `interview-brief.md` is in the output set
5. `references/research-agent-prompts.md` — template prompts for the parallel research phase

If a worked example exists in the codebase (look at `a-docs/architecture/notification/`), read it for the canonical shape and tone.

## The workflow

There are six phases. **Don't skip Phase 0** — the proposal step is what makes the rest of the work converge fast.

### Phase 0 — Capture intent and propose the output set

Before researching anything, propose the deliverables and confirm scope. This costs one short message and saves a research round.

What to confirm with the user (ask only what isn't already clear from the conversation):

1. **System / feature name** — and what it *is* in one sentence.
2. **Code scope** — which apps/packages/folders to inspect. Be specific (e.g. `apps/platform-api`, `apps/home`).
3. **Infra scope** — which cloud (Azure / AWS / GCP / none), which subscription/account, what's worth inventorying.
4. **Existing docs scope** — work folders, knowledge base, design docs. Often `a-works/<feature>` and `a-kb/.../<feature>`.
5. **Output folder** — where the docs land. Default: `a-docs/architecture/<feature>/`.
6. **Audience** — interview prep / onboarding / design review / general reference. Drives which optional docs to include and the calibration of `interview-brief.md` (see `references/interview-brief-by-level.md`).
7. **Specific decisions to spotlight** — the user often knows which tradeoffs they want to talk about. Lean into those.

Then propose the doc set explicitly. Default:

| File | Always | Reason |
|---|---|---|
| `raw-context.md` | Yes | Source of truth for the others. Even if the user wouldn't read it, the writing phases need it. |
| `architecture.md` | Yes | The deep doc. The "captures everything." |
| `diagrams.md` | Yes | Visuals. Always worth the cost. |
| `tradeoffs.md` | Yes | The decisions and what each cost. |
| `interview-brief.md` | If audience = interview | The exam-prep distillation. |
| `failure-modes.md` | If audience = interview or staff+ | For the "what would you change" angle. |

Confirm the set with the user. Adjust based on their answer. **Then start.**

### Phase 1 — Parallel research

Spawn 3-5 research agents in a single message so they run concurrently. Use the prompts in `references/research-agent-prompts.md` — they're templated for code A, code B, infra, and docs.

Adjust the agent set per system:
- Backend-only feature: drop the code-B (frontend) agent.
- No cloud surface: drop the infra agent.
- No prior docs: drop the docs agent (or note its emptiness explicitly).

Each agent returns a structured report. Don't synthesize on the fly — wait until all reports are back, then write `raw-context.md` from them.

### Phase 2 — Write `raw-context.md`

Synthesize all agent reports into one file. Structure:

1. **Code findings — primary surface** (from code-A agent)
2. **Code findings — secondary surface** (from code-B agent, if applicable)
3. **Infrastructure inventory** (from infra agent, if applicable). Include a "What's NOT here" subsection — the absence of services is as informative as their presence.
4. **Design doc findings** (from docs agent, if applicable). Quote design intent verbatim where it's captured.
5. **Cross-cutting themes** — patterns visible across all sources (compliance constraints, recurring design principles, etc.)
6. **Essential file index** — every file path that the architecture.md should be able to reference. With this index in hand, the writing phases don't need to re-research.

This file should be 1500-3500 lines for a medium system. Dense is fine; this is the raw material, not the polished surface.

### Phase 3 — Write `architecture.md`

The deep narrative. The reader should be able to recall the whole system after reading this. Recommended structure:

1. **What this system does** — one sentence. Then "what it is NOT" — equally important.
2. **Scale & constraints** — current numbers, regulatory or accessibility constraints.
3. **The N layers** — most systems have 3-5 architectural layers (intake → processing → storage → delivery, or similar). Walk through each, naming responsibilities and replaceability.
4. **Per-layer deep dive** — one section per layer. Each names the contract, the implementation, the test surface, the extension points.
5. **Data model** — the schema. Why each non-obvious column shape was chosen.
6. **Pluggability** — if extensibility is a story, document the extension points and what changes when you add a new instance.
7. **Cross-cutting concerns** — observability, compliance, testing strategy.
8. **A "quick mental map for whiteboard"** — at the end. An ASCII sketch the reader can recall.

Tone: confident, sourced (file paths and line numbers everywhere), and willing to explain non-obvious choices with their rationale. Length: 500-1500 lines depending on system complexity.

### Phase 4 — Write `diagrams.md`

Use the diagram catalog in `references/diagram-catalog.md`. Default set:

1. C4 context — system in its world
2. Component view — inside the system
3. Sequence — happy path of the most common flow
4. Sequence — one interesting edge case (subtle correctness detail, race-condition handling, etc.)
5. State machine — if any entity has non-trivial state transitions
6. ERD — the data model
7. Deployment — cloud topology, if there is one
8. Pluggability deltas — if extensibility is a story

After every diagram, a `**Memorize:**` block. This is the study aid.

### Phase 5 — Write `tradeoffs.md`

**This is the hard part. Read `references/tradeoff-format.md` before writing.**

The lesson from the founding run: a tradeoff section that lists *differences* between options is failing. Every row in every tradeoff table must show **+** (what this option GAINS on this axis) AND **−** (what this option LOSES on this axis). If both options gain on an axis, that's shared ground — move it to a "What they share (not tradeoffs)" subsection. Hidden tradeoffs are the failure mode to avoid.

Pick the 5-10 most decision-worthy moments in the system. For each, use the full structure from the reference: context → "what each pattern actually is" → side-by-side tradeoff table → "what they share" → why-the-chosen-option-won (numbered priority order) → "what would change our mind" → defense scripts (if interview-facing) → "what we accept" → adjacent alternatives → one-line summary.

Order matters — put the most decision-worthy (often the most-asked-about-in-interviews) first. Section 1 is where the interviewer goes deep, so it deserves the deepest treatment.

End with a "**Bonus impressive/challenging bits**" section — 5-10 paragraphs naming smaller-but-interesting design details (the clever idempotency, the late-stage correctness insight, the abstraction built ahead of need with justification). These are the candidate's interview ammo.

### Phase 6 — Write `interview-brief.md` (if applicable)

Read `references/interview-brief-by-level.md` first. Calibrate to the user's interview level.

Standard structure:

1. **30-second elevator pitch** — verbatim paragraph to memorize.
2. **Numbers to memorize** — table of concrete numbers.
3. **The 3-minute "tell me about the architecture" answer** — structured spoken script.
4. **The deepest decision (the question to be ready for)** — full script + likely follow-ups.
5. **N key decisions, each with a 30-sec script** — one per major tradeoff.
6. **Impressive bits to flex on (use sparingly)** — 4-6 detail-level brags, pick 1-2 per interview.
7. **Home-app / cross-surface architectural notes** — if applicable.
8. **"What would you change?"** — structured three-category answer (bugs, gaps, scale).
9. **Likely interview Q&A** — 8-12 questions with paragraph-length answers.
10. **The "I don't know" answers** — three templated graceful-deflection scripts.
11. **Things to NOT do in the interview**.
12. **Night-before checklist** — concrete pre-interview actions.

### Phase 7 — Write `failure-modes.md` (if applicable)

Three categories: loss windows, capacity sharing, observability gaps. Plus a known-bugs section if the codebase has self-documented bugs (often `bugs.md` in the work folder). Plus a one-paragraph scaling roadmap ("at 1x today, at 10x I'd change A, at 100x B").

Honest self-criticism beats hidden bugs. The known-bugs section is a strength signal, not a weakness signal.

## The quality bar

Before declaring the doc set done, audit:

1. **Every claim in every doc traces to a file path / line number / Azure resource / config value in `raw-context.md`.** If you can't ground a claim, either remove it or re-research.

2. **Every tradeoff table cell has + AND −.** If not, move that row to "What they share."

3. **Every diagram has a Memorize block.**

4. **The interview brief opens with a paragraph the user could memorize verbatim** — not bullet points.

5. **"What would you change?" is concrete, not generic.** Names a specific bug or specific scale-change action.

6. **The naming traps are named first.** If a pattern in the system shares a name with something it isn't (`.emit()` vs EDA, `events` vs domain events, etc.), the brief and tradeoffs both call this out before the interviewer can probe.

7. **Each major decision in `tradeoffs.md` has a "what would change our mind" section.** This is the staff-level signal — it shows you understand the rejected option's value, not just its costs.

If any audit fails, fix before delivering.

## End-of-run handoff to the user

When the doc set is complete, deliver a short status message summarizing:

- The files written (path + line count).
- Where each decision is hit at three levels of depth (interview-brief pitch → tradeoffs deep-dive → architecture implementation).
- The user's recommended reading order for their immediate need (typically: interview-brief night-before, tradeoffs §1 aloud, diagrams to practice redrawing).

Resist the urge to summarize the system itself in the handoff — that's what the docs are for.

## When to push back

The user may ask for a partial output set or a system the skill doesn't fit cleanly. Push back when:

- The system is too new to have a "tradeoffs.md" — there were no real decisions yet because the system hasn't been stressed. Offer to write architecture.md and diagrams.md only.
- The user wants pure code documentation, not architecture — direct them to use a code-explainer skill instead. This skill is for the WHY, not the WHAT.
- The user wants to document a system they don't actually own — clarify that the discovery phase will surface the code state, not the design intent. If there are no docs and no contributing engineers to interview, the tradeoffs section will be thin.

In each case, name the constraint and offer the alternative.

## Memory writing

After each completed run, evaluate whether the session produced a learning worth capturing in `memory.md`. Write an entry if:

- The user corrected something mid-session in a way that generalizes (theme: tradeoffs vs differences in the founding run)
- A pattern emerged that wasn't obvious from the references
- An anti-pattern almost shipped — name it so the next run catches it

Don't capture:
- System-specific facts (those belong in the docs you wrote, not in skill memory)
- Generic writing advice not tied to a real incident
- Things already in `SKILL.md` or the references

Add a dated line under `## Updated by` whenever you append.
