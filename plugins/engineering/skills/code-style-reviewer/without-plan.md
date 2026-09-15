# Code-Style Review — Without Plan

This file is the procedural source of truth when no usable plan or task document exists.

When `code-review-manager` requests reusable assignments, Steps 1–7 return the complete code-style manifest and stop. The manager controls the combined proposal, approval, workflow, merger, and artifact.

## Procedure

1. **Load contracts.** Read `reference.md`, `memory.md`, and `../../review-workflows/review-contract.md` completely. Completion: selection, ownership, evidence, output, and execution contracts are known.
2. **Resolve the basis.** Identify project root, requested files/diff/branch, comparison base, complete changed-file manifest, and output path. Completion: every reviewed file is known.
3. **Read the convention router.** Select the global router first or project router only when global is absent, following `reference.md`. If neither exists, record exactly: `Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.` Completion: one router/root or explicit absence is recorded.
4. **Run the path pass.** Match target paths/extensions through router summaries and exact candidate `paths` metadata. Completion: every selected path convention has its exact pattern, matched file, and reason.
5. **Run the content pass.** Inspect the request, diff, imports, APIs, schemas, and changed behavior. Select content conventions only for observed semantic triggers; a keyword alone is insufficient. Completion: every selected content convention has a concrete behavior reason.
6. **Resolve examples.** For every implementation responsibility, discover the closest established repository example because no plan-named examples exist. Record why each is comparable. Review changed tests as ordinary files, without inferring test completeness.
7. **Design assignments.** Give every reviewed file exactly one code-style owner; keep cohesive source/tests/contracts together and assign every selected convention/example. Every code-style assignment uses role `reviewer-junior` and omits a model override so the role supplies Luna high. Reconcile ownership against the changed-file manifest. Completion: no file has missing or duplicate code-style ownership and every assignment has the fixed role with no model override.
8. **Display the proposal.** Show every field required by `reference.md`, including each convention's exact path/content reason, owner, and examples. State: `Planned-test completeness will not be assessed because no usable plan was provided or discovered.`
9. **Obtain approval.** Pause unless autonomous execution was explicit. Re-display any revised proposal. Completion: approved or autonomous.
10. **Execute in parallel.** Launch the shared workflow with the approved `reviewedFiles`, `codeStyleOwnership`, and assignments unchanged. Any failed/missing assignment makes the run incomplete.
11. **Merge and publish.** Validate reviewer results, run the dedicated merger, validate its output, then write one cohesive artifact with convention accounting and the no-plan limitation.
12. **Surface results.** Report counts, top findings, limitations, and output path; propose memory only after human confirmation.
