# create-plan-task — original vs. gold fixes

This is the reference fix set for an output-quality eval of the **skill-creating** meta-skill.
We took one real skill, `create-plan-task`, which already broke several skill-authoring rules,
and hand-built the corrected **gold** version. Each fix below shows the **original** (before) and
the **gold** (after) side by side, the rule it satisfies, why it matters, and which eval
assertion checks it. The bolded assertions (J1–J3) are *judgment* checks a linter cannot see —
they are the point of the eval.

Reader's job: compare before vs. after per fix and see exactly what "following the rules" changed.

## Summary of the 6 fixes

| # | What changed | Rule | Assertion | Kind |
|---|--------------|------|-----------|------|
| 1 | Description drops the caller clause "Invoked by plan-prep" | Caller-agnostic (R1) | M4 | mechanical |
| 2 | Body stops detecting "how it was invoked"; decides from task-list state | Caller-agnostic (R1) | **J1**, M5 | judgment |
| 3 | The rename is propagated everywhere without breaking behavior | Behavior-preserving | **J2** | judgment |
| 4 | Declares `arguments` and references them bare as `$name` | Declare args (R3) + bare $name (R4) | M2, M3 | mechanical |
| 5 | Fixes a broken markdown link in an example | Structural / valid links | M1 | mechanical |
| 6 | KEEPS legitimate plan-prep prerequisite references (no over-scrub) | Don't over-correct | **J3** | judgment |

---

## Fix 1 — Description: remove the caller clause

**Rule:** Caller-agnostic (R1). A description must say *what the skill does* and *when to use it* —
never name who invokes it. **Assertion: M4.**

**Before (original)**
```yaml
description: Create one implementation task in a plan-prep work folder. Writes a `task/task-NN.md`
  file with the full Context / Implementation / Verification / Post verification tasks structure,
  and inserts an entry in `task/task-list.md`. Invoked by `plan-prep` (Phase 2) during initial
  breakdown AND standalone when new bugs or scope arise mid-execution. Triggers on "add a task",
  "new task", "another task to the plan", "create plan task", or "/create-plan-task".
```

**After (gold)**
```yaml
description: Create one implementation task in a plan-prep work folder. Writes a `task/task-NN.md`
  file with the full Context / Implementation / Verification / Post verification tasks structure,
  and adds its `task/task-list.md` entry when one isn't already present. Use when adding a task to
  an existing plan — during initial plan breakdown or when new bugs or scope surface mid-execution.
  Triggers on "add a task", "new task", "another task to the plan", "create plan task", or
  "/create-plan-task".
```

**Why:** "Invoked by `plan-prep` (Phase 2)" couples the skill to a specific caller. The gold keeps
the same two scenarios (initial breakdown / mid-execution) but frames them as *when to use it*, so
the skill reads identically no matter who triggers it.

---

## Fix 2 — Body: decide from STATE, not from the caller (the headline fix)

**Rule:** Caller-agnostic (R1). Don't branch on how the skill was invoked; branch on observable
state or an explicit argument. **Assertions: J1 (judgment), M5.**

**Before (original)**
```markdown
## Modes

This skill has two invocation modes. Detect mode from how the skill was invoked:

| Mode | How it's invoked | task-list.md behavior |
|------|------------------|------------------------|
| `from-plan-prep` | Called by `plan-prep` (Phase 2 of `how-does-the-work-break-down.md`). The
  caller passes a marker like "mode: from-plan-prep" in the invocation message. | The task-list.md
  entry already exists (Phase 1 wrote the full wave structure). **Do not insert a new entry.** Only
  create the `task-NN.md` file. |
| `standalone` | Default. User invokes the skill directly mid-execution to add a new task (newly-
  found bug, scope shift, etc.). | The task-list.md entry does not exist. **Insert it after the
  last `- [x]` line in the `## Tasks` section**, under a `### Wave N — Added during execution`
  heading (create the heading if missing). |
```

**After (gold)**
```markdown
## task-list.md: insert an entry, or not

Whether to add a `task-list.md` entry depends on **whether one already exists for this task** —
read it from the file, don't branch on how the skill was started. After computing the next task
number (Step 1), look in `task-list.md` for an entry pointing to `task-{NN}.md`:

| State of `task-list.md` | Behavior |
|-------------------------|----------|
| **Entry already present** — the full wave structure was written up front when the plan was broken
  down. | **Do not insert a new entry.** Only create the `task-NN.md` file. |
| **No entry yet** — a task added mid-execution (newly-found bug, scope shift, etc.). | **Insert it
  after the last `- [x]` line in the `## Tasks` section**, under a `### Wave N — Added during
  execution` heading (create the heading if missing). |
```

**Why:** The original keyed behavior on *who* called it — and on a magic `mode: from-plan-prep`
marker the caller had to pass. The distinguishing fact was always observable: *does a task-list
entry already exist?* The gold reads that from the file. Same behavior, zero coupling — and it now
works no matter how it's launched. This is exactly the kind of fix `validate.py` cannot detect,
which is why the eval grades it by judgment (J1).

---

## Fix 3 — Propagate the rename without breaking behavior

**Rule:** A decoupling rewrite must stay behavior-preserving and internally consistent — no
dangling references to the removed modes. **Assertion: J2 (judgment).**

Every spot that referenced the old modes was updated to the state-based framing:

**Before → After**
```diff
- - `{work-folder}/task/task-list.md` — updated only in `standalone` mode.
+ - `{work-folder}/task/task-list.md` — updated only when no entry for the task exists yet.

- ### Step 6 — Update task-list.md (standalone mode only)
- In `from-plan-prep` mode, **skip this step** — the entry already exists.
- In `standalone` mode:
+ ### Step 6 — Update task-list.md (only when no entry exists yet)
+ If an entry for this task already exists (Step "task-list.md: insert an entry, or not"), **skip this step**.
+ Otherwise:

- - Next: "Run the task with `executing-single-plan-task` skill" (standalone) / return control to plan-prep (from-plan-prep)
+ - Next: "Run the task with `executing-single-plan-task` skill"

- - **Subagent does the writing.** ... Same pattern as `plan-prep` Phase 2.
+ - **Subagent does the writing.** ... Same orchestrate-then-verify pattern used elsewhere in the project.

- - Updating task-list.md in `from-plan-prep` mode (causes duplicate entries)
+ - Inserting a second task-list.md entry when one already exists for the task (causes duplicates)
```

**Why:** A half-done rename is worse than none — it leaves contradictory instructions. The four
behaviors the skill guarantees all survive: it still creates exactly one `task-NN.md`, still adds a
list entry only when none exists (no duplicates), still keeps Final Validation last, and still skips
the clarifying chat when the task is already fully specified.

---

## Fix 4 — Declare arguments, reference them bare

**Rule:** Inputs must be declared as `arguments` (R3) and referenced bare as `$name` in the body
(R4) — backticks render the literal label instead of substituting the value. **Assertions: M2, M3.**

**Before (original)**
```markdown
argument-hint: [optional: work folder path] [optional: short task description]
---
...
## Inputs
- **First positional arg (optional):** path to the work folder ...
- **Second positional arg (optional):** short description of the task ...
...
If the user did not pass a work folder path, auto-detect:
```

**After (gold)**
```markdown
argument-hint: [optional: work folder path] [optional: short task description]
arguments: [work_folder, task_description]
---
...
## Inputs
- **$work_folder (optional):** path to the work folder ...
- **$task_description (optional):** short description of the task ...
...
If $work_folder was not provided, auto-detect:
```

**Why:** The skill had an `argument-hint` but never declared `arguments`, and referred to inputs as
"First/Second positional arg." Declaring them and using bare `$work_folder` / `$task_description`
makes the inputs real substitutable values and self-documenting.

---

## Fix 5 — Fix the broken link

**Rule:** Markdown links must resolve; `validate.py` errors on a broken relative link. **Assertion: M1.**

**Before → After**
```diff
-      - [ ] [Task NN: Name](task-NN.md) — [one-line description] [depends on: Task XX / "none"]
+      - [ ] [Task {NN}: Name](task-{NN}.md) — [one-line description] [depends on: Task XX / "none"]
```

**Why:** Inside an example block, `](task-NN.md)` parses as a real relative link to a file that
doesn't exist → a validator error. Using the `{NN}` placeholder marks it as a template, which the
validator correctly skips. (Borderline: this is partly a validator limitation — it doesn't ignore
fenced code — but the placeholder is the right authoring fix either way.)

---

## Fix 6 — KEEP the legitimate plan-prep references (the guard)

**Rule:** Removing caller-coupling must not become over-scrubbing. References to plan-prep as a
*prerequisite the user runs first* or as the *artifact* (`plan-prep.md`) are legitimate and stay.
**Assertion: J3 (judgment).**

**Unchanged in both original and gold (intentionally kept)**
```markdown
The work folder must already contain `plan-prep.md` and `task/task-list.md` — this skill does not
bootstrap a plan from scratch.

## Prerequisites
1. `{work-folder}/plan-prep.md` exists. If not:
   > "I can't add a task without a `plan-prep.md` in this work folder. Run the `plan-prep` skill
   > first to establish requirements, landscape, and flow."
```

**Why:** The distinction is the whole point of Rule 1. "Invoked by plan-prep" (who calls me) is
coupling and was removed. "plan-prep.md must exist first" (a prerequisite the user satisfies) is
not coupling and was kept. A naive fix that deletes every mention of plan-prep would fail J3.

---

## Where to focus when reviewing

- **Fix 2 + Fix 3 are the real test.** They are the caller-agnostic decoupling and its
  behavior-preserving propagation — the value a linter can't measure.
- **Fix 6 is the trap.** The easy mistake is over-correcting and scrubbing the legitimate
  prerequisite references. Gold keeps them on purpose.
- Fixes 1, 4, 5 are mechanical and a competent agent may get them even without the skill — they
  are the baseline, not the differentiator.
