---
name: skill-creating
description: Creates and improves Claude skills — scaffolds folders, writes triggering descriptions, applies progressive disclosure, validates structure, and adds memory or templates. Invoke only via the `/skill-creating` slash command.
disable-model-invocation: true
---

# Skill Creating

Guide for authoring consistent, well-triggered, well-structured Claude skills.

## Rules

The constraints that decide whether a skill works — each links to its reference for detail and rationale.

1. **Caller-agnostic.** Nothing names or branches on what invokes the skill; pass runtime context as an argument or inject it with `` !`command` ``. See `references/description-writing.md`.
2. **Description = capability + when.** Lead with what it does, then "Use when ..." triggers; no implementation or caller names; lean, but keep the trigger signal. See `references/description-writing.md`.
3. **Declare arguments.** Inputs → `argument-hint` + named `arguments`, documented in the body. See `references/arguments-and-dynamic-context.md`.
4. **Reference arguments bare: `$name`.** Backticks render the literal label, not the value. See `references/arguments-and-dynamic-context.md`.
5. **Inject, don't hardcode.** A value computable at load time uses `` !`command` ``; hardcoded values rot. See `references/arguments-and-dynamic-context.md`.
6. **Every line earns its place.** Cut what doesn't change behavior; explain *why* over *how*. The `agents/necessity-auditor.md` audit enforces this.

**Structural rules:** `SKILL.md` (with `name:` + `description:`) is the only required file; the directory name must match `name:`; no `README.md` inside the skill folder; forward-slash paths only; relative markdown links, never `@path` force-loads; MCP tool references fully qualified (`ServerName:tool_name`); if a `## Memory` section exists, `memory.md` must exist beside it.

Full failure-mode catalog: `references/anti-patterns.md`.

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
- `references/arguments-and-dynamic-context.md` — declaring arguments, bare `$name` substitution, injecting live data
- `references/progressive-disclosure.md` — three-level loading model
- `references/folder-structure.md` — when to use `scripts/`, `references/`, `templates/`, `assets/`
- `references/subagents.md` — running a skill, or one step of it, in an isolated subagent
- `references/testing.md` — trigger tests and functional tests
- `references/eval-driven-development.md` — the opt-in build order: evals and a baseline *before* the docs
- `references/evaluating.md` — measuring output quality with baseline evals
- `references/script-quality.md` — only if the skill bundles executable scripts
- `references/anti-patterns.md` — failure modes to avoid
- `agents/necessity-auditor.md` — the line-by-line necessity audit brief

If the user is resuming a conversation where the skill intent is already clear, skip the interview step. Still read the relevant references.

## Process for a new skill

1. **Fetch canonical docs.** WebFetch both URLs in "Canonical sources" above. Scan for anything not already reflected in this skill's references.
2. **Capture intent.** Scan the current conversation for answers. Run the interview from `references/interview-questions.md` for what's missing. Pin down 2–3 concrete use cases in Trigger/Steps/Result form before writing files.
3. **Offer the build approach.** For a verifiable skill (objectively checkable output), ask the user whether to build it **eval-driven** — evals and a baseline first, then minimal instructions written to pass them — or **draft-first** (this process, evals offered at the end). If they opt into eval-driven, follow `references/eval-driven-development.md` to set up the baseline and cases now, then return here to draft. Skip the offer for subjective skills and small edits.
5. **Choose the name.** Apply `references/naming.md`. Confirm with the user.
6. **Draft the description.** Apply `references/description-writing.md`. Lead with the capability, then "Use when ...", then key trigger phrases. Third person, caller-agnostic. Confirm with the user.
7. **Decide arguments and dynamic context.** If the skill takes inputs, declare `argument-hint` + `arguments` and reference them bare in the body. If it needs live data, inject it with `` !`command` ``. See `references/arguments-and-dynamic-context.md`.
8. **Write trigger tests.** Draft 3 queries that should trigger the skill and 3 that should not (see `references/testing.md`). These double as a sanity check on the description.
9. **Scaffold the folder.** Either:
   - Run `python scripts/scaffold.py` for a guided interview, or
   - Copy `templates/basic-skill/` (or `templates/with-memory/`) and fill in placeholders
10. **Decide what lives where.** Apply `references/progressive-disclosure.md` and `references/folder-structure.md`. Only create subfolders you have real content for.
11. **Audit for necessity.** Dispatch the `agents/necessity-auditor.md` brief as a subagent over the new skill (see `references/subagents.md`). Apply the cuts that hold up — a fresh context catches bloat the author is blind to.
12. **Validate.** Run `python scripts/validate.py <skill-folder>`. Fix errors. Warnings are informational.
13. **Verify triggering.** Ask the user to open a fresh session and say *"When would you use the [skill name] skill?"* Claude should paraphrase the description and name the right trigger contexts. If it doesn't, the description is under-triggering — return to step 6.
14. **Offer evals.** If the skill wasn't built eval-driven, ask whether the user wants to measure output quality with baseline evals, and if so, pair on 2–3 realistic test prompts. Skip for purely subjective skills. See `references/evaluating.md`.
15. **Run the checklist.** Walk the `## Checklist` below end to end as the acceptance gate. Don't declare the skill done until every applicable line passes.

## Process for modifying an existing skill

1. Read the whole skill first — SKILL.md, memory.md, every reference and template. Understand the shape before changing anything.
2. Ask what's wrong: under-triggering, bad output, missing use case, overfit to a scenario?
3. Apply the smallest change that addresses the problem. Don't rewrite sections that are working.
4. Audit for necessity if the change added material — dispatch `agents/necessity-auditor.md` over the skill and apply the cuts that hold up.
5. Re-run `python scripts/validate.py <skill-folder>`.
6. If the change is substantive, offer to pair on evals to confirm it's an improvement (`references/evaluating.md`).
7. Walk the `## Checklist` below over the changed skill before declaring it done.

## Checklist — run every time a skill is created or changed

This is the acceptance gate, distilled from Anthropic's best-practices checklist plus this repo's house rules. Walk it before declaring any new or edited skill done — make a TodoWrite item per unchecked line and resolve each. `python scripts/validate.py <skill-folder>` auto-checks the items marked **(validator)**; the rest need judgment the linter can't apply. Skip the "Scripts" group if the skill bundles no executable code.

### Description & triggering

- [ ] Capability-first: opens with what the skill does, not "Use when ..." **(validator warns)**
- [ ] Includes a "Use when ..." clause naming concrete trigger phrases, keywords, file types, and contexts — pushy, not literal **(validator warns if absent)**
- [ ] Third person; no first-person or "you can" voice **(validator warns)**
- [ ] Caller-agnostic — names no caller and no before/after step; 10–1024 chars; no `<`/`>` **(validator)**
- [ ] No implementation detail (which files/tools it touches) crowding out the trigger signal

### Name & structure

- [ ] Name is lowercase kebab-case, matches the directory, no reserved (`claude`/`anthropic`) or vague (`helper`/`tool`/…) words; gerund for process skills, verb+noun for actions **(validator)**
- [ ] `SKILL.md` present with `name:` + `description:`; no `README.md` inside the folder; forward-slash relative links only, no `@path` force-loads **(validator)**
- [ ] Declared arguments have an `argument-hint` and are referenced bare as `$name`, never backticked **(validator warns)**
- [ ] MCP tools written fully qualified as `ServerName:tool_name`
- [ ] If a `## Memory` section exists, `memory.md` exists beside it **(validator)**

### Progressive disclosure & content

- [ ] SKILL.md body under ~500 lines; detail spilled into `references/` **(validator warns over 500)**
- [ ] References are one level deep from SKILL.md (no `SKILL.md → a.md → b.md` chains)
- [ ] Reference files over 100 lines open with a table of contents
- [ ] Each script's intent is stated as execute ("Run …") or read ("See … for the algorithm")
- [ ] No time-sensitive phrasing — legacy guidance lives in a collapsed "old patterns" section
- [ ] One term per concept throughout; no synonym drift
- [ ] Examples are concrete (real paths/inputs), not abstract
- [ ] Complex multi-step workflows give Claude a copyable progress checklist
- [ ] Only adds knowledge Claude lacks; every line changes behavior (run the `agents/necessity-auditor.md` audit)
- [ ] One default per choice point, with an escape hatch — not a menu of options

### Scripts (only if the skill bundles code)

- [ ] Scripts solve error conditions themselves rather than punting to Claude
- [ ] No voodoo constants — every magic value documents its rationale
- [ ] Validation/feedback loop for fragile or destructive operations (validate → fix → repeat)
- [ ] Failure messages name the problem and list valid options
- [ ] Required packages listed with install command; no assuming tools are installed

### Testing & evals

- [ ] 3 should-trigger and 3 should-not queries pass (`references/testing.md`)
- [ ] Fresh-session check done: "When would you use the [skill] skill?" paraphrases the intended trigger surface
- [ ] Tested on each model the skill will run on (Haiku/Sonnet/Opus) — terse enough for the strongest, complete enough for the weakest
- [ ] For verifiable skills: evals offered — ≥3 realistic cases run against a no-skill (or prior-version) baseline (`references/evaluating.md`)
- [ ] `python scripts/validate.py <skill-folder>` exits clean (errors fixed; warnings reviewed)

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

- `scripts/validate.py` — deterministic lint. Checks frontmatter, naming, description, arguments (hint present, declared args referenced bare as `$name`, not backticked), links, line count, memory consistency, forbidden files (like `README.md` in the skill folder), XML tags, Windows-style paths. Run on every skill before finishing. `python scripts/validate.py ~/.claude/skills/my-skill`
- `scripts/scaffold.py` — interactive interview that generates a new skill folder.

## Agents shipped with this skill

- `agents/necessity-auditor.md` — a brief to hand a subagent that audits a skill line-by-line for dead weight and returns a prioritized cut-list. Dispatch it over any skill before finishing; see `references/subagents.md`.

## Writing style

- Imperative, not MUST/NEVER in all caps.
- Explain *why* briefly where it matters.
- Only add knowledge Claude doesn't already know.
- Consistent terminology — pick one term per concept and stick to it.
- No time-sensitive phrasing ("after August 2025..."). Put legacy guidance in an "old patterns" collapsed section.
