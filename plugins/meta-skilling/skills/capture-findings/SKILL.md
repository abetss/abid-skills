---
name: capture-findings
description: Persists the findings or writeup the assistant just produced as a markdown file and renders it to a self-contained HTML artifact via generating-html-artifacts, keeping the two in sync. Use when the user names a writeup or says "capture this", "write up your findings", "save this as a report or artifact", or asks to update an existing capture or re-sync its HTML to the markdown.
argument-hint: "[name]"
---

# Capture findings

Persists what the assistant wants the user to see as a markdown file, then renders that file into an HTML artifact — and re-renders when either side changes. The markdown is the editable source of truth; the HTML is the rendered, shareable view. Both live in a folder named after the title so the artifact can grow nested pages later.

## How this skill runs

This skill runs **inline, in the conversation that produced the content** — read the just-produced findings directly from context and any files on disk. The work then splits in two, by what each half needs:

- **Generating the markdown** needs the full detail. Gather it from the conversation and hand it *complete, not condensed* to a dispatched subagent that writes the markdown (brief: `agents/generate-markdown.md`) — it can't see the conversation, so it preserves only the depth you forward. Running inline rather than as a fork is what makes that work: the agent doing the forwarding is the one that actually holds the detail.
- **Rendering the HTML** is mechanical and needs no conversation, so it goes to the **generating-html-artifacts** skill, which forks itself and keeps that work out of this context.

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
- [ ] 2. Gather the full findings from the conversation (and any files they reference) — the complete detail, not a summary
- [ ] 3. Dispatch the generate-markdown subagent (see below) to write <slug>/<slug>.md
- [ ] 4. Render: invoke generating-html-artifacts on the .md to produce <slug>/<slug>.html
- [ ] 5. Open <slug>/<slug>.html; report both paths
```

### Update content

The generate-markdown subagent edits the existing markdown per the user's request, then it is re-rendered.

```
- [ ] 1. Read the existing <slug>/<slug>.md
- [ ] 2. Dispatch the generate-markdown subagent with the existing markdown + the requested change (surgical — change only what was asked) to rewrite <slug>/<slug>.md
- [ ] 3. Render: invoke generating-html-artifacts on the .md to refresh <slug>/<slug>.html
- [ ] 4. Open <slug>/<slug>.html; report what changed
```

### Re-render

The user edited the markdown themselves and wants the HTML brought up to date. **Do not rewrite or restructure the markdown** — the user's `.md` is the source of truth; only the HTML is regenerated. No composer here.

```
- [ ] 1. Read <slug>/<slug>.md exactly as the user left it (do not modify it)
- [ ] 2. Render: invoke generating-html-artifacts on the .md to regenerate <slug>/<slug>.html
- [ ] 3. Open <slug>/<slug>.html; confirm it reflects the current markdown
```

## Dispatching generate-markdown (Create / Update)

Run this as a subagent (the **Agent** tool, `general-purpose`) — never inline — so the writing happens in its own agent context. Give it three things:

1. **Its brief** — `agents/generate-markdown.md` (how to structure the writeup and preserve depth).
2. **The full findings text, verbatim** — the reasoning, the options weighed, the tradeoffs, the concrete specifics. Not a pre-condensed blurb: the subagent sees only what you pass, so anything you drop here is lost. For an Update, also pass the existing markdown and the exact change requested.
3. **The slug, H1 title, and output path** `<slug>/<slug>.md`.

It writes that file and returns the path. The depth-preservation craft lives in the brief; your job at this step is to forward the complete content.

## Dispatching the HTML render

In every mode, produce the HTML by invoking the **generating-html-artifacts** skill (via the Skill tool) pointed at `<slug>/<slug>.md`, asking for `<slug>/<slug>.html`. Never hand-write the HTML here — always go through that skill so artifacts stay consistent.

## Opening

The artifact is a **self-contained static HTML** — just open the file in the browser: on macOS, `open <slug>/<slug>.html`. That's all. **Don't spin up a web server for it, and you don't need to verify or QA it — it's a simple self-contained HTML, so opening the file is enough.**

## Scope

- Use this skill whenever the assistant's output should be **persisted as a markdown + HTML pair**, or when an existing pair needs its content updated or its HTML re-synced.
- For one-off HTML with no markdown source, or when the user hands you an existing `.html`, use **generating-html-artifacts** directly — don't wrap it in this skill.
