# Skill-creating — Lessons Learned

This file captures things past skill-creating sessions got wrong or that users corrected. SKILL.md and references already cover the design rules — only add entries here when something surprised us or was explicitly fixed.

## Contents

- Canonical-source drift — what to check when re-reading the official docs
- Non-obvious corrections from real sessions
- Anti-patterns from real failures

## Canonical-source drift

The two canonical URLs in SKILL.md evolve faster than this skill. When fetching them, scan for:

- New frontmatter fields (license, allowed-tools, compatibility, metadata sub-keys)
- New patterns (the PDF currently documents 5; count them)
- Changes to line/word budgets or limits
- New anti-patterns added to the "checklist for effective Skills"

If any of those appear to have changed since this skill was last updated, tell the user and offer to update the relevant reference file.

## Non-obvious corrections

### 2026-04-23 — Description convention was inverted

Earlier versions of `references/description-writing.md` and `scripts/scaffold.py` told authors to start descriptions with `Use when ...`. Every official Anthropic example leads with **capability first** (`[What it does]. Use when [triggers].`). The inverted convention was producing descriptions that under-matched Claude's selection heuristics. If you find an existing skill that starts with "Use when ...", flag it and offer to flip the order; the capability sentence should come first.

**How to apply:** When reviewing any skill's description, first check whether the opening words state the capability. If they state a trigger, rewrite.

## Anti-patterns from real failures

### Scaffold.py creates `README.md` files in subfolders

`scripts/scaffold.py` currently writes placeholder `README.md` files into `scripts/`, `references/`, `templates/`, `assets/` subdirectories when those are created. The canonical rule ("no README.md inside a skill folder") arguably extends to subdirectories. The validator only flags READMEs at the skill root, not in subfolders.

**How to apply:** If you're modifying scaffold.py, replace those subfolder READMEs with a PLACEHOLDER.md or stdout-only guidance. Until that's fixed, remind users who run scaffold.py to delete the subfolder READMEs before shipping the skill.

## Updated by

- 2026-04-23 — Initial creation alongside rewrite to match canonical best-practices docs.
