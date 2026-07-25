---
name: generating-html-artifacts
description: Generates spacious, high-contrast, keyboard-navigable, agent-readable self-contained HTML artifacts by COMPOSING a page from a component library — a component per content type (tradeoff matrix, diff viewer, timeline, stat cards, excalidraw/mermaid diagrams, steps, tables…) assembled onto a shared shell. Use when the user asks to create, generate, build, render, or export an artifact, report, doc, dashboard, summary, plan, map, or page as HTML — when they mention an "HTML artifact", want output as a single .html file, or hand you an existing .html file and ask to apply this skill / improve its readability, contrast, spacing, theming, or navigation.
model: sonnet
context: fork
---

# Generating HTML artifacts (component composition)

Produces a single self-contained `.html` file (inline CSS + JS, no external dependencies, opens by double-click) that is spacious, high-contrast, keyboard-navigable, theme-aware, and easy for both humans and other agents to read.

Unlike a template library, this skill never forces the whole page into one shape. You **compose** the artifact: a shared page shell plus one component per content block — a tradeoff comparison gets `comparison-matrix`, a diff gets `diff-viewer`, an ASCII diagram gets `diagram-excalidraw`, KPIs get `stat-cards`. Choices are small, local, and hard to get wrong.

## How this skill runs

This skill runs in a **forked subagent** (`context: fork`) on the model set in the frontmatter above, so the reference-reading, generation, and validation stay out of the main conversation context. A fork does **not** inherit the conversation — it sees only this skill body plus `$ARGUMENTS`. The invoking agent must pass what's needed in the arguments: the **source** to render (a markdown file path is ideal — pass the path, not pasted text) and the **output** `.html` path. Work only from `$ARGUMENTS` and files on disk (including `brand.md` / `memory.md` / `references/`); never assume conversation history.

$ARGUMENTS

## Read before generating

- `brand.md` — the saved theme/brand (accent, fonts, radius). Read it every run and apply it. Update it when the user gives brand feedback.
- `memory.md` — accumulated "do it differently next time" feedback. Read it every run; apply every applicable lesson.
- `references/design-rules.md` — the hard rules: type scale, spacing scale, contrast, the no-gray rule, dark mode, accessibility, the shell's page frame, and how composition works. Read when generating or fixing an artifact.
- `references/components-catalog.md` — **the decision layer**: every component and page pattern, with when-to-use / avoid-when / schema. Read every run; it is how you choose.
- `references/navigation-patterns.md` — sidebar TOC vs tab panels, with accessible implementations. Read when deciding navigation.
- `references/depth-and-diagrams.md` — the `<!-- more -->` fold convention and the mermaid pre-render pipeline. Read when the source has `<!-- more -->` markers or ```mermaid``` blocks.
- `references/excalidraw-diagrams.md` — converting ASCII/ANSI box diagrams into embedded Excalidraw scenes. Read whenever the source has ASCII/ANSI diagrams.
- `assets/shell.html` — the page scaffold every composed artifact starts from.
- `assets/components/*.html` — the fragment library. Read the files for every component you use.
- `assets/components-demo.html` — every component rendered with sample content; the visual reference for what "good" looks like.

## The non-negotiable rules

These are summarized from `references/design-rules.md`. When in doubt, read that file.

1. **Single self-contained file.** Inline all CSS and JS. No CDNs, no external fonts, no build step. It must work offline by double-clicking. One sanctioned exception: the Excalidraw canvas embed (`references/excalidraw-diagrams.md`) loads its renderer from pinned CDNs as progressive enhancement — offline it must degrade to the original ASCII block, never break the page.
2. **Body text ≥ 18px.** Secondary/meta text ≥ 16px. UI chrome (badges, tab labels) ≥ 14px. Never below 14px.
3. **No gray text.** Secondary text uses a *darker ink*, not a mid-gray. Every text/background pair meets WCAG AA (≥ 4.5:1 normal, ≥ 3:1 large); aim for 7:1 on body text.
4. **High contrast surfaces.** Clear separation between background, surfaces (cards), and ink. **Code blocks follow the theme** via the `--code-*` tokens — never pin code to a fixed-dark panel. Only intentionally-dark elements use the fixed `--inverse` / `--inverse-foreground` tokens. Define every token you reference — an undefined `var(--code-bg)`/`var(--card)` renders **black**. Components only use tokens defined in `assets/shell.html`.
5. **Spacious.** Use the 8px spacing scale, generous section gaps. Prose is capped ~72ch; **components span the full content width** of the 1600px shell — wide pages are the point, wide text lines are not.
6. **Light + dark, both — auto only.** Ship both palettes via `prefers-color-scheme`; the theme follows the OS setting. **No toggle, no `[data-theme]`, no `localStorage`.** Pull accent/fonts from `brand.md`.
7. **Keyboard-friendly (recommended, not required).** Visible focus rings and real interactive elements (`button`, `a`, `summary`) where it's cheap. A skip link and landmarks are nice-to-have warnings in the validator.
8. **Semantic + agent-readable.** Use `header`/`nav`/`main`/`section`/`footer`, one `h1`, ordered headings, real `ul`/`table`. Embed a raw-content mirror in a `<script type="text/markdown" id="artifact-source">` block so an agent can extract the exact source without parsing the DOM.
9. **Render faithfully — never summarize *away*.** Every piece of detail in the source (reasoning, options, tradeoffs, specifics, diagrams) must stay **reachable** in the output. Shape what's visible at first glance through **progressive disclosure** (tldr-card up front, details-fold for depth), so the surface is compact but nothing is lost. Render ```mermaid``` blocks as diagrams (`diagram-mermaid`); render ASCII/ANSI box diagrams as embedded Excalidraw (`diagram-excalidraw`).

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Read brand.md + memory.md; note accent/fonts and any applicable lessons
- [ ] 2. Read references/components-catalog.md. Decide the page shape first: is the WHOLE artifact one interactive tool (deck / triage board / flag editor / prompt tuner)? If yes → copy the matching assets/patterns/ file whole, swap in real content + data arrays, jump to step 7.
- [ ] 3. Content inventory: walk the source block by block. For each block, name the component you'll use + a one-line reason (e.g. "§3 options → comparison-matrix — 3 options sharing 4 axes"). This list goes in your final summary.
- [ ] 4. Pre-render diagrams: ```mermaid``` blocks → python scripts/render_diagrams.py <source>.md. ASCII/ANSI box diagrams → convert to Excalidraw scenes (references/excalidraw-diagrams.md); preview via the Excalidraw MCP (read_me → create_view) when the MCP is available.
- [ ] 5. Compose: copy assets/shell.html. Fill title/lead/TOC — top-level entries per section, plus `<a class="sub">` sub-entries for sections with 3+ jump-worthy h3 subsections (give those h3s ids). For each section, paste the component fragments per your inventory — component CSS into the == COMPONENT STYLES == slot, HTML into the section, JS before the scrollspy script. Fill real content; replace every demo placeholder.
- [ ] 6. Render `<!-- more -->` folds as details-fold cards; inline mermaid fragments; embed excalidraw figures (references/depth-and-diagrams.md, references/excalidraw-diagrams.md).
- [ ] 7. Apply brand, auto light+dark, the type/spacing/contrast rules. Fill the markdown source mirror verbatim.
- [ ] 8. Validate: python scripts/validate_artifact.py <file.html>
- [ ] 9. Fix every error and review warnings; re-run until clean
- [ ] 10. If you invented a reusable block, save a candidate component + note it in your summary (see "Growing the library")
- [ ] 11. A simple content/document artifact needs no browser QA (the validator covers the hard rules). If the artifact has rendered diagrams or interactive JS, open the file once (`open <file>.html` — never a web server) and check both themes: no shapes overlap, interactions work, console is error-free.
- [ ] 12. Polish pass: re-read the artifact top to bottom as a reader, not a builder (references/design-rules.md, "The polish pass") — hierarchy, rhythm, alignment, fit, weight balance. Refine what's there rather than adding more.
- [ ] 13. End your summary with the component inventory (step 3), then the artifact's full absolute path on its own line.
```

**Step 2 — page shape:** patterns are the exception, composition is the rule. A document that *mentions* a board/deck/config is still a document — compose it.

**Step 3 — the inventory is the design review.** It replaces the old "pick one template, name a runner-up" guess. If you can't name a component for a block, it's prose (section + paragraphs), a callout, or a details-fold — those three cover almost everything.

## Choosing components

See `references/components-catalog.md` — it has a quick-scan routing table and a card per component (when / avoid / schema / variants). Read the component FILE before using it: the header comment carries the assembly contract (what goes in the head slot, what's per-instance, which ids must be unique). Common pairings:

- Options with shared criteria + a recommendation → `comparison-matrix`; without shared axes → `pros-cons`.
- Chronology with timestamps → `timeline`; timeless procedure → `steps`; unordered to-dos → `checklist`.
- Numbers to look up → `data-table`; numbers to see as a shape → `chart`; 2–5 headline KPIs → `stat-cards`.
- Vocabulary the page assumes (4+ terms) → `glossary`; an attributed quotation → `quote`.
- Parallel variants of one slot (per-language, per-platform) → `tabs`; a cited image or illustration → `figure`.
- Code to copy → `code-block`; a change to review → `diff-viewer`; code to teach → `annotated-code`.
- ASCII diagram → `diagram-excalidraw`; mermaid → `diagram-mermaid`; process with per-step depth → `flowchart`.

## Growing the library

The library is a living seed. When you invent a block worth reusing:

- **In the run (forked):** save it placeholder-ized and rule-compliant to `assets/components/candidates/NN-short-name.html`, and draft its catalog card in `references/components-catalog.candidates.md` (NOT the live catalog). End your summary with a clearly delimited block: *"Proposed new component `candidates/NN-short-name.html` — <one-line description>. Confirm to promote, or discard."*
- **After the run (main thread):** the calling agent asks the user. On **yes**, move the candidate into `assets/components/` and merge its card into `references/components-catalog.md`. On **no**, delete both. The live library changes only on an explicit human yes.

## Rendering from a markdown file

When given a markdown file and asked to produce an HTML artifact:
1. Read the markdown and the references (components-catalog always; depth-and-diagrams for ```mermaid```/`<!-- more -->`; excalidraw-diagrams for ASCII diagrams).
2. Do the content inventory (workflow step 3) against the actual sections.
3. Pre-render diagrams (workflow step 4).
4. Compose onto the shell: the H1 becomes the title, `##`/`###` become sections, and each block gets its component. Keep lists/tables/links as real HTML elements even when no component applies.
5. Embed the **markdown verbatim** in the source mirror (keep the ```mermaid```/ASCII blocks in it).
6. Apply brand, light+dark, and all design rules. Validate and fix.
7. Write the HTML next to the markdown (same folder, same base name) unless a path was specified.

## Applying the skill to an existing .html file

When the user hands you an existing artifact and asks to apply this skill:
1. Read the file and the references.
2. Preserve all content and meaning. This is a presentation/structure upgrade, not a rewrite of substance.
3. Re-compose onto the shell: bump fonts, kill grays, add auto light+dark (no toggle), add navigation, swap blocks for their proper components, add the source mirror.
4. Validate and fix.

## When html is ready
Always open it in the browser.

## Memory

After a session, write to `memory.md` when the user corrects how an artifact was built (spacing, color, a component choice, a missing affordance) or when a technique worked unusually well. Write brand/theme preferences (accent color, font choice, density) to `brand.md` instead. Do not record anything already covered in the references or generic advice — only real, applicable lessons.
