#!/usr/bin/env python3
"""Pre-render the ```mermaid``` code blocks in a markdown file to inline-ready SVG.

Run, don't read:
    python scripts/render_diagrams.py path/to/source.md

Why this exists: artifacts must be a single self-contained file that works offline by
double-click, so we cannot load Mermaid from a CDN at view time. Instead we render every
diagram to SVG *now* (via mermaid-cli, fetched on demand with `npx`) and inline the result.
Each diagram is rendered twice — once for the light palette, once for the dark — because a
single SVG bakes in its colors and would be unreadable in the other theme. The two SVGs are
wrapped in one <figure> that shows the right one per theme (CSS in assets/template.html).

Output: a sibling folder `<base>.diagrams/` holding one HTML fragment per block
(`diagram-1.html`, `diagram-2.html`, …) plus a `manifest.txt` mapping each fragment to the
first line of its mermaid source so you know where to inline it. Inline fragment N where the
Nth ```mermaid``` block sits in the document, then drop the raw block from the visible HTML
(keep it in the markdown source + the source-mirror script — it stays human-readable and
re-renderable).

Requires Node (`npx`). mermaid-cli is fetched automatically on first run via `npx -y`.
Brand colors default to brand.md; override with flags if the artifact uses a different accent.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

# Brand-tuned Mermaid "base" theme variables (see brand.md). The base theme is the only
# fully customizable one, so we drive both palettes through themeVariables for an on-brand look.
# Deliberately NOT overriding fontFamily: mermaid-cli pre-computes every node's box size with its
# own font, so swapping in a wider font here makes labels overflow and clip ("USER" -> "USEF").
# We let it keep its default font (web-safe) so the sizing it bakes in stays correct on screen.
LIGHT_VARS = {
    "primaryColor": "#e6f1ec", "primaryBorderColor": "#1c6b46", "primaryTextColor": "#10472d",
    "lineColor": "#33383f", "secondaryColor": "#ffffff", "tertiaryColor": "#f7f7f5",
}
DARK_VARS = {
    "primaryColor": "#16352a", "primaryBorderColor": "#5bbd8a", "primaryTextColor": "#9fe3c0",
    "lineColor": "#cdd2d8", "secondaryColor": "#1d2126", "tertiaryColor": "#14171a",
}

MERMAID_BLOCK = re.compile(r"^[ \t]*```+[ \t]*mermaid[ \t]*\n(.*?)^[ \t]*```+[ \t]*$",
                           re.DOTALL | re.MULTILINE)


def config_json(theme_vars):
    import json
    return json.dumps({"theme": "base", "themeVariables": theme_vars})


def normalize_svg(svg, slug):
    """Make one mermaid SVG safe to inline alongside others and to pass the artifact validator."""
    # Strip any XML prolog / doctype so it drops straight into the body.
    svg = re.sub(r"^\s*<\?xml.*?\?>\s*", "", svg, flags=re.DOTALL)
    svg = re.sub(r"^\s*<!DOCTYPE[^>]*>\s*", "", svg, flags=re.DOTALL)
    # Mermaid namespaces every internal id under "my-svg" (markers, gradients) and references
    # them via url(#my-svg_...). Inlining two SVGs that share these ids cross-wires their
    # arrowheads. Rewrite the whole namespace to a per-fragment slug to keep refs intact.
    svg = svg.replace("my-svg", slug)
    # The validator errors on any font-size < 14px; mermaid emits 12px on edge labels. Floor it.
    svg = re.sub(r"(font-size\s*:\s*)([0-9.]+)(px)",
                 lambda m: f"{m.group(1)}{max(14.0, float(m.group(2))):g}{m.group(3)}", svg)
    # Let it scale down inside its figure instead of overflowing.
    svg = svg.replace('style="max-width:', 'style="width:100%;height:auto;max-width:', 1)
    # mermaid sizes each label's foreignObject with its own (headless) font; a wider viewer
    # font would clip the text ("USER" -> "USEF"). Let the centered labels spill instead.
    style = ("<style>foreignObject{overflow:visible}"
             ".nodeLabel,.edgeLabel,.entityLabel{white-space:nowrap}</style>")
    svg = re.sub(r"(<svg\b[^>]*>)", r"\1" + style, svg, count=1)
    return svg.strip()


def render_theme(blocks_md, theme_vars, workdir, tag):
    """Render all blocks for one theme in a single mermaid-cli launch. Returns list of SVGs."""
    in_md = os.path.join(workdir, f"in-{tag}.md")
    out_md = os.path.join(workdir, f"out-{tag}.md")
    cfg = os.path.join(workdir, f"cfg-{tag}.json")
    with open(in_md, "w", encoding="utf-8") as f:
        f.write(blocks_md)
    with open(cfg, "w", encoding="utf-8") as f:
        f.write(config_json(theme_vars))
    cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", in_md, "-o", out_md,
           "-c", cfg, "-b", "transparent"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        sys.exit("ERROR: `npx` not found. Install Node.js to render Mermaid diagrams.")
    except subprocess.TimeoutExpired:
        sys.exit("ERROR: mermaid-cli timed out (>600s).")
    if res.returncode != 0:
        sys.stderr.write(res.stdout + "\n" + res.stderr + "\n")
        sys.exit(f"ERROR: mermaid-cli failed for the {tag} render. Fix the diagram syntax above.")
    # mermaid-cli writes out-<tag>-1.svg, out-<tag>-2.svg, … in block order.
    svgs = []
    i = 1
    while True:
        p = os.path.join(workdir, f"out-{tag}-{i}.svg")
        if not os.path.exists(p):
            break
        with open(p, encoding="utf-8") as f:
            svgs.append(f.read())
        i += 1
    return svgs


def main():
    ap = argparse.ArgumentParser(description="Pre-render mermaid blocks to inline dual-theme SVG.")
    ap.add_argument("markdown", help="path to the markdown source file")
    ap.add_argument("--light", action="append", default=[], metavar="KEY=HEX",
                    help="override a light themeVariable, e.g. primaryBorderColor=#1c6b46")
    ap.add_argument("--dark", action="append", default=[], metavar="KEY=HEX",
                    help="override a dark themeVariable")
    args = ap.parse_args()

    for kv in args.light:
        k, _, v = kv.partition("=")
        LIGHT_VARS[k.strip()] = v.strip()
    for kv in args.dark:
        k, _, v = kv.partition("=")
        DARK_VARS[k.strip()] = v.strip()

    if not os.path.exists(args.markdown):
        sys.exit(f"ERROR: file not found: {args.markdown}")
    with open(args.markdown, encoding="utf-8") as f:
        md = f.read()

    blocks = [m.group(1).strip() for m in MERMAID_BLOCK.finditer(md)]
    if not blocks:
        print("No ```mermaid``` blocks found — nothing to render.")
        return

    # One combined markdown per theme → one mermaid-cli launch per theme, not one per diagram.
    blocks_md = "\n\n".join(f"```mermaid\n{b}\n```" for b in blocks)

    with tempfile.TemporaryDirectory() as workdir:
        print(f"Rendering {len(blocks)} diagram(s) in light + dark themes…")
        light_svgs = render_theme(blocks_md, LIGHT_VARS, workdir, "light")
        dark_svgs = render_theme(blocks_md, DARK_VARS, workdir, "dark")

    if not (len(light_svgs) == len(dark_svgs) == len(blocks)):
        sys.exit(f"ERROR: expected {len(blocks)} SVGs per theme, got "
                 f"{len(light_svgs)} light / {len(dark_svgs)} dark.")

    base = os.path.splitext(os.path.basename(args.markdown))[0]
    out_dir = os.path.join(os.path.dirname(os.path.abspath(args.markdown)), f"{base}.diagrams")
    os.makedirs(out_dir, exist_ok=True)

    manifest = []
    for n, (lsvg, dsvg, src) in enumerate(zip(light_svgs, dark_svgs, blocks), 1):
        light = normalize_svg(lsvg, f"d{n}l")
        dark = normalize_svg(dsvg, f"d{n}d")
        fragment = (
            f'<figure class="diagram" role="group" aria-label="diagram {n}">\n'
            f'  <div class="diagram-svg diagram-light">{light}</div>\n'
            f'  <div class="diagram-svg diagram-dark" aria-hidden="true">{dark}</div>\n'
            f'</figure>\n'
        )
        frag_path = os.path.join(out_dir, f"diagram-{n}.html")
        with open(frag_path, "w", encoding="utf-8") as f:
            f.write(fragment)
        first_line = src.splitlines()[0].strip() if src.splitlines() else "(empty)"
        manifest.append(f"diagram-{n}.html  <-  ```mermaid``` block {n}: {first_line}")

    with open(os.path.join(out_dir, "manifest.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")

    print(f"\nWrote {len(blocks)} fragment(s) to {out_dir}/")
    print("Inline each fragment where its mermaid block sits, then remove the raw block")
    print("from the visible HTML (keep it in the source mirror). Mapping:\n")
    print("\n".join("  " + m for m in manifest))


if __name__ == "__main__":
    main()
