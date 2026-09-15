# How Does the Work Break Down?

> Turn the plan into executable tasks — break down, detail, and equip each one for implementation.

## Need

Break the work into actionable tasks with clear dependencies, then give each task enough context, guidance, and reference material that the implementer can execute without re-discovering what was already learned during planning.

## Output Structure

All output is written to a `task/` folder inside the work folder:

```
{work-folder}/
  plan-prep.md               (written in earlier components)
  architecture/
    table-of-contents.md      (architecture decision index)
    ADR-NNN-short-title.md    (one file per material decision)
  task/
    task-list.md             (index: waves, dependencies, links)
    task-01.md               (one file per task, zero-padded)
    task-02.md
    task-03.md
    ...
    task-NN.md               (Grand QA)
    task-NN+1.md             (Write Work Review Guide)
```

**File naming rule:** Zero-pad task numbers to 2 digits (`task-01.md`, `task-12.md`). If there are more than 99 tasks, pad to 3 (`task-001.md`).

**Status convention:** Every actionable item — in `task-list.md`, in each task's `## Implementation`, `## Verification`, and `## Post verification tasks` sections — is a checkbox that progresses through three states:

- `- [ ]` — todo
- `- [-]` — in progress
- `- [x]` — done

Top-level task status lives in `task-list.md`. Per-item progress inside a task file lives in the checkboxes within its own sections.

**Reset rule (critical):** Whenever a new item is added under `## Post verification tasks` (because code review or QA surfaced something that requires a code change), ALL checkboxes in `## Verification` MUST be reset to `- [ ]`. Once the fix lands and the Post verification task is `- [x]`, the full `## Verification` section is re-run. The task is only complete when every checkbox in `## Implementation`, `## Verification`, and `## Post verification tasks` is `- [x]` at the same time.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute and return every architecture point discovered while breaking down the work; leave its ownership, resolution, and artifacts to the shared protocol.

## Process

### No-Orphans Gate

Before Phase 1, enforce the shared protocol's no-orphans gate. Begin task breakdown only when the gate passes; unresolved blocking decisions prevent task breakdown. If breakdown surfaces a new architecture point, contribute it and rerun the gate before writing the task list.

### Phase 1: Task Breakdown

Based on everything documented in `plan-prep.md`, `technical-design.md` when produced by selected Design the Solution concerns, `architecture/table-of-contents.md`, and the relevant ADRs, identify every discrete piece of work. Use the flows, technical design, design discovery artifacts, QA scenarios, reference files, and architecture decisions to identify what needs to be built.

#### Task isolation gate

Each implementation task owns one independently complete outcome. Split candidate work when its parts can be implemented, verified, reverted, or consumed independently. Separate independent components, APIs, behaviors, migrations, or other deliverables instead of grouping them because they use the same tool or file type.

Keep the supporting types, tests, and mechanical steps that are necessary to complete that one outcome in the same task. Do not split work into fragments that have no independently useful result.

Before adding a task to `task-list.md`, state its single outcome and confirm that no separable outcome remains bundled inside it.

**Do NOT read conventions/SOPs/skills yet** — that happens in Phase 2 when detailing each task.

**Categorize by dependency wave and maximize each wave:**
- What must be first? (DB schema, types, core interfaces)
- What truly consumes another task's output? Add a dependency only for that concrete input
- What can run in parallel? Place every independent task in the same widest safe wave
- What is the critical path, and which dependencies are merely conventional ordering that should be removed?

**Write the task list to `task/task-list.md`:**

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence from requirements]
**Architecture:** [From plan-prep.md / architecture/table-of-contents.md and relevant ADRs]
**Tech Stack:** [Key technologies]

---

## Tasks

### Wave 1 — Must Be Done First (no dependencies)
- [ ] [Task 01: Name](task-01.md) — [what and why first]
- [ ] [Task 02: Name](task-02.md) — [what and why first]

### Wave 2 — Sequential (depends on Wave 1)
- [ ] [Task 03: Name](task-03.md) (depends on Task 01) — [what]
- [ ] [Task 04: Name](task-04.md) (depends on Task 03) — [what]

### Wave 3 — Independent
- [ ] [Task 05: Name](task-05.md) — [what]
- [ ] [Task 06: Name](task-06.md) — [what]

### Final Validation (auto-added, run last)
- [ ] [Task NN: Grand QA](task-NN.md)
- [ ] [Task NN+1: Write Work Review Guide](task-NN+1.md)
```

**Status tracking:** `task-list.md` is where task status lives. Checkboxes progress `[ ]` → `[-]` (in progress) → `[x]` (complete). Individual `task-NN.md` files do not carry top-level task status.

Only ask user for input if something about the breakdown feels uncertain. Otherwise, proceed to Phase 2.

---

### Phase 2: Detail Each Task

**Phase 2 is delegated to the `create-plan-task` skill.** The plan-prep owner finalizes `task-list.md` first and remains its only writer. Then invoke `create-plan-task` in `from-plan-prep` mode concurrently for every task whose context is complete. Each invocation owns one exclusive `task-NN.md`; no task-writing worker edits `task-list.md`.

Hold only tasks with unresolved user questions or missing required inputs. After those blockers resolve, dispatch the next largest ready set rather than reverting to one-task-at-a-time authoring.

The skill owns:

- the four-section task file template (`## Context` / `## Implementation` / `## Verification` / `## Post verification tasks`)
- the subagent dispatch + verification of the returned file
- the Interface Contracts and targeted Tests (What to Test) how-tos
- the per-task structure and reset semantics

See `/Users/abtinghods/.claude/skills/create-plan-task/SKILL.md` and its `task-template.md` for the full template and rules. Do not re-implement them here.

**Plan-prep's responsibility in Phase 2 (for each task):**

1. **Check if discussion is needed.** Same judgment as before — is the task straightforward from `plan-prep.md`, or are there architecture decisions / ambiguities to resolve first?
2. **If discussion is needed, collaborate with the user.** Settle on the function signature, paths of logic, and smallest necessary targeted tests. Discuss task-level QA only when the user explicitly requested it. Same questions as before — don't follow a rigid script.
3. **Invoke `create-plan-task`** with mode `from-plan-prep`. Pass the agreed context:
   - work folder path
   - the task number + name (already present in `task-list.md`)
   - paste of the relevant sections from `plan-prep.md` (flow diagram for this task, technical details, reference files)
   - paste the relevant sections from `technical-design.md` when it was produced by selected Design the Solution concerns
   - paste the relevant entries from `architecture/table-of-contents.md` and their ADRs
   - paste design artifacts if relevant (`design-discovery-result.md`, `view-model-props.md`, component variants, etc.)
   - the discussion outcomes from step 2 (agreed signature, paths, and targeted tests)
   - any task-level QA the user explicitly requested; otherwise state that QA is omitted and retained for Grand QA
   - the fixed review contract: exactly one code-style review over all files changed by this task, using role `reviewer-junior`; no other reviewer lens
4. **The skill creates the task file and reports back.** Because the task-list.md entry already exists from Phase 1, `create-plan-task` in `from-plan-prep` mode does NOT touch `task-list.md` — it only writes `task-NN.md`.

Resolve known shared questions before dispatch, then run all non-blocked task-file invocations concurrently up to available capacity. Verify each exclusive file independently and let the plan-prep owner consolidate status after the batch.

Only pause for user input when there's a real ambiguity, a decision you can't make alone, or something that feels wrong. Don't ask for approval on every task.

---

### Final Validation Tasks (auto-added, do not ask user)

Always add these two tasks as the last tasks in `task-list.md`, in this exact order. Each gets its own task file in the `task/` folder. Phase 2 of plan-prep uses `create-plan-task` (`from-plan-prep` mode) to author each of these as well — the content guidelines below feed into the discussion context the skill receives.

**Grand QA** (`task-NN.md`)

This task produces a regression-validated `qa.md` and a Playwright E2E suite that codifies it. The default path is the **two-step pipeline**: write QA cases → write E2E tests directly. The optional `qa-execution` middle step (manual qa-runner round) and the optional `qa-exploratory` tail step are only included when there's a specific reason — they are NOT the default.

- Depends on: all implementation tasks, including each task's code-style review
- `## Implementation` → Steps:

  **Default (two-step pipeline):**
  1. **Write QA cases** — run the `manual-qa-case-writing` skill to produce/update `qa.md` covering functional, accessibility (WCAG 2.2 AA), PIPEDA, and performance dimensions.
  2. **Codify as E2E tests** — run the `writing-e2e-tests` skill against `qa.md`. The skill probes the browser itself (qa-runner exploratory mode, Source B) to capture verbatim labels and authors Page Objects + journey tests. Run the suite until green.

  **Optional middle step — `qa-execution` (manual scripted round):**

  Insert step 1.5 **only when**:
  - The user explicitly asks for a manual QA pass before automation, OR
  - You judge a scripted manual round is materially better than going straight to E2E (e.g. the feature has heavy judgment/visual cases that won't reduce well to deterministic Playwright assertions, or the team wants a pre-automation human-checkpointed report).

  When included: run `qa-execution`. The `qa-runner` agent writes `evidence/TC-NNN/evidence.json` with `role` + `accessible_name` per the qa-runner evidence contract, plus `REPORT.md`. Step 2 (`writing-e2e-tests`) then reads that evidence directly (Source A in `verify-before-selectors.md`) instead of probing again.

  **Optional tail step — `qa-exploratory`:**

  Add **only when** the user asks for an exploratory sweep, or when the feature warrants one (pre-release, accessibility-sensitive UI, novel UX). When included: run with at least one charter per primary persona (writes `FINDINGS.md`), then triage **INLINE within this same cycle**:
  - **P0/P1 missing-coverage** → promote to `qa.md` via `manual-qa-case-writing`; add Post verification task; re-run step 2 (and step 1.5 if it was in the pipeline).
  - **P0/P1 pure defect** → Post verification task to fix; re-run.
  - **P2 clear bug** → defer or promote inline if cheap.
  - **P2 friction** → note only; does not block.

- `## Verification`:
  - [ ] `qa.md` exists and reflects the feature
  - [ ] Playwright E2E suite green on `pnpm --filter e2e test`
  - [ ] (If qa-execution was run) all cases in `qa.md` are PASS in the latest qa-runner round
  - [ ] (If qa-exploratory was run) FINDINGS.md exists and no P0/P1 findings are open
  - [ ] If any code changes landed during this cycle, re-run the affected task's code-style review with role `reviewer-junior`
- `## Post verification tasks`: track follow-up fixes with links to `qa.md` entries AND any P0/P1 finding (if exploratory ran). Adding any item resets `## Verification` per the reset rule.

#### Pipeline diagram

```
                  ┌─────────────────────────┐
   feature spec ─►│ manual-qa-case-writing  │  ── writes ──►  qa.md
                  └────────────┬────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │                                     │
        DEFAULT path                       OPTIONAL path
       (skip 1.5)                         (insert 1.5 on
            │                              user-ask or
            │                              judgment-heavy
            │                              feature)
            │                                     │
            │                                     ▼
            │                       ┌─────────────────────────┐
            │                       │ qa-execution            │
            │            reads ────►│   ↳ qa-runner (scripted)│
            │             qa.md     └────────────┬────────────┘
            │                                    │
            │                                    │ writes
            │                                    ▼
            │                          REPORT.md
            │                          evidence/TC-NNN/
            │                            evidence.json
            │                            (role + accessible_name)
            │                            before.png / after.png
            │                                    │
            │                                    │
            ▼                                    ▼
     ┌─────────────────────────────────────────────────┐
     │ writing-e2e-tests                               │
     │   ↳ Source B: probes browser itself             │
     │     (when qa-execution was skipped)             │
     │   ↳ Source A: reads REPORT.md + evidence/       │
     │     (when qa-execution ran — no second probe)   │
     └────────────────────────┬────────────────────────┘
                              │ writes
                              ▼
                  apps/e2e/src/pages/**/*.ts
                  apps/e2e/src/tests/**/*.journey.e2e.ts
                              │
                              │ run green
                              ▼
                       suite passes
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
       DEFAULT done                    OPTIONAL tail
                                       (user-ask /
                                        pre-release /
                                        a11y-sensitive)
                                                │
                                                ▼
                                  ┌─────────────────────────┐
                                  │ qa-exploratory          │
                                  │   ↳ qa-runner           │
                                  │     (charter mode)      │
                                  └────────────┬────────────┘
                                               │ writes
                                               ▼
                                        FINDINGS.md
                                               │
                                               ▼
                                       INLINE TRIAGE
                                       ┌───────┴───────┐
                                  P0/P1 missing      P0/P1 pure
                                   coverage           defect
                                       │                │
                              promote → qa.md     fix code
                              (re-run from         (re-run from
                               step 1)              latest step)
```

#### Artifact examples

**`qa.md`** — produced by `manual-qa-case-writing`. 6-field cases keyed by TC-ID.
```markdown
## TC-01 — Caregiver adds a Regular-rate timesheet entry
- Role: cg1
- Preconditions: signed in, current pay period open, no entries yet
- Steps:
  1. Go to /at/timesheet
  2. Click "Add Entry" on the dashed card
  3. Pick day "Tue 21st", rate "Regular", times 09:00-17:00
  4. Click "Save"
- Expected: lands on /at/timesheet, row "Tue" shows "09:00 - 17:00", "8h", "Regular"
- Priority: P0
- Status: [ ]
```

**`evidence/TC-01/evidence.json`** — produced by `qa-runner` (only when `qa-execution` ran). Keys downstream `writing-e2e-tests` uses verbatim.
```json
{
  "verdict": "PASS",
  "checks": [
    {
      "selector": "a.dashed-card",
      "role": "link",
      "accessible_name": "Add new entry",
      "visible_text": "Add Entry",
      "expected": "navigates to /at/timesheet/{id}/line/create",
      "actual": "navigated to /at/timesheet/abc-123/line/create"
    },
    {
      "selector": "input[type=radio][value=tue-21]",
      "role": "radio",
      "accessible_name": "Tue 21st",
      "expected": "selected after click",
      "actual": "selected"
    },
    {
      "selector": "button[type=submit]",
      "role": "button",
      "accessible_name": "Save",
      "expected": "submits form",
      "actual": "form submitted, redirected to /at/timesheet"
    }
  ],
  "screenshots": ["before.png", "after.png"]
}
```

**`REPORT.md`** — produced by `qa-runner`. Roll-up for the round.
```markdown
# QA Round 1 — Timesheet entry add

## Executive Summary
- Verdict: GO
- Pass rate: 12/12 (100%)
- Top issues: none

## Run Metadata
- Branch: feature/timesheet-entry-add
- URL: http://localhost:3002
- Browser: Chromium 131.x

## Passed (12)
TC-01 ✓  TC-02 ✓  TC-03 ✓  ...
```

**`apps/e2e/src/pages/at/timesheet/add-entry-page.ts`** — produced by `writing-e2e-tests`. Selector strings come from `accessible_name` in evidence.json.
```typescript
export class AddEntryPage {
  constructor(private page: Page) {}

  async pick_day(day: ShiftDay): Promise<void> {
    await this.page.getByRole('radio', { name: /^tue 21st$/i }).check({ force: true })
  }

  async click_save_button(): Promise<AttendantTimesheetOverviewPage> {
    await this.page.getByRole('button', { name: /^save$/i }).click()
    return new AttendantTimesheetOverviewPage(this.page)
  }
}
```

**`apps/e2e/src/tests/timesheet/add-entry.journey.e2e.ts`** — the test that walks TC-01 end-to-end.
```typescript
test('cg1 adds a Regular-rate entry for Tue', async ({ cg1_page }) => {
  const overview = new AttendantTimesheetOverviewPage(cg1_page)
  await overview.goto()
  const form = await overview.click_add_entry_button()
  await form.pick_day({ week_day: 'tue', period_week_num: 1 })
  await form.pick_rate_type('Regular')
  await form.fill_times('09:00', '17:00')
  await form.click_save_button()
  await overview.expect_entry_visible({
    day: { week_day: 'tue', period_week_num: 1 },
    times: '09:00 - 17:00',
    rate_type: 'Regular',
    duration: '8h',
    approval: { manager: 'pending', attendant: 'pending' },
  })
})
```

**`FINDINGS.md`** — produced by `qa-runner` in exploratory mode (only when `qa-exploratory` ran).
```markdown
# Exploratory Findings — 2026-04-27 — keyboard-only attendant

## Charter
Persona: cg1 navigating timesheet entry with keyboard only. Goal: file
a Regular entry for today using Tab/Enter/Space only.

## Findings

### Finding 1: Day-picker radios not reachable by Tab
- Severity: P1
- Category: a11y
- What I tried: Tab from page top
- What happened: focus skips from "Add Entry" link past the radios to "Save"
- What I expected: Tab visits each day radio in order
- Evidence: screenshots/keyboard-trap.png
- Proposed test case: TC-13 — keyboard-only day selection
```

**Write Work Review Guide** (`task-NN+1.md`)
- Depends on: Grand QA (clean pass)
- `## Implementation` → Steps: run the `write-review-guide` skill to generate `review-walkthrough.md`
- Runs once after Grand QA is clean — NOT part of the QA cycle

---

## After all tasks complete

Present summary:
- Total task count by wave
- Execution options: `executing-all-tasks` skill (supervised, parallel where dependencies allow) or `executing-single-plan-task` skill (one at a time)
- Hand over the path to `task/task-list.md` as the entry point for execution

## Mid-execution additions

If new bugs or scope adjustments surface DURING task execution and need to be planned the same way, read existing `plan-prep.md`, `architecture/table-of-contents.md`, and the relevant ADRs, then call `create-plan-task` standalone (mode auto-defaults to `standalone`) and pass those contents as context. The skill will:

- compute the next task number
- write the full task file
- insert the entry in `task-list.md` under a `### Wave N — Added during execution` heading, placed after the last `- [x]` line and before the Final Validation block

Plan-prep does not need to be re-run for this.

## Rules

- **Don't over-ask** — Only pause for user input when genuinely needed. If the task is clear from plan-prep.md, create it and move on
- **Phase 1 before Phase 2** — Don't read conventions/SOPs/skills until Phase 2 (the `create-plan-task` subagent does that)
- **Delegate to `create-plan-task`** — Do not re-implement the four-section task template here; that lives in the `create-plan-task` skill
- **Targeted tests stay with their task** — Include only the smallest automated tests needed to prove the task's isolated outcome and immediate integration seam
- **Broad verification belongs to Grand QA** — Do not add package-wide, repository-wide, or feature-wide suites to an implementation task unless the user explicitly requires one
- **No per-task QA by default** — Planning QA scenarios feed Grand QA, not implementation tasks. Include task-level QA only when the user explicitly requests it
- **What to test, not how** — Describe test behaviors, not test implementation
- **Use pnpm scripts** — e.g., `pnpm check` instead of raw commands
- **Top-level status lives in task-list.md** — Individual task files do not carry `[ ]/[-]/[x]` at the top of the file
- **Every actionable item is a checkbox** — Implementation Tests, Implementation Steps, Verification items, Post verification tasks all use `- [ ]` — never numbered lists or plain bullets
- **Reset Verification on new Post verification task** — The moment a Post verification task is added, every checkbox in `## Verification` resets to `- [ ]`. Re-run the full section when the Post verification tasks are all `[x]`
- **One isolated outcome per task** — Split independently implementable, verifiable, revertible, or consumable outcomes into separate tasks

## Common Mistakes

- Writing into a single `plan-tasks.md` instead of the `task/` folder
- Re-implementing the task template inline instead of calling `create-plan-task`
- Reading conventions/SOPs/skills from the main thread (the `create-plan-task` subagent does that)
- Separating tests into their own tasks
- Adding task-level QA or copying Planning QA scenarios into a task without an explicit user request
- Adding broad test commands that do not directly prove the task's isolated outcome
- Generic file lists ("read conventions") instead of specific files
- Mixing Implementation and Verification (e.g., putting test-running steps under Implementation)
- Generic verification checkbox items ("run tests") instead of task-specific ones
- Forgetting to update `task-list.md` after creating a new task file (Phase 1 should have it; standalone `create-plan-task` handles it)

## Output

Write `task/task-list.md` (Phase 1) and let `create-plan-task` write each `task/task-NN.md` (Phase 2). Everything under the work folder's `task/` subdirectory — no `plan-tasks.md` single file.
