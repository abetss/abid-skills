---
name: generating-html-artifacts
description: Generates spacious, high-contrast, keyboard-navigable, agent-readable self-contained HTML artifacts. Use when the user asks to create, generate, build, render, or export an artifact, report, doc, dashboard, summary, plan, map, or page as HTML — when they mention an "HTML artifact", want output as a single .html file, or hand you an existing .html file and ask to apply this skill / improve its readability, contrast, spacing, theming, or navigation.
---

# Generating HTML artifacts

Produces a single self-contained `.html` file (inline CSS + JS, no external dependencies, opens by double-click) that is spacious, high-contrast, keyboard-navigable, theme-aware, and easy for both humans and other agents to read.

## Read before generating

- `brand.md` — the saved theme/brand (accent, fonts, radius). Read it every run and apply it. Update it when the user gives brand feedback.
- `memory.md` — accumulated "do it differently next time" feedback. Read it every run; apply every applicable lesson.
- `references/design-rules.md` — the hard rules: type scale, spacing scale, contrast, the no-gray rule, dark mode, accessibility. Read when generating or fixing an artifact.
- `references/navigation-patterns.md` — how to choose sidebar TOC vs tab panels, with accessible implementations. Read when deciding navigation.
- `assets/template.html` — the self-contained scaffold to copy from. Start here for a new artifact.

## The non-negotiable rules

These are summarized from `references/design-rules.md`. When in doubt, read that file.

1. **Single self-contained file.** Inline all CSS and JS. No CDNs, no external fonts, no build step. It must work offline by double-clicking.
2. **Body text ≥ 18px.** Secondary/meta text ≥ 16px. UI chrome (badges, tab labels) ≥ 14px. Never below 14px.
3. **No gray text.** Secondary text uses a *darker ink*, not a mid-gray. Every text/background pair meets WCAG AA (≥ 4.5:1 normal, ≥ 3:1 large); aim for 7:1 on body text.
4. **High contrast surfaces.** Clear separation between background, surfaces (cards), and ink.
5. **Spacious.** Use the 8px spacing scale, generous section gaps, and a readable measure (~65–75ch). Whitespace is a feature, not waste.
6. **Light + dark, both.** Ship both palettes via `prefers-color-scheme` AND a `[data-theme]` override, plus an in-page toggle that persists to `localStorage`. Pull accent/fonts from `brand.md`.
7. **Keyboard-navigable.** Skip link to `#main`, visible focus rings (never `outline:none` without a replacement), logical tab order, real interactive elements (`button`, `a`).
8. **Semantic + agent-readable.** Use `header`/`nav`/`main`/`section`/`footer`, one `h1`, ordered headings, real `ul`/`table`. Embed a raw-content mirror in a `<script type="text/markdown" id="artifact-source">` block so an agent can extract the exact source without parsing the DOM.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Read brand.md + memory.md; note accent/fonts and any applicable lessons
- [ ] 2. Decide navigation (references/navigation-patterns.md): TOC vs tabs
- [ ] 3. Generate from assets/template.html, filling content + the markdown source mirror
- [ ] 4. Apply brand, light+dark palettes, the type/spacing/contrast rules
- [ ] 5. Validate: python scripts/validate_artifact.py <file.html>
- [ ] 6. Fix every error and review warnings; re-run until clean
- [ ] 7. If verifying visually, open in a browser and check both themes
```

**Step 2 — navigation choice (quick heuristic):**
- Long-form / linear / a document you read top-to-bottom → **sidebar TOC** (sticky, scrollspy).
- Dashboard / grouped panels / "switch between views" → **tab panels**.
- Both can coexist (TOC for sections, tabs inside a section). See `references/navigation-patterns.md`.

**Step 5 — the validator** is run, not read. It flags font sizes under 18px, gray/low-contrast text, missing dark mode, missing landmarks, missing skip link, and a missing source mirror. Treat errors as blocking.

## Rendering from a markdown file

When given a markdown file (e.g. by the `capture-findings` skill) and asked to produce an HTML artifact:
1. Read the markdown and the references.
2. Map its structure to the artifact: the H1 becomes the title, `##`/`###` become sections, lists/tables/links carry over as real HTML elements.
3. Choose navigation per `references/navigation-patterns.md` (long-form markdown → sidebar TOC).
4. Embed the **markdown verbatim** in the `<script type="text/markdown" id="artifact-source">` mirror — it is already the canonical source.
5. Apply brand, light+dark, and all design rules. Validate and fix.
6. Write the HTML next to the markdown (same folder, same base name) unless a path was specified.

## Applying the skill to an existing .html file

When the user hands you an existing artifact and asks to apply this skill:
1. Read the file and the references.
2. Preserve all content and meaning. This is a presentation/structure upgrade, not a rewrite of substance.
3. Bring it up to every rule above: bump fonts, kill grays, add light+dark + toggle, add navigation, add skip link + landmarks, add the source mirror.
4. Validate and fix.

## Memory

After a session, write to `memory.md` when the user corrects how an artifact was built (spacing, color, a layout choice, a missing affordance) or when a technique worked unusually well. Write brand/theme preferences (accent color, font choice, density) to `brand.md` instead. Do not record anything already covered in the references or generic advice — only real, applicable lessons.
