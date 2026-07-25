#!/usr/bin/env python3
""" Scripted grader for the generating-html-artifacts eval set.

Run, don't read:
  python scripts/grade_artifact.py path/to/file.html check-id [check-id...]
  python scripts/grade_artifact.py path/to/file.html --eval 3 [--out grading.json]

A check-id is one of the registry entries below (e.g. "validator-clean",
"uses-component:timeline", "contains:22:14"). Assertions in evals/evals.json carry
a "check" field when they are scriptable; the rest need an LLM/human grader.

With --eval, every scripted assertion of that eval is graded and the result is
printed (and optionally written as grading.json in the skill-creator format:
{"expectations": [{"text", "passed", "evidence"}]}). Assertions without a
"check" field are listed as pending for the LLM grader.

Exit code is non-zero if any check fails.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = SKILL_ROOT / "scripts" / "validate_artifact.py"
EVALS_JSON = SKILL_ROOT / "evals" / "evals.json"

COMPONENT_MARKERS = {
    "section": 'class="c-section',
    "tldr-card": "c-tldr",
    "callout": "c-callout",
    "details-fold": "c-fold",
    "stat-cards": "c-stats",
    "data-table": "c-table",
    "comparison-matrix": "c-matrix",
    "pros-cons": "c-pc",
    "timeline": "c-tl",
    "steps": "c-steps",
    "code-block": "c-codeblock",
    "diff-viewer": "c-diff",
    "annotated-code": "c-annot",
    "file-tree": "c-ftree",
    "flowchart": "c-flowchart",
    "diagram-excalidraw": "c-diagram-excalidraw",
    "diagram-mermaid": "c-diagram-mermaid",
    "chart": "c-chart",
    "tabs": "c-tabs",
    "glossary": "c-gloss",
    "checklist": "c-check",
    "quote": "c-quote",
    "figure": "c-figure",
}

PATTERN_MARKERS = {
    "slide-deck": "deck-nav",
    "triage-board": 'class="board"',
    "feature-flags": "btn-stack",
    "prompt-tuner": "preview-panel",
}


def check_validator_clean(html, low, path):
    r = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                       capture_output=True, text=True)
    tail = "\n".join(r.stdout.splitlines()[-6:])
    return r.returncode == 0, f"validator exit {r.returncode}; tail: {tail}"


def check_self_contained(html, low, path):
    ext = re.findall(r'<link[^>]+href=["\'](https?://[^"\']+)', low) + \
          re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)', low)
    allowed = [u for u in ext if re.match(r"https://(esm\.sh|cdn\.jsdelivr\.net/npm/@excalidraw)/", u)]
    ok = len(ext) == len(allowed) and (not ext or "excalidraw-scene" in low)
    return ok, f"external urls: {ext or 'none'}"


def check_auto_theme(html, low, path):
    has_media = "prefers-color-scheme: dark" in low.replace(" ", "") or \
                "prefers-color-scheme:dark" in low
    bad = [t for t in ("data-theme", "localstorage") if t in low]
    return has_media and not bad, f"media query: {has_media}; toggle machinery: {bad or 'none'}"


def check_source_mirror(html, low, path):
    m = re.search(r'<script[^>]*type="text/markdown"[^>]*>(.*?)</script>', html, re.S | re.I)
    n = len(m.group(1).strip()) if m else 0
    return n >= 200, f"source mirror content length: {n} chars"


def check_toc(html, low, path):
    m = re.search(r'<nav[^>]*class="toc".*?</nav>', html, re.S | re.I)
    links = len(re.findall(r'href="#', m.group(0))) if m else 0
    return links >= 2, f"toc links: {links}"


def check_toc_subs(html, low, path):
    m = re.search(r'<nav[^>]*class="toc".*?</nav>', html, re.S | re.I)
    subs = len(re.findall(r'class="sub"', m.group(0))) if m else 0
    return subs >= 1, f"toc sub-entries: {subs}"


def check_mermaid_prerendered(html, low, path):
    has_fig = 'class="diagram' in low
    cdn = "mermaid" in " ".join(re.findall(r'<script[^>]+src=["\']([^"\']+)', low)).lower()
    return has_fig and not cdn, f"diagram figure: {has_fig}; mermaid loaded at view time: {cdn}"


def check_excalidraw_embed(html, low, path):
    ok = "excalidraw-scene" in low and "c-diagram-excalidraw-fallback" in low
    return ok, (f"scene: {'excalidraw-scene' in low}; "
                f"ascii fallback: {'c-diagram-excalidraw-fallback' in low}")


def _uses(marker):
    def f(html, low, path):
        return marker in html, f"marker {marker!r} present: {marker in html}"
    return f


def run_check(check_id, html, path):
    low = html.lower()
    simple = {
        "validator-clean": check_validator_clean,
        "self-contained": check_self_contained,
        "auto-theme": check_auto_theme,
        "source-mirror": check_source_mirror,
        "toc": check_toc,
        "toc-subs": check_toc_subs,
        "mermaid-prerendered": check_mermaid_prerendered,
        "excalidraw-embed": check_excalidraw_embed,
    }
    if check_id in simple:
        return simple[check_id](html, low, path)
    for prefix, table in (("uses-component:", COMPONENT_MARKERS), ("uses-pattern:", PATTERN_MARKERS)):
        if check_id.startswith(prefix):
            name = check_id[len(prefix):]
            if name not in table:
                return False, f"unknown {prefix[:-1]} {name!r}"
            return _uses(table[name])(html, low, path)
    if check_id.startswith("contains:"):
        needle = check_id[len("contains:"):].lower()
        return needle in low, f"{needle!r} present: {needle in low}"
    if check_id.startswith("not-contains:"):
        needle = check_id[len("not-contains:"):].lower()
        return needle not in low, f"{needle!r} absent: {needle not in low}"
    return False, f"unknown check id {check_id!r}"


def main():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        sys.exit(0 if args else 2)
    path = Path(args[0])
    html = path.read_text(encoding="utf-8")

    eval_id, out = None, None
    checks = []
    i = 1
    while i < len(args):
        if args[i] == "--eval":
            eval_id = int(args[i + 1]); i += 2
        elif args[i] == "--out":
            out = Path(args[i + 1]); i += 2
        else:
            checks.append(args[i]); i += 1

    if eval_id is not None:
        spec = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
        ev = next((e for e in spec["evals"] if e["id"] == eval_id), None)
        if ev is None:
            print(f"no eval with id {eval_id} in {EVALS_JSON}")
            sys.exit(2)
        scripted = [(a["text"], a["check"]) for a in
                    spec.get("shared_assertions", []) + ev["assertions"] if "check" in a]
        pending = [a["text"] for a in
                   spec.get("shared_assertions", []) + ev["assertions"] if "check" not in a]
        checks = [c for _, c in scripted]
        labels = {c: t for t, c in scripted}
    else:
        pending, labels = [], {}

    results, failures = [], 0
    for c in checks:
        passed, evidence = run_check(c, html, path)
        failures += 0 if passed else 1
        text = labels.get(c, c)
        results.append({"text": text, "passed": passed, "evidence": f"[{c}] {evidence}"})
        print(f"{'PASS' if passed else 'FAIL'}  {c}  — {text}\n      {evidence}")

    if pending:
        print(f"\nPending LLM/human grading ({len(pending)}):")
        for t in pending:
            print(f"  ? {t}")

    if out:
        out.write_text(json.dumps({"expectations": results}, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {out}")
    print(f"\n{len(checks) - failures}/{len(checks)} scripted checks passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
