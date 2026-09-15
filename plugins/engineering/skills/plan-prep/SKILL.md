---
name: plan-prep
description: Modular engineering planning — from requirements intake through implementation-ready tasks. Composable Step selected per feature. Replaces separate plan-prep and plan-implement workflows.
argument-hint: "[work folder path]"
disable-model-invocation: true
---

# Plan Preparation & Implementation Planning

You are a principle software engineer and received this requirements to complete.

**Work folder:** First argument (if a file, use its parent directory)

## Session Persistence

Check for `plan-prep-progress.md` in the work folder. If it exists, read it and resume where left off. Update it after every completed component.

## Input

`requirements.md` or a file the user pass as requirement must exist in the work folder. If not:

> "I need requirements before starting. Provide a requirements document."

## Output

- `{work-folder}/plan-prep.md` — Analysis, understanding, and selected-component outputs
- `{work-folder}/technical-design.md` — Aggregate modules, boundaries, interfaces, types, schemas, and contracts when those Design the Solution concerns are selected
- `{work-folder}/existing-solutions.md` — Native platform capabilities and nearby existing implementations when Discover Existing Capabilities and Solutions is selected
- `{work-folder}/solution-research.md` — Broader external precedent research when Research Solution Precedents is selected
- `{work-folder}/architecture/table-of-contents.md` — Index of material architecture decisions
- `{work-folder}/architecture/ADR-NNN-short-title.md` — One dedicated ADR per material architecture decision
- `{work-folder}/task/task-list.md` — Index of tasks grouped by dependency wave, with links to task files
- `{work-folder}/task/task-NN.md` — One file per task (zero-padded), with Context / Implementation / Verification / Post verification tasks sections

---

## Steps

**Step 1:** Understanding What Needs to Be Done. Read and follow `components/understanding-the-work/SKILL.md`

**Step 2:** Compose the planning. Read and follow `components/composing-the-plan/SKILL.md` to select components and map their actual dependencies. Execute the approved composition sequentially, in parallel, or iteratively as those dependencies require.

### Components

| Component | File | When to include |
|-----------|------|-----------------|
| Planning QA Scenarios | `components/planning-qa-scenarios/SKILL.md` | Always |
| Understand the Current Repo Landscape | `components/understanding-current-repo-landscape/SKILL.md` | Work modifies or integrates with an existing repository or codebase |
| Discover Existing Capabilities and Solutions | `components/discover-existing-capabilities-and-solutions/SKILL.md` | Work builds on a named platform, creates a new tool/extension/system, or requires an adopt-versus-extend-versus-build decision |
| Design the Solution | `components/design-the-solution/SKILL.md` | Desired flows, module boundaries, contracts, or architecture decisions need design |
| Research Solution Precedents | `components/research-solution-precedents/SKILL.md` | Broader external evidence would improve an unfamiliar, consequential, or contested decision after nearby solutions are understood |
| How Does the Work Break Down? | `components/how-does-the-work-break-down/SKILL.md` | Work requires more than one implementation task |

Architecture-decision discovery is cross-cutting, not a selectable component. Every selected component reads and follows `components/architecture-decision-protocol.md`, surfaces the architecture points found during its own work, and returns contributions to the plan-prep/workflow owner. The workflow owner consolidates the architecture table of contents; parallel workers return contributions rather than editing it.

**Supporting files:**
- `development/skill-development-notes.md` — Notes for future skill iterations (not read during execution)

## Delegated Skills & Agents

This skill orchestrates but delegates heavy work:

| Tool | Used by | What it does |
|------|---------|--------------|
| `architect-solution` skill | Architecture-decision owners | Expertise-routed direct or multi-perspective resolution, with one exact ADR owner per assigned decision |
| `create-plan-task` skill | How Does the Work Break Down? | Writes each `task-NN.md` (four-section template, subagent dispatch, file verification). Plan-prep invokes in `from-plan-prep` mode so `task-list.md` is not double-updated. Same skill is invoked standalone mid-execution for ad-hoc additions. |
| `code-style-reviewer` with role `reviewer-junior` | Each implementation task | Runs exactly one focused code-style review over the files changed by that task |
| `manual-qa-case-writing` skill | How Does the Work Break Down? | Writes/updates `qa.md` for the Grand QA cycle (default step 1) |
| `writing-e2e-tests` skill | How Does the Work Break Down? | Codifies `qa.md` cases as Playwright journey tests (default step 2). Probes the browser itself unless qa-runner evidence is already on disk. |
| `qa-execution` skill | How Does the Work Break Down? | OPTIONAL: scripted manual QA round. Insert between manual-qa-case-writing and writing-e2e-tests only when the user asks for it or when judgment/visual cases warrant a human-checkpointed report. Its evidence (with `role` + `accessible_name`) then feeds `writing-e2e-tests`. |
| `qa-exploratory` skill | How Does the Work Break Down? | OPTIONAL: charter-based exploratory sweep. Add only on user request or for pre-release / a11y-sensitive features. P0/P1 findings are promoted inline back into qa.md. |
| `write-review-guide` skill | How Does the Work Break Down? | Final review walkthrough generation |

## Process

1. Read and follow `components/understanding-the-work/SKILL.md`.
2. Read and follow `components/composing-the-plan/SKILL.md`; get user approval on the selected components and dependency plan.
3. Execute the approved dependency plan:
   - Read each selected component's file
   - Follow its process, running the largest dependency-ready set concurrently and iterating only where outputs create real dependencies
   - Document output in the component's specified artifact
   - Verify the component's required coverage and completion criteria; an agent exit or populated artifact alone is not completion
   - At each component's approval checkpoint, get user approval before dependent work proceeds
4. Present final summary. Get approval.

## Rules

- Before starting any component, announce exactly: `Plan prep: {Component Name} starting`
- At every execution boundary, run the largest ready set concurrently up to available concurrency; serialize only true input dependencies, user checkpoints, or single-writer operations
- Do not add planning-artifact review stages unless the user explicitly requests the specific review
- Each component has approval checkpoints — do not advance without user confirmation
- Ask clarifying questions rather than making assumptions
- Surface architecture points through `components/architecture-decision-protocol.md`
- Document decisions with rationale
- Use exact file paths (`path/to/file.ts:123-145`), not vague references
- Show full data shapes, not abbreviated JSON
- Use Mermaid for dependency, flow, sequence, state, and architecture diagrams when they aid understanding; place each diagram in the component-owned artifact beside the content it explains
- Delegate to specialized skills and agents — don't replicate their work
- Preserve component procedures in delegated prompts and verify their completion criteria before accepting results
