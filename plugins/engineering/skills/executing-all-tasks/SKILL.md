---
name: executing-all-tasks
description: Supervises execution of an entire plan task list — dispatches each task to a disposable subagent running executing-single-plan-task, picks a model tier per task, verifies the task file on disk before closing it, and loops until every task is done. Use when a work folder's task/task-list.md should be executed end to end — "execute all tasks", "run the whole task list", "finish the plan", "work through the remaining tasks".
---

# Executing All Tasks

## Overview

Run every task in a plan work folder to completion by supervising, never implementing.

- **Supervisor (this context):** product owner + engineering lead. Picks tasks, dispatches agents, verifies artifacts, updates `task-list.md`. Does no implementation work — a thin supervisor context is what lets one run survive a long task list.
- **Task agent (one per task, disposable):** a subagent that runs the `executing-single-plan-task` skill in its own context and returns a report. Its context is thrown away after the task; durable knowledge lives in `walkthrough.md`.

**Announce at start:** "Executing all tasks in {work-folder} under supervision."

## Inputs

Path to a work folder containing `task/task-list.md`. The skill finds pending tasks itself — no task number required.

## The Loop

Repeat until a stop condition fires (see "Stop conditions").

### Step 1 — Pick the next eligible task(s)

Read `{work-folder}/task/task-list.md`, including its cross-task rules.

A task is **eligible** when:
- Its entry is `[-]` (in progress — a resume; the per-task skill picks up from checkbox state) or `[ ]` (pending). Prefer `[-]` first, then `[ ]`, in wave order.
- Every task named in its `Depends on:` is `[x]` in `task-list.md`. Explicit `Depends on:` is authoritative; wave order applies when no dependencies are listed.
- It shares no files with a task currently running — check each task's `Files` list and the task list's cross-task ownership rules (e.g. "file X is owned by Task NN only").

Dispatch **all eligible tasks in parallel**, one agent each. If a task's dependencies aren't met, skip it and check the next — an unmet dependency is a scheduling fact, not a blocker.

If no task is `[ ]` or `[-]`: the list is done — announce completion and stop. If pending tasks remain but none is eligible and none is running: that's a dependency deadlock — stop and flag the user.

### Step 2 — Check for blockers on each picked task

STOP and flag the user if any of these fire:

- The task's `## Verification` includes "User has acknowledged the decision" or an equivalent human-review gate — the supervisor cannot self-approve a decision task.
- The task's Implementation calls for a **destructive or shared-state action** (force-push, DB migration, production deploy, package publish) the user hasn't pre-authorized.
- A previously completed task left `## Post verification tasks` items `[ ]` or `[-]` (shouldn't happen if the per-task skill finished cleanly, but check before moving on).

### Step 3 — Pick the model tier for the agent

If the user has given model/effort instructions for this run, follow those. Otherwise pick a tier from the task file's own signals:

| Tier | Use for | Signals in the task file |
|------|---------|--------------------------|
| **Strongest** (highest effort) | Decisions, architecture, security-sensitive code, final review and QA | Decision/architecture tasks; auth, permissions, or personal-data handling; "Grand Code Review" / "Grand QA"; Verification steps that require judgment, not just running commands |
| **Standard** | Well-specified implementation | Complete Interface Contracts, enumerated tests, Similar Files to copy — the hard thinking was done at plan time |
| **Fast** (lowest cost) | Mechanical work | Copy/label changes, renames, file moves, doc-generation tasks (e.g. review guide) |

Map tiers to whatever models the harness offers. When torn between two tiers, pick the stronger. A task mixing tiers runs at its highest-tier component — never let a fast model make a decision embedded in a mechanical task.

### Step 4 — Dispatch the agent

The agent runs `executing-single-plan-task` in its own context. **Prompt pattern** (use verbatim, fill in `[…]`):

```
You are a [role, e.g. principal software engineer] with expertise in [domain].

Use the executing-single-plan-task skill exactly as written. Do not deviate
from its checklist. Read walkthrough.md for prior-task context before starting.

Work folder: [absolute path]
Task file:   [absolute path]/task/task-NN.md
Walkthrough: [absolute path]/walkthrough.md

When you finish, return:
1. A short summary of files changed (paths + one line each).
2. Confirmation that every checkbox in task-NN.md is [x] across
   ## Implementation, ## Verification, and ## Post verification tasks —
   or, if a step required dispatching a subagent and spawning subagents
   is not available to you, say so: leave that checkbox [ ], leave the
   task entry [-], and add a ## Post verification tasks entry naming
   what needs dispatching.
3. Any deviations from the plan and why (these belong in walkthrough.md).
4. Output of verification commands you ran (test counts, type-check and
   lint status).

If you hit a blocker you cannot resolve, return without marking the task
done — list what's blocked and why. Do not falsify checkboxes.
```

If the user has pre-authorized destructive operations for this run (e.g. a migration command, `git push`), state that in the prompt so the agent doesn't pause to ask.

### Step 5 — Verify the artifact before approving

The agent's return summary is **not** authoritative — `task-NN.md` on disk is. Read the file and run this gate. A single unchecked box anywhere fails the gate.

| Check | What to look for |
|-------|-----------------|
| Every `## Implementation` checkbox is `[x]` | Tests + Steps. Any `[ ]` or `[-]` means the agent didn't finish. |
| Every `## Verification` checkbox is `[x]` | Automation tests, Code review, QA, Others. |
| Every `## Post verification tasks` checkbox is `[x]` | Code-review and QA follow-ups all closed. |
| Reset rule respected | Post-verification items `[x]` but Verification items `[ ]` means the agent forgot to re-run Verification after fixing follow-ups — send back. |
| Skill-invoking steps actually ran the skill | For tasks whose steps name a skill (code review team, QA execution, review-guide writing), that skill's own artifact must exist on disk (e.g. `code-review.md`, QA `REPORT.md`, the review-guide file). A hand-written "equivalent" fails this row — agents substitute prose for skill runs and tick the box. |
| Surfaced dispatch blocker handled | If the agent reported a step needing a subagent it couldn't spawn: the checkbox must be `[ ]` with a `## Post verification tasks` entry naming the dispatch. Dispatch that subagent yourself, land the result, then close — never close the box with the work undone. |
| Cross-check the diff | Compare the working-tree diff (`git status` / `git diff --stat`) against the agent's claimed file list. A claim with no diff is a falsified artifact — flag to the user; do not approve. |
| Interface Contracts honored | The diff matches the shape declared in `## Implementation → Interface Contracts`. |
| Deviations documented | Any plan deviation lives in `walkthrough.md`. |

**If every row passes:** mark the task entry `[x]` in `task-list.md` yourself. The agent does not have authority to close its own task — closing it is the supervisor boundary.

**If any row fails:** send the agent back with concrete feedback ("In `task-NN.md`, these checkboxes are not `[x]`: …"). Continue the *same* agent if the harness supports it — it keeps working context. If it can't, dispatch a fresh agent whose prompt includes the failure list plus the prior agent's summary. Max 2 send-backs per task; escalate to the user after that.

### Step 6 — Manage supervisor context

If context usage exceeds roughly 40% of the window, compact/summarize (however the harness does it) before the next iteration, retaining only:

- A link to `{work-folder}/walkthrough.md` (durable cross-task context lives there).
- A link to `{work-folder}/task/task-list.md` (current task state lives there).
- Architectural decisions and key file references.
- The instruction: "Continue with the next eligible task using the executing-all-tasks skill. Read walkthrough.md for prior-task context, then proceed."

Below the threshold, skip it — cost without benefit.

### Step 7 — Loop

Announce: `Continuing with the next task.` Return to **Step 1**.

## Stop conditions

The loop stops only when:

- A blocker from Step 2 fires — flag clearly and wait for the user.
- No `[ ]` or `[-]` tasks remain — done.
- Pending tasks remain but none is eligible and none is running (dependency deadlock).
- The Step 5 gate fails twice for the same task (after 2 send-backs).
- A task agent reports a blocker it couldn't resolve.
- The user interrupts.

On stop, print a terse summary: tasks completed this run, task-list state (done / remaining), and the blocker (if any) with what the user needs to resolve it.

## Common mistakes

- **Executing a task in the supervisor context.** Invoking `executing-single-plan-task` directly collapses supervisor and implementer into one context and loses everything the architecture buys — isolation, the artifact-review boundary, fresh per-task focus. Dispatch an agent every time, even for a task that looks small.
- **Trusting the agent's "done" report without reading the file.** Agents fabricate completion. The gate reads `task-NN.md` from disk and cross-checks the diff precisely because reports lie.
- **Accepting a hand-written substitute for a skill run.** "I reviewed the code myself" is not a `code-review-team` run; a paragraph of QA notes is not a QA `REPORT.md`. The artifact check exists because this substitution happens and looks plausible.
- **Stopping on an unmet dependency.** Skip to the next eligible task; only a deadlock (pending tasks, none eligible, none running) stops the run.
- **Compacting too early or too late.** Don't compact at 10% "just in case"; don't wait until the window is nearly full and thrash.
- **Closing the task entry from the agent's side.** Only the supervisor marks `[x]` in `task-list.md`, after the gate passes — that boundary is what makes the verification real.
