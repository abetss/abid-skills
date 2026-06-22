---
name: executing-plan-task-list-sequential
description: Executes every pending task in a `task/` folder sequentially. Spawns a principal-engineer agent per task (via the Agent tool, NOT a skill call), hands it the task file, and verifies the artifact against every checkbox before approving and moving on. Compacts between tasks when context exceeds a threshold. Use when the user wants a whole `task/` folder worked through end-to-end without typing between tasks — e.g. "run the task list", "work through all remaining tasks", "complete the plan autonomously", "execute the task folder", "keep going until blocked", "do all pending tasks", "run the plan", or when given a path to a `task-list.md` / work folder and asked to finish it. Do NOT use for a single task (use `executing-single-plan-task` instead) or when tasks should run in parallel with cross-task quality gates (use `execute-all-supervised` instead).
---

# Executing a Plan Task List

## Overview

Create a team of agent
- main: you as the product owner and engineering lead
- principle software engineer: Opus with xhigh effort

You pass the following task to the principle software engineer agent, when its done you check its artificat to see if everything is complete and no shortcut was taking. If you had any question, ask the member. You are responsible for every checkbox of the task to be completed.

Loop through a `task/` folder one task at a time. Each iteration: **spawn a principal-engineer agent via the Agent tool** (NOT via a Skill call), hand it the task file, verify the artifact when it returns, then decide whether to compact, then pick the next task. The agent itself runs the `executing-single-plan-task` skill in its own context — see Step 3 for the exact dispatch pattern. Durable state lives on disk in `walkthrough.md` + `task-list.md`; both the supervisor's session AND each agent's session are expendable between tasks.

**Core principle:** the current task gets full focus; between-task context is the two files on disk, nothing more.

**Announce at start:** "I'm using the execute-task-list-sequential skill to work through this task folder."

## Inputs

Path to a work folder containing a `task/task-list.md` file. The skill finds pending tasks itself — no task number required.

## The Loop

Repeat until a stop condition fires (see "Stop conditions" below).

### Step 1 — Pick the next task

Read `{work-folder}/task/task-list.md`. Pick, in priority order:
1. First `[-]` (in-progress) task in wave order
2. First `[ ]` (pending) task in wave order

If neither exists: the task list is done. Announce completion and stop.

### Step 2 — Check for a blocker on that task

STOP and flag the user if any of these fire:

- A **dependency** (`Depends on:` in the task's `## Context`) is not yet `[x]` in `task-list.md`.
- The task's `## Verification` includes "User has acknowledged the decision" or an equivalent ARCH-style human-review gate — decision tasks require user input and the skill cannot self-approve.
- The task's Implementation explicitly calls for a **destructive or shared-state action** (force-push, DB migration, production deploy, package publish) that the user hasn't pre-authorized.
- The previous iteration's task left items under `## Post verification tasks` as `[ ]` or `[-]` (shouldn't happen if `executing-single-plan-task` finished cleanly, but double-check before moving on).

### Step 3 — Pick the dispatch mode for this task

Most tasks are **per-task implementation**: spawn a principal-engineer agent (Step 3a). Some tasks are **multi-agent orchestration tasks** that require dispatching parallel reviewers — those CANNOT be delegated to a subagent because subagents do not have the `Agent` tool. Handle them yourself or surface to the user (Step 3b).

**Decide which mode applies:**

- **Step 3a (per-task implementation)** — the task implements a feature, fixes a bug, refactors code, writes tests. Code review on the diff is per-task and runs inline in the implementer agent's own context (per `executing-single-plan-task` Step 4 rule #8). The implementer agent has everything it needs.

- **Step 3b (the task itself dispatches subagents)** — the task's `## Implementation` invokes a skill or step that itself dispatches subagents. Subagents lack the `Agent` tool, so delegating these tasks causes silent failure or fallback. Don't let that happen.

#### Step 3a — Spawn the principal-engineer agent for the task

Use the **Agent tool** (NOT the Skill tool) with `subagent_type: "general-purpose"`. The agent runs the `executing-single-plan-task` skill itself in its own context. Your context is the supervisor's; the agent's is disposable per-task.

**Why an agent and not a skill call:** invoking `executing-single-plan-task` in your own thread collapses supervisor and engineer into one context. You lose context isolation, you lose the artifact-review boundary, and you become the engineer rather than the lead. Use the Agent tool, every time, even when the task looks small.

#### Step 3b — Tasks that require dispatching subagents

If the task's `## Implementation` invokes a skill or step that itself dispatches subagents, do not delegate to a subagent — subagents lack the `Agent` tool, dispatch will silently fail or fall back, and you'll get an artifact that ticks the box without doing the work. Run such tasks yourself in this thread; verify your own artifact against Step 4 the same way you'd verify an implementer's. Budget-pressure escape: ask the user to run in a fresh session — skipping is not an option, only relocating.

**Agent prompt pattern** (use verbatim, fill in `[…]`):

```
Use the executing-single-plan-task skill exactly as written. Do not deviate
from its checklist. Read walkthrough.md for prior-task context before starting.

Work folder: [absolute path]
Task file:   [absolute path]/task/task-NN.md
Walkthrough: [absolute path]/walkthrough.md

When you finish, return:
1. A short summary of files changed (paths + one-line each).
2. Confirmation that every checkbox in task-NN.md is [x] across
   ## Implementation, ## Verification, and ## Post verification tasks
   — OR, per the subagent dispatch contract in `executing-single-plan-task`
   rule #8, a clear statement that a step required dispatching a subagent
   and the `Agent` tool was not available in your context. In that case:
   leave the corresponding checkbox `[ ]`, leave the task entry `[-]`,
   add a `## Post verification tasks` entry naming what needs dispatching,
   and state in your return summary that you left the task open pending
   external dispatch.
3. Any deviations from the plan and why (these belong in walkthrough.md).
4. Output of any verification commands you ran (test counts, type-check
   results, biome status).

If you hit a blocker you cannot resolve, return without marking the task
done — list what's blocked and why. Do not falsify checkboxes.
```

If the user has pre-authorized destructive operations for this run (e.g. `prisma migrate dev`, `git push`), state that explicitly in the agent prompt so the agent doesn't pause to ask.

### Step 4 — Verify the artifact before approving

The agent's return summary is **not** authoritative — `task-NN.md` on disk is. Read the file and run this gate. A single unchecked box anywhere fails the gate.

| Check | What to look for |
|-------|-----------------|
| Every `## Implementation` checkbox is `[x]` | Tests + Steps. If any is `[ ]` or `[-]`, the agent didn't finish. |
| Every `## Verification` checkbox is `[x]` | Automation tests, Code review, QA, Others. |
| Every `## Post verification tasks` checkbox is `[x]` | Code-review and QA follow-ups all closed. |
| Reset rule respected | If `## Post verification tasks` items are `[x]` but `## Verification` items are `[ ]`, the agent forgot to re-run Verification after fixing follow-ups — send back. |
| **No subagent-dispatch blocker pending** | If the implementer indicates a task step required dispatching a subagent and the `Agent` tool was not in its context (per `executing-single-plan-task`'s subagent dispatch contract), the corresponding checkbox MUST be `[ ]` and a `## Post verification tasks` entry MUST name what needs dispatching. Do NOT close the task entry until **you** (the supervisor) dispatch the named subagent yourself — see Step 4a below. Closing the box without doing the work is the failure mode this rule exists to prevent. |
| Cross-check git | `git status` and `git diff --stat` against the agent's claimed file list. A claim with no diff is a falsified artifact — flag explicitly to the user; do not approve. |
| Interface Contracts honored | The diff matches the shape declared in the task's `## Implementation → Interface Contracts` block. |
| Deviations documented | Any plan deviation lives in `walkthrough.md`. |

**If every row passes:** mark the task entry `[x]` in `task-list.md` yourself. The agent does not have authority to close its own task — closing it is the supervisor boundary.

**If any row fails:** continue the same agent via SendMessage with concrete feedback ("In `task-NN.md`, the following checkboxes are not `[x]`: …"). Max 2 send-backs per task; escalate to the user after that. Do NOT spawn a fresh agent — that loses the agent's working context.

### Step 4a — Implementer couldn't dispatch a subagent

Fires when the implementer's return indicates a task step required dispatching a subagent and the `Agent` tool was not in its context (per `executing-single-plan-task`'s subagent dispatch contract).

Detection: implementer's return summary + on-disk state. Signals — task entry stuck at `[-]` after a clean return; one or more `## Verification` rows `[ ]` paired with a `## Post verification tasks` entry naming an external dispatch; summary saying a step required dispatching a subagent that wasn't available. The combination of disk state + report is authoritative.

Handling:

1. Confirm on disk: blocked checkbox is `[ ]`, task entry is `[-]`, `## Post verification tasks` names the gap (which subagent + scope).
2. Dispatch the named subagent from this thread (you have `Agent`). Pass it the scope the task specifies.
3. Land any findings as `## Post verification tasks` entries (triggers reset); send back to implementer; re-enter Step 4 on next return.
4. If the dispatched subagent returned clean: mark the originally-blocked checkbox `[x]`, mark the supervisor-dispatch Post-verification entry `[x]`, re-run Step 4, close the task entry `[x]`.
5. One-line note in `walkthrough.md` recording the supervisor-side dispatch.

### Step 5 — Decide whether to compact

Check current context usage. If **either** threshold fires — **usage > 40% of the window** OR **usage > 200K tokens** (whichever hits first) — run `/compact` with this focus directive BEFORE the next iteration:

```
Retain only:
- A link to {work-folder}/walkthrough.md (durable cross-task context lives there).
- A link to {work-folder}/task/task-list.md (current task state lives there).
- Architectural decision and related file references
- The instruction: "Continue with the next available task in the task list using the execute-task-list-sequential skill. Read walkthrough.md for prior-task context if needed, then proceed."

Drop all in-session exploration, file reads, option drafts, tool outputs, and intermediate reasoning. The two files above are the source of truth.
```

If the thresholds are not crossed, skip compacting — cost without benefit.

### Step 6 — Loop

Announce: `Continuing with the next task.` Return to **Step 1**.

---

## Stop conditions

The loop stops only when:

- A blocker from Step 2 fires — flag clearly and wait for the user.
- The task list has no remaining `[ ]` or `[-]` tasks.
- The user interrupts.
- The Step 4 verification gate fails twice for the same task (after 2 send-backs) — escalate to user.
- The principal-engineer agent reports a blocker it couldn't resolve.

On stop, print a terse summary:
- Tasks completed this run
- Current state of the task list (tasks done / remaining)
- The blocker (if any) and what the user needs to resolve it

---

## Relationship to other skills

- **`executing-single-plan-task`** — handles one task end-to-end (context → implementation → verification → task-list update → walkthrough update). This skill orchestrates by **spawning a principal-engineer agent** that itself runs `executing-single-plan-task` in its own context. We do NOT invoke `executing-single-plan-task` directly in the supervisor's thread — that would collapse the team-of-agents architecture into a single context.
- **`execute-all-supervised`** — orchestrator with parallel task agents and cross-task quality gates. Use that when tasks can run in parallel and need cross-task coherence checks. Use **this** skill when tasks must run sequentially (e.g., the task list says so, or dependencies are linear).

---

## Common mistakes

- **Invoking `executing-single-plan-task` in your own context.** The whole skill is built on agent isolation. If you call the sub-skill directly via the Skill tool, you collapse main+engineer into one context and lose every benefit — context isolation, the artifact-review boundary, fresh per-task focus. Use the Agent tool, every time, even when the task looks small.
- **Trusting the agent's "done" report without reading the file.** Agents fabricate completion. Read `task-NN.md` from disk and verify every checkbox + `git diff` before approving. A claim with no diff is a falsified artifact — flag explicitly to the user.
- **Continuing past a blocker.** The Step 2 blockers exist because the task genuinely can't be auto-completed. Don't rationalize around them.
- **Compacting too early or too late.** The 40% / 200K-token threshold is the rule; don't compact at 10% ("just in case") and don't wait for 70% (cache miss tax compounds).
- **Losing the walkthrough.** The principal-engineer agent writes to `walkthrough.md` on significant decisions — if it skipped that on a task where a real decision was made, flag it via SendMessage before approving the task. Compacting discards session context; `walkthrough.md` is the only cross-task record.
- **Closing the task entry from the agent prompt.** The principal-engineer agent updates `task-NN.md` checkboxes. Only the supervisor (this skill, main thread) marks the entry `[x]` in `task-list.md` after the Step 4 verification gate passes. That's the supervisor boundary that makes the architecture meaningful.
- **Spawning a fresh agent on send-back.** When verification fails, continue the same agent via SendMessage — the agent has working context (file reads, recent decisions). A new Agent call starts cold and re-does the discovery work. Send-back is a feedback channel, not a restart.
