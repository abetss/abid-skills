# Code-Style Review — With Plan

This file is the procedural source of truth when a usable plan or task document exists.

When `code-review-manager` requests reusable assignments, Steps 1–8 return the complete code-style manifest and stop. The manager controls the combined proposal, approval, workflow, merger, and artifact.

## Procedure

1. **Load contracts.** Read `reference.md`, `memory.md`, and `../../review-workflows/review-contract.md` completely. Completion: selection, ownership, evidence, output, and execution contracts are known.
2. **Resolve the basis.** Identify project root, work folder, plan/tasks, comparison base, complete changed-file manifest, and output path. Read the plan completely. Completion: every reviewed file is tied to intent or explicitly plan-external.
3. **Extract obligations.** Record files, convention references, example references, every promised test/verification scenario, exceptions, and deferrals. Completion: every checkable plan statement is represented.
4. **Read the convention router.** Select the global router first or project router only when global is absent, following `reference.md`. If neither exists, record exactly: `Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.` Completion: one router/root or explicit absence is recorded.
5. **Run the path pass.** Match target paths/extensions through router summaries and exact candidate `paths` metadata. Completion: every selected path convention has its exact pattern, matched file, and reason.
6. **Run the content pass.** Inspect the task, diff, imports, APIs, schemas, and changed behavior. Select content conventions only for observed semantic triggers; a keyword alone is insufficient. Completion: every selected content convention has a concrete behavior reason.
7. **Resolve examples and tests.** Read plan-named examples first. Discover comparable repository examples only for responsibilities with none named. Map every promised test to candidate evidence or explicit absence. Completion: examples and all planned tests are accounted for.
8. **Design assignments.** Give every reviewed file exactly one code-style owner; keep cohesive source/tests/contracts together and assign every selected convention/example/test. Every code-style assignment uses role `reviewer-junior` and omits a model override so the role supplies Luna high. Reconcile ownership against the changed-file manifest. Completion: no file has missing or duplicate code-style ownership and every assignment has the fixed role with no model override.
9. **Display the proposal.** Show every field required by `reference.md`, including each convention's exact path/content reason, owner, examples, and planned-test source. Completion: the user can inspect the complete run.
10. **Obtain approval.** Pause unless autonomous execution was explicit. Re-display any revised proposal. Completion: approved or autonomous.
11. **Execute in parallel.** Launch the shared workflow with the approved `reviewedFiles`, `codeStyleOwnership`, and assignments unchanged. Any failed/missing assignment makes the run incomplete.
12. **Merge and publish.** Validate reviewer results, run the dedicated merger, validate its output, then write one cohesive artifact with convention accounting and the complete IMPLEMENTED/PARTIAL/MISSING matrix.
13. **Surface results.** Report counts, top findings, test statuses, limitations, and output path; propose memory only after human confirmation.
