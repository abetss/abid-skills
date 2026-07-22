# ANSI / ASCII box diagrams → Excalidraw canvas

When the source markdown contains a **hand-drawn ASCII/ANSI box diagram** (a fenced code
block built from box-drawing characters), do NOT render it as a plain `<pre>` code block.
Convert it into an **Excalidraw diagram** and embed it as an interactive, read-only
Excalidraw canvas in the artifact.

## Detecting an ANSI diagram

A fenced code block (language tag empty, `text`, `ascii`, or `ansi`) counts as an ANSI
diagram when it contains several box-drawing / arrow characters:

```
─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╔ ╗ ╚ ╝ ╭ ╮ ╰ ╯ ▲ ▼ ◄ ► ↑ ↓ ← →
```

Ordinary code blocks (no box-drawing chars) and ```` ```mermaid ```` blocks are NOT ANSI
diagrams — leave them alone (mermaid follows `depth-and-diagrams.md`).

## Workflow

1. **Convert** the ASCII drawing into Excalidraw *shorthand elements* (format below).
   Keep the layout faithful: same boxes, same labels, same flow direction, same grouping.
   Colors come from the palette below — pick by role (input, processing, output, storage…),
   not at random. One `fontSize: 16–20` for labels, 20+ for titles.
2. **If the Excalidraw MCP server is available** (tools like `mcp__excalidraw*read_me` /
   `create_view`): call `read_me` once for the authoritative format reference, then
   `create_view` with your elements JSON to render/validate the diagram. Reuse the exact
   same elements JSON in the HTML embed. If the MCP is not available in this environment,
   skip the preview and embed directly.
3. **Embed** the scene in the artifact with the snippet below: interactive canvas when
   online, original ASCII as the offline fallback.
4. Keep the original ASCII block **verbatim** in the artifact's markdown source mirror
   (it already is — the mirror holds the whole source).

## Element format (shorthand)

Required per element: `type`, `id` (unique string), `x`, `y`, `width`, `height`.
Defaults (omit): `strokeColor: "#1e1e1e"`, `backgroundColor: "transparent"`,
`fillStyle: "solid"`, `strokeWidth: 2`, `roughness: 1`, `opacity: 100`.

- **Rectangle**: `{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }`
  — add `"roundness": { "type": 3 }` for rounded corners.
- **Ellipse / diamond**: same shape with `"type": "ellipse"` / `"diamond"`.
- **Labeled shape (preferred)**: `"label": { "text": "Hello", "fontSize": 20 }` on any
  rectangle/ellipse/diamond — auto-centered, container auto-resizes. No separate text element.
- **Standalone text** (titles/annotations only):
  `{ "type": "text", "id": "t1", "x": 150, "y": 40, "text": "Title", "fontSize": 24 }`
  — `x` is the LEFT edge; to center at `cx`: `x = cx - text.length * fontSize * 0.25`.
- **Arrow**:
  `{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0, "points": [[0,0],[150,0]], "endArrowhead": "arrow" }`
  — `points` are [dx,dy] offsets from x,y; `endArrowhead`: `null | "arrow" | "bar" | "dot" | "triangle"`;
  arrows can also carry `"label": { "text": "…" }`.
- **Arrow bindings** (arrows stick to shapes):
  `"startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] }`,
  `"endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }`
  — fixedPoint: top `[0.5,0]`, bottom `[0.5,1]`, left `[0,0.5]`, right `[1,0.5]`.
- Array order = z-order (first = back).

Layout rules: design for ~800×600; min labeled-box size 120×60; ≥20px gaps; min fontSize
16 (14 only for minor annotations); no emoji in text. Zone rectangles (grouping regions):
a large low-opacity (`opacity: 30–40`) rectangle behind the group plus a small standalone
text label at its top-left.

### Palette

Strokes/accents: blue `#4a9eed`, amber `#f59e0b`, green `#22c55e`, red `#ef4444`,
purple `#8b5cf6`, pink `#ec4899`, cyan `#06b6d4`.
Fills (`backgroundColor` + `fillStyle: "solid"`): light blue `#a5d8ff` (inputs/primary),
light green `#b2f2bb` (success/output), light orange `#ffd8a8` (warning/external),
light purple `#d0bfff` (processing), light red `#ffc9c9` (error), light yellow `#fff3bf`
(notes/decisions), light teal `#c3fae8` (storage/data).
Zones (with `opacity: 30`): blue `#dbe4ff`, purple `#e5dbff`, green `#d3f9d8`.

Do NOT emit the MCP streaming pseudo-elements (`cameraUpdate`, `delete`,
`restoreCheckpoint`) for the HTML embed — the embed filters them out, but they are noise
in the scene JSON. (When calling the MCP's `create_view` for a preview, a leading
`cameraUpdate` is welcome there.)

## Embedding the canvas in the artifact

The embed is **progressive enhancement**: it loads Excalidraw from a CDN (esm.sh +
jsdelivr, pinned versions) and renders a read-only canvas per scene. Offline, each
diagram degrades to the original ASCII block — the artifact never breaks, so this is the
one sanctioned exception to the no-CDN rule (the validator allows exactly these hosts
when a scene block is present).

**Once per page, in `<head>`:**

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@0.18.0/dist/prod/index.css">
<script>window.EXCALIDRAW_ASSET_PATH = "https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@0.18.0/dist/prod/";</script>
<script type="importmap">
{"imports":{
  "react":"https://esm.sh/react@19.0.0",
  "react/jsx-runtime":"https://esm.sh/react@19.0.0/jsx-runtime",
  "react-dom":"https://esm.sh/react-dom@19.0.0",
  "react-dom/client":"https://esm.sh/react-dom@19.0.0/client"}}
</script>
```

**Per diagram, where the ASCII block sat:**

```html
<figure class="excalidraw-diagram">
  <div class="excalidraw-canvas" role="img" aria-label="Diagram: <short description>"></div>
  <button type="button" class="excalidraw-toggle" hidden>Live canvas</button>
  <script type="application/json" class="excalidraw-scene">
  [ …the shorthand elements JSON… ]
  </script>
  <pre class="excalidraw-fallback"><code>…original ASCII block, HTML-escaped…</code></pre>
</figure>
```

**CSS (adapt values to the artifact's tokens):**

```css
.excalidraw-diagram { margin: var(--space-4, 32px) 0; }
.excalidraw-canvas { border: 1px solid var(--border, #d0d0d0); border-radius: var(--radius, 12px); overflow: hidden; display: none; }
.excalidraw-canvas svg { display: block; width: 100%; height: auto; }
.excalidraw-diagram.excalidraw-live .excalidraw-canvas { display: block; }
.excalidraw-diagram.excalidraw-live .excalidraw-fallback { display: none; }
.excalidraw-diagram.excalidraw-live .excalidraw-toggle { display: inline-block; }
.excalidraw-canvas.excalidraw-interactive { height: 480px; }
.excalidraw-canvas.excalidraw-interactive svg { height: 100%; }
.excalidraw-fallback { margin: 0; overflow-x: auto; }
```

**Once per page, before `</body>`:**

```html
<script type="module">
try {
  const React = await import("react");
  const { createRoot } = await import("react-dom/client");
  const E = await import("https://esm.sh/@excalidraw/excalidraw@0.18.0?external=react,react-dom");
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  // Excalidraw's font must be loaded BEFORE convertToExcalidrawElements, or label
  // text is measured with fallback metrics and overflows its shape.
  try { await document.fonts.load("20px Excalifont"); } catch {}
  // convertToExcalidrawElements does NOT grow shapes to fit their labels — measure
  // and widen them ourselves (keeps each shape's center fixed).
  const mctx = document.createElement("canvas").getContext("2d");
  const fitLabels = (raw) => {
    for (const el of raw) {
      if (!el.label || !el.width) continue;
      const fs = el.label.fontSize || 20;
      mctx.font = `${fs}px Excalifont`;
      const needW = Math.max(...el.label.text.split("\n").map(l => mctx.measureText(l).width)) + 64;
      if (needW > el.width) { el.x -= (needW - el.width) / 2; el.width = needW; }
      const needH = el.label.text.split("\n").length * fs * 1.25 + 36;
      if (needH > el.height) { el.y -= (needH - el.height) / 2; el.height = needH; }
    }
    return raw;
  };
  for (const sceneEl of document.querySelectorAll("script.excalidraw-scene")) {
    const fig = sceneEl.closest(".excalidraw-diagram");
    const host = fig.querySelector(".excalidraw-canvas");
    const toggle = fig.querySelector(".excalidraw-toggle");
    try {
      const raw = fitLabels(JSON.parse(sceneEl.textContent));
      const elements = E.convertToExcalidrawElements(
        raw.filter(el => !["cameraUpdate", "delete", "restoreCheckpoint"].includes(el.type)),
        { regenerateIds: false });
      // Default display: inline SVG export (crisp, correct text — this is also how the
      // excalidraw-mcp app renders inline). NOT the <Excalidraw> component, whose canvas
      // text painter clips label glyphs in an embedded context.
      const svg = await E.exportToSvg({ elements, appState: { exportWithDarkMode: dark }, files: null });
      host.appendChild(svg);
      fig.classList.add("excalidraw-live");
      // Optional: swap in the interactive canvas (pan/zoom) on demand.
      let root = null;
      toggle.hidden = false;
      toggle.addEventListener("click", () => {
        if (!root) {
          host.classList.add("excalidraw-interactive");
          host.textContent = "";
          root = createRoot(host);
          root.render(React.createElement(E.Excalidraw, {
            excalidrawAPI: (api) => {
              const fit = () => api.scrollToContent(api.getSceneElements(), { fitToContent: true, viewportZoomFactor: 0.9 });
              requestAnimationFrame(fit);
              setTimeout(fit, 1500);
            },
            initialData: { elements, appState: { viewModeEnabled: true, zenModeEnabled: true, gridSize: null, theme: dark ? "dark" : "light" } },
            viewModeEnabled: true
          }));
          toggle.textContent = "Static image";
        } else {
          root.unmount();
          root = null;
          host.classList.remove("excalidraw-interactive");
          host.textContent = "";
          host.appendChild(svg);
          toggle.textContent = "Live canvas";
        }
      });
    } catch { /* bad scene JSON — ASCII fallback stays visible */ }
  }
} catch { /* offline / CDN unreachable — ASCII fallbacks stay visible */ }
</script>
```

Notes:

- The import map must appear before any `<script type="module">` on the page.
- The scene JSON stays in the DOM (`script.excalidraw-scene`) so agents can extract the
  exact diagram data without parsing the canvas.
- The SVG export follows the OS theme via `exportWithDarkMode`; the interactive canvas
  via `theme`. Custom element colors keep their explicit hex values either way.
- Style `.excalidraw-toggle` like the artifact's other buttons (it is UI chrome, ≥14px) —
  use the artifact's STRONG color token (e.g. `--primary`), not a pale surface tint like
  `--accent`, or the button will look washed out.
- After generating, open the artifact once and check: the SVG diagram renders and matches
  the ASCII original (same boxes/flow/labels), the toggle swaps to the live canvas and
  back, no console errors, and the fallback shows when the network is off.
