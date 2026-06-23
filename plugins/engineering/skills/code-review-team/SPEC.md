# Code Review Team — Specification

This is the running spec for the `code-review-team` skill. It captures decisions, requirements, behaviors, and open tensions established during design. Update this file as decisions evolve. SKILL.md is the executable orchestration; this is the human reference.

(Note: per skill-authoring guidance, a `README.md` inside a skill folder is disallowed. This file is the equivalent — the spec, the rationale, the open questions — for human readers.)

## Purpose

A multi-agent code review that runs specialized reviewers ("profiles") in parallel against a feature branch or work/task folder, then compiles their findings into a single review document.

The skill exists to:

- Catch problems no single reviewer catches alone (architecture, style, business rules, security all need different lenses).
- Produce findings the author can act on directly — code shown, fixes suggested, severity scoped.
- Surface gaps in documentation, conventions, product knowledge, and security controls — not only code defects.
- Serve as a learning surface for the human reviewer, not just the code author.

## Active profiles (4)

| Profile | Body | Checklist | Model | Output shape | When to use |
|---|---|---|---|---|---|
| **architect** | `profiles/architect.md` | `profiles/architect-checklist.md` (15 categories) | opus | Introduced / Exposed / Observed buckets + Critical / Major / Minor severity | grand review + complex backend tasks |
| **code-style-guide-expert** | `profiles/code-style-guide-expert.md` | conventions themselves are the checklist | sonnet | Block / Human Review / Suggestion | every review, one agent per applicable convention |
| **domain-expert** | `profiles/domain-expert.md` | `profiles/domain-expert-checklist.md` (19 categories) | opus | Block / Human Review / Suggestion | every business-logic task + grand review |
| **security-expert** | `profiles/security-expert.md` | `profiles/security-expert-checklist.md` (22 categories) | opus | Block / Human Review / Suggestion **plus** Critical / Major / Minor severity | grand by default; per-task only when explicitly requested |

Four other profiles (accessibility, designer, human-advocate, performance-expert) live in `profiles/archive/` for now — generic review lenses to be revisited after the four active ones are battle-tested.

## Shared profile spine

Every active profile follows the same section order:

1. When to use this profile
2. What the review is for
3. Context you receive
4. Output shape
5. How to approach the review
6. What NOT to flag
7. Profile-specific outputs (gaps + teaching moments where applicable)

Each profile declares its own context needs and (where useful) its own embedded prompt template, rather than SKILL.md imposing a uniform shape. Profiles are fundamentally different lenses; the spine is what stays consistent.

## Common patterns across profiles

- **Gap-finding is a first-class output**, not a footnote
  - architect → architecture-doc gaps (your project's architecture docs)
  - code-style-guide-expert → convention gaps (your project's convention / style-guide docs)
  - domain-expert → product-doc gaps (your project's product / business-knowledge docs)
  - security-expert → security-doc gaps (threat models, runbooks, auth-boundary docs)
- **Action states or buckets, not raw severity**, except where severity carries weight (security)
- **Known-gaps memory** — agent reads `memory.md` to skip already-flagged findings unless a change worsens them
- **Agent runs `git diff` itself** — no pre-computed diff is shoveled in
- **Teaching moments** — architect, domain-expert, and security-expert produce a learning appendix for the human reviewer (not the code author). code-style-guide-expert does not.

## Convention-exception protocol

A project-wide convention worth adopting alongside this skill: document it in your project's shared/general convention doc (wherever your conventions live).

When code deviates from a convention, the deviation must be declared with an inline comment:

```
// convention-exception: <convention-file-name> — <one-line reason>
```

- Deviation **without** the comment → Block
- Deviation **with** the comment → Human Review (a human judges whether the reason holds)

The code-style-guide-expert profile enforces this. If a project hasn't adopted the convention-exception convention yet, the reviewer raises it as a convention-gap Suggestion on first encounter.

## Finding format requirements (all profiles)

Every finding must be **thorough enough to act on without opening the file**. A finding is more than a one-liner.

### Required structure for each finding

1. **Header line** — action state (and severity for security), file path with line range or surface name, vulnerability/concern class
2. **What's there now** — show the actual code in a fenced code block, **labelled with the filename and line range directly above the block**. The reader should not have to open the file to understand the finding.

   *Example label*: `**What's there now** — backend/src/handlers/save.ts:42-50:`

   ```ts
   // current code copied verbatim
   const x = doSomething(req.body.input);
   ```

3. **Why it's a problem** — concrete reasoning, framed in the lens of the profile (architecture / convention / product / security)
4. **What to do instead** — show the suggested code in a fenced code block, **also labelled with the target filename and line range**. The label tells the author exactly where to apply the change.

   *Example label*: `**Suggested change** — backend/src/handlers/save.ts:42-50:`

   ```ts
   // proposed replacement
   const x = doSomething(validatedInput);
   ```

5. **If multiple options** — show each option in its own code block with a short note on the tradeoff between them
6. **Diagrams where they help** — ASCII or Mermaid, especially for architecture findings, state-machine findings, and security flows
7. **References** — link to the convention / rule / OWASP entry / product doc that grounds the finding, where applicable
8. **For Human Review findings** — include the existing justification (e.g. the `convention-exception` comment, or the existing test that suggests intent) and explain why a human must judge

### Why this matters

Thin findings ("line 42: missing await") get ignored or take five extra steps to act on. Thorough findings travel well: a non-author reviewing the document later understands the issue without context. The skill is a teaching surface as much as a defect surface — code blocks and diagrams make findings legible even months after the run.

## Output document structure

Each run produces one document in the work folder (or wherever the user specifies). Suggested name: `code-review-rev-N.md` where N starts at 1 and increments per run on the same feature.

Top-level structure:

```
# Code Review — <feature name> — Revision N

Date, scope (file count, profiles run), mode (per-task / grand)

## Summary
- Block count, Human-Review count, Suggestion count per profile
- The handful of findings that matter most (top 5–10)

## Findings by profile
### Architect
   ### Introduced
   ### Exposed
   ### Observed
   ### Architecture-doc gaps
   ### Teaching moments

### Code Style Guide Expert (one section per convention agent)
   ### Block
   ### Human Review
   ### Suggestion (convention gaps)

### Domain Expert
   ### Block
   ### Human Review
   ### Suggestion (product-doc gaps)
   ### Teaching moments

### Security Expert
   ### Block — Critical
   ### Block — Major
   ### Block — Minor
   ### Human Review
   ### Suggestion (security-doc gaps)
   ### Teaching moments

## Files marked not-relevant
List of changed files each profile chose not to review, with reason.

## Memory updates proposed
Findings the reviewer suggests promoting to memory.md (false-positive pattern, calibration adjustment, etc.).
```

Each finding inside these sections follows the thorough format above (current code block + suggested code block + reasoning + references + diagrams when useful).

## Run modes

- **Per-task review** — runs after a single `task-NN.md` is implemented. Lighter team: code-style-guide-expert always; domain-expert when business logic is touched; architect when complex backend; security-expert only on explicit request.
- **Grand review** — runs after all tasks in a feature are complete, before merge. Full team: all four active profiles run.

The skill should accept the mode as input or infer it from the work folder state (e.g. all tasks marked complete = grand review).

## Memory

Single `memory.md` at the skill root, used by all profiles. Each profile reads only entries scoped to its lens (entries should be prefixed with the profile name or live in profile-named subsections).

Memory holds:

- False positives confirmed by the human across runs
- Severity / action-state calibration adjustments
- Recurring convention / doc / product gaps that have been *consciously deferred* (so the reviewer stops re-flagging them every run)

Memory does NOT hold:

- One-off findings from a specific feature
- Project-specific architecture notes (those belong in your project's architecture docs)
- Conventions (those belong in your project's convention / style-guide docs)

## Open tensions

These are decisions that have working defaults but should be re-examined after the skill has run on real reviews:

1. **Repetition memory shape** — the architect can re-flag the same architecture-doc gap on every run. Default: read memory.md, skip already-logged gaps unless the current change worsens them. Need to verify this works in practice.
2. **Subsystem vs repo scope** — when architect explores beyond the diff, how far? Default: agent decides; in practice we may need to cap at the subsystem containing the diff.
3. **Per-task profile selection** — how SKILL.md decides which profiles to run for a per-task review. Currently each profile self-declares "When to use this profile" — orchestrator reads those sections. This needs a real test run to validate.
4. **Cross-repo skill sync** — the skill lives in your Claude Code config (e.g. `~/.claude/` or a plugin), while the conventions it references live in project repos. If you maintain multiple repos, you'll need a strategy to keep convention references aligned.
5. **Output filename collision** — when multiple revisions run on the same feature, default `code-review-rev-N.md` increments. SKILL.md needs to detect existing files and pick the next N.
6. **Run-mode detection** — should SKILL.md infer per-task vs grand from work-folder state, or always require an explicit input? Default: input-driven, but with a heuristic fallback.

## Process improvements established during design

- **Voice-first interview shape** for new profiles: goals → ground truth → scope → context → output → when-to-use. Used for architect, code-style-guide-expert, domain-expert, security-expert. Worth keeping when adding more profiles.
- **Wide brainstorm before checklist** — for any profile that needs a checklist, brainstorm broadly first (the way we did 15 categories for architect, 19 for domain, 22 for security), then prune. Don't start with a small list and grow it.
- **Each profile owns its prompt template** — profiles vary too much for a single SKILL.md template. Profile body declares what context it needs and (optionally) how it wants to be addressed. SKILL.md is the dispatcher, not the prompter.

## Files in the skill

```
code-review-team/
├── SKILL.md                                  # orchestrator
├── SPEC.md                                   # this file
├── memory.md                                 # cross-run memory
└── profiles/
    ├── architect.md
    ├── architect-checklist.md
    ├── code-style-guide-expert.md
    ├── domain-expert.md
    ├── domain-expert-checklist.md
    ├── security-expert.md
    ├── security-expert-checklist.md
    └── archive/
        ├── accessibility.md
        ├── designer.md
        ├── human-advocate.md
        └── performance-expert.md
```
