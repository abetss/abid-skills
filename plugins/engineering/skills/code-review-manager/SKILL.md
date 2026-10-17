---
name: code-review-manager
description: Plans and runs a complete multi-lens code review, choosing reviewers, workflow roles, models, thinking effort, parallelism, and a final merger that produces one cohesive review artifact. Use when reviewing a feature branch, PR, changed files, task/work folder, or completed implementation before merge.
---

# Code Review Manager

Own the review from evidence gathering through one cohesive artifact. Select applicable reviewer skills, compose their reusable worker contracts into one approved workflow run, and send every validated result through a dedicated merger. [SPEC.md](SPEC.md) is the human reference; this file owns execution.

## Read before planning

- [Review memory](memory.md)
- [Shared execution contract](../../review-workflows/review-contract.md)
- [Code-style reviewer](../code-style-reviewer/SKILL.md)
- [Architecture reviewer](../architecture-reviewer/SKILL.md)
- [Domain expert reviewer](../domain-expert-reviewer/SKILL.md)
- [Security reviewer](../security-reviewer/SKILL.md)
- [Performance reviewer](../performance-reviewer/SKILL.md)

Read every selected skill and every reference/checklist/router it requires. Use reusable worker contracts only; standalone approval and launch steps do not run inside the manager.

## Lens selection

For a grand review, select all five lenses unless the user explicitly overrides them. Performance still runs on documentation-only or no-runtime grand reviews and returns not-relevant accounting. For a per-task review:

- **code-style-reviewer** — always; path/content-selected conventions, repository examples, and planned tests when a plan exists.
- **architecture-reviewer** — boundaries, schemas/migrations, infrastructure, modules/integrations, cross-application contracts, or other architectural concerns.
- **domain-expert-reviewer** — business rules, states, invariants, journeys, validation, data integrity, consent, audit, or privacy-sensitive product behavior.
- **security-reviewer** — auth/session/token handling, authorization, endpoints/middleware, third-party calls, uploads, dependencies/secrets, or untrusted input reaching a sink.
- **performance-reviewer** — queries/indexes, unbounded data, async fan-out, polling, rendering/bundles, memory/listeners, workers/queues, caching, or performance budgets.

Use an explicit lens override verbatim. Record why every selected and skipped lens applies.

## Procedure

1. **Resolve the basis.** Identify project root, comparison base, complete changed-file manifest, plans/tasks/requirements, review mode, and artifact path. Read the full diff and relevant intent files. Completion: every reviewed file and changed behavior is known or explicitly unknown.
2. **Read memory.** Read the manager's `memory.md` for orchestration guidance. Read each selected reviewer skill's own `memory.md` for lens-specific false positives, accepted trade-offs, calibration, and deferred gaps. Completion: every selected lens has local memory accounting and no specialist memory is inferred from the manager's file.
3. **Select lenses.** Apply the rules above or the user's exact override. Read each selected skill's reusable contract and linked material. Completion: every selected/skipped lens has an evidence-based rationale.
4. **Build the code-style manifest.** Ask `code-style-reviewer` to select its with-plan or without-plan branch and return assignments without approval or launch. It reads the selected convention router, runs exact path matching and evidence-based semantic matching, assigns each reviewed file one code-style owner, prefers plan-named examples, discovers examples when none are named, and accounts for all planned tests. Completion: every file has exactly one code-style owner and every selected convention has a specific path/content reason.
5. **Route architecture expertise.** When architecture is selected, require `architecture-reviewer` to follow canonical `architect-solution`: inspect its optional local `experts/` first (absent equals empty), then consult every `ACTIVE` global expertise trigger only for material concerns still uncovered. Read each selected entry point and required relative reference. Completion: selected local/global expertise, covered concerns, references, and problem/solution reasons are explicit, or the manifest records that no supplemental expertise applies.
6. **Build specialist manifests.** Ask each other selected lens to partition its files/evidence without launching. Reconcile ownership per lens; cross-lens overlap is intentional. Completion: every file, lens, evidence source, convention, and selected architecture expertise bundle has an owner.
7. **Choose execution profiles.** Fix every code-style assignment to role `reviewer-junior` with no model override so it inherits Luna high. For every other lens, choose `reviewer-shallow`, `reviewer-staff`, or `reviewer-thorough`, then choose a verified model override only when justified. Use the least expensive capability that can exhaustively handle the scope. Separately choose the merger model and effort. Completion: every code-style assignment has the fixed role and no override; every other reviewer and the merger has a recorded role, model, thinking effort, and rationale.
8. **Build self-contained prompts.** Create a temporary checkout only when the review requires one. Put temporary checkouts and review files in the task's work folder or `<project-root>/tmp/` (ensure repository-local temporary files are Git-ignored); if neither is available, use `~/Ork/.worktrees/` for checkouts and `~/Ork/tmp/` for other files. Use these locations rather than the OS `/tmp` or `/private/tmp`. Before launch, verify the chosen path is permitted by the reviewer's file tools, and put its exact absolute path and an explicit `cd` instruction in the assignment; set the reviewer working directory to that path only when the execution interface supports it. Follow the shared execution contract. Include project/basis details, files, lens/checklist/router paths, selected conventions and reasons, selected expertise entry points, required references, and reasons, examples, plans/tests, relevant memory, and output rules. Completion: workflow agents need no main-thread context and can read the assigned checkout and review files.
9. **Display one combined proposal.** Show scope/mode/artifact, plan status, selected/skipped lenses, every file/lens/role/model assignment, each file's code-style owner, selected conventions with path/content reasons, examples, planned-test source, architecture expertise with entry points, required references, and reasons, grouping rationale, total agents/parallelism, limitations, merger role/model, and optional council models. Completion: the complete run and its cost/quality choices are inspectable.
10. **Ask once.** Pause for approval unless autonomous execution was explicit. Incorporate requested changes and re-display the updated proposal. Autonomous runs still record it. Completion: approved or autonomous.
11. **Execute once.** Launch `../../review-workflows/review.js` with the approved files, ownership, assignments, per-assignment model overrides, and merger configuration unchanged. Any failed, missing, extra, identity-mismatched, or coverage-mismatched assignment makes the run incomplete.
12. **Merge.** The workflow validates all reviewer packets, optionally obtains two independent council analyses, and then launches one `reviewer-thorough` merger with the approved merger model. The merger receives the approved manifest and all immutable evidence and returns one cohesive Markdown report. Completion: one report preserves lens, action state, bucket, severity where defined, evidence, planned-test status, gaps, teaching moments, and positive findings.
13. **Validate and publish.** Validate the merged report against every reviewer result, then write that report to the approved artifact path. Report counts, top findings, selected convention/expertise evidence, planned-test statuses or no-plan limitation, other limitations, and artifact path. Propose memory updates only after human confirmation.

A council analysis, surviving subset of failed assignments, or unvalidated merger output is partial evidence, not a completed review.
