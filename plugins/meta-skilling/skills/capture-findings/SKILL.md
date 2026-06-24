---
name: capture-findings
description: Captures and presents the output you want to show the user — findings, analysis, research, a writeup — into a markdown file, generates a HTML artifact from it (via generating-html-artifacts), opens the HTML for the user, and keeps the two in sync on later edits. Argument guide, Pass the content you'd otherwise print in the terminal; the structuring and rendering are handled for you. Use when the gives a name for a writeup, or says "capture this", "write up your findings", "save this as a report or artifact", "make me a writeup", "turn this into a doc or page". Also use to UPDATE an existing capture — "update the named doc or markdown", "add a section to it", "the markdown is updated, regenerate or refresh the HTML", "sync the HTML to the markdown". Output is a folder named after the title holding the markdown source and its HTML artifact.
model: haiku
context: fork
---

# Capture findings

Writes what the AI wants the user to see into a markdown file, then converts that file into an HTML artifact — and re-renders when either side changes. The markdown is the editable source of truth; the HTML is the rendered, shareable view. Both live in a folder named after the title so the artifact can grow nested pages later.

## How this skill runs

This skill runs in a **forked subagent** (`context: fork`) on the **haiku** model so the markdown-composing and HTML-generation work stays out of the main conversation context. A fork does **not** inherit the conversation — it sees only this skill body plus `$ARGUMENTS`. So the invoking (main) agent must pass everything needed in the arguments:

- the **content to capture** — the findings/analysis/summary text, *with its full detail*: the
  reasoning, the options weighed, the tradeoffs, the specifics. Pass the depth, not a pre-condensed
  blurb; this skill turns a clean overview + full detail into a click-to-expand artifact, but it
  can only preserve depth that reaches it. And
- the **name/slug** for the output (if the user gave one).

Work only from `$ARGUMENTS` and files already on disk. Never assume access to prior conversation. For Update / Re-render modes, the existing `<slug>/<slug>.md` on disk is the source of truth.

$ARGUMENTS

## Naming and layout

The user usually supplies a name when invoking (e.g. `/capture-findings auth-audit`). From it:

- Derive a kebab-case **slug** (lowercase, hyphens) for the folder and filenames.
- Keep the human-friendly version as the document's H1 title.
- If no name was given, infer the target from context (the slug the user references) or propose a short slug and confirm before writing.

Layout in the **current working directory**:

```
<slug>/
  <slug>.md     # editable markdown source of truth
  <slug>.html   # rendered HTML artifact (entry point; sub-pages may be added later)
```

## Three modes

Pick the mode from what the user asked:

| User intent | Mode |
|---|---|
| New writeup from a name / "capture this" | **Create** |
| "Update the <name> doc", "add a section", "change X in <name>" | **Update content** |
| "I edited the markdown, regenerate the HTML", "sync HTML to the markdown" | **Re-render** |

### Create

```
- [ ] 1. Resolve the slug + H1 title
- [ ] 2. Compose the findings as clean markdown (see below)
- [ ] 3. Write <slug>/<slug>.md
- [ ] 4. Render: invoke generating-html-artifacts on the .md to produce <slug>/<slug>.html
- [ ] 5. Open <slug>/<slug>.html; report both paths
```

### Update content

The AI edits the markdown per the user's request, then re-renders.

```
- [ ] 1. Read the existing <slug>/<slug>.md
- [ ] 2. Apply the requested edits to the markdown (surgical — change only what was asked)
- [ ] 3. Write the updated <slug>/<slug>.md
- [ ] 4. Render: invoke generating-html-artifacts on the .md to refresh <slug>/<slug>.html
- [ ] 5. Open <slug>/<slug>.html; report what changed
```

### Re-render

The user edited the markdown themselves and wants the HTML brought up to date. **Do not rewrite or restructure the markdown** — the user's `.md` is the source of truth; only the HTML is regenerated.

```
- [ ] 1. Read <slug>/<slug>.md exactly as the user left it (do not modify it)
- [ ] 2. Render: invoke generating-html-artifacts on the .md to regenerate <slug>/<slug>.html
- [ ] 3. Open <slug>/<slug>.html; confirm it reflects the current markdown
```

## Composing the markdown (Create / Update)

Put the substance the user should see, structured for reading:
- One `#` H1 title; a short lead paragraph with the takeaway.
- Logical `##`/`###` sections; real `-`/`1.` lists and `|` tables for tabular data.
- Links where useful.

Keep it content. Presentation — contrast, spacing, navigation, theming — is the HTML skill's job, not yours here.

### Preserve depth — summarize forward, not away

The most common failure of this skill is over-summarizing: distilling each decision or finding
down to a one-line "Recommend: …" and dropping the reasoning behind it. A reader can't act on a
verdict without the *why* — the problem it solves, the options that lost, the tradeoffs. A clean
overview is good as the **first** thing the reader sees; it is not enough as the **only** thing.
(Work only with the detail you were given in `$ARGUMENTS` — don't invent reasoning to fill a
fold. If the arguments are already thin, capture them faithfully rather than padding.)

The goal is **progressive disclosure**: the reader sees the high level first and goes deeper
only if they want to — like zooming a map. The fold below is the default way to express that (it
becomes a click-to-expand card), but it is one strategy, not a rule — a long self-contained
finding can instead become its own linked detail page, and a short item with nothing behind it
stays a plain section. Choose per item; don't force a fold everywhere. Feel free to be creative about this considering high UX.

So for any item that carries real depth (a decision, a recommendation, an analyzed option, a
finding), write **both** layers:

- **Summary** — the title and a one-line takeaway. This is what the reader scans. Keep it tight.
- **`<!-- more -->`** — an HTML-comment fold marker on its own line.
- **Detail** — everything you'd otherwise throw away: the context/problem, the options
  considered and why each won or lost, the tradeoffs, the consequences, concrete specifics
  (field names, values, examples). This is the part that makes the verdict trustworthy.

```markdown
### 14 · User / auth stub

**Recommend:** minimal `users` table, one seeded row.

<!-- more -->

**The decision.** We need a `user_id` to hang episodes and turns off of, but real auth is out
of scope for the baseline.

**Options.**
- *Hardcoded `user_id` constant* — least code today, but `Episode.user_id` / `Turn.author_id`
  aren't real foreign keys, so adding auth later means a schema migration and a backfill.
- *Minimal `users` table, one seeded row* — a few more lines now; the foreign keys are real
  from day one and the auth retrofit is just "stop seeding, start inserting".

**Why this one.** The retrofit cost dominates. A one-row table is still a stub but avoids a
painful migration.

​```mermaid
erDiagram
  USER ||--o{ EPISODE : owns
  EPISODE ||--o{ TURN : has
​```
```

Only fold when there's genuinely more to show. A short item with nothing behind it stays a plain
section — don't invent a fold or pad the detail. The fold protects depth; it doesn't create it.
The `generating-html-artifacts` skill turns each `<!-- more -->` section into a click-to-expand
card, so the overview stays scannable and the detail is one click away.

### Diagrams

When structure, flow, a data model, or a decision tree is easier shown than told, add a fenced
```mermaid``` block (in the detail, not the summary). Write plain Mermaid — the HTML skill
pre-renders it to an inline, theme-aware diagram. Match the shape to the idea: `flowchart` for
stages/pipelines/decisions, `erDiagram` for data models, `stateDiagram-v2` for lifecycles,
`sequenceDiagram` for call order. Keep each diagram to one idea; two small diagrams beat one
crowded one.

## Dispatching the HTML render

In every mode, produce the HTML by invoking the **generating-html-artifacts** skill (via the Skill tool) pointed at `<slug>/<slug>.md`, asking for `<slug>/<slug>.html`. That skill embeds the markdown verbatim as the artifact's machine-readable source mirror and applies all readability, contrast, navigation, and light/dark rules. Never hand-write the HTML here — always go through that skill so artifacts stay consistent.

## Opening

On macOS, run `open <slug>/<slug>.html`. If the user wants visual confirmation, use the browser (Chrome MCP) instead.

## Scope

- Use this skill whenever the AI's output should be **persisted as a markdown + HTML pair**, or when an existing pair needs its content updated or its HTML re-synced.
- For one-off HTML with no markdown source, or when the user hands you an existing `.html`, use **generating-html-artifacts** directly — don't wrap it in this skill.
