---
name: architecture-reviewer
description: Reviews code changes for architectural strengths, weaknesses, gaps, coupling, boundaries, resilience, and change cost. Use for an architecture review, architectural code review, system-boundary review, or an architecture lens without the full thorough review.
---

# Architecture Reviewer

Plan and run a read-only architecture review as a standalone skill, or return assignments for `code-review-manager` without starting nested approval or execution.

## Read before planning

- [Architecture lens contract](reference.md)
- [Architecture checklist](checklist.md)
- [Shared execution contract](../../review-workflows/review-contract.md)
- [Architecture review memory](memory.md)
- [Canonical architect solution](../architect-solution/SKILL.md)

Read the lens, checklist, execution contract, and canonical architect-solution skill completely. Architect-solution owns architecture expertise routing; the reviewer applies its result rather than maintaining a second router.

## Passive architecture expertise

Follow architect-solution's local-first fallback exactly:

1. Inspect `../architect-solution/experts/` for local `*/expertise.md` entry points. Treat an absent directory as empty.
2. Compare every local trigger with the reviewed problem, proposed or implemented solution, constraints, system qualities, and likely failure modes.
3. Load each materially relevant local entry point and its required relative references.
4. For every material concern not covered locally, read `/Users/abtinghods/.agents/expertise/table-of-content.md` completely, consider every `ACTIVE` entry, and ignore every other status.
5. Load only materially relevant global `expertise.md` entry points and their required relative references.

Local expertise takes precedence for plugin-specific guidance; global expertise fills uncovered concerns. These are passive references, not skills, and the complete library is never loaded by default.

## Standalone procedure

1. **Resolve the basis.** Identify project root, requested files/diff/branch/work folder, comparison base, mode, plan/task files, and output path. Completion: every changed file and intended behavior is listed or explicitly unknown.
2. **Name architecture evidence.** Read relevant intent, architecture docs, schemas/policies, contracts, tests, and memory. Record exact paths and absent evidence classes. Completion: architecture claims have named evidence or an explicit gap.
3. **Route expertise.** Apply the canonical architect-solution routing gate: inspect its optional local `experts/` first, treat absence as empty, then use the global expertise index only for uncovered material concerns. Read selected entry points and all references they require. Completion: every material concern records its selected local/global expertise and concrete problem/solution reason, or records that no supplemental expertise applies.
4. **Apply the lens.** Use `reference.md`, selected expertise guidance, and all 15 checklist categories. Classify every file as architecture-relevant or not relevant and choose tight, medium, or wide exploration. Completion: no file, selected expertise, or applicable category is silently dropped.
5. **Design assignments.** Partition by cohesive subsystem, boundary, data flow, or selected expertise concern. Keep contracts and callers together. Assign one primary reviewer per file and choose `reviewer-shallow`, `reviewer-staff`, or `reviewer-thorough`, plus a justified model and thinking effort; architecture defaults to thorough with higher effort, uses staff for ordinary bounded cross-file analysis, and uses shallow only for a direct low-ambiguity check. Completion: every file, evidence source, expertise bundle, and checklist area has one owner.
6. **Build self-contained prompts.** Include basis, files, lens/checklist/router paths, selected expertise entry points, required references, selection reasons, memory, exploration breadth, Introduced/Exposed/Observed mapping, severity, documentation gaps, positives, and teaching moments. Completion: agents need no conversation history.
7. **Display the proposal.** Show scope, plan, evidence, exploration breadth, every assignment's role/model/effort, selected expertise with reasons, grouping, parallelism, output, merger, and verified models. Completion: the complete review is inspectable.
8. **Obtain approval.** Pause unless autonomous execution was explicit. Autonomous runs still record the proposal. Completion: approved or autonomous.
9. **Run in parallel.** Launch `../../review-workflows/review.js` with approved assignments unchanged. Missing or failed work makes the run incomplete.
10. **Merge and publish.** Validate reviewer results, run the dedicated merger, validate its output, then write one cohesive artifact preserving lens, action state, bucket, severity, selected-expertise provenance, and file accounting.
11. **Surface results.** Report counts, top findings, selected expertise, gaps, limitations, and output path; propose memory only after human confirmation.

## Reusable worker contract

When `code-review-manager` requests assignments, perform Steps 1–6 and return:

- Stable `id`, `label`, `lens: architecture`, selected workflow role, model/thinking effort, and self-contained instructions.
- Assigned files, architecture evidence, memory, exploration breadth, and grouping rationale.
- Every selected expertise entry point, required reference, and concrete relevance reason, or explicit no-expertise accounting.
- Explicit not-applicable files, expertise entries, and checklist categories.

Stop at the manifest. The manager handles its one proposal, approval, workflow, merger, and artifact.
