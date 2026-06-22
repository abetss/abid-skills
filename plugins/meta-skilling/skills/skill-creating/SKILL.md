---
name: abid/skill-creating
description: Creates and improves Claude skills — scaffolds folders, writes triggering descriptions, applies progressive disclosure, validates structure, and adds memory or templates. Invoke only via the `/skill-creating` slash command.
disable-model-invocation: true
---

# Skill Creating

Guide for authoring consistent, well-triggered, well-structured Claude skills.

## Canonical sources

Anthropic's public guidance is the authoritative reference. Before creating a new skill (or making a substantive change to one), fetch both URLs. This skill's `references/` files are a distilled, opinionated version — if the canonical docs disagree, the canonical docs win. Tell the user when they've moved ahead of this skill.

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf

For small tweaks to an existing skill (renaming, fixing a broken link), skip the fetch — the local references are current enough.

## Read before you start

- `memory.md` — lessons from past skill-creating sessions
- `references/interview-questions.md` — capture intent before writing anything
- `references/description-writing.md` — the single most load-bearing file; descriptions are all Claude sees before deciding to invoke
- `references/naming.md` — rules, banned words, good/bad examples
- `references/progressive-disclosure.md` — three-level loading model
- `references/folder-structure.md` — when to use `scripts/`, `references/`, `templates/`, `assets/`
- `references/testing.md` — trigger tests and functional tests
- `references/script-quality.md` — only if the skill bundles executable scripts
- `references/anti-patterns.md` — failure modes to avoid

If the user is resuming a conversation where the skill intent is already clear, skip the interview step. Still read the relevant references.

## Process for a new skill

1. **Fetch canonical docs.** WebFetch both URLs in "Canonical sources" above. Scan for anything not already reflected in this skill's references.
2. **Capture intent.** Scan the current conversation for answers. Run the interview from `references/interview-questions.md` for what's missing. Pin down 2–3 concrete use cases in Trigger/Steps/Result form before writing files.
3. **Choose the name.** Apply `references/naming.md`. Confirm with the user.
4. **Draft the description.** Apply `references/description-writing.md`. Lead with the capability, then "Use when ...", then key trigger phrases. Third person. Confirm with the user.
5. **Write trigger tests.** Draft 3 queries that should trigger the skill and 3 that should not (see `references/testing.md`). These double as a sanity check on the description.
6. **Scaffold the folder.** Either:
   - Run `python scripts/scaffold.py` for a guided interview, or
   - Copy `templates/basic-skill/` (or `templates/with-memory/`) and fill in placeholders
7. **Decide what lives where.** Apply `references/progressive-disclosure.md` and `references/folder-structure.md`. Only create subfolders you have real content for.
8. **Validate.** Run `python scripts/validate.py <skill-folder>`. Fix errors. Warnings are informational.
9. **Verify triggering.** Ask the user to open a fresh session and say *"When would you use the [skill name] skill?"* Claude should paraphrase the description and name the right trigger contexts. If it doesn't, the description is under-triggering — return to step 4.

## Process for modifying an existing skill

1. Read the whole skill first — SKILL.md, memory.md, every reference and template. Understand the shape before changing anything.
2. Ask what's wrong: under-triggering, bad output, missing use case, overfit to a scenario?
3. Apply the smallest change that addresses the problem. Don't rewrite sections that are working.
4. Re-run `python scripts/validate.py <skill-folder>`.

## Memory (opt-in for the skill you're creating)

**Not every skill needs memory.** Do NOT add a memory section to a new skill unless the user explicitly asks for it.

### When memory makes sense

- Correctness depends on accumulated lessons (past bugs, past corrections, domain gotchas)
- Past sessions are likely to encounter surprises a fresh agent would repeat
- The skill runs often enough that a memory file will actually get written to

### Adding memory to an existing skill

1. Confirm the user explicitly asked for memory.
2. Copy the `## Memory` section from `templates/with-memory/SKILL.md` into the skill's SKILL.md (below the description, above Process).
3. Adapt the domain-specific wording.
4. Create `memory.md` using `templates/with-memory/memory.md` as a starting point.
5. Update the skill's "read first" list to reference `memory.md`.

### What to capture in memory

- User corrections mid-session (naming, structure, tone, preference)
- Bugs in previous output you almost repeated
- Anti-patterns from real failures
- Techniques that were unusually effective
- Systemic patterns across multiple sessions

### What NOT to capture

- Anything already in SKILL.md, references, or templates
- Generic advice not tied to a real incident
- Project facts (belong in project docs or CLAUDE.md)
- Obvious "do better" statements

## Scripts shipped with this skill

- `scripts/validate.py` — deterministic lint. Checks frontmatter, naming, description, links, line count, memory consistency, forbidden files (like `README.md` in the skill folder), XML tags, Windows-style paths. Run on every skill before finishing. `python scripts/validate.py ~/.claude/skills/my-skill`
- `scripts/scaffold.py` — interactive interview that generates a new skill folder.

## Writing style

- Imperative, not MUST/NEVER in all caps.
- Explain *why* briefly where it matters.
- Only add knowledge Claude doesn't already know.
- Consistent terminology — pick one term per concept and stick to it.
- No time-sensitive phrasing ("after August 2025..."). Put legacy guidance in an "old patterns" collapsed section.

## Hard rules

- `SKILL.md` is the only required file. Frontmatter must include `name:` and `description:`.
- Directory name MUST match `name:` in frontmatter.
- No `README.md` inside a skill folder. Repo-level READMEs for human readers live OUTSIDE the skill folder.
- Descriptions are the only thing Claude sees before deciding to invoke. Put all "when to use" info there.
- Do NOT use `@path/file.md` references — they force-load. Use relative markdown links.
- Forward slashes only in paths, even on Windows.
- If a `## Memory` section exists in SKILL.md, `memory.md` must exist in the same folder.
- MCP tool references must be fully qualified: `ServerName:tool_name`.

## Anti-patterns

See `references/anti-patterns.md` for detail. Short list:

- Under-triggering descriptions (plain, literal, or workflow-summarizing)
- Description that leads with "Use when ..." instead of with the capability
- Heavy-handed MUSTs/NEVERs in all caps
- Dumping everything into SKILL.md
- Overfitting fixes to specific test cases
- Creating empty `scripts/`/`references/` folders "just in case"
- `README.md` inside a skill folder
- Time-sensitive language ("after August 2025...")
- Offering many options without a default + escape hatch
- Unqualified MCP tool names
- Banned name words: `claude`, `anthropic`, `helper`, `utility`, `manager`, `tool`, `handler`
