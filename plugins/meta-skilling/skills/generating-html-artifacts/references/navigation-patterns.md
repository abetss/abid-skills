# Navigation patterns

How to make artifacts navigable by clicks and by keyboard. Pick per content shape; the two patterns can coexist.

## Contents
- Choosing: sidebar TOC vs tab panels
- Sidebar TOC (with scrollspy)
- Tab panels (ARIA tabs pattern)
- Shared keyboard rules

## Choosing

| Content shape | Pattern |
|---|---|
| Long-form, linear, read top-to-bottom (guides, reports, maps, plans) | **Sidebar TOC** |
| Grouped views you switch between, dashboards, "either/or" sections | **Tab panels** |
| A long doc where one section has sub-views | TOC for the doc, **tabs inside** that section |

Default to a sidebar TOC for documents; reach for tabs when the user is choosing *which* content to see rather than scrolling through all of it.

## Sidebar TOC (with scrollspy)

- A sticky `<nav aria-label="Contents">` beside the content; on narrow screens it moves to the top (static) or collapses into a `<details>`.
- Each link targets a section `id`. Clicking scrolls to it.
- Scrollspy: an `IntersectionObserver` adds `aria-current="true"` to the link for the section in view. Keyboard-safe and cheap.
- Gate `scroll-behavior:smooth` behind `prefers-reduced-motion: no-preference`.

```html
<nav aria-label="Contents" class="toc">
  <a href="#intro" aria-current="true">Intro</a>
  <a href="#setup">Setup</a>
</nav>
<main id="main">
  <section id="intro" aria-labelledby="intro-h"><h2 id="intro-h">Intro</h2>…</section>
</main>
```

## Tab panels (ARIA tabs pattern)

Use the real ARIA pattern — not just styled buttons:

```html
<div class="tabs">
  <div role="tablist" aria-label="Views">
    <button role="tab" id="t1" aria-selected="true"  aria-controls="p1">Overview</button>
    <button role="tab" id="t2" aria-selected="false" aria-controls="p2" tabindex="-1">Detail</button>
  </div>
  <section role="tabpanel" id="p1" aria-labelledby="t1">…</section>
  <section role="tabpanel" id="p2" aria-labelledby="t2" hidden>…</section>
</div>
```

Keyboard behavior (required):
- `Tab` moves into the tablist to the selected tab, then out to the panel — only the active tab is in the tab order (`tabindex="-1"` on the rest).
- `ArrowLeft`/`ArrowRight` move between tabs; `Home`/`End` jump to first/last.
- Activating a tab sets `aria-selected`, shows its panel, and `hidden`s the others.

## Shared keyboard rules

- Skip link to `#main` is the first focusable element.
- Visible `:focus-visible` ring on every nav link, tab, and toggle.
- All navigation must work with keyboard alone; verify by tabbing through before declaring done.
