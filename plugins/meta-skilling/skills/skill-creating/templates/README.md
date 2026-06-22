## Templates for new skills

Two starting points. Copy one of these folders, rename to match the chosen `name` (lowercase kebab-case, matching the `name:` field in `SKILL.md`), and fill in the placeholders.

- **`basic-skill/`** — minimum viable skill: SKILL.md only.
- **`with-memory/`** — SKILL.md plus a `memory.md` scaffold and the Memory section already wired in. Only use this when the user explicitly asks for memory.

**Important:** this README lives at `templates/README.md`, deliberately outside the skill templates themselves. Don't place a `README.md` inside a skill folder — Anthropic's canonical rule forbids it, and the validator will flag it. Human-facing docs for a distributed skill go in the repo-level README, outside the skill folder.
