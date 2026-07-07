## Running a skill — or one step of it — in a subagent

A subagent runs in its own isolated context: it does not see the conversation history, and
its result is summarized back to the caller. Two patterns matter for skill authoring.

## Contents

- `context: fork` — run the whole skill in isolation
- Picking the agent type
- Using a subagent for one step of a skill
- When isolation helps (and when it hurts)
- Source

## `context: fork` — run the whole skill in isolation

Add `context: fork` to frontmatter to run the skill in a fresh subagent. The rendered
SKILL.md content becomes the subagent's prompt.

```yaml
---
name: deep-research
description: Researches a topic thoroughly across the codebase. Use when the user asks for a deep dive on how something works.
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find the relevant files.
2. Read and analyze them.
3. Summarize findings with specific file references.
```

This only makes sense when the skill contains an actual **task**. A skill that is pure
reference material ("use these conventions") has nothing for the subagent to *do* — it
returns without meaningful output. Forked skills are task skills, not knowledge skills.

## Picking the agent type

The `agent` field chooses the execution environment (system prompt, tools, permissions):

- `Explore` / `Plan` — read-only, small context; they skip CLAUDE.md and git status, so the
  subagent sees essentially only the skill content. Good for research and planning.
- `general-purpose` — full tool access; the default when `agent` is omitted.
- Any custom subagent defined in `.claude/agents/`.

## Using a subagent for one step of a skill

A skill that itself runs inline can still **dispatch a subagent for a single step** — useful
when that step needs a clean context or independent judgment. Instead of forking the whole
skill, the body instructs the model to spawn a subagent and hand it a brief.

Two cases this skill uses:

- **Auditing a draft for necessity.** Spawn a subagent, give it `agents/necessity-auditor.md`
  as its instructions plus the path to the skill under review. A fresh context judges the
  draft on its own merits, without the authoring conversation biasing it toward "every line I
  wrote is needed."
- **Running an eval.** Each eval run starts from a clean context so the result reflects only
  what the SKILL.md says, not leftover state from authoring it. One subagent per run gives
  that isolation for free. See `evaluating.md`.

When you dispatch a step like this, give the subagent three things: the brief (the agent
file), the target path, and exactly what to return.

## When isolation helps (and when it hurts)

- **Helps:** independent judgment (audits, reviews), clean-context evals, large read-heavy
  work you don't want crowding the main context.
- **Hurts:** anything that needs the conversation so far. The subagent can't see it, so a
  step that depends on what was just discussed should stay inline.

## Source

Claude Code skills docs — "Run skills in a subagent": https://code.claude.com/docs/en/skills
