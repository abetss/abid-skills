# Design rules

The hard rules for every HTML artifact. The validator (`scripts/validate_artifact.py`) checks the mechanical ones; this file is the source of truth.

## Contents
- Type scale (font sizes)
- Spacing scale
- Contrast and the no-gray rule
- Color and surfaces
- Light + dark theming
- Accessibility and keyboard
- Semantic structure and the agent-readable source mirror

## Type scale

Base body text is **18px** minimum. Use a modest scale; do not go below the listed minimums.

| Role | Size | Notes |
|---|---|---|
| Body / paragraphs / list content | 18px | the floor for anything you read in sentences |
| Lead / intro paragraph | 20–22px | |
| Secondary (captions, "why" notes, card values) | 16–17px | still high-contrast, never gray |
| h3 | 20–22px | |
| h2 | 26–30px | |
| h1 | 36–44px | one per page |
| UI chrome (badges, tab labels, uppercase eyebrows) | 14–16px | the only place below 16px is allowed |

- Line-height: 1.5–1.75 for body, ~1.15–1.25 for large headings.
- Measure: cap body text at ~65–75ch for readability (`max-width` on the text column).

## Spacing scale

Use an 8px base scale: **4, 8, 16, 24, 32, 48, 64, 96**. Prefer the larger end — artifacts should feel spacious.

- Section-to-section gap: 48–64px.
- Card / panel padding: 20–28px.
- Page padding: 24px mobile, 48–72px desktop.
- Don't crowd: if two blocks touch, add space before adding a border.

## Contrast and the no-gray rule

- Every text/background pair must meet **WCAG 2.2 AA**: ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥ 24px, or ≥ 18.66px bold). Aim for **7:1** on body text.
- **No gray text.** "Gray" = a near-neutral color (R≈G≈B) at mid luminance, e.g. `#6b7280`, `#9ca3af`, `#888`. These fail contrast and read as disabled. For secondary text use a *darker ink* that still meets 4.5:1 — e.g. light mode `#33383f` on white (~10:1), dark mode a light near-white on the dark surface.
- Near-black inks with a slight hue (e.g. `#1a1d21`) are fine — they are not "gray text", they are ink.
- Don't convey meaning by color alone; pair color with text or shape (badges have labels, not just hues).

## Color and surfaces

Define a small set of CSS custom properties and theme them:

```
--bg          page background
--surface     cards / panels (distinct from --bg)
--ink         primary text (high contrast on --bg and --surface)
--ink-2       secondary text (still ≥ 4.5:1, NOT gray)
--line        borders / dividers
--accent      brand accent (from brand.md)
--accent-soft accent-tinted background
--accent-ink  text color for use on --accent-soft (must meet contrast)
```

Surfaces must be visibly distinct from the page background while keeping ink contrast high in both.

## Light + dark theming

Ship **both** palettes in one file:

```css
:root { /* light palette */ }
@media (prefers-color-scheme: dark) { :root { /* dark palette */ } }
[data-theme="light"] { /* light palette (manual override) */ }
[data-theme="dark"]  { /* dark palette (manual override) */ }
```

- A visible toggle button sets `document.documentElement.dataset.theme` and persists to `localStorage`; on load, restore it.
- In dark mode, light near-white secondary text is correct and is *not* a "gray text" violation — the no-gray rule targets low-contrast mid-grays on light backgrounds.
- Pull `--accent` and the font stack from `brand.md`.

## Accessibility and keyboard

- First focusable element is a **skip link** to `#main` (visually hidden until focused).
- Visible focus ring on every interactive element: a clear `:focus-visible` outline. Never `outline:none` without an equally visible replacement.
- Use real `<button>` and `<a>` for interactions; tabs follow the ARIA tabs pattern (see navigation-patterns.md).
- Honor `prefers-reduced-motion`: gate smooth-scroll and transitions behind it.
- Respect zoom: use `rem`/`px` sensibly; never disable user scaling.

## Semantic structure and the agent-readable source mirror

- Landmarks: `<header>`, `<nav>`, `<main id="main">`, `<footer>`. One `<h1>`; heading levels in order (no skipping).
- Real lists (`<ul>`/`<ol>`) and real `<table>` for tabular data — never fake them with `<div>`s.
- **Source mirror:** embed the artifact's content as Markdown so agents can read it verbatim:

```html
<script type="text/markdown" id="artifact-source">
# Title
## Section
...the raw content as markdown...
</script>
```

Keep the mirror in sync with the visible content. It is the canonical machine-readable copy.
