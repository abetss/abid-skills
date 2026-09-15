---
name: executing-single-plan-task
description: When executing a single task from a task/ folder (produced by plan-prep) with full context, following all steps and verifications
---

# Executing a Plan Task

## Overview

Execute ONE task from a `task/` folder. Read the task's context, follow its Implementation steps exactly, run every Verification check, and report completion.

**Core principle:** One task at a time, with quality gates at the end.

**Announce at start:** "I'm using the executing-single-plan-task skill to implement this task."

## Inputs

The user provides either:
- **Path to a work folder** — the skill opens `{work-folder}/task/task-list.md` and asks which task, or reads the first `[-]` in-progress task, or reads the first `[ ]` pending task, in that priority order, OR
- **Path to a specific task file** — `{work-folder}/task/task-NN.md`

Either way, the skill resolves:
- `task-list.md` path (for marking status)
- `task-NN.md` path (the task to execute)
- `walkthrough.md` path in the same work folder (created if missing, for documenting significant decisions across tasks)

---

## The Process

### Step 1: Load and Review

1. Read `task/task-list.md` — understand the whole feature, dependencies, and which wave this task belongs to
2. Read the target `task/task-NN.md`
3. Read `walkthrough.md` if it exists — pick up context from previously completed tasks
4. Review critically — identify any questions or concerns
5. If concerns: raise them with your human partner before starting
6. If no concerns: proceed

---

### Step 2: Review Task Before Starting

Before executing, review the task and confirm understanding:

1. **Read all context specified in the task's `## Context` section:**
   - Files listed under `Read for Context`
   - Files listed under `Similar Files`
   - Convention / SOP / Skill / Rule files listed

2. **Summarize understanding (to yourself, not to the user unless asked):**
   - Why (business reason)
   - Current State → Desired State delta
   - Files to create/modify/delete
   - Patterns to follow (from similar files)

3. **If concerns:** Raise them before starting
4. **If clear:** Mark task as in progress and proceed

5. **Mark task as in progress in `task-list.md`:**
   - Change `- [ ] [Task NN: ...](task-NN.md)` to `- [-] [Task NN: ...](task-NN.md)` in the wave list

---

### Step 3: Execute the Implementation Section

The task's `## Implementation` section has three parts. Follow them in order.

**Checkbox convention:** Every `- [ ]` item in `Tests (What to Test)` and `Steps` is a tracked unit of work. Before starting an item, change `- [ ]` to `- [-]` (in progress). When complete, change `- [-]` to `- [x]`. Do not mark `[x]` until the work is actually done.

1. **Interface Contracts** — Use the function signature and path comments as the shape of what to build. This is a code block, not a checklist — don't deviate without documenting why.
2. **Tests (What to Test)** — For each `- [ ]` item: mark `- [-]`, write that test following the pattern from the Similar Files in Context, mark `- [x]`.
3. **Steps** — For each `- [ ]` step: mark `- [-]`, do it, mark `- [x]`. Execute the steps in order.

Every checkbox under `## Implementation` must be `- [x]` before moving to Step 4.

---

### Step 4: Run the Verification Section

The task's `## Verification` section has four subsections. Each is a gate — fail any and the task is not complete.

```
## Verification

### Automation tests
- [ ] [task-specific test runs]

### Code review
- [ ] Run `code-style-reviewer` with exactly one assignment using role `reviewer-junior` over every file changed by this task

### QA
**Case 1: [title]**
- ... steps ...
- [ ] Pass

### Others
- [ ] [biome, type-check, other commands]
```

**Rules:**

1. **Reset before starting.** Before running ANY verification, reset ALL checkboxes in the `## Verification` section of this task's file to `- [ ]`. This ensures you're verifying the CURRENT code, not a previous state.

2. **Use the three states.** `- [ ]` = queued, `- [-]` = running now, `- [x]` = passed. Move each item through the states as you run it. Don't skip the `[-]` state for long-running checks — it's how interrupted work gets resumed without confusion.

3. **Check only when verified.** Mark `- [x]` ONLY after the check actually passes. If it fails, it stays `- [ ]` (or goes back to `- [ ]` from `- [-]`) and becomes a **BLOCKER** — fix the issue or report it.

4. **Reset on ANY code change.** If a code review finding or QA bug requires you to modify files, reset ALL `## Verification` checkboxes back to `- [ ]` and re-run them ALL. A previous pass is meaningless after code changes.

5. **Reset when a Post verification task is added.** The moment you add a new item under `## Post verification tasks` — which happens whenever code review or QA surfaces something that needs fixing — reset ALL `## Verification` checkboxes to `- [ ]`. Work through the Post verification tasks (each moves `[ ]` → `[-]` → `[x]`), and only re-run `## Verification` once every Post verification task is `- [x]`.

6. **All must be checked to complete.** The task cannot be marked complete in `task-list.md` until every checkbox in `## Implementation`, `## Verification`, AND `## Post verification tasks` is `- [x]` simultaneously. No partial state allowed.

7. **QA uses the browser.** Every QA case in the `### QA` subsection with "Navigate to", "Click", or a URL path — use the `qa-execution` skill (which launches the `qa-runner` agent) to verify in a running browser. If the dev server is already running, use it. If it's NOT running, start it. If it crashes or won't start, that's a **BLOCKER** — fix the server issue yourself or report it. Do not skip browser verification or work around a broken server. There is no partial QA.

8. **Subagent dispatch contract.** Some task steps require dispatching a subagent via the `Agent` tool — work the task author intentionally wants run in a separate context.

   - If `Agent` IS in your tool list: dispatch as the task specifies; wait for the return; land findings; close the checkbox.
   - If `Agent` is NOT in your tool list (you are inside a subagent, or the harness disabled dispatch): do not work around it by running the dispatched work inline. Leave the checkbox `[ ]`, add a `## Post verification tasks` entry naming what needs dispatching (which subagent + scope), leave the task entry `[-]`, and state in your return summary that a step required dispatching a subagent, the tool was not available, and you left the task open.
   - Never substitute yourself for a dispatched subagent. The task asked for dispatch to get work done in a different context — running it inline defeats that.

   This skill does not assume what your caller will do with the surfaced blocker.

9. **Populate `## Post verification tasks` as work surfaces.** As code review and QA runs finish, append new `- [ ]` items with links into `code-review.md`, `qa.md`, or inline notes. Each new item triggers the Verification reset in rule #5. Work items through `[ ]` → `[-]` → `[x]`.

---

### Step 5: Report Completion

1. **Verify every checkbox in the task file is `- [x]`.** Scan each of these three sections and confirm NO `- [ ]` or `- [-]` remains:
   - Every item under `## Implementation` (Tests, Steps)
   - Every item under `## Verification` (Automation tests, Code review, QA Pass checkboxes, Others)
   - Every item under `## Post verification tasks` (Code Review follow-ups, QA follow-ups)

   If ANY checkbox is not `[x]`, you are NOT done. Go back to Step 3 or Step 4 as appropriate.

2. Report:
   - Files changed (created, modified, deleted)
   - Final status of all three checkbox sections (all `[x]`)
   - Items added to `## Post verification tasks` during execution and how each was resolved
   - Implementation notes (decisions made, any deviations from plan)
3. Mark task as complete in `task-list.md`: change `- [-] [Task NN: ...](task-NN.md)` to `- [x] [Task NN: ...](task-NN.md)`
4. Document in `walkthrough.md` (same folder as `task-list.md`):
   - Decisions made and why
   - Learnings discovered
   - Deviations from plan (if any)
   - Files created/modified
   (Only document significant items — skip if nothing notable.)

---

## When to Stop and Ask

**STOP immediately when:**
- Instruction is unclear or ambiguous
- Missing dependency or file not found
- Test fails and you don't know why
- Convention file conflicts with task instructions
- Edge case not covered in task
- Dev server not running or crashes during browser QA
- Browser QA reveals a bug that blocks verification
- A dependency task (`Depends on:` in `## Context`) is not yet marked `[x]` in `task-list.md`

**Ask for clarification rather than guessing.**

---

## Remember

- **Read context first** — Similar Files, Conventions, Skills before coding
- **Checkbox progression** — `- [ ]` (todo) → `- [-]` (in progress) → `- [x]` (done). This applies to every item in Implementation, Verification, and Post verification tasks, AND to the top-level task entry in `task-list.md`
- **Follow the task exactly** — Don't add features not in the task
- **Handle listed edge cases** — Everything in `## Context`'s Data Flow and in the QA cases must be covered
- **Run all verifications** — Don't skip checks, don't skip subsections
- **QA cases are inline** — They live in the task file, not in a separate qa.md
- **Adding a Post verification task resets Verification** — Any new item under `## Post verification tasks` means every `## Verification` checkbox goes back to `- [ ]` and must be re-run once the Post verification tasks are all `- [x]`
- **All three sections must be green to complete** — Implementation, Verification, and Post verification tasks must ALL be `[x]` simultaneously
- **Report honestly** — If something didn't work, say so
- **Document learnings** — Add significant decisions to `walkthrough.md`
- **One task only** — Don't start the next task without approval

## Common Mistakes

- **Looking for `plan-tasks.md`** — The format is now a `task/` folder with `task-list.md` + `task-NN.md` files
- **Mixing Implementation and Verification** — Implementation is what you build; Verification is what you run to confirm it works
- **Skipping a Verification subsection** — Code review is always required; Automation tests, QA, or Others may be absent only when the task deliberately omits them
- **Skipping context read** — Always read similar files and conventions first
- **Adding unlisted features** — Only implement what's in the task
- **Continuing after failure** — Stop and report if tests fail
- **Guessing on ambiguity** — Ask for clarification
- **Not updating `task-list.md`** — status must move `[ ]` → `[-]` → `[x]` as you progress

---

## Anti-Rationalization

These are excuses agents use to skip browser verification. None are valid:

- **"Tests pass, so it works"** — Unit tests verify logic, not wiring. A button with an empty `onClick` passes every test. Only a browser click catches it.
- **"The page renders"** — Rendering is not the same as functioning. A form that renders perfectly but submits to a no-op is a broken form.
- **"I'll verify at the end / during Grand QA"** — Each task's QA cases exist to catch bugs AT THAT TASK, not 15 tasks later when the cause is buried.
- **"Browser testing isn't in my verification checklist"** — If the `### QA` subsection says "navigate to", "click", "submit", or mentions a URL, it IS browser testing. Don't reinterpret it.
- **"The code looks correct"** — `handle_submit()` looked correct too. It was an empty function. Code review doesn't catch empty implementations that type-check.
- **"The server isn't running so I'll work around it"** — A broken server is a BLOCKER, not a workaround opportunity. Stop, fix it, then resume. There is no half-way QA.
