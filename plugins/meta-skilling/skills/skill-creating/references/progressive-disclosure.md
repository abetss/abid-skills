## Progressive disclosure

Skills load in three tiers. Design the skill around this loading model instead of treating SKILL.md as a flat document where everything lives.

## The three levels

1. **Metadata** — the `name` and `description` from frontmatter. Always in Claude's context, across every conversation. Budget ~100 words total. This is what triggers the skill.
2. **SKILL.md body** — loaded into context whenever the skill triggers. Aim for under 500 lines. This is where the workflow and core rules live.
3. **Bundled resources** — files under `references/`, `scripts/`, `templates/`, `assets/`. Loaded on demand when Claude decides to read them. Unlimited size. Scripts are special — they can execute without being read into context at all.

## Implications

- SKILL.md should behave like a short index that points at `references/` for detail, not a dump of every rule.
- Scripts don't consume context unless you actually `Read` them. A 2000-line validator costs zero tokens until Claude needs to debug it.
- Cross-references should be ordinary relative markdown links. Claude reads them only when the workflow in SKILL.md points there.

## Keep references one level deep

All reference files must link directly from SKILL.md. Do not daisy-chain — `SKILL.md → a.md → b.md → c.md` is a known failure mode: when Claude follows a reference from another reference, it often partial-reads (e.g. `head -100`) rather than fully reading, and ends up with incomplete information.

Bad:
```
SKILL.md → references/advanced.md → references/details.md → references/deep.md
```

Good:
```
SKILL.md → references/advanced.md
SKILL.md → references/details.md
SKILL.md → references/deep.md
```

## Table of contents for files over 100 lines

A long reference file should open with a terse TOC so Claude can see the full scope even if it previews with a partial read.

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
```

## Soft limit: 500 lines for SKILL.md

Not a hard fail — a signal. If SKILL.md approaches 300–400 lines, start moving detail into `references/` files. By 500 lines, the body is competing with the rest of the conversation for context budget.

## Rule of thumb for splitting

- Topic is a detailed rulebook (schemas, taxonomies, bad/good tables) → `references/`.
- Topic is a reusable output scaffold → `templates/`.
- Topic is deterministic, rule-based logic → `scripts/`.
- Topic is a static artifact the output needs (fonts, HTML, images) → `assets/`.

## Execute vs read intent for scripts

When SKILL.md mentions a script, state explicitly whether Claude should run it or read it:

- "Run `scripts/validate.py <folder>`" — execute; output consumes tokens, the script body does not.
- "See `scripts/analyze.py` for the algorithm" — read as reference; the whole file enters context.

Most utility scripts are for execution. Reading is only for when the script is the reference material itself.
