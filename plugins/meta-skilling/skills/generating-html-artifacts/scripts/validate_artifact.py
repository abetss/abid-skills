#!/usr/bin/env python3
"""Heuristic validator for HTML artifacts produced by the generating-html-artifacts skill.

Run, don't read:  python scripts/validate_artifact.py path/to/file.html

Checks the mechanical rules from references/design-rules.md. It is heuristic — it
parses inline CSS with regex and cannot resolve the full cascade, so it errs toward
flagging things for human review rather than silently passing. Exit code is non-zero
if any ERROR is found.
"""
import html as html_mod
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}")
        sys.exit(2)


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def is_gray(rgb):
    """Near-neutral (R~=G~=B) at mid luminance: the disallowed 'gray text'."""
    r, g, b = rgb
    spread = max(rgb) - min(rgb)
    total = r + g + b
    near_neutral = spread <= 18
    # exclude near-black ink (dark) and near-white (fine on dark bg)
    mid_luminance = 150 <= total <= 600
    return near_neutral and mid_luminance


def demo_signatures():
    """Distinctive demo phrases from the component/pattern fragments.

    Each fragment ships with sample content the generator must replace. Phrases of
    4+ words from that sample content are distinctive enough that finding one in a
    real artifact means demo placeholder text leaked through.
    """
    sigs = {}
    for folder in ("assets/components", "assets/patterns"):
        for frag in sorted((SKILL_ROOT / folder).glob("*.html")):
            text = frag.read_text(encoding="utf-8")
            text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
            text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
            text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
            text = re.sub(r"<[^>]+>", "\n", text)
            text = html_mod.unescape(text)
            phrases = set()
            for line in text.splitlines():
                norm = " ".join(line.split())
                words = [w for w in norm.split() if re.search(r"[a-zA-Z0-9]", w)]
                if len(words) >= 4 and len(norm) >= 20:
                    phrases.add(norm)
            if phrases:
                sigs[frag.name] = phrases
    return sigs


def visible_text(html):
    """Artifact text with scripts (incl. the source mirror), styles and tags removed."""
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html_mod.unescape(text).split())


def main():
    if len(sys.argv) != 2:
        print("usage: validate_artifact.py <file.html>")
        sys.exit(2)
    path = sys.argv[1]
    html = read(path)
    low = html.lower()
    errors, warnings = [], []

    # --- structure ---
    if "<!doctype html>" not in low:
        errors.append("Missing <!DOCTYPE html>.")
    if not re.search(r"<html[^>]*\blang=", low):
        warnings.append("Missing lang attribute on <html>.")
    # Landmarks and a single <h1> are accessibility niceties, not hard requirements —
    # report them as warnings so purpose-built layouts (decks, boards) aren't blocked.
    for tag, label in [("<main", "<main> landmark"),
                       ("<nav", "<nav> landmark"),
                       ("<header", "<header> landmark"),
                       ("<footer", "<footer> landmark")]:
        if tag not in low:
            warnings.append(f"Missing {label} (accessibility nicety).")
    if low.count("<h1") == 0:
        warnings.append("No <h1> found — most artifacts should have one title.")
    elif low.count("<h1") > 1:
        warnings.append(f"{low.count('<h1')} <h1> elements — usually there should be one.")

    # --- self-contained ---
    ext_urls = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)', low) + \
               re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)', low)
    if ext_urls:
        # Excalidraw canvas embeds (references/excalidraw-diagrams.md) may load their
        # renderer from pinned CDNs as progressive enhancement, with an ASCII fallback.
        excalidraw_ok = "excalidraw-scene" in low and all(
            re.match(r'https://(esm\.sh|cdn\.jsdelivr\.net/npm/@excalidraw)/', u)
            for u in ext_urls)
        if excalidraw_ok:
            warnings.append("Excalidraw embed uses CDN resources — confirm the ASCII fallback renders offline.")
        else:
            errors.append("External CDN resource referenced — artifact must be self-contained.")
    if "@import url(http" in low.replace(" ", ""):
        errors.append("CSS @import of a remote URL — artifact must be self-contained.")

    # --- dark mode (auto-only; no toggle) ---
    if "prefers-color-scheme: dark" not in low and "prefers-color-scheme:dark" not in low:
        errors.append("No 'prefers-color-scheme: dark' — ship light AND dark palettes (auto, no toggle).")

    # --- skip link (accessibility nicety) ---
    if not re.search(r'href=["\']#(main|content|skip)', low):
        warnings.append("No skip link to #main found (accessibility nicety).")

    # --- source mirror ---
    if 'type="text/markdown"' not in low and "type='text/markdown'" not in low:
        errors.append('Missing agent-readable source mirror (<script type="text/markdown">).')

    # --- focus handling ---
    if re.search(r"outline\s*:\s*none", low) and ":focus-visible" not in low:
        warnings.append("outline:none used without a :focus-visible replacement — check focus rings.")

    # --- font sizes ---
    sizes = []
    for m in re.finditer(r"font-size\s*:\s*([0-9.]+)px", low):
        sizes.append(float(m.group(1)))
    tiny = [s for s in sizes if s < 14]
    smallish = sorted({s for s in sizes if 14 <= s < 18})
    if tiny:
        errors.append(f"font-size below 14px found: {sorted(set(tiny))} — too small for any text.")
    if smallish:
        warnings.append(f"font-size 14–17px found: {smallish} — OK only for UI chrome (badges/labels), "
                        "never for body or content text (body must be >=18px).")
    # body specifically
    bm = re.search(r"body\s*\{[^}]*?font-size\s*:\s*([0-9.]+)px", low, re.S)
    if bm:
        if float(bm.group(1)) < 18:
            errors.append(f"body font-size is {bm.group(1)}px — must be >=18px.")
    else:
        warnings.append("Could not find an explicit body font-size — confirm body text is >=18px.")

    # --- undefined CSS custom properties (an undefined var(--x) renders BLACK/transparent) ---
    # Scan markup + styles only; the markdown source mirror may legitimately quote CSS.
    code_zones = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    refs = set()
    for m in re.finditer(r"var\(\s*(--[\w-]+)\s*(\)|,)", code_zones):
        if m.group(2) == ")":  # no fallback — an undefined ref renders garbage
            refs.add(m.group(1))
    defs = set(re.findall(r"(--[\w-]+)\s*:", code_zones))
    undefined = sorted(refs - defs)
    if undefined:
        errors.append(f"Custom properties used via var() but never defined: {', '.join(undefined)} — "
                      "undefined custom properties render as black/transparent, not a fallback.")

    # --- blocking dialogs (freeze the page + any automated QA) ---
    dialogs = sorted({m for m in re.findall(r"\b(alert|confirm|prompt)\s*\(", html)})
    if dialogs:
        warnings.append(f"Blocking dialog(s) used ({', '.join(d + '()' for d in dialogs)}) — "
                        "replace with inline UI; they freeze the page and break QA.")

    # --- gray text ---
    grays = set()
    for m in re.finditer(r"(?:^|[^-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})", html):
        rgb = hex_to_rgb(m.group(1))
        if rgb and is_gray(rgb):
            grays.add(m.group(1))
    if grays:
        warnings.append(f"Possible gray text colors (verify contrast / replace with darker ink): {sorted(grays)}")

    # --- duplicate ids (break TOC links, scrollspy, aria) ---
    ids = re.findall(r'\bid\s*=\s*"([^"]+)"', html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errors.append(f"Duplicate id attribute(s): {', '.join(dupes)} — ids must be unique "
                      "(give each diagram SVG and component instance its own prefix).")

    # --- in-page navigation integrity ---
    anchors = sorted(set(re.findall(r'href\s*=\s*"#([^"]+)"', low)))
    broken = [a for a in anchors if not re.search(r'\bid\s*=\s*"' + re.escape(a) + r'"', html)]
    if broken:
        errors.append(f"In-page link(s) point to missing ids: {', '.join('#' + b for b in broken)}.")
    if 'class="toc"' in low:
        section_ids = set(re.findall(r"<section[^>]*\bid\s*=\s*\"([^\"]+)\"", html))
        unlinked = sorted(s for s in section_ids if s not in anchors)
        if unlinked:
            warnings.append(f"Sections not reachable from any in-page link: {', '.join(unlinked)} "
                            "— add them to the TOC.")

    # --- demo placeholder leak (skipped in the showcase page itself) ---
    if "<!-- showcase: demo content intentional -->" not in html:
        vis = visible_text(html)
        for frag_name, phrases in demo_signatures().items():
            leaked = sorted(p for p in phrases if p in vis)
            if leaked:
                errors.append(f"Demo placeholder text from {frag_name} leaked into the artifact: "
                              f"\"{leaked[0][:80]}\" — replace every sample with real content.")

    # --- report ---
    print(f"Validating: {path}\n")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
        print()
    if not errors and not warnings:
        print("Clean — no issues found.")
    elif not errors:
        print("No errors. Review warnings above.")
    print()
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
