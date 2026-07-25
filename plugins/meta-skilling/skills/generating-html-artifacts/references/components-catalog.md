# Components catalog

The decision layer of this skill. Pages are **composed**, not templated: walk the source
block by block and pick the component whose presentation fits each block. Choices are
small and local — a primer can be sections + an excalidraw diagram + a data table +
a comparison matrix. There is no single "right template" to guess wrong.

> **Components are blueprints, not finished output.** Each file under
> `assets/components/` is a fragment (contract comment + scoped CSS + HTML demo + JS if
> any). Copy the CSS into the shell's `/* == COMPONENT STYLES == */` slot, the HTML into
> a `<section>`, the JS before the scrollspy script — then fill in real content and run
> `scripts/validate_artifact.py`. The demo content is placeholder; the contract
> (tokens, type scale, auto light/dark, source mirror) wins.

How to choose, per block: ask **"what does the reader need to DO with this block —
compare, scan, follow, judge, copy, or explore?"** — not "what topic is this."

## Quick-scan routing

| Content block looks like… | Use | Not when… |
|---|---|---|
| Any top-level topic | [section](#section) | sub-part of a topic (h3 + prose) |
| The conclusion, up front | [tldr-card](#tldr-card) | mid-page emphasis (callout) |
| Caveat / risk / prerequisite inline | [callout](#callout) | page-level summary (tldr-card) |
| Attributed quotation (who said it matters) | [quote](#quote) | your own emphasis (callout) |
| Detail that should be opt-in | [details-fold](#details-fold) | critical warnings; nesting folds |
| 2–5 parallel variants of one slot | [tabs](#tabs) | every reader needs every variant |
| 2–5 headline numbers | [stat-cards](#stat-cards) | >5 numbers (data-table) |
| Numbers best seen as a shape | [chart](#chart) | exact value lookup (data-table) |
| Genuinely tabular rows | [data-table](#data-table) | options × judgment axes (matrix) |
| 2–4 options × shared axes, with a pick | [comparison-matrix](#comparison-matrix) | no recommendation to make |
| Alternatives without shared axes | [pros-cons](#pros-cons) | shared criteria (matrix) |
| Chronology where *when* matters | [timeline](#timeline) | timeless process (steps) |
| Ordered process / phases | [steps](#steps) | timestamped events (timeline) |
| Unordered action items to tick off | [checklist](#checklist) | ordered procedure (steps) |
| Vocabulary the page assumes (4+ terms) | [glossary](#glossary) | <4 terms (inline); long defs (fold) |
| Copyable code sample | [code-block](#code-block) | inline mentions (`code`); diffs |
| A unified diff | [diff-viewer](#diff-viewer) | plain code (code-block) |
| Code needing per-line explanation | [annotated-code](#annotated-code) | self-explanatory snippets |
| Repo layout / where things live | [file-tree](#file-tree) | interactive explorer needed |
| Image/SVG prose cites by number | [figure](#figure) | mermaid/ASCII/data series |
| ASCII/ANSI box diagram in source | [diagram-excalidraw](#diagram-excalidraw) | ordinary code block; mermaid |
| ```mermaid``` block in source | [diagram-mermaid](#diagram-mermaid) | ASCII source; clickable steps |
| Process with per-step detail | [flowchart](#flowchart) | static structure, no detail |

**Page patterns** (`assets/patterns/`) — use INSTEAD of composing when the whole artifact
is one interactive tool: [slide-deck](#slide-deck), [triage-board](#triage-board),
[feature-flags](#feature-flags), [prompt-tuner](#prompt-tuner). If the artifact is a
document with sections — even one that mentions decks, boards, or configs — compose.

---

## Display components

Static/structural display components — the backbone of document-style artifacts. All CSS is prefix-scoped (`c-*`); all color comes from the shell's tokens.

### section
- **File:** `assets/components/section.html`
- **It is:** the standard anchored topic wrapper: `<section id>` + h2, with optional eyebrow/kicker and lede.
- **When to use:** every top-level topic block of a composed page; the `id` is what the sidebar TOC/scrollspy links to.
- **Avoid when:** sub-parts inside a topic — use h3 + prose, a card, or details-fold instead of nesting sections.
- **Schema:** id, optional eyebrow (≤ 6 words), h2 title, optional 1-2 sentence lede, then any body content/components.
- **Variants:** with/without eyebrow; lede optional. Nested TOC: when a section has 3+ jump-worthy h3 subsections, give each h3 an id and add an `<a class="sub">` under its TOC link (the shell styles and scrollspies sub-entries).

### tldr-card
- **File:** `assets/components/tldr-card.html`
- **It is:** a prominent accent-surface summary card stating the conclusion up front.
- **When to use:** immediately after the page header, one per page — incident reviews, status reports, decision docs, long explorations.
- **Avoid when:** mid-page emphasis (use callout) or short artifacts where the lead paragraph already says it all.
- **Schema:** label (default "TL;DR"), 2-4 sentence summary, optional 2-4 key-point bullets.
- **Variants:** none; bullets optional.

### callout
- **File:** `assets/components/callout.html`
- **It is:** a bordered aside with left accent bar + inline SVG icon for must-not-miss notes.
- **When to use:** caveats, risks, prerequisites, deprecation notices — inline in the reading flow.
- **Avoid when:** page-level summaries (tldr-card) or long content (details-fold); never stack more than two.
- **Schema:** variant, optional bold title, 1-2 sentences.
- **Variants:** `info` (primary), `note` (neutral), `warning`, `danger` — classes `c-callout--info/note/warning/danger`.

### quote
- **File:** `assets/components/quote.html`
- **It is:** an attributed pull-quote — large quoted text on a primary left bar, with a name + source caption.
- **When to use:** a quotation whose weight comes from who said it — cited articles, decision-makers, users from research.
- **Avoid when:** quoting yourself (prose or callout), long excerpts, or more than one or two per page.
- **Schema:** 1–3 sentence quotation, attribution name, source (linked when a URL exists).
- **Variants:** none.

### details-fold
- **File:** `assets/components/details-fold.html`
- **It is:** a native `<details>` card — always-visible title + verdict line, full detail behind a click. No JS.
- **When to use:** overview→detail splits: per-option deep dives, FAQs, expandable list items.
- **Avoid when:** hiding critical warnings or the main conclusion; never nest folds.
- **Schema:** per fold — h3 title, one-line summary (the verdict), detail body (any content).
- **Variants:** add `open` to start expanded.

### tabs
- **File:** `assets/components/tabs.html`
- **It is:** an accessible tab set (real `role=tablist` + buttons, ←/→ keyboard support) showing one of 2–5 panels in the same slot.
- **When to use:** parallel variants of one thing — per-language code, per-platform install steps, before/after states.
- **Avoid when:** every reader needs every variant (stack sections instead), >5 tabs, or sequential content (tabs hide order).
- **Schema:** per tab — 1–2 word label + panel content; the most common case starts active.
- **Variants:** none structurally. IDs must be unique per instance (prefix per instance, e.g. `t1-`, `t2-`).

### stat-cards
- **File:** `assets/components/stat-cards.html`
- **It is:** a responsive grid of 2-5 KPI cards: big tabular number, uppercase label, optional delta.
- **When to use:** headline metrics before the prose — weekly status, incident impact, experiment results.
- **Avoid when:** more than 5 numbers (data-table) or metrics without clear label/timeframe.
- **Schema:** per card — value, label, optional delta (direction glyph + words, never color alone), optional attention flag.
- **Variants:** delta `c-stat-delta--up/down/flat`; card flag `c-stat--flag` (warning left border).

### data-table
- **File:** `assets/components/data-table.html`
- **It is:** a real `<table>` in a horizontal-scroll wrapper: styled uppercase header, row hover, bottom caption.
- **When to use:** genuinely tabular data the reader scans or compares — latency budgets, checklists with owners, experiment arms.
- **Avoid when:** options × judgment axes with a recommendation (comparison-matrix) or 2-3 key numbers (stat-cards).
- **Schema:** optional caption, column headers, rows; `class="num"` on numeric th/td for right-aligned tabular figures.
- **Variants:** numeric alignment via `.num`.

### chart
- **File:** `assets/components/chart.html`
- **It is:** a dependency-free inline-SVG bar or line chart rendered from a JSON `data-chart` attribute — grid lines, axis labels, value labels, legend, one highlightable item; themes via tokens.
- **When to use:** numbers the reader should see as a *shape* — magnitude comparison across categories (bar) or trend across ordered points (line); 2–12 points, 1–2 series.
- **Avoid when:** exact value lookup matters more than shape (data-table — and keep the table alongside when both matter), >2 series or >12 points, or anything needing a real charting library.
- **Schema:** `{ type: "bar"|"line", unit?, highlight?, labels[], series: [{ name, values[] }] }` in `data-chart` (single-quoted attribute); the `<figcaption>` states the takeaway in words.
- **Variants:** bar / line; `highlight` index flags one bar/point in `--warning`. One shared `<script>` wires all instances.

### comparison-matrix
- **File:** `assets/components/comparison-matrix.html`
- **It is:** THE tradeoff component — options × decision axes as a real table, one recommended option highlighted with an accent column + "Recommended" badge.
- **When to use:** architecture/tooling/library choices, build-vs-buy, migration targets — whenever 2-4 options share decision criteria.
- **Avoid when:** raw data rows (data-table) or when there's no recommendation to make.
- **Schema:** axes as rows (`th scope="row"`), options as columns, short cell values with ✓ / ~ / ✗ glyphs + words; recommended option's th/tds get `c-matrix-rec` and its header gets `c-matrix-badge`.
- **Variants:** none beyond the expected recommended-column highlight.

### pros-cons
- **File:** `assets/components/pros-cons.html`
- **It is:** 2-3 side-by-side cards, each an option with headed "Advantages" / "Drawbacks" lists (✓ / ✕ markers).
- **When to use:** alternatives whose tradeoffs don't share a common set of axes — lighter than comparison-matrix.
- **Avoid when:** the same criteria apply to all options (comparison-matrix) or a single option's tradeoffs (callout/prose).
- **Schema:** per column — h3 title, optional one-line framing, advantages list, drawbacks list (3-5 short items each).
- **Variants:** 2 or 3 columns (grid auto-fits).

### timeline
- **File:** `assets/components/timeline.html`
- **It is:** a vertical rail with dots, monospace timestamp chips, and event cards.
- **When to use:** chronological events where *when* matters — incident timelines, release history, dated milestones.
- **Avoid when:** ordered-but-timeless process steps (steps) or 2-3-entry schedules (prose).
- **Schema:** per entry — timestamp, body (optional bold lead-in + 1-2 sentences), optional dot kind.
- **Variants:** dot `c-tl-dot--impact` (destructive), `--ok` (success), `--key` (primary), default neutral.

### steps
- **File:** `assets/components/steps.html`
- **It is:** a numbered `<ol>` of process steps on a connector rail, with status markers and optional file/system tags.
- **When to use:** implementation phases, runbook procedures, rollout/migration sequences.
- **Avoid when:** timestamped events (timeline) or unordered lists.
- **Schema:** per step — h3 title, 1-3 sentences, optional mono tags; optional status class on the `<li>`.
- **Variants:** step status — default, `is-done` (filled ✓ marker), `is-current` (primary ring).

### checklist
- **File:** `assets/components/checklist.html`
- **It is:** a card of real checkboxes with imperative action items and optional owner/why notes; ticked items strike through. No JS.
- **When to use:** unordered action items the reader works through — postmortem follow-ups, pre-launch checks, migration preconditions.
- **Avoid when:** ordered procedures (steps) or status reporting (ticks are session-local and unsaved).
- **Schema:** optional group label; per item — verb-first label, optional note (owner, deadline, why).
- **Variants:** pre-ticked via `checked`. IDs unique per instance (`chk1-`, `chk2-`…).

### glossary
- **File:** `assets/components/glossary.html`
- **It is:** a two-column definition grid (`<dl>`) — bold term (code-formatted for identifiers) + 1–2 sentence definition, auto-fitting columns.
- **When to use:** vocabulary the rest of the page assumes — acronym decoders, term lists of 4+ entries.
- **Avoid when:** fewer than 4 terms (define inline), definitions with examples (details-fold or a section), more than term+definition columns (data-table).
- **Schema:** per item — term, 1–2 sentence definition.
- **Variants:** none.

---

## Code components

Components for showing code, diffs, and project structure. All follow the theme automatically: code surfaces use `--code-bg`/`--code-fg` and the `--code-*` syntax tokens, and add/del tints use `color-mix` on `--success`/`--destructive`.

### code-block
- **File:** `assets/components/code-block.html`
- **It is:** the shell's `pre.code` extended with a header bar (language pill + optional filename) and a working copy-to-clipboard button (`navigator.clipboard` with a textarea/`execCommand` fallback; inline "Copied" feedback, never `alert()`).
- **When to use:** the default for any multi-line code sample worth copying — API examples, configs, CLI sessions, function listings.
- **Avoid when:** inline identifier mentions (use `code`), diffs (use diff-viewer), code needing explanation callouts (use annotated-code).
- **Schema:** `{ language, filename?, code }` — code is pre-escaped and marked up with the shell's syntax classes `.kw/.fn/.str/.cm/.num`.
- **Variants:** filename may be omitted. Multiple instances per page are fine; the one script wires them all.

### diff-viewer
- **File:** `assets/components/diff-viewer.html`
- **It is:** a pure unified-diff viewer — one card per file with a header bar (path + add/del counts), hunk headers, and add/del/context rows with line numbers and +/− markers.
- **When to use:** code review summaries, before/after changes, migration output — anything expressed as a unified diff over one or more files.
- **Avoid when:** plain code samples (code-block), prose/option comparisons (table or matrix), review comment threads (deliberately out of scope — this viewer is pure).
- **Schema:** `{ files: [{ path, adds, dels, hunks: [{ header, lines: [{ type: "add"|"del"|"ctx", ln, code }] }] }] }` — rows use `white-space:pre`, so leading whitespace is literal; escape `<`, `>`, `&`.
- **Variants:** add `c-diff-noln` to `.c-diff` to hide the line-number gutter.

### annotated-code
- **File:** `assets/components/annotated-code.html`
- **It is:** a code block on a card with numbered circular markers (①②③) at the end of annotated lines, each marker linked to a matching numbered note in a list below the block; the target note highlights on jump (`:target`).
- **When to use:** teaching material and walkthroughs where specific lines need guided explanation.
- **Avoid when:** self-explanatory snippets (code-block), change-focused views (diff-viewer), more than ~6 notes (split the block).
- **Schema:** `{ filename?, code, notes }` — append `<a class="c-annot-mark" href="#ID-N">N</a>` to each annotated line; note N is `<li id="ID-N">`. IDs must be unique per instance on the page.
- **Variants:** header bar may be omitted; notes may contain inline code and links.

### file-tree
- **File:** `assets/components/file-tree.html`
- **It is:** a static nested `<ul>` rendered as a directory tree — CSS guide lines (vertical rails + stubs), CSS-drawn folder icons (box + tab, `--primary`) and file icons (bordered sheet with folded corner), with `role="tree"`/`treeitem`/`group` semantics.
- **When to use:** showing a repo layout, scaffold output, or "where things live" overview.
- **Avoid when:** an interactive/expandable explorer is needed (this tree is static), or trees deeper than ~5 levels (show the relevant subtree).
- **Schema:** nested `<ul>`; each `<li role="treeitem">` holds `<span class="c-ftree-dir">name/</span>` (folder) or `<span class="c-ftree-file">name.ext</span>` (file); folder children go in a nested `<ul role="group">`. The trailing `/` on folders is written in the text, not added by CSS.
- **Variants:** none.

---

## Diagram components

Pick by source format: ASCII box drawing → `diagram-excalidraw`; ```mermaid``` block → `diagram-mermaid`; a process with per-step detail worth exploring → `flowchart`; a cited image or illustration → `figure`.

### diagram-excalidraw
- **File:** `assets/components/diagram-excalidraw.html`
- **It is:** an embedded Excalidraw scene — renders as an inline SVG (with a "Live canvas" toggle to an interactive pan/zoom canvas) and degrades to the original ASCII block offline.
- **When to use:** the source markdown contains a hand-drawn ASCII/ANSI box diagram (box-drawing characters). Convert it to Excalidraw shorthand elements per `references/excalidraw-diagrams.md` and embed.
- **Avoid when:** the block is ordinary code, a ```mermaid``` diagram, or the artifact must work fully offline as its primary mode (the render needs the pinned CDN once).
- **Schema:** per diagram — shorthand-elements JSON (type/id/x/y/width/height + labels, arrows, bindings), an aria-label, the original ASCII as fallback. Element colors use the fixed Excalidraw palette from `references/excalidraw-diagrams.md` (content art — explicit hex is fine there). Head block (CSS link, `EXCALIDRAW_ASSET_PATH`, importmap) and module loader go in ONCE per page; the `<figure>` repeats per diagram.
- **Variants:** none.

### diagram-mermaid
- **File:** `assets/components/diagram-mermaid.html`
- **It is:** the pre-rendered two-SVG figure — one `<figure class="diagram">` holding a light-palette SVG and a dark-palette SVG, with the shell's CSS showing the one matching the active theme.
- **When to use:** the source markdown has a ```mermaid``` block. Run `python scripts/render_diagrams.py <source>.md`, then inline the emitted fragment where the block sat (pipeline details in `references/depth-and-diagrams.md`).
- **Avoid when:** the diagram is an ASCII box drawing or needs clickable annotated steps.
- **Schema:** per diagram — light SVG + dark SVG (from the render script, baked per-theme colors), an aria-label, a caption stating the takeaway. The raw mermaid source stays in the markdown mirror, not the visible HTML. No CSS to paste (shell ships `figure.diagram`).
- **Variants:** none.

### flowchart
- **File:** `assets/components/flowchart.html`
- **It is:** a clickable-step flowchart — HTML/CSS boxes joined by arrows, with a sticky side panel showing the selected step's detail. Steps are real `<button>`s, so the whole chart is keyboard-navigable.
- **When to use:** a process, pipeline, or decision flow where each step has detail worth showing on demand (what runs, duration, failure modes).
- **Avoid when:** the diagram is static structure with no per-step detail (use `diagram-mermaid`) or comes from an ASCII source (use `diagram-excalidraw`).
- **Schema:** per flowchart — steps (key, title, one-line meta, variant, detail block with heading + meta + body + optional `pre.code`), with labeled branch lanes after a decision step. Each detail block's `data-step` must match its button's.
- **Variants:** step variants — default, `.is-decision` (accent gate), `.is-failure` (destructive border/lane), `.is-terminal` (success border). Multiple instances per page OK.

### figure
- **File:** `assets/components/figure.html`
- **It is:** a numbered, captioned figure card with a stable `id` — the generic wrapper for screenshots, exported images (inlined), and hand-built SVG illustrations that prose cites by number ("see Figure 2").
- **When to use:** a visual asset the text refers to by number or that needs a takeaway caption and anchor.
- **Avoid when:** mermaid blocks (diagram-mermaid), ASCII diagrams (diagram-excalidraw), data series (chart), or purely decorative images (leave those out).
- **Schema:** `id="fig-<slug>"`, media (inline SVG or inlined `<img>` — no external files), numbered caption stating the takeaway. Number figures sequentially across the page.
- **Variants:** none.

---

## Page patterns

Page patterns are **whole-page alternatives to composition**. When the entire artifact is a single interactive tool, don't start from `assets/shell.html` and compose components — copy one of these files whole (it already carries the shell's token palette, auto light/dark, type scale, and the `artifact-source` mirror) and replace the demo content and the data arrays with the real content. Each file's header comment repeats its contract.

If the artifact is a document with sections — even one that mentions decks, boards, or configs — compose from components instead; patterns are for when the page *is* the tool.

### slide-deck
- **File:** `assets/patterns/slide-deck.html`
- **It is:** a keyboard/button-driven presentation deck — one full-viewport slide at a time, swapped by class toggle (no scroll-snap), with a slide counter and Prev/Next controls.
- **When to use:** status updates, demos, pitch/recap talks, decision meetings — anything meant to be stepped through screen by screen.
- **Avoid when:** the content is a reference doc or tutorial the reader scrolls and re-reads.
- **Schema:** one `<section class="slide">` per screen, content inside `.slide-inner`. Demo slide archetypes: title, shipped list, progress bars, metrics + sparkline, decision slide (`.invert`), next-steps list.
- **Variants:** `.invert` on a slide gives a fixed-dark emphasis slide (uses `--inverse`; text and accents re-pin automatically).

### triage-board
- **File:** `assets/patterns/triage-board.html`
- **It is:** a four-column drag-and-drop prioritization board with per-column counts and point totals, tag filtering, and "Copy as markdown" export of the current arrangement.
- **When to use:** cycle/sprint triage, backlog cuts, prioritization workshops — any "sort these items into ranked buckets and take the result away" task.
- **Avoid when:** the list is already decided or read-only — a static table component is cheaper.
- **Schema:** `COLUMNS` array (`key`, `label`, `rationale`) and `INITIAL` array of items (`id`, `title`, `tag` ∈ bug/feat/chore/debt, `est` ∈ S/M/L, `owner`, `col`). Render, drag/drop, filter, reset, and markdown export are generic.
- **Variants:** tag classes (`tag-bug`, `tag-feat`, `tag-chore`, `tag-debt`) map to destructive/success/accent/warning tints.

### feature-flags
- **File:** `assets/patterns/feature-flags.html`
- **It is:** a form-based editor for a config file of boolean toggles — grouped switch rows with dependency warnings, a live unified diff of pending changes, and copy-diff / copy-full-JSON buttons.
- **When to use:** editing feature-flag sets, settings manifests, permission matrices — any boolean-options config where dependencies and the final diff matter.
- **Avoid when:** the config is read-only documentation, or options aren't booleans (selects/numbers need real form components).
- **Schema:** `GROUPS` array: `{ id, label, flags: [{ key, desc, on, requires?, rollout? }] }`. `requires` wires the live warning when a flag is on without its prerequisite; `rollout` renders a % badge.

### prompt-tuner
- **File:** `assets/patterns/prompt-tuner.html`
- **It is:** a live template editor — a `contenteditable` prompt template with `{{slot}}` highlighting on the left, and sample records on the right that re-render the filled template on every keystroke (caret preserved), plus char/token counter and copy-prompt.
- **When to use:** tuning LLM prompts, email/message macros, codegen templates — anything where you want to see one template filled by several concrete examples at once.
- **Avoid when:** documenting a prompt statically, or when one example rendering suffices.
- **Schema:** `DEFAULT_TEMPLATE` (string with `{{slot}}` placeholders), `SAMPLES` (array of `{ label, planClass, data }` records), `KNOWN_SLOTS` (valid slot names — unknown ones render with the dashed warning style).

---

*Components replace the old page-template library; markup patterns were mined from the
MIT-licensed `anthropics/html-effectiveness` seed set and rebuilt on this skill's tokens.*
