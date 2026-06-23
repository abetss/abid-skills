---
name: plan-prep
description: Modular engineering planning — from requirements intake through implementation-ready tasks. Composable Step selected per feature. Replaces separate plan-prep and plan-implement workflows.
argument-hint: [work folder path]
---

# Plan Preparation & Implementation Planning

An engineer receives a handoff from product and design, then figures out how to build it.
Design artifacts are settled facts — do not question or redo design decisions.

**Work folder:** First argument (if a file, use its parent directory)

## Session Persistence

Check for `plan-prep-progress.md` in the work folder. If it exists, read it and resume where left off. Update it after every completed component.

## Prerequisites

`requirements.md` must exist in the work folder. If not:

> "I need requirements before starting. Provide a requirements document."

## Input

Follow the `understanding-the-work.md` component for input handling.

## Output

- `{work-folder}/plan-prep.md` — Analysis, understanding, decisions (Step 1-4)
- `{work-folder}/task/task-list.md` — Index of tasks grouped by dependency wave, with links to task files (Step 5)
- `{work-folder}/task/task-NN.md` — One file per task (zero-padded), with Context / Implementation / Verification / Post verification tasks sections (Step 6)
- `{work-folder}/architecture-decisions.md` — Created by `architect-solution` skill when component 4 runs

---

## Steps

**Step 1:** Understanding What Needs to Be Done. Read and follow `understanding-the-work.md`

**Step 2:** Compose the planning. Read and follow `composing-the-plan.md` to decide which components to include and in what order.
å
### Components

| Component | File | When to include |
|-----------|------|-----------------|
| Planning QA Scenarios | `planning-qa-scenarios.md` | Always |
| Understanding the Current Landscape | `understanding-current-landscape.md` | Always |
| Flow Design | `flow-design.md` | Always |
| Finding the Right Solution | `finding-the-right-solution.md` | Architectural decisions | |
| How Does the Work Break Down? | `how-does-the-work-break-down.md` | Always |

**Supporting files:**
- `skill-development-notes.md` — Notes for future skill iterations (not read during execution)

## Delegated Skills & Agents

This skill orchestrates but delegates heavy work:

| Tool | Used by | What it does |
|------|---------|--------------|
| `architect-solution` skill | Component 3 | Multi-perspective architecture decisions via `code-architect` agents |
| `create-plan-task` skill | Component 6 | Writes each `task-NN.md` (four-section template, subagent dispatch, file verification). Plan-prep invokes in `from-plan-prep` mode so `task-list.md` is not double-updated. Same skill is invoked standalone mid-execution for ad-hoc additions. |
| `code-reviewer` agent (sonnet) | Component 6 | Per-task and grand code reviews |
| `manual-qa-case-writing` skill | Component 5 | Writes/updates `qa.md` for the Grand QA cycle (default step 1) |
| `writing-e2e-tests` skill | Component 5 | Codifies `qa.md` cases as Playwright journey tests (default step 2). Probes the browser itself unless qa-runner evidence is already on disk. |
| `qa-execution` skill | Component 5 | OPTIONAL: scripted manual QA round. Insert between manual-qa-case-writing and writing-e2e-tests only when the user asks for it or when judgment/visual cases warrant a human-checkpointed report. Its evidence (with `role` + `accessible_name`) then feeds `writing-e2e-tests`. |
| `qa-exploratory` skill | Component 5 | OPTIONAL: charter-based exploratory sweep. Add only on user request or for pre-release / a11y-sensitive features. P0/P1 findings are promoted inline back into qa.md. |
| `write-review-guide` skill | Component 5 | Final review walkthrough generation |

## Process

1. Read and follow `understanding-the-work.md` — this component proposes which other Step to include and in what order
2. Get user approval on the proposed component sequence
3. Execute each approved component in order:
   - Read the component's file
   - Follow its process
   - Document output in the appropriate file (`plan-prep.md` for analysis/decisions, or the `task/` folder for the task breakdown)
   - Get user approval before moving to next
4. Present final summary. Get approval.

## Rules

- Each component has approval checkpoints — do not advance without user confirmation
- Ask clarifying questions rather than making assumptions
- Surface point of discusions for Architecture
- Document decisions with rationale
- Use exact file paths (`path/to/file.ts:123-145`), not vague references
- Show full data shapes, not abbreviated JSON
- Use diagrams where they aid understanding
- Delegate to specialized skills and agents — don't replicate their work
