#!/usr/bin/env python3
"""
Interactive scaffolder for a new Claude Code skill.

Runs an interview to capture intent, then writes a starter skill folder with:
  - SKILL.md (frontmatter + skeleton body, draft description built from answers)
  - memory.md (only if user wants opt-in memory)
  - scripts/, references/, templates/, assets/ subfolders (only for the ones
    the user actually needs, never empty "just in case" folders)

Usage:
    python scaffold.py
    python scaffold.py --dry-run      # prints plan without writing files
    python scaffold.py --output-dir ~/.claude/skills

Interview structure:
    1. Capture intent (4 core questions)
    2. Follow-up probes (edge cases, examples, dependencies)
    3. Discovery (scripts, templates, references, assets, memory)
    4. Confirm summary
    5. Write files
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path.home() / ".claude" / "skills"
RESERVED_NAME_WORDS = {"claude", "anthropic"}
BANNED_NAME_WORDS = {"helper", "utility", "manager", "tool", "handler"}


@dataclass
class Intent:
    name: str = ""
    one_liner: str = ""               # what it enables
    trigger_contexts: str = ""        # when to trigger
    output_format: str = ""           # what success looks like
    test_cases_needed: bool = False
    edge_cases: str = ""
    examples: str = ""
    dependencies: str = ""

    needs_scripts: bool = False
    scripts_description: str = ""
    needs_templates: bool = False
    templates_description: str = ""
    needs_references: bool = False
    references_description: str = ""
    needs_assets: bool = False
    assets_description: str = ""
    needs_memory: bool = False
    memory_rationale: str = ""


def prompt(label: str, default: str | None = None, required: bool = True) -> str:
    hint = f" [{default}]" if default else ""
    while True:
        try:
            answer = input(f"{label}{hint}\n> ").strip()
        except EOFError:
            print("\n(no input — aborting)", file=sys.stderr)
            sys.exit(130)
        if not answer and default is not None:
            return default
        if answer:
            return answer
        if not required:
            return ""
        print("  (this one is required)")


def prompt_yes_no(label: str, default: bool = False) -> bool:
    default_hint = "Y/n" if default else "y/N"
    while True:
        try:
            answer = input(f"{label} [{default_hint}]\n> ").strip().lower()
        except EOFError:
            print("\n(no input — aborting)", file=sys.stderr)
            sys.exit(130)
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("  (please answer y or n)")


def print_section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def kebab_suggest(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    cleaned = re.sub(r"\s+", "-", cleaned).strip("-")
    return cleaned or "new-skill"


def validate_name(name: str) -> list[str]:
    problems: list[str] = []
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        problems.append("must be lowercase kebab-case (a-z, 0-9, hyphens only)")
    for reserved in RESERVED_NAME_WORDS:
        if reserved in name.split("-"):
            problems.append(f"contains reserved word `{reserved}`")
    for banned in BANNED_NAME_WORDS:
        if banned in name.split("-"):
            problems.append(f"contains vague word `{banned}` — pick something more specific")
    return problems


def capture_intent() -> Intent:
    intent = Intent()

    print_section("1. What this skill does")
    print("First, the 4 core questions from Anthropic's skill-creator pattern.")
    print()

    intent.one_liner = prompt(
        "What should this skill enable Claude to do? (one sentence)"
    )
    intent.trigger_contexts = prompt(
        "When should Claude invoke it? What phrases or contexts should trigger it?\n"
        "(examples: 'user says X', 'user is editing timesheets', 'user asks to document a feature')"
    )
    intent.output_format = prompt(
        "What does successful output look like?\n"
        "(a markdown file? a JSON schema? a code change? nothing — just side effects?)"
    )
    intent.test_cases_needed = prompt_yes_no(
        "Should this skill have test cases? (yes for objectively verifiable, no for subjective)",
        default=False,
    )

    print_section("2. Follow-up details")
    intent.edge_cases = prompt(
        "Any edge cases or weird inputs you want the skill to handle correctly?\n"
        "(press Enter to skip)",
        required=False,
    )
    intent.examples = prompt(
        "Any example inputs the skill should handle? Paths to example files are fine.\n"
        "(press Enter to skip)",
        required=False,
    )
    intent.dependencies = prompt(
        "Does the skill need any external tools, MCPs, or environment setup?\n"
        "(press Enter to skip)",
        required=False,
    )

    print_section("3. What bundled resources does this skill need?")
    print("Each 'yes' here creates a subfolder in the skill. Each 'no' keeps the")
    print("skill minimal. Don't create folders you don't have real content for.")
    print()

    intent.needs_scripts = prompt_yes_no(
        "Will the skill run deterministic code — validators, generators, linters, data transforms?",
        default=False,
    )
    if intent.needs_scripts:
        intent.scripts_description = prompt(
            "  What will the scripts do? (one line per script if multiple)"
        )

    intent.needs_templates = prompt_yes_no(
        "Will the skill produce output in a consistent shape — templates to copy from?",
        default=False,
    )
    if intent.needs_templates:
        intent.templates_description = prompt(
            "  What templates? (e.g. 'a page doc template', 'a form scaffold')"
        )

    intent.needs_references = prompt_yes_no(
        "Is there a large body of reference material — schemas, rules, taxonomies — that would bust the 500-line budget?",
        default=False,
    )
    if intent.needs_references:
        intent.references_description = prompt(
            "  What references? (e.g. 'naming rules', 'description-writing guide', 'schema catalog')"
        )

    intent.needs_assets = prompt_yes_no(
        "Does the output include non-text files — HTML, fonts, icons, images?",
        default=False,
    )
    if intent.needs_assets:
        intent.assets_description = prompt(
            "  What assets? (e.g. 'email HTML template', 'icon set')"
        )

    intent.needs_memory = prompt_yes_no(
        "Will past sessions of this skill produce learnings that future sessions should remember?\n"
        "(opt-in; most skills don't need memory)",
        default=False,
    )
    if intent.needs_memory:
        intent.memory_rationale = prompt(
            "  Why? What kind of lessons would accumulate?\n"
            "  (user corrections? gotchas found in data? bugs found in previous output?)"
        )

    print_section("4. Skill name")
    suggested = kebab_suggest(intent.one_liner.split(".")[0])
    while True:
        name = prompt(
            "Skill name (lowercase kebab-case, folder name will match this)",
            default=suggested,
        )
        problems = validate_name(name)
        if not problems:
            intent.name = name
            break
        for p in problems:
            print(f"  ✗ {p}")
        print("  Try again.")

    return intent


def draft_description(intent: Intent) -> str:
    """Build a draft description from the intent answers.

    Canonical pattern is capability-first: [what the skill does]. Use when [triggers].
    See references/description-writing.md. Leading with 'Use when ...' is an anti-pattern
    flagged by the validator.
    """
    core = intent.one_liner.strip().rstrip(".")
    triggers = intent.trigger_contexts.strip().rstrip(".")
    return (
        f"{core}. Use when {triggers}, "
        f"even if the user doesn't explicitly name the skill."
    )


def render_summary(intent: Intent, output_path: Path) -> str:
    lines = [
        "SUMMARY OF INTERVIEW",
        "-" * 60,
        f"Name:            {intent.name}",
        f"Output folder:   {output_path}",
        "",
        f"One-liner:       {intent.one_liner}",
        f"Triggers:        {intent.trigger_contexts}",
        f"Output format:   {intent.output_format}",
        f"Test cases:      {'yes' if intent.test_cases_needed else 'no'}",
        "",
        "Bundled resources:",
        f"  scripts/       {'yes — ' + intent.scripts_description if intent.needs_scripts else 'no'}",
        f"  templates/     {'yes — ' + intent.templates_description if intent.needs_templates else 'no'}",
        f"  references/    {'yes — ' + intent.references_description if intent.needs_references else 'no'}",
        f"  assets/        {'yes — ' + intent.assets_description if intent.needs_assets else 'no'}",
        f"  memory.md      {'yes — ' + intent.memory_rationale if intent.needs_memory else 'no'}",
        "",
        "Draft description (PREVIEW — you'll refine this):",
        f"  {draft_description(intent)}",
    ]
    return "\n".join(lines)


def render_skill_md(intent: Intent) -> str:
    description = draft_description(intent)
    sections = [
        "---",
        f"name: {intent.name}",
        f"description: {description}",
        "---",
        "",
        f"# {intent.name.replace('-', ' ').title()}",
        "",
        intent.one_liner.strip(),
        "",
    ]

    if intent.needs_memory:
        sections += [
            "## Memory",
            "",
            "Read `memory.md` before starting. It captures lessons from past sessions.",
            "",
            "### Reading memory",
            "Before starting, scan memory entries for:",
            "- TODO: add domain-specific scan criteria",
            "",
            "### Writing to memory",
            "After completing a session, write an entry if:",
            "- A user explicitly corrected something",
            "- You found a bug you almost repeated",
            "- A technique was unusually effective",
            "",
            "Do NOT capture things already in SKILL.md, generic advice, or obvious statements.",
            "",
        ]

    sections += [
        "## When to use",
        "",
    ]
    for trigger in _split_triggers(intent.trigger_contexts):
        sections.append(f"- {trigger}")
    sections.append("")

    sections += [
        "## Process",
        "",
        "1. TODO: first step",
        "2. TODO: second step",
        "3. TODO: third step",
        "",
        "## Expected output",
        "",
        intent.output_format.strip(),
        "",
    ]

    if intent.edge_cases:
        sections += ["## Edge cases", "", intent.edge_cases.strip(), ""]

    if intent.needs_scripts:
        sections += [
            "## Scripts",
            "",
            f"See `scripts/`. Intent: {intent.scripts_description}",
            "",
        ]
    if intent.needs_templates:
        sections += [
            "## Templates",
            "",
            f"See `templates/`. Intent: {intent.templates_description}",
            "",
        ]
    if intent.needs_references:
        sections += [
            "## References",
            "",
            f"See `references/`. Intent: {intent.references_description}",
            "",
        ]
    if intent.needs_assets:
        sections += [
            "## Assets",
            "",
            f"See `assets/`. Intent: {intent.assets_description}",
            "",
        ]

    if intent.dependencies:
        sections += ["## Dependencies", "", intent.dependencies.strip(), ""]

    sections += [
        "## Notes for the author",
        "",
        "This SKILL.md was scaffolded by `skill-creating/scripts/scaffold.py`.",
        "Things to do before shipping:",
        "",
        "- Refine the description. It's the single most important field. See",
        "  `~/.claude/skills/skill-creating/references/description-writing.md`.",
        "- Fill in the TODO steps in the Process section above.",
        "- Replace this 'Notes for the author' section with real content or delete it.",
        "- Run `python ~/.claude/skills/skill-creating/scripts/validate.py "
        f"{Path.home() / '.claude' / 'skills' / intent.name}` before finishing.",
    ]

    return "\n".join(sections) + "\n"


def _split_triggers(trigger_contexts: str) -> list[str]:
    # Split on semicolons, commas, or "or" — one bullet per trigger.
    parts = re.split(r";|\bor\b|,", trigger_contexts)
    triggers = [p.strip().rstrip(".") for p in parts if p.strip()]
    return triggers or [trigger_contexts.strip()]


def render_memory_md(intent: Intent) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# {intent.name.replace('-', ' ').title()} — Lessons Learned",
        "",
        "This file captures things past sessions got wrong or that users corrected.",
        "SKILL.md already covers the design rules — only add entries here when",
        "something surprised us or was explicitly fixed.",
        "",
        f"## Rationale (from intake)",
        "",
        intent.memory_rationale.strip(),
        "",
        "## Non-obvious corrections",
        "",
        "(Add entries here as they arise.)",
        "",
        "## Anti-patterns from real failures",
        "",
        "(Add entries here as they arise.)",
        "",
        "## Updated by",
        "",
        f"- {today} — Initial creation via scaffold.py",
    ]
    return "\n".join(lines) + "\n"


def render_placeholder_readme(folder_name: str, description: str) -> str:
    return (
        f"# {folder_name}\n\n"
        f"{description}\n\n"
        f"Delete this README once you've added real files.\n"
    )


def write_skill(intent: Intent, output_path: Path, dry_run: bool = False) -> list[Path]:
    planned: list[Path] = []

    skill_md = output_path / "SKILL.md"
    planned.append(skill_md)
    if not dry_run:
        output_path.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(render_skill_md(intent), encoding="utf-8")

    if intent.needs_memory:
        memory_md = output_path / "memory.md"
        planned.append(memory_md)
        if not dry_run:
            memory_md.write_text(render_memory_md(intent), encoding="utf-8")

    if intent.needs_scripts:
        scripts_dir = output_path / "scripts"
        readme = scripts_dir / "README.md"
        planned.append(readme)
        if not dry_run:
            scripts_dir.mkdir(parents=True, exist_ok=True)
            readme.write_text(
                render_placeholder_readme("scripts/", intent.scripts_description),
                encoding="utf-8",
            )

    if intent.needs_templates:
        templates_dir = output_path / "templates"
        readme = templates_dir / "README.md"
        planned.append(readme)
        if not dry_run:
            templates_dir.mkdir(parents=True, exist_ok=True)
            readme.write_text(
                render_placeholder_readme("templates/", intent.templates_description),
                encoding="utf-8",
            )

    if intent.needs_references:
        references_dir = output_path / "references"
        readme = references_dir / "README.md"
        planned.append(readme)
        if not dry_run:
            references_dir.mkdir(parents=True, exist_ok=True)
            readme.write_text(
                render_placeholder_readme("references/", intent.references_description),
                encoding="utf-8",
            )

    if intent.needs_assets:
        assets_dir = output_path / "assets"
        readme = assets_dir / "README.md"
        planned.append(readme)
        if not dry_run:
            assets_dir.mkdir(parents=True, exist_ok=True)
            readme.write_text(
                render_placeholder_readme("assets/", intent.assets_description),
                encoding="utf-8",
            )

    return planned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Parent directory to create the skill in (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without touching disk",
    )
    args = parser.parse_args()

    print()
    print("Skill scaffolder — interactive interview")
    print("=" * 60)
    print("Answers can be short phrases. Press Ctrl+C any time to abort.")

    try:
        intent = capture_intent()
    except KeyboardInterrupt:
        print("\n(aborted)", file=sys.stderr)
        return 130

    output_path = args.output_dir / intent.name

    print_section("5. Review")
    print(render_summary(intent, output_path))

    if output_path.exists():
        print()
        print(f"⚠  {output_path} already exists. Scaffolding would overwrite SKILL.md")
        print("  and any placeholder READMEs. Existing files in subfolders are untouched.")
        if not prompt_yes_no("Continue anyway?", default=False):
            print("(aborted)")
            return 0

    print()
    if not prompt_yes_no("Write the skill now?", default=True):
        print("(aborted)")
        return 0

    planned = write_skill(intent, output_path, dry_run=args.dry_run)

    print()
    if args.dry_run:
        print("DRY RUN — would write:")
    else:
        print("Wrote:")
    for p in planned:
        print(f"  {p}")
    print()
    print("Next steps:")
    print(f"  1. Review {output_path / 'SKILL.md'} — especially the description")
    print(f"  2. Fill in the TODO items")
    print(
        f"  3. python {Path(__file__).parent / 'validate.py'} {output_path}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
