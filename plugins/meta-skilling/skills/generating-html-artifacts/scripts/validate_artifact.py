#!/usr/bin/env python3
"""Heuristic validator for HTML artifacts produced by the generating-html-artifacts skill.

Run, don't read:  python scripts/validate_artifact.py path/to/file.html

Checks the mechanical rules from references/design-rules.md. It is heuristic — it
parses inline CSS with regex and cannot resolve the full cascade, so it errs toward
flagging things for human review rather than silently passing. Exit code is non-zero
if any ERROR is found.
"""
import re
import sys


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
    for tag, label in [("<main", "<main> landmark"),
                       ("<nav", "<nav> landmark"),
                       ("<header", "<header> landmark"),
                       ("<footer", "<footer> landmark")]:
        if tag not in low:
            errors.append(f"Missing {label}.")
    if low.count("<h1") == 0:
        errors.append("No <h1> found.")
    elif low.count("<h1") > 1:
        warnings.append(f"{low.count('<h1')} <h1> elements — there should be exactly one.")

    # --- self-contained ---
    if re.search(r'<link[^>]+href=["\']https?://', low) or re.search(r'<script[^>]+src=["\']https?://', low):
        errors.append("External CDN resource referenced — artifact must be self-contained.")
    if "@import url(http" in low.replace(" ", ""):
        errors.append("CSS @import of a remote URL — artifact must be self-contained.")

    # --- dark mode ---
    if "prefers-color-scheme: dark" not in low and "prefers-color-scheme:dark" not in low:
        errors.append("No 'prefers-color-scheme: dark' — ship light AND dark palettes.")
    if "data-theme" not in low:
        warnings.append("No [data-theme] override found — the manual theme toggle may be missing.")

    # --- skip link ---
    if not re.search(r'href=["\']#(main|content|skip)', low):
        warnings.append("No skip link to #main found.")

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

    # --- gray text ---
    grays = set()
    for m in re.finditer(r"(?:^|[^-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})", html):
        rgb = hex_to_rgb(m.group(1))
        if rgb and is_gray(rgb):
            grays.add(m.group(1))
    if grays:
        warnings.append(f"Possible gray text colors (verify contrast / replace with darker ink): {sorted(grays)}")

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
