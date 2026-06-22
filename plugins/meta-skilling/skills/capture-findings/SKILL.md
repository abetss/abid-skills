---
name: capture-findings
description: Captures the AI's findings, analysis, research, or summary into a markdown file and renders it as a polished navigable HTML artifact via the generating-html-artifacts skill, then keeps the two in sync on later edits. Use when the user invokes /capture-findings, gives a name for a writeup, or says "capture this", "write up your findings", "save this as a report or artifact", "make me a writeup", "turn this into a doc or page". Also use to UPDATE an existing capture — "update the named doc or markdown", "add a section to it", "the markdown is updated, regenerate or refresh the HTML", "sync the HTML to the markdown". Output is a folder named after the title holding the markdown source and its HTML artifact.
---

# Capture findings

Writes what the AI wants the user to see into a markdown file, then converts that file into an HTML artifact — and re-renders when either side changes. The markdown is the editable source of truth; the HTML is the rendered, shareable view. Both live in a folder named after the title so the artifact can grow nested pages later.

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

## Dispatching the HTML render

In every mode, produce the HTML by invoking the **generating-html-artifacts** skill (via the Skill tool) pointed at `<slug>/<slug>.md`, asking for `<slug>/<slug>.html`. That skill embeds the markdown verbatim as the artifact's machine-readable source mirror and applies all readability, contrast, navigation, and light/dark rules. Never hand-write the HTML here — always go through that skill so artifacts stay consistent.

## Opening

On macOS, run `open <slug>/<slug>.html`. If the user wants visual confirmation, use the browser (Chrome MCP) instead.

## Scope

- Use this skill whenever the AI's output should be **persisted as a markdown + HTML pair**, or when an existing pair needs its content updated or its HTML re-synced.
- For one-off HTML with no markdown source, or when the user hands you an existing `.html`, use **generating-html-artifacts** directly — don't wrap it in this skill.
