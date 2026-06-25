#!/usr/bin/env python3
"""
Validate a Claude Code skill folder.

Checks frontmatter, naming, description quality, links, memory consistency,
and line-count budget. Run before shipping a new skill or after editing one.

Usage:
    python validate.py <skill-folder>
    python validate.py ~/.claude/skills/my-skill

Exit codes:
    0 = no errors (warnings may still be printed)
    1 = one or more errors
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


RESERVED_NAME_WORDS = {"claude", "anthropic"}
BANNED_NAME_WORDS = {"helper", "utility", "manager", "tool", "handler"}
LINE_BUDGET_SOFT = 500  # warning
DESCRIPTION_MIN = 10
DESCRIPTION_MAX = 1024
FIRST_PERSON_TOKENS = {"i", "i'll", "i've", "my", "we'll", "we've", "you'll"}
TRIGGER_PHRASES = (
    "use when",
    "when the user",
    "when user",
    "when working",
    "triggers on",
    "trigger on",
    "use for",
)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> bool:
        return not self.errors

    def render(self, skill_path: Path) -> str:
        lines = [f"Validating: {skill_path}"]
        if self.errors:
            lines.append("")
            lines.append(f"ERRORS ({len(self.errors)}):")
            for e in self.errors:
                lines.append(f"  ✗ {e}")
        if self.warnings:
            lines.append("")
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"  ! {w}")
        if not self.errors and not self.warnings:
            lines.append("  ✓ all checks passed")
        return "\n".join(lines)


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    """Return (fields, body_line_offset). Raises ValueError on malformed frontmatter.

    Supports simple `key: value` lines and multi-line values where subsequent
    indented lines are appended to the previous field (YAML folded/literal style).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening `---`")
    closing = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing = i
            break
    if closing is None:
        raise ValueError("missing closing `---`")

    fields: dict[str, str] = {}
    current_key: str | None = None
    for raw in lines[1:closing]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Indented continuation line → append to previous field
        if raw and raw[0] in " \t" and current_key is not None:
            fields[current_key] = (fields[current_key] + " " + stripped).strip()
            continue
        if ":" not in raw:
            raise ValueError(f"frontmatter line is not key:value → {raw!r}")
        key, _, value = raw.partition(":")
        current_key = key.strip()
        fields[current_key] = value.strip()
    return fields, closing + 1


def is_kebab_case(s: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s))


def has_first_person(description: str) -> bool:
    # Strip quoted trigger phrases first — they're verbatim user utterances
    # ("respond to my code reviews"), not the skill's own voice. Then match
    # whole words so "i" doesn't fire inside "UI" and "my" doesn't fire inside
    # a quoted phrase.
    prose = re.sub(r'"[^"]*"', " ", description.lower())
    for token in FIRST_PERSON_TOKENS:
        if re.search(r"(?<![\w'])" + re.escape(token) + r"(?![\w'])", prose):
            return True
    return False


def parse_arguments_field(value: str) -> list[str]:
    """Parse the `arguments` frontmatter value into a list of names.

    Accepts a YAML inline list `[a, b]` or a space/comma-separated string `a b`.
    """
    v = value.strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    parts = re.split(r"[,\s]+", v.strip())
    return [p.strip() for p in parts if p.strip()]


def check_arguments(fields: dict[str, str], body: str, report: Report) -> None:
    """Validate argument declarations and their use in the body.

    - `arguments` declared without `argument-hint` loses the autocomplete hint.
    - A declared argument should be referenced bare (`$name`) in the body, never
      backticked — backticks render the literal label instead of substituting the value.
    """
    arg_field = fields.get("arguments")
    hint = fields.get("argument-hint")
    names = parse_arguments_field(arg_field) if arg_field else []

    if names and not hint:
        report.warn(
            "`arguments` is declared but `argument-hint` is missing — add a hint so the "
            "slash-command autocomplete shows the expected arguments"
        )

    for name in names:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            continue  # only check plain identifier names
        esc = re.escape(name)
        backticked = re.search(r"`\$\{?" + esc + r"\}?`", body)
        bare = re.search(r"(?<![\w`])\$" + esc + r"\b", body)
        if backticked:
            report.warn(
                f"argument `${name}` appears backticked in the body — backticks render the "
                f"literal label instead of substituting the value; write it bare as ${name}"
            )
        elif not bare:
            report.warn(
                f"declared argument `{name}` is never referenced as ${name} in the body — "
                f"reference it or drop it from `arguments`"
            )


def check_frontmatter(fields: dict[str, str], skill_path: Path, report: Report) -> None:
    name = fields.get("name")
    description = fields.get("description")

    if not name:
        report.err("frontmatter missing `name:`")
    if not description:
        report.err("frontmatter missing `description:`")

    if name:
        if name != skill_path.name:
            report.err(f"frontmatter name `{name}` does not match directory name `{skill_path.name}`")
        if not is_kebab_case(name):
            report.err(f"name `{name}` is not lowercase kebab-case (a-z, 0-9, hyphens)")
        if "_" in name:
            report.err(f"name `{name}` contains underscores — use hyphens")
        if " " in name:
            report.err(f"name `{name}` contains spaces — use hyphens")
        for reserved in RESERVED_NAME_WORDS:
            if reserved in name.lower().split("-"):
                report.err(f"name `{name}` contains reserved word `{reserved}`")
        for banned in BANNED_NAME_WORDS:
            if banned in name.lower().split("-"):
                report.warn(f"name `{name}` contains vague word `{banned}` — consider a more specific name")

    if description:
        desc_len = len(description)
        if desc_len < DESCRIPTION_MIN:
            report.err(f"description is too short ({desc_len} chars, min {DESCRIPTION_MIN})")
        if desc_len > DESCRIPTION_MAX:
            report.err(f"description is too long ({desc_len} chars, max {DESCRIPTION_MAX})")
        lower_desc = description.lower()
        if not any(phrase in lower_desc for phrase in TRIGGER_PHRASES):
            report.warn(
                "description lacks a triggering clause (e.g. 'Use when ...', 'Triggers on ...') — "
                "Claude needs explicit trigger contexts to decide when to invoke"
            )
        if lower_desc.startswith("use when"):
            report.warn(
                "description starts with 'Use when ...' — canonical pattern is capability-first: "
                "'[what the skill does]. Use when [triggers].' See references/description-writing.md"
            )
        if has_first_person(description):
            report.warn("description appears to use first person (I/my/we/you'll) — prefer third person")
        if "<" in description or ">" in description:
            report.err("description contains XML angle brackets (< or >) — forbidden in frontmatter")


def check_links(body: str, skill_path: Path, report: Report) -> None:
    # Find all [text](path) markdown links where path is not a URL
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for match in pattern.finditer(body):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if target.startswith("@"):
            report.err(f"link `{target}` uses `@path/` syntax which force-loads the file — use relative links instead")
            continue
        # Skip template placeholder paths like `{subfolder}/{filename}.md`
        if "{" in target or "}" in target:
            continue
        if "\\" in target:
            report.err(f"link `{target}` uses Windows-style backslash — use forward slashes only")
            continue
        # Strip any anchor
        target_path = target.split("#")[0]
        if not target_path:
            continue
        resolved = (skill_path / target_path).resolve()
        if not resolved.exists():
            report.err(f"broken link: `{target}` → {resolved} does not exist")


def check_forbidden_files(skill_path: Path, report: Report) -> None:
    """README.md inside a skill folder is forbidden by Anthropic's canonical rule.
    Human-facing docs belong in the repo-level README, outside the skill folder."""
    readme = skill_path / "README.md"
    if readme.exists():
        report.err(
            "README.md exists inside the skill folder — forbidden per canonical guidance. "
            "Move to a repo-level README outside this folder."
        )
    # Also check case variants that would slip past SKILL.md casing on macOS
    for variant in ("readme.md", "Readme.md", "readme.MD"):
        p = skill_path / variant
        if p.exists() and p.name != readme.name:
            report.err(f"{variant} exists inside the skill folder — forbidden (see README.md rule)")


def check_memory_consistency(body: str, skill_path: Path, report: Report) -> None:
    # A skill "uses memory" only if it instructs Claude to read memory.md.
    # Merely having a section titled "Memory" (e.g. "## Memory guidance") does
    # not count — guidance is not an instruction.
    reads_memory = bool(
        re.search(r"[Rr]ead\s+`memory\.md`", body)
        or re.search(r"^\s*[-*]\s+`memory\.md`", body, re.MULTILINE)
    )
    memory_file = skill_path / "memory.md"
    if reads_memory and not memory_file.exists():
        report.err("SKILL.md instructs Claude to read `memory.md` but the file does not exist in the skill folder")
    if memory_file.exists() and not reads_memory:
        report.warn("`memory.md` exists but SKILL.md does not instruct Claude to read it — the skill won't use it")


def check_line_count(body: str, report: Report) -> None:
    count = len(body.splitlines())
    if count > LINE_BUDGET_SOFT:
        report.warn(f"SKILL.md body is {count} lines (soft limit {LINE_BUDGET_SOFT}) — consider splitting detail into `references/`")


def validate(skill_path: Path) -> Report:
    report = Report()

    if not skill_path.exists():
        report.err(f"skill folder does not exist: {skill_path}")
        return report
    if not skill_path.is_dir():
        report.err(f"path is not a directory: {skill_path}")
        return report

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        report.err("SKILL.md is missing")
        return report

    text = skill_md.read_text(encoding="utf-8")
    if not text.strip():
        report.err("SKILL.md is empty")
        return report

    try:
        fields, body_offset = parse_frontmatter(text)
    except ValueError as exc:
        report.err(f"frontmatter malformed: {exc}")
        return report

    body = "\n".join(text.splitlines()[body_offset:])

    check_frontmatter(fields, skill_path, report)
    check_arguments(fields, body, report)
    check_links(body, skill_path, report)
    check_memory_consistency(body, skill_path, report)
    check_line_count(body, report)
    check_forbidden_files(skill_path, report)

    return report


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    skill_path = Path(sys.argv[1]).expanduser().resolve()
    report = validate(skill_path)
    print(report.render(skill_path))
    return 0 if report.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
