---
name: generating-html-artifacts
description: Generates spacious, high-contrast, keyboard-navigable, agent-readable self-contained HTML artifacts. Use when the user asks to create, generate, build, render, or export an artifact, report, doc, dashboard, summary, plan, map, or page as HTML — when they mention an "HTML artifact", want output as a single .html file, or hand you an existing .html file and ask to apply this skill / improve its readability, contrast, spacing, theming, or navigation.
model: haiku
context: fork
---

# Generating HTML artifacts

Produces a single self-contained `.html` file (inline CSS + JS, no external dependencies, opens by double-click) that is spacious, high-contrast, keyboard-navigable, theme-aware, and easy for both humans and other agents to read.

## How this skill runs

This skill runs in a **forked subagent** (`context: fork`) on the **haiku** model so the reference-reading, generation, and validation stay out of the main conversation context. A fork does **not** inherit the conversation — it sees only this skill body plus `$ARGUMENTS`. The invoking agent must pass what's needed in the arguments: the **source** to render (a markdown file path is ideal — pass the path, not pasted text) and the **output** `.html` path. Work only from `$ARGUMENTS` and files on disk (including `brand.md` / `memory.md` / `references/`); never assume conversation history.

$ARGUMENTS

## Read before generating

- `brand.md` — the saved theme/brand (accent, fonts, radius). Read it every run and apply it. Update it when the user gives brand feedback.
- `memory.md` — accumulated "do it differently next time" feedback. Read it every run; apply every applicable lesson.
- `references/design-rules.md` — the hard rules: type scale, spacing scale, contrast, the no-gray rule, dark mode, accessibility. Read when generating or fixing an artifact.
- `references/navigation-patterns.md` — how to choose sidebar TOC vs tab panels, with accessible implementations. Read when deciding navigation.
- `references/depth-and-diagrams.md` — the expandable overview→detail card pattern (the `<!-- more -->` fold) and how to pre-render Mermaid to inline SVG. Read whenever the source has detailed decisions/findings, any `<!-- more -->` markers, or ```mermaid``` blocks.
- `references/templates-table.md` — the **layout routing table**: a library of purpose-built templates (deck, comparison, flowchart, status report, interactive editors…) and how to pick one. Read every run to choose the layout.
- `assets/templates/` — the seed template library the routing table points at (blueprints to copy + adapt).
- `assets/template.html` — the generic sidebar-TOC document scaffold; the **bespoke fallback** when no library template fits (and the right default for long-form findings/reports).

## The non-negotiable rules

These are summarized from `references/design-rules.md`. When in doubt, read that file.

1. **Single self-contained file.** Inline all CSS and JS. No CDNs, no external fonts, no build step. It must work offline by double-clicking.
2. **Body text ≥ 18px.** Secondary/meta text ≥ 16px. UI chrome (badges, tab labels) ≥ 14px. Never below 14px.
3. **No gray text.** Secondary text uses a *darker ink*, not a mid-gray. Every text/background pair meets WCAG AA (≥ 4.5:1 normal, ≥ 3:1 large); aim for 7:1 on body text.
4. **High contrast surfaces.** Clear separation between background, surfaces (cards), and ink. **Code blocks follow the theme** (light surface + dark syntax in light, dark + bright in dark) via the `--code-*` tokens — never pin code to a fixed-dark panel and never hardcode light hex for code text. Only intentionally-dark elements (dark "primary" buttons, inverted slides) use the fixed `--inverse` / `--inverse-foreground` tokens. Define every token you reference — an undefined `var(--code-bg)`/`var(--card)` renders **black**.
5. **Spacious.** Use the 8px spacing scale, generous section gaps, and a readable measure (~65–75ch). Whitespace is a feature, not waste.
6. **Light + dark, both — auto only.** Ship both palettes via `prefers-color-scheme`; the theme follows the OS setting. **No toggle, no `[data-theme]`, no `localStorage`.** Pull accent/fonts from `brand.md`.
7. **Keyboard-friendly (recommended, not required).** Visible focus rings (never `outline:none` without a replacement) and real interactive elements (`button`, `a`) where it's cheap. A skip link to `#main` and strict landmarks are nice-to-have, not mandatory — the validator reports them as warnings.
8. **Semantic + agent-readable.** Use `header`/`nav`/`main`/`section`/`footer`, one `h1`, ordered headings, real `ul`/`table`. Embed a raw-content mirror in a `<script type="text/markdown" id="artifact-source">` block so an agent can extract the exact source without parsing the DOM.
9. **Preserve depth — never flatten.** If the source has detail (reasoning, options, tradeoffs, diagrams), the artifact must keep it. Show a scannable summary up front, but put the full detail one click away — don't summarize it out of existence. Honor `<!-- more -->` folds and render ```mermaid``` blocks as diagrams. See `references/depth-and-diagrams.md`.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Read brand.md + memory.md; note accent/fonts and any applicable lessons
- [ ] 2. Choose the layout (references/templates-table.md): pick the best-fit template, or decide bespoke. Name choice + runner-up in one line.
- [ ] 3. Decide navigation if bespoke (references/navigation-patterns.md): TOC vs tabs
- [ ] 4. If the source has ```mermaid``` blocks: python scripts/render_diagrams.py <source>.md
- [ ] 5. Generate: copy the chosen template from assets/templates/ and adapt its content + JS data — OR build from assets/template.html if bespoke. Fill the markdown source mirror.
- [ ] 6. If you used a library template, bring it up to our rules (see references/templates-table.md): brand palette, largish fonts, source mirror.
- [ ] 7. Render `<!-- more -->` folds as <details class="item"> cards; inline diagram fragments (references/depth-and-diagrams.md)
- [ ] 8. Apply brand, auto light+dark, the type/spacing/contrast rules
- [ ] 9. Validate: python scripts/validate_artifact.py <file.html>
- [ ] 10. Fix every error and review warnings; re-run until clean
- [ ] 11. If you invented a reusable layout, save a candidate + note it in your summary (see "Growing the library")
- [ ] 12. QA in a browser, BOTH themes: open the file, flip prefers-color-scheme, and confirm code follows the theme, no diagram shapes overlap, every interaction works, and the console is error-free (see design-rules.md "Generation-time pitfalls")
```

**Step 2 — layout choice:** see "Choosing the layout" below.

**Step 3 — navigation choice (bespoke only, quick heuristic):**
- Long-form / linear / a document you read top-to-bottom → **sidebar TOC** (sticky, scrollspy).
- Dashboard / grouped panels / "switch between views" → **tab panels**.
- Both can coexist (TOC for sections, tabs inside a section). See `references/navigation-patterns.md`.

**Step 9 — the validator** is run, not read. ERRORS are blocking: font sizes under 18px (body) / under 14px (any), gray/low-contrast text, missing dark mode, and a missing source mirror. Accessibility items (skip link, landmarks) are warnings — review them, but they don't block.

## Choosing the layout

Markdown flattens every deliverable into one scrolling column. The template library exists so the
**layout matches the shape of the information** — a deck looks like a deck, a comparison is
side-by-side, a process is a flowchart, a backlog is a draggable board.

1. Assess what the reader needs to **DO** with the content: compare / scan / navigate / follow /
   see-structure / review / edit.
2. Open `references/templates-table.md`, find the single best-fit row, and **name the choice +
   runner-up in one line** before building.
3. **If a template fits:** copy it from `assets/templates/`, swap in the real content (and its JS
   data arrays for interactive ones), then **bring it up to our rules** (brand palette, largish
   fonts, source mirror — checklist in the routing table). Templates are blueprints, not finished
   output; every artifact still passes `validate_artifact.py`.
4. **If nothing fits:** build bespoke from `assets/template.html` + `references/design-rules.md`
   (the right default for long-form findings/reports), or graft two templates together.

## Growing the library

The library is a living seed, not a fixed set. When you invent a layout worth reusing:

- **In the run (forked):** save the new layout as a **candidate** — write it, placeholder-ized and
  already brought up to our rules, to `assets/templates/candidates/NN-short-name.html`, and draft a
  routing row in `references/templates-table.candidates.md` (NOT the live table). Then add a clearly
  delimited block at the **end** of your return summary: *"Proposed new template
  `candidates/NN-short-name.html` — <one-line description>. Confirm to promote, or discard."* Keep
  it trailing so callers that only want the artifact path aren't disrupted.
- **After the run (main thread):** the calling agent asks the user. On **yes**, move the candidate
  into `assets/templates/` and merge its row into `references/templates-table.md`. On **no**, delete
  the candidate file and its drafted row. The live library and routing table change only on an
  explicit human yes.

## Rendering from a markdown file

When given a markdown file (e.g. by the `capture-findings` skill) and asked to produce an HTML artifact:
1. Read the markdown and the references. If it has ```mermaid``` blocks or `<!-- more -->` folds, read `references/depth-and-diagrams.md`.
2. If there are ```mermaid``` blocks, pre-render them first: `python scripts/render_diagrams.py <source>.md`. You'll inline the resulting fragments in step 4.
3. Map its structure to the artifact: the H1 becomes the title, `##`/`###` become sections, lists/tables/links carry over as real HTML elements.
4. Render depth: a section with a `<!-- more -->` fold becomes a `<details class="item">` card (summary before the marker, detail after); inline each diagram fragment where its mermaid block sat and drop the raw block from the visible HTML.
5. Choose navigation per `references/navigation-patterns.md` (long-form markdown → sidebar TOC).
6. Embed the **markdown verbatim** in the `<script type="text/markdown" id="artifact-source">` mirror — it is already the canonical source (keep the ```mermaid``` blocks in it).
7. Apply brand, light+dark, and all design rules. Validate and fix.
8. Write the HTML next to the markdown (same folder, same base name) unless a path was specified.

## Applying the skill to an existing .html file

When the user hands you an existing artifact and asks to apply this skill:
1. Read the file and the references.
2. Preserve all content and meaning. This is a presentation/structure upgrade, not a rewrite of substance.
3. Bring it up to every rule above: bump fonts, kill grays, add auto light+dark (no toggle), add navigation, add the source mirror. (Skip link + landmarks are optional niceties.)
4. Validate and fix.

## Memory

After a session, write to `memory.md` when the user corrects how an artifact was built (spacing, color, a layout choice, a missing affordance) or when a technique worked unusually well. Write brand/theme preferences (accent color, font choice, density) to `brand.md` instead. Do not record anything already covered in the references or generic advice — only real, applicable lessons.
