---
name: domain-expert-reviewer
description: Reviews code changes for product correctness, business rules, state transitions, invariants, user journeys, and domain commitments. Use when the user asks for a domain review, business-logic review, product-correctness review, or a domain lens without a full multi-lens review.
---

# Domain Expert Reviewer

Plan and run a read-only product-correctness review as a standalone skill, or return approved-shape assignments for a combined review.

## Read before planning

- [Domain lens contract](reference.md)
- [Domain checklist](checklist.md)
- [Shared execution contract](../../review-workflows/review-contract.md)
- [Domain review memory](memory.md)

Read each applicable file completely. The lens contract and checklist preserve the full 19-category domain review.

## Standalone procedure

1. **Resolve the review basis.** Identify the repository root, requested files/diff/branch/work folder, comparison base, run mode, usable plans/tasks/requirements, and output path. Completion: every changed file is listed and every available source of product intent is known.
2. **Name the evidence.** Read relevant task files, acceptance criteria, product/business-knowledge docs, schemas and authorization policies, tests, adjacent business logic, and domain-memory entries. Record exact paths and absent evidence classes. Completion: each product claim can be tied to evidence or identified as undocumented.
3. **Apply the lens.** Use `reference.md` and all 19 checklist categories to map business rules, states, invariants, journeys, side effects, roles, tenants, and product commitments touched by the change. Completion: every changed file and applicable category is accounted for.
4. **Design assignments.** Partition by cohesive journey, entity lifecycle, invariant set, or business flow. Keep implementation, tests, and cross-feature callers together. Assign one primary reviewer per file. Use `reviewer-thorough` for ambiguous or high-consequence invariants, `reviewer-staff` for ordinary cohesive cross-file flows, and `reviewer-shallow` only for a narrow explicit product-doc comparison; choose the model and thinking effort separately. Completion: each file, rule, journey, and evidence source has one owner.
5. **Build self-contained prompts.** Include the shared assignment fields, exact lens/checklist paths or full contents, the no-severity Block/Human Review/Suggestion rules, product-doc gaps, journey/test obligations, positive findings, and teaching moments. Completion: an agent with no conversation history can execute each assignment.
6. **Display the proposal.** Show scope, plan status, exact product evidence, every assignment's role/model/effort, grouping rationale, total agents/parallelism, output path, merger, and verified model choices. Completion: the proposed review can be inspected before launch.
7. **Obtain approval.** Pause for approval unless autonomous execution was explicitly requested. Autonomous runs still display and record the proposal. Completion: scope is approved or autonomous mode is explicit.
8. **Run the workflow.** Launch `../../review-workflows/review.js` with the approved assignments unchanged. Treat any missing or failed assignment as a terminal incomplete run. Completion: every assignment returns a schema-valid result.
9. **Merge and publish.** Follow the shared workflow rules. Validate reviewer results, run the dedicated merger, and write its validated cohesive artifact while preserving lens, action state, and bucket and omitting severity from every domain finding. Completion: the artifact accounts for every file and does not present partial evidence as complete.
10. **Surface results.** Report counts by action state, the most consequential product findings, evidence gaps, limitations, and output path. Propose memory updates only after human confirmation.

## Reusable worker contract

When the requested output is assignments for a combined review, perform Steps 1–5 and return an assignment manifest with:

- Stable `id`, `label`, `lens: domain`, selected workflow `role`, model/thinking effort, and complete `instructions`.
- Assigned files, product evidence, relevant memory, affected journeys/invariants, grouping rationale, and the explicit rule that domain findings omit severity.
- Explicit not-applicable files and checklist categories.

Stop at the manifest. `code-review-manager` handles the one proposal, approval gate, workflow launch, merger, and final artifact; this mode starts no nested approval or workflow.
