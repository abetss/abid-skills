# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code **plugin marketplace** named `abid-skills`. It is not an application — it ships
Markdown-defined skills (and a few agents) that get installed into other people's Claude Code
setups. There is no build, no runtime, and no dependency install. "Code" here is almost entirely
Markdown plus a couple of Python helper scripts.

## Layout

```text
.claude-plugin/marketplace.json   # the catalog — lists every plugin and its source path
plugins/<name>/
  .claude-plugin/plugin.json      # plugin manifest (name, description, version, author)
  skills/<skill>/SKILL.md         # one folder per skill; may include references/, scripts/, templates/, assets/
  agents/<agent>.md               # subagent definitions (engineering/, qa/ only)
workflows/                        # human-readable cheat sheets chaining skills — NOT executed
```

Four plugins: **product** (design), **engineering** (planning/review/debugging/docs + 3 agents),
**qa** (QA runs + qa-runner agent), **meta-skilling** (skill authoring + HTML artifacts).

## Adding or changing things

- **New plugin** → create `plugins/<name>/.claude-plugin/plugin.json` AND add an entry to
  `.claude-plugin/marketplace.json`. The two must stay in sync; the marketplace's `source`
  points at the plugin folder.
- **New skill** → `plugins/<plugin>/skills/<skill>/SKILL.md`. The folder name MUST equal the
  `name:` in the SKILL.md frontmatter. Update the plugin's `plugin.json` description and the
  root `README.md` table if the skill is user-facing.
- **Authoring skills is itself a skill.** Read `plugins/meta-skilling/skills/skill-creating/SKILL.md`
  and its `references/` before writing or substantially editing any SKILL.md — it is the
  authoritative house style (description-writing, naming, progressive disclosure, anti-patterns).

## Validate a skill

```bash
python plugins/meta-skilling/skills/skill-creating/scripts/validate.py <skill-folder>
# e.g. python .../validate.py plugins/engineering/skills/commit-git
```

Exit 0 = clean (warnings allowed), 1 = errors. Run it after editing any SKILL.md. There is no
test runner or linter beyond this.

## Skill conventions (enforced by the validator — non-obvious ones)

- Frontmatter requires `name:` and `description:`. Directory name must match `name:`.
- **No `README.md` inside a skill folder** — human-facing READMEs live at the repo level only.
- **No `@path/file.md` force-load references** — use plain relative Markdown links so the
  referenced file loads on demand, not eagerly.
- Forward slashes in all paths, even for Windows.
- MCP tool references must be fully qualified: `ServerName:tool_name`.
- If a `## Memory` section exists in a SKILL.md, a `memory.md` must exist beside it.
- Descriptions are the only thing Claude sees before invoking — lead with the capability, then
  "Use when …", then trigger phrases. Third person. Keep SKILL.md under ~500 lines; spill detail
  into `references/`.
- Banned name words: `claude`, `anthropic`, `helper`, `utility`, `manager`, `tool`, `handler`.

## Commit conventions

Prefixes `feat:` / `fix:` / `chore:`, optional `[TICKET]` prefix, third-person present tense
("adds" not "added"). See `plugins/engineering/skills/commit-git/SKILL.md`.
