---
name: create-plan-task
description: Create one implementation task in a plan-prep work folder. Writes a `task/task-NN.md` file with the full Context / Implementation / Verification / Post verification tasks structure, and inserts an entry in `task/task-list.md`. Invoked by `plan-prep` (Phase 2) during initial breakdown AND standalone when new bugs or scope arise mid-execution. Triggers on "add a task", "new task", "another task to the plan", "create plan task", or "/create-plan-task".
argument-hint: "[optional: work folder path] [optional: short task description]"
---

# Create Plan Task

Produce one well-formed implementation task in an existing plan-prep work folder.

The task file follows the same four-section structure used everywhere in the project (`## Context` / `## Implementation` / `## Verification` / `## Post verification tasks`), with checkbox progress tracking and inline QA cases.

## Inputs

- **First positional arg (optional):** path to the work folder (or to any file inside it — use the parent directory). If omitted, the skill auto-detects the work folder from uncommitted git changes (see "Resolving the work folder" below).
- **Second positional arg (optional):** short description of the task. Used as a seed for the clarifying conversation.

The work folder must already contain `plan-prep.md` and `task/task-list.md` — this skill does not bootstrap a plan from scratch.

## Resolving the work folder

If the user did not pass a work folder path, auto-detect:

1. Run `git status --porcelain` from the repo root.
2. Collect all changed paths under `a-works/` (`A`, `M`, `??`, `MM`, `AM` — any status).
3. For each unique top-level work-folder candidate under `a-works/` (typically `a-works/<area>/<feature>/`), check whether it contains both `plan-prep.md` and `task/task-list.md`. Only directories that satisfy BOTH count as candidates.

   Implementation hint: in this repo, work folders sit at depth 3 (e.g. `a-works/scheduling/prod-156-scheduling-bug-fixes/`). For each changed path, walk up its ancestors until you find one that contains `plan-prep.md` + `task/task-list.md`. Dedupe.

4. **Exactly one candidate** → use it. Tell the user one line: "Using work folder: `<path>` (auto-detected from uncommitted changes)."
5. **Zero candidates** → ask the user:
   > "I can't find a plan-prep work folder in uncommitted changes. Which work folder should I add the task to? (e.g. `a-works/<area>/<feature>/`)"
6. **More than one candidate** → ask the user to pick:
   > "Multiple work folders have uncommitted changes:
   > - `a-works/...`
   > - `a-works/...`
   >
   > Which one?"

Never guess when there are zero or multiple candidates. Never search outside `a-works/` — that's where work folders live in this repo.

## Modes

This skill has two invocation modes. Detect mode from how the skill was invoked:

| Mode | How it's invoked | task-list.md behavior |
|------|------------------|------------------------|
| `from-plan-prep` | Called by `plan-prep` (Phase 2 of `how-does-the-work-break-down.md`). The caller passes a marker like "mode: from-plan-prep" in the invocation message. | The task-list.md entry already exists (Phase 1 wrote the full wave structure). **Do not insert a new entry.** Only create the `task-NN.md` file. |
| `standalone` | Default. User invokes the skill directly mid-execution to add a new task (newly-found bug, scope shift, etc.). | The task-list.md entry does not exist. **Insert it after the last `- [x]` line in the `## Tasks` section**, under a `### Wave N — Added during execution` heading (create the heading if missing). |

## Output

- `{work-folder}/task/task-NN.md` — the new task file. `NN` is zero-padded to 2 digits (3 digits if there are already ≥100 tasks).
- `{work-folder}/task/task-list.md` — updated only in `standalone` mode.

## Prerequisites

Verify before starting:

1. `{work-folder}/plan-prep.md` exists. If not:
   > "I can't add a task without a `plan-prep.md` in this work folder. Run the `plan-prep` skill first to establish requirements, landscape, and flow."
2. `{work-folder}/task/task-list.md` exists. If not:
   > "There's a `plan-prep.md` but no `task/task-list.md` yet. Run `plan-prep` to completion first — it produces the task list shell."
3. `{work-folder}/task/` directory exists.

## Process

### Step 1 — Compute the next task number

Scan `{work-folder}/task/` for existing `task-NN.md` files (including any final-validation tasks like Grand Code Review / Grand QA / Write Work Review Guide). The next task number is `max(existing) + 1`, zero-padded.

**Caveat for standalone mode:** if the work folder already has Grand Code Review / Grand QA / Write Work Review Guide tasks at the end (e.g. `task-05.md`, `task-06.md`, `task-07.md`), the new task takes the next number (`task-08.md`), and the **task-list.md entry must be inserted BEFORE the Final Validation block** so the Final Validation tasks still run last. The skill keeps the existing final-validation filenames as-is — do not renumber.

In short:
- New filename: `task-{next}.md` (next = max of all existing + 1)
- Position in task-list.md (standalone mode only): after the last `- [x]` line, but always before the `### Final Validation` heading

### Step 2 — Read context

Read whichever of these exist (skip silently if absent):

- `{work-folder}/plan-prep.md` — feature understanding, flow diagrams, similar files
- `{work-folder}/architecture-decisions.md` — settled architectural calls
- `{work-folder}/requirements.md` — acceptance criteria
- `{work-folder}/task/task-list.md` — existing task names + waves (to phrase dependencies correctly)
- `{work-folder}/code-review.md` — if the standalone task is a code-review follow-up
- `{work-folder}/qa.md` — if the standalone task is a QA follow-up
- Design artifacts referenced by `plan-prep.md` (`design-discovery-result.md`, `view-model-props.md`, etc.)

You only need to skim — the detailed reading is done by the subagent in Step 4.

### Step 3 — Clarify with the user (skip when obvious)

Default behavior is **conversational, not scripted**. Decide whether discussion is needed.

**Skip discussion entirely** when:
- Mode is `from-plan-prep` AND the caller already gave you a clear task name, agreed signature, paths, tests, and QA cases (Phase 2 Step 2 of `how-does-the-work-break-down.md` happened upstream).
- Mode is `standalone` AND the user provided a second positional argument that's specific enough (file paths, expected behavior, test scenarios).

**Have a brief discussion** otherwise. Ask only what's actually ambiguous:

- What's the task's one-line name?
- Which files get created / modified / deleted?
- What's the function/component signature (inline types)?
- What's the input → paths-of-logic → output?
- Which tests need to exist? (behaviors + example inputs, not assertions)
- Which QA cases? (happy path, edge cases, accessibility for UI)
- What does it depend on? Does anything depend on it?

Don't follow a rigid script. Stop asking when you have enough to write the task file. **Don't ask questions you could answer yourself from the context files.**

### Step 4 — Dispatch a subagent to write the task file

Use the `Agent` tool (general-purpose subagent). The subagent does the heavy reading (conventions, SOPs, similar files) so it doesn't pollute your context.

Follow the subagent prompt pattern in `task-template.md`. The template file also contains:
- The exact four-section task file structure with all sub-headings
- The Interface Contracts / Tests-What-to-Test / QA Cases how-tos
- The rules the subagent must follow
- The reset rule for `## Verification` when `## Post verification tasks` items are added

### Step 5 — Verify the returned task file

Open the file. Confirm:

- Four top-level sections present in order: `## Context`, `## Implementation`, `## Verification`, `## Post verification tasks`
- `## Context` has Why / Current State / Desired State + Files / Depends on / Read for Context / Similar Files / Conventions blocks
- `## Implementation` has Interface Contracts, then `Tests (What to Test)` as `- [ ]` checkboxes, then `Steps` as `- [ ]` checkboxes
- `## Verification` has four subsections (`### Automation tests`, `### Code review`, `### QA`, `### Others`) — each with task-specific `- [ ]` checkboxes. A subsection may be omitted ONLY if truly non-applicable (e.g. no QA for an internal-only refactor); never leave it as a placeholder.
- `## Post verification tasks` exists as a placeholder with the Code Review follow-ups / QA follow-ups structure and the reset-rule note
- Every actionable item is a `- [ ]` checkbox (not a numbered list, not a plain bullet)
- QA cases (when present) are inline in full detail (preconditions, numbered steps, expected, single `- [ ] Pass` checkbox), not linked out to `qa.md`
- Paths are project-relative (except skill paths under `/Users/abtinghods/.claude/skills/`)

If any of the above is missing, send the subagent a targeted follow-up to fix only that gap. Do not rewrite the whole file.

### Step 6 — Update task-list.md (standalone mode only)

In `from-plan-prep` mode, **skip this step** — the entry already exists.

In `standalone` mode:

1. Read `{work-folder}/task/task-list.md`.
2. Find the **last** `- [x]` line inside the `## Tasks` block. This is the insertion anchor.
3. Find the `### Final Validation` heading (or equivalent — `### Final Validation (auto-added, run last)`, etc.). If the anchor is below it, fall back to inserting immediately before the Final Validation heading.
4. Check whether a `### Wave N — Added during execution` heading already exists between the anchor and Final Validation.
   - **If yes:** append the new bullet at the end of that section's list.
   - **If no:** create a new section right after the anchor (and before Final Validation):

     ```markdown
     ### Wave N — Added during execution

     - [ ] [Task NN: Name](task-NN.md) — [one-line description] [depends on: Task XX / "none"]
     ```

     where `N` is one greater than the highest existing wave number in the file.
5. Use the Edit tool to perform the insertion. Preserve all surrounding formatting.

If no `- [x]` lines exist (no task is checked yet), insert the section immediately after the very last wave block, still before Final Validation.

### Step 7 — Report back

End with a terse summary:

- New task: `task-NN.md` — [one-line name]
- Inserted in: `task-list.md` § Wave N (standalone) / pre-existing entry (from-plan-prep)
- Next: "Run the task with `executing-single-plan-task` skill" (standalone) / return control to plan-prep (from-plan-prep)

## Delegated Tools & Skills

| Tool / Skill | Used for |
|--------------|---------|
| `Agent` (general-purpose subagent) | Heavy reading + writing the task file (Step 4). Keeps main thread context clean. |
| `manual-qa-case-writing` patterns | The inline QA cases in `### QA` follow this skill's 6-field format — see `task-template.md`. |
| Edit tool | task-list.md insertion (Step 6). |

## Rules

- **One task per invocation.** If the user describes multiple tasks, ask which to do first; do not bulk-create.
- **Never bootstrap a plan.** This skill assumes `plan-prep.md` + `task/task-list.md` already exist. Send the user to `plan-prep` if not.
- **Don't ask scripted questions.** Have a brief, targeted conversation only when the task is genuinely ambiguous. The point of having `plan-prep.md` is so the skill can pull most context from there.
- **Don't renumber existing tasks.** New tasks always take the next integer. Even if Final Validation tasks (`task-05`, `task-06`, etc.) are already numbered higher, the new task gets the next number — only the task-list.md ordering changes.
- **Stay surgical with task-list.md.** Insert one new section or one new bullet. Don't reformat the rest of the file.
- **Subagent does the writing.** Main thread orchestrates and verifies; subagent reads conventions/SOPs and writes `task-NN.md`. Same pattern as `plan-prep` Phase 2.
- **Verify before reporting done.** Open the file, run the Step 5 checklist. Failed checks → targeted follow-up subagent message, not a rewrite.

## Common Mistakes

- Asking the user for a work folder path before trying to auto-detect from `git status` (run the resolver first; only ask if zero or multiple candidates)
- Defaulting to the most-recently-modified work folder when multiple candidates exist (ask instead — picking silently hides intent)
- Bootstrapping a fresh plan when no `plan-prep.md` exists (refuse instead)
- Writing the task file directly from the main thread instead of dispatching the subagent
- Skipping Step 5 verification because "the subagent's summary said it's done"
- Renumbering existing Final Validation tasks to push them to the bottom (don't — they keep their numbers; only the task-list.md ordering puts them last)
- Inserting the new entry at the very bottom of task-list.md (below Final Validation) — Final Validation must always run last
- Asking the user a script of questions when the answer is already in `plan-prep.md`
- Updating task-list.md in `from-plan-prep` mode (causes duplicate entries)
- Numbered lists (`1.`, `2.`) or plain bullets for actionable items — every actionable item is `- [ ]`

## Files

- `SKILL.md` — this file
- `task-template.md` — the exact four-section template, subagent prompt pattern, and how-tos
