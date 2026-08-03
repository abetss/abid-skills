# Candidate components

Not part of the live catalog yet. Promoted to `references/components-catalog.md` and
`assets/components/` only on explicit human confirmation (see "Growing the library" in SKILL.md).

---

### chart-frame
- **File:** `assets/components/candidates/01-chart-frame.html`
- **It is:** a fixed-light (`#ffffff`, never themed) frame + horizontal-scroll wrapper for
  embedding a pre-rendered chart SVG (Vega-Lite, D3, matplotlib exports — anything with a baked-in
  white background and dark text) inside the standard `figure` component.
- **When to use:** the source references an already-rendered chart image/SVG that cannot be
  re-themed (its colors are baked in, not driven by CSS custom properties), and the artifact must
  stay legible in dark mode without the page's dark background bleeding around a white chart.
- **Avoid when:** the chart is authored with theme tokens itself (e.g. the existing `chart`
  component's inline SVG already uses `var(--foreground)`/`var(--border)` and themes on its own —
  no fixed-light frame needed).
- **Schema:** `.c-figure > .chart-frame > .chart-scroll > <svg>` (raw inlined SVG, own
  width/height/viewBox) `+ figcaption.c-figure-cap` for the numbered caption.
- **First used:** SR&ED FY2026 evidence report (`a-works/operations/260727-sred-jira-backfill/SRED-FY2026-REPORT.html`) — four Vega-Lite chart SVGs (timeline, tickets-by-month, commits, core-support pie) inlined into a document meant to render correctly for a reader in dark mode, per explicit source-brief instruction to keep a light surface behind each chart.
