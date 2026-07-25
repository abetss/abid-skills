#!/usr/bin/env python3
"""Aggregate grading results from an eval iteration into a benchmark.

Run, don't read:
  python scripts/aggregate_benchmark.py evals-workspace/iteration-1 --skill-name generating-html-artifacts

Expects the layout from evals/README.md:

  iteration-N/
    <eval-name>/                (e.g. 0-migration-options-comparison)
      <config>/                 (e.g. with_skill, without_skill, old_skill, sonnet, haiku)
        grading.json            {"expectations": [{"text", "passed", "evidence"}]}
        timing.json             (optional) {"duration_s": 123, "total_tokens": 45678}

Writes benchmark.json + benchmark.md into the iteration directory: pass rate,
duration and tokens per configuration, with a per-eval breakdown and the delta
against the first (baseline) configuration.
"""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if sys.argv[1:] else 2)
    it_dir = Path(sys.argv[1])
    skill_name = "skill"
    if "--skill-name" in sys.argv:
        skill_name = sys.argv[sys.argv.index("--skill-name") + 1]

    configs, rows = [], {}
    for eval_dir in sorted(p for p in it_dir.iterdir() if p.is_dir()):
        for cfg_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            cfg = cfg_dir.name
            if cfg not in configs:
                configs.append(cfg)
            grading_path = cfg_dir / "grading.json"
            if not grading_path.exists():
                continue
            grading = json.loads(grading_path.read_text(encoding="utf-8"))
            exp = grading["expectations"]
            timing = {}
            timing_path = cfg_dir / "timing.json"
            if timing_path.exists():
                timing = json.loads(timing_path.read_text(encoding="utf-8"))
            rows.setdefault(cfg, {})[eval_dir.name] = {
                "passed": sum(1 for e in exp if e["passed"]),
                "total": len(exp),
                "failed": [e["text"] for e in exp if not e["passed"]],
                **{k: timing.get(k) for k in ("duration_s", "total_tokens") if k in timing},
            }

    if not rows:
        print(f"no grading.json files found under {it_dir}")
        sys.exit(1)

    summary = {"skill_name": skill_name, "iteration": it_dir.resolve().name, "configs": []}
    for cfg in configs:
        evals = rows.get(cfg, {})
        passed = sum(e["passed"] for e in evals.values())
        total = sum(e["total"] for e in evals.values())
        entry = {
            "name": cfg,
            "pass_rate": round(passed / total, 3) if total else None,
            "passed": passed,
            "total": total,
            "duration_s": _sum(evals, "duration_s"),
            "total_tokens": _sum(evals, "total_tokens"),
            "evals": {name: f'{e["passed"]}/{e["total"]}' for name, e in evals.items()},
        }
        summary["configs"].append(entry)

    baseline = summary["configs"][0]
    for entry in summary["configs"][1:]:
        if baseline["pass_rate"] is not None and entry["pass_rate"] is not None:
            entry["delta_vs_" + baseline["name"]] = round(entry["pass_rate"] - baseline["pass_rate"], 3)

    (it_dir / "benchmark.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [f"# Benchmark — {skill_name} ({it_dir.name})", ""]
    hdr = ["config", "pass rate", "passed", "duration_s", "tokens", "delta"]
    lines.append("| " + " | ".join(hdr) + " |")
    lines.append("|" + "---|" * len(hdr))
    for entry in summary["configs"]:
        delta = next((v for k, v in entry.items() if k.startswith("delta_vs_")), "—")
        lines.append("| {name} | {pass_rate} | {passed}/{total} | {duration_s} | {total_tokens} | {d} |".format(
            d=delta, **{k: (v if v is not None else "—") for k, v in entry.items() if k != "evals"}))
    lines.append("")
    lines.append("## Per-eval")
    lines.append("")
    eval_names = sorted({n for e in summary["configs"] for n in e["evals"]})
    lines.append("| eval | " + " | ".join(c["name"] for c in summary["configs"]) + " |")
    lines.append("|" + "---|" * (len(summary["configs"]) + 1))
    for name in eval_names:
        lines.append("| " + name + " | " + " | ".join(c["evals"].get(name, "—") for c in summary["configs"]) + " |")
    lines.append("")
    lines.append("## Failed assertions")
    lines.append("")
    for cfg in configs:
        for eval_name, e in rows.get(cfg, {}).items():
            for t in e["failed"]:
                lines.append(f"- **{cfg} / {eval_name}**: {t}")
    (it_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {it_dir / 'benchmark.json'} and {it_dir / 'benchmark.md'}")
    for entry in summary["configs"]:
        print(f"  {entry['name']}: {entry['passed']}/{entry['total']} ({entry['pass_rate']})")


def _sum(evals, key):
    vals = [e[key] for e in evals.values() if e.get(key) is not None]
    return round(sum(vals), 1) if vals else None


if __name__ == "__main__":
    main()
