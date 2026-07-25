# Design rules

The hard rules for every HTML artifact. The validator (`scripts/validate_artifact.py`) checks the mechanical ones; this file is the source of truth.

## Contents
- Type scale (font sizes)
- Page frame (the shell)
- Composition (components, not page templates)
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
- Measure: cap *prose* (paragraphs, list items, blockquotes) at ~70–75ch for readability. This cap applies to text only — **components** (tables, comparison matrices, diagrams, diffs, stat-card rows) span the full content width of the shell.

## Page frame (the shell)

`assets/shell.html` is the page scaffold every composed artifact starts from: a centered container capped at **1600px**, a 260px sticky sidebar TOC, and a fluid content column. Wide pages are the point — use the width for components, not for longer text lines (see the measure rule above).

## Composition (components, not page templates)

Pages are **composed** from `assets/components/*.html` fragments, chosen per content block via `references/components-catalog.md`:

- Each component file holds one pattern: a contract comment (when/when-not/schema/variants), its HTML, its scoped CSS, and its JS if any.
- Paste component CSS into the shell's `/* == COMPONENT STYLES == */` slot, component HTML into sections, and component JS before the scrollspy script. Component CSS is class-prefix-scoped, so fragments never collide.
- One page mixes as many components as the content needs — a primer can be sections + a comparison matrix + an excalidraw diagram + a data table. Don't force the whole page into one shape.
- If the WHOLE artifact is a single interactive tool (deck, triage board, flag editor, prompt tuner), use a page pattern from `assets/patterns/` instead of composing.
- Invented a genuinely reusable block? Add it as a candidate component (see "Growing the library" in SKILL.md).

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

Use **semantic** custom-property names (shadcn/ui-style) and theme them — never name a token after its color (no `--green`, no `--clay`):

```
--background          page background
--foreground          primary text (high contrast on --background)
--card                cards / panels (distinct from --background)
--card-foreground     text on cards
--muted               subtle fill / tinted surface
--muted-foreground    secondary text (still ≥ 4.5:1, NOT gray)
--border              borders / dividers
--primary             brand accent / action color (from brand.md)
--primary-foreground  text on --primary
--accent              accent-tinted background
--accent-foreground   text on --accent
--secondary           secondary accent
--code-bg / --code-fg                  code surface / base code text — BOTH follow the theme
--code-comment / -keyword / -string / -number / -fn   syntax colors — follow the theme (dark on light, bright on dark)
--inverse / --inverse-foreground       fixed-dark surface + light text (dark buttons, inverted slides) — does NOT flip
--success / --warning / --destructive  status colors (badges, diff add/del)
```

Surfaces must be visibly distinct from the page background while keeping text contrast high in both themes.

**The surface model is not optional — the page is never pure white.** Cards/panels are `--card` (white) and sit on a `--background` that is a step darker, so they visibly lift off the page:

```
                    light            dark
--background        #f7f7f5  ← off-white, NOT #ffffff
--card              #ffffff          #1d2126
--foreground        #1a1d21          #f2f3f4
--muted-foreground  #33383f          #cdd2d8
--border            #d9d8d4          #2c323a
--primary           #1c6b46          #5bbd8a
```

A common failure is setting `--background` and `--card` both to white — then cards disappear into the page. Always give `--background` an off-white (light) / slightly-elevated-dark (dark) value distinct from `--card`, and give cards a visible `--border`.

**Code blocks FOLLOW the theme — light surface + dark syntax in light mode, dark surface + bright syntax in dark mode.** The surface is `--code-bg` (off-white `#f1f1ee` light / near-black `#16191d` dark), base text is `--code-fg`, and syntax pulls from `--code-keyword` / `--code-string` / `--code-comment` / `--code-number` / `--code-fn` — *all of which flip* between themes. This is the rule's most common failure mode in two directions:

- **Don't pin code to a fixed-dark surface.** A dark code panel sitting in a light page reads as "not following the light theme." Let `--code-bg`/`--code-fg` flip.
- **Don't hardcode light hex for code text** (e.g. `color:#E8E6DE` on `pre`, or `.fn{color:#C9B98A}`). Those vanish on the light panel in light mode. Route base text through `--code-fg` and identifiers through `--code-fn`.
- **Don't reuse a non-code-token surface color as text** (e.g. `color:var(--muted)`), and **don't leave `--code-bg` undefined** — an undefined `fill:var(--code-bg)` renders **black** (this is what made SVG boxes black; see "Surfaces" — also applies to `--card`).

The templates wire syntax classes (`.kw/.fn/.str/.cm/.num`) to the `--code-*` tokens and, where a code panel re-pins inherited tokens, pin them to the *themed* `--code-*` values so a code block nested in a card still resolves correctly. The validator cannot resolve a code block's background, so **check code contrast by eye in both themes.**

**Intentionally-dark surfaces** (dark "primary" buttons, inverted hero slides, a dark preview stage) are the exception — they should stay dark in *both* themes. Use `--inverse` (surface) + `--inverse-foreground` (text) for those, never `--code-bg` (which now flips) and never `--card`/theme inks.

## Light + dark theming

Ship **both** palettes in one file, **auto-following the OS setting — no toggle button**:

```css
:root { /* light palette */ }
@media (prefers-color-scheme: dark) { :root { /* dark palette */ } }
```

- Theme switches automatically with `prefers-color-scheme`. Do **not** add a manual toggle, a `[data-theme]` override, or any `localStorage` theme persistence — it's deliberately dropped to keep artifacts simple.
- In dark mode, light near-white secondary text is correct and is *not* a "gray text" violation — the no-gray rule targets low-contrast mid-grays on light backgrounds.
- Pull `--accent` and the font stack from `brand.md`.

## Accessibility and keyboard (recommended, not required)

These are **nice-to-have**, not hard requirements — the validator reports them as warnings, never errors. Include them when they're cheap (the generic scaffold already does); don't contort a purpose-built layout to satisfy them.

- A **skip link** to `#main` (an invisible link, revealed on focus, that lets keyboard users jump past the nav). Good to have; optional.
- Visible focus ring on interactive elements: a clear `:focus-visible` outline. If you set `outline:none`, give it a visible replacement.
- Prefer real `<button>` and `<a>` for interactions; tabs follow the ARIA tabs pattern (see navigation-patterns.md).
- Honor `prefers-reduced-motion`: gate smooth-scroll and transitions behind it.
- Respect zoom: use `rem`/`px` sensibly; never disable user scaling.

The **hard** requirements that are never relaxed are the readability ones: largish text (type scale), high contrast / no-gray, a single self-contained file, auto light+dark, and the agent-readable source mirror.

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

## Generation-time pitfalls (QA every output)

The templates are correct, but *adapting* them re-introduces these bugs — and `validate_artifact.py` already catches the hard rules automatically. A **simple content/document artifact is self-contained static HTML and needs no browser check** — opening the file is enough. But the pitfalls below only surface when you open an **interactive or diagram** artifact, so for those **open the file in a browser** (`open <file>.html` — never spin up a web server) and check both light and dark before declaring done (flip `prefers-color-scheme`, don't just read the code).

- **Quotes — get the context right (two different rules):**
  - *Inside `<script>` JS strings:* an apostrophe in content (`'You've connected'`) inside a single-quoted string is a syntax error that kills the *entire* script — every handler silently stops. Use double quotes (`"You're set"`) or escape (`\'`).
  - *Inside inline HTML event attributes* (`onclick="fn('Team')"`): the attribute is already double-quoted, so use **single** quotes for the JS string args. Do **NOT** backslash-escape (`onclick="fn(\"Team\")"` makes the browser end the attribute early and silently disables the handler). This is a common over-correction of the rule above.
  - After generating, check the console for errors and confirm handlers actually fire.
- **No blocking dialogs.** Never use `alert()` / `confirm()` / `prompt()` — they freeze the page (and any automated QA). Show status inline instead.
- **Keep interaction indices consistent.** In multi-screen/step flows, the index you pass to a handler (`goToScreen(n)`) must match how elements are identified (`#screen-n`) and how the step indicator is addressed (0- vs 1-based). An off-by-one advances the dots but shows the wrong screen — only visible when you click through.
- **Re-space diagrams and flowcharts when you change them.** Adding a node, widening a box, or inserting a step shifts everything below it — boxes overlap, arrows cross labels. After editing SVG geometry, verify no shapes overlap and no arrow passes through a box. Route feedback/return arrows in their own clear lane (don't let two curves converge or cross).
- **Define every token you reference.** `fill:var(--code-bg)` or `background:var(--card)` with the token *undefined* renders **black** / transparent — not a fallback. Confirm `--card`, `--code-bg`, `--inverse` etc. exist in `:root`.
- **Interactions must actually work.** Click through every button/flow you add; a prototype that doesn't advance is worse than a static page.
- **Don't drive navigation through mandatory scroll-snap.** `scroll-snap-type: y mandatory` + `scroll-snap-stop: always` fights `scrollIntoView()`/`scrollTo()` and can strand the view on slide 1 while the counter advances. For slide decks / step flows, show one panel at a time with a class toggle (`.slide.active{display:flex}`, others `display:none`) — robust and theme-agnostic.

## The polish pass (before declaring done)

After the artifact validates, take one final pass over it as a **reader**, not a builder. The goal is cohesion, not more content — if the instinct is to add another component, stop and instead make what is already there more of a piece. This pass is where "correct" becomes "crafted":

- **Hierarchy:** exactly one loudest element per screenful. If the tldr-card, three callouts, and a highlighted matrix all shout at once, demote the callouts.
- **Rhythm:** section gaps consistent; no two components cramped together without their margins; no headings stacked without intervening prose.
- **Alignment:** cards in a row read as a set; stat and chart numerals stay tabular; table columns line up.
- **Fit:** nothing overflows, overlaps, or clips — diagram labels inside their shapes, chart axis labels inside the plot, inline SVGs sized deliberately (explicit width/height, not stretched).
- **Weight balance:** the page shouldn't be all chrome — if folds, callouts, and cards outnumber plain reading flow roughly 3:1, promote some content back to prose.
- Read the page once in **each theme**. The "someone labored over this" impression comes from this pass, not from more features.
