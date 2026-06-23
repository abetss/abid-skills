---
name: code-review-team
description: Runs a multi-agent code review on a feature branch or task folder. Spawns specialized reviewers (architect, code-style-guide-expert, domain-expert, security-expert) in parallel and compiles their findings into a single thorough review document with current/suggested code blocks per finding. Use when reviewing a feature branch, PR, changed files, or a task/work folder, when the user says "review this", "code review", "run code review", "review the branch", "review the task", "review the changes", or "run the review team", and when verifying changes before merge after an implementation skill finishes.
---

# Code Review Team

Multi-agent dispatcher that runs the four active expert profiles (`profiles/*.md`) in parallel against a feature's diff and compiles their findings into one document. Profiles own their own prompts and context shape; this skill selects which profiles run, wires per-agent context, spawns them, and merges the output.

The canonical specification lives in `SPEC.md`. When this file and `SPEC.md` disagree, `SPEC.md` wins — fix `SKILL.md`.

## Precondition: Agent tool required

This skill **must** run from a context that has the `Agent` tool. Without `Agent` you cannot dispatch parallel reviewer subagents — and the per-profile parallel design is the whole point of the skill. A linear inline review against the rubric is **not** a valid fallback; it loses lens isolation and tends to skim.

**Before doing anything else, check:**

- Are you the user's main thread (the supervisor)? You have `Agent`. Proceed.
- Are you a subagent (someone called you via `Agent({subagent_type: ...})`)? You almost certainly DO NOT have `Agent`. **STOP.** Return to your caller with: "I cannot run `code-review-team` from a subagent context — the parallel-dispatch primitive is not available here. Surface this back to the supervisor (or the user); they should run the skill themselves in their own context, or start a fresh `claude code` session for it."

Do NOT silently fall back to inline review. Inline review is the per-task implementer's job; it is not what this skill produces.

## Memory

Read `memory.md` in this directory before starting. It holds cross-run false positives, accepted trade-offs, calibration notes, and deferred gaps that reviewers should not re-flag.

### Reading memory

Before launching agents, scan `memory.md` for entries scoped to each selected profile (entries are prefixed with the profile name). Pass each profile's slice of memory into its agent prompt so the reviewer skips known false positives, applies calibrated severities, and avoids re-flagging consciously deferred gaps.

### Writing to memory

After the human reviews the output document, ask whether any findings belong in memory. Add only entries that:

- The human explicitly confirmed as false positive, calibration, accepted trade-off, or deferred gap
- Are reusable across features (not tied to one feature's code)

Do NOT capture: one-off feature findings, project conventions (those belong in your project's convention/style-guide docs, wherever they live), architecture notes (those belong in your project's architecture docs), or product knowledge (those belong in your project's product/business-knowledge docs).

## Inputs

- **Work folder path** *(optional)* — if your project uses a per-feature work folder (the planning skills in this plugin use a `task/` subfolder with `task-list.md` and `task-NN.md` files), point the skill at it. It may also contain prior `code-review-rev-N.md` files. When no work folder is provided, review the feature branch / diff directly.
- **Run mode** *(required, inferred if absent)* — `per-task` or `grand`. If the user doesn't specify, infer from the work folder: all tasks marked complete in `task-list.md` → `grand`; otherwise `per-task`. (With no work folder, default to `grand` for a whole-branch review.) **Always confirm the inferred mode with the user before proceeding.**
- **Profile override** *(optional)* — explicit list of profile names to run, overriding the default selection rules. Use only when the user names them.
- **Output filename** *(optional)* — defaults to `code-review-rev-N.md` in the work folder (or the repo root if there is no work folder), where N is the next integer above any existing `code-review-rev-*.md` (start at 1).

## Workflow

1. **Validate inputs and confirm mode.** If a work folder is provided, check it exists (and, if your project uses the convention, contains a `task/` subfolder). Infer mode if not given; confirm with the user. Determine output filename (auto-increment N).
2. **Discover active profiles.** List `profiles/*.md` excluding `*-checklist.md` and anything under `profiles/archive/`. The current four are `architect.md`, `code-style-guide-expert.md`, `domain-expert.md`, `security-expert.md`.
3. **Select profiles to run.** For each active profile, read its `## When to use this profile` section and apply the rule against this run's mode and diff. Defaults below in *Profile selection*.
4. **Read memory.** Slice `memory.md` per profile.
5. **Wire context per profile.** Each profile's `## Context you receive` section declares what it needs. Resolve those (paths, files, task references) per agent — do not impose a uniform context shape. Pass the diff metadata (file list); the agent runs `git diff` itself for full content.
6. **For code-style-guide-expert: enumerate one agent per matching convention OR rule doc.** Conventions can live in two equally authoritative places, and the reviewer must walk **both** if the project uses them:

   - **Convention / style-guide docs** — wherever your project keeps them (e.g. a `docs/conventions/` tree, a style guide, ADRs). If those docs carry a `domain` / scope marker in frontmatter or a heading, match it against the changed file paths.
   - **Project rule docs** — e.g. `.claude/rules/*.md` (and per-package `*/.claude/rules/*.md`) if your project has them. Match each rule's `When:` glob (declared in the rule's frontmatter or first heading) against the changed file paths.

   Spawn **one code-style-guide-expert agent per matching doc** (whether convention or rule — pick whichever applies; if a file matches both a convention and a rule, both agents run, each in its own lens). Each agent gets exactly ONE doc plus the files in scope for that doc's domain/glob. Do NOT pass a bundle of conventions+rules to a single agent — the parallel design exists precisely to keep each lens narrow.

   If the project has no convention or rule docs, or none match the diff (rare — typically only build/config changes), skip code-style-guide-expert for this run and note that in the review document. Do NOT inline-skim the diff as a token gesture.
7. **Spawn all selected agents in a single parallel wave** as `code-reviewer` subagents (architect findings use the `code-architect` subagent). Each prompt includes: the profile body, the profile's checklist (if one exists), the profile-specific context, the relevant memory slice, the run mode, and the output-filename context.
8. **Collect findings.** As each agent returns, validate that every finding follows the profile's required format — header line, filename+line-labelled "What's there now" code block, reasoning, filename+line-labelled "Suggested change" code block, references where applicable. Push back on the agent (resume) if findings are too thin.
9. **Compile the review document** at the chosen output path, following the structure in `SPEC.md` → *Output document structure*. Do not dedupe across profiles by default — the same line flagged from two lenses is two valid findings; collapse only when both findings come from the same lens.
10. **Surface a terse summary to the user**: counts per state per profile, top 5–10 findings, and the output path.
11. **Prompt for memory updates** after the user reviews the document. Write only confirmed entries to `memory.md`.

## Profile selection (defaults)

Always run on grand review unless the profile body says otherwise. Per-task selection follows each profile's `## When to use this profile` rule:

- **code-style-guide-expert** — runs every review, per-task and grand. One agent per matching convention or rule doc (see Step 6 — convention/style-guide docs AND project rule docs are both first-class sources).
- **architect** — runs on grand review and on per-task when the diff includes backend/handler/schema files (e.g. files under `backend/**`, database schema files, files under `*/handlers/`, `*/services/`, `*/jobs/`, `*/queues/`, access-control / authorization policies — adapt these globs to your repo). Skips frontend-only diffs.
- **domain-expert** — runs on grand review and on per-task when the diff touches business logic — calculations, state transitions, workflows, validation, user-facing flows, or privacy/compliance-sensitive data handling. Skips pure UI tweaks, pure refactors, build/config changes.
- **security-expert** — runs on grand review by default. On per-task only when the user explicitly requests it, or when the task touches auth, sessions, tokens, access-control / authorization policies, new endpoints/middleware, third-party integrations, file uploads, or input that reaches a database/shell/template.

If the user supplies an explicit profile override, use that list verbatim and skip the rule application.

## Convention scoping (code-style-guide-expert)

For each convention doc in your project's convention/style-guide tree:

- If the doc declares a `domain` / scope field (in frontmatter or a heading), read it and match changed files accordingly. *For example*, in a frontend/backend split: a `frontend` doc → match changed files under `frontend/**`; a `backend` doc → match changed files under `backend/**`; a `shared` doc → match all changed files. Adapt these example scopes and globs to your repo's layout.
- If the convention has no matching changed files, skip it (don't spawn an agent for it).

If a `task/` folder is provided, prefer convention references found in `task/task-list.md` and `task-NN.md` (typically under a `## Context` → conventions/rules section) as the seed list. Always union with conventions whose scope matches changed files; the seed list is a hint, not a cap.

If more than ~10 changed files fall under one convention, split into two agents along a natural boundary (e.g. the frontend vs backend split) so each agent's context stays manageable.

## Agent prompt shape

Each profile owns its own prompt structure. The orchestrator does not impose a uniform template. The prompt to each `code-reviewer` subagent should include, in order:

1. The profile body content (`profiles/<profile>.md`) verbatim — this declares its own goal, output format, and context expectations.
2. The profile's checklist content (`profiles/<profile>-checklist.md`) verbatim, if one exists.
3. The profile-specific context resolved in step 5 of the workflow (file list, task file paths, schema path, etc. — whatever the profile's "Context you receive" section requested).
4. The relevant `memory.md` slice for this profile.
5. The run mode (`per-task` or `grand`) and a short note on why this profile was selected.
6. Instructions to return findings in the profile's declared output shape, with every finding meeting the *Finding format requirements* in `SPEC.md` (filename+line-labelled current/suggested code blocks, reasoning, references).

For the code-style-guide-expert, also include: the single assigned convention doc verbatim, and the list of changed files in scope for that convention's domain.

## Output document

Write the compiled findings to the chosen output path (default `code-review-rev-N.md` in the work folder). Follow the structure in `SPEC.md` → *Output document structure*. Required sections:

- `# Code Review — <feature> — Revision N` with date, scope, mode
- `## Summary` — counts per profile, top 5–10 findings
- `## Findings by profile` — one section per profile, using the profile's declared bucket structure (architect: Introduced/Exposed/Observed; style-guide/domain: Block/Human Review/Suggestion; security: Block/Human Review/Suggestion **plus** Critical/Major/Minor)
- `## Files marked not-relevant` — what each profile chose not to review and why
- `## Memory updates proposed` — candidate entries for `memory.md` pending human confirmation

Each finding follows the `SPEC.md` *Finding format requirements*: header line, **What's there now** block labelled with `<filename>:<line-range>`, reasoning, **Suggested change** block also labelled, references / diagrams / alternatives where useful.

## Open tensions

These are working defaults — re-examine after real runs. See `SPEC.md` → *Open tensions* for the full list.

- **Repetition across runs** → read `memory.md` deferred-gaps entries and skip them unless the current change worsens them.
- **Architect exploration scope** → pass-through; the architect profile decides. SKILL.md does not cap.
- **Per-task profile selection** → driven by each profile's `## When to use` section + the rules above. Validate against real runs.
- **Output filename collision** → auto-increment `code-review-rev-N.md` from existing files in the work folder.

## Files in this skill

```
SKILL.md          # this file — orchestrator
SPEC.md           # canonical spec, decisions, rationale
memory.md         # cross-run memory shared by all profiles
profiles/
  architect.md
  architect-checklist.md
  code-style-guide-expert.md
  domain-expert.md
  domain-expert-checklist.md
  security-expert.md
  security-expert-checklist.md
  archive/        # four inactive profiles, do not run
```
