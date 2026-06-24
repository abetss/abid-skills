# Depth and diagrams

How to give an artifact a scannable overview AND full depth on demand, and how to render
diagrams that stay self-contained. Read this when the source has decisions/findings that
deserve detail, or any `<!-- more -->` markers or ```mermaid``` blocks.

## Contents
- The overview/detail problem
- The fold marker (`<!-- more -->`)
- Rendering an expandable item card
- Diagrams: pre-render Mermaid to inline SVG
- Inlining the diagram fragments
- Choosing a diagram shape

## The overview/detail problem

A grid of cards that each show a one-line takeaway reads beautifully — but it's a dead end if
that's *all* there is. The reader can't act on "Recommend: minimal users table" without the
reasoning, the options that lost, and the tradeoffs behind it. The fix is progressive
disclosure: keep the clean overview as the always-visible front of each card, and put the full
depth one click away. Nothing is summarized *out* of existence — it's summarized *forward*.

## The fold marker

When a section's markdown contains an HTML comment `<!-- more -->`, treat it as a fold:

- Everything **before** the marker is the **summary** — always visible (the title, the lead, a
  `**Recommend:**` line). This is what the reader scans.
- Everything **after** the marker is the **detail** — collapsed behind a click (the reasoning,
  options, tradeoffs, tables, and any diagram).

The marker is invisible in plain markdown, so the `.md` source still reads naturally. If a
section has no `<!-- more -->`, render it normally (no disclosure) — don't force a fold where
there's nothing to hide.

## Rendering an expandable item card

Map a folded section to a native `<details>` disclosure — keyboard-accessible, works with no
JS, and degrades to "all open" if scripting is off. The CSS lives in `assets/template.html`
(`details.item`).

```html
<details class="item">
  <summary>
    <div class="item-summary">
      <h3>14 · User / auth stub</h3>
      <p><strong>Recommend:</strong> minimal <code>users</code> table, one seeded row.</p>
    </div>
  </summary>
  <div class="item-detail">
    <p>Options: a hardcoded <code>user_id</code> constant · a minimal <code>users</code> table.
       The constant is less code today but forces a painful retrofit once auth lands…</p>
    <ul><li>Real foreign keys from day one (Episode.user_id, Turn.author_id).</li>…</ul>
    <!-- a pre-rendered diagram fragment goes here when it clarifies -->
  </div>
</details>
```

Notes:
- The heading stays inside `<summary>` so the whole row is the click target and the disclosure
  is announced correctly. Don't nest interactive controls (links, buttons) inside `<summary>`.
- Keep the summary genuinely short — title + one takeaway line. If you find yourself putting
  three paragraphs in the summary, the fold is in the wrong place.
- Headings still count for the heading order and the TOC. Give each `<details>` a stable `id`
  if you want the TOC to link to it.

## Diagrams: pre-render Mermaid to inline SVG

Artifacts must open offline by double-click, so we can't pull Mermaid from a CDN at view time.
Instead, render every diagram to SVG ahead of time and inline the result. Author diagrams as
ordinary ```mermaid``` fenced blocks in the markdown source (they stay human-readable and
re-renderable), then run the bundled script:

```bash
python scripts/render_diagrams.py <source>.md
```

It finds every ```mermaid``` block, renders each one **twice** (light + dark palette — a single
SVG bakes in its colors and would be unreadable in the other theme), normalizes the output, and
writes one ready-to-inline HTML fragment per block to `<source>.diagrams/`, with a
`manifest.txt` mapping fragments to blocks. It renders all diagrams in just two mermaid-cli
launches regardless of count. Requires Node (`npx`); mermaid-cli is fetched automatically.

The script handles the sharp edges for you: it floors any sub-14px label text (the validator
errors on it), rewrites Mermaid's shared internal ids so multiple inlined SVGs don't cross-wire
their arrowheads, and makes each SVG scale to its container.

## Inlining the diagram fragments

Each fragment is a `<figure class="diagram">` holding both SVGs; the template's CSS shows the
one matching the active theme. Inline fragment N where the Nth ```mermaid``` block sat, then
**remove the raw ```mermaid``` block from the visible HTML** — but keep it in the markdown source
and in the `<script type="text/markdown" id="artifact-source">` mirror, so the diagram stays
editable and the source stays complete.

```html
<figure class="diagram" role="group" aria-label="data model">
  <div class="diagram-svg diagram-light"><svg …>…</svg></div>
  <div class="diagram-svg diagram-dark" aria-hidden="true"><svg …>…</svg></div>
  <figcaption>Episode → Turn → Annotation, owned by User.</figcaption>
</figure>
```

Add a `<figcaption>` so the diagram is meaningful to screen readers and to agents reading the
source. Diagrams belong inside the `.item-detail`, not the summary — they're depth, not scan.

## Choosing a diagram shape

Reach for a diagram when structure or flow is hard to hold in prose. Match the shape to the idea:

| The idea | Mermaid shape |
|---|---|
| Stages, pipelines, tiers, "raw → processed" | `flowchart LR` / `flowchart TD` |
| A decision with options and consequences | `flowchart TD` with branch nodes |
| Data model / entities and relationships | `erDiagram` |
| Lifecycle / status transitions | `stateDiagram-v2` |
| Who calls whom, request/response order | `sequenceDiagram` |
| Nested layers / containment | `flowchart` with `subgraph` |

Keep each diagram to one idea. Two small diagrams beat one that tries to show everything —
they render with more breathing room and are far easier to read.
