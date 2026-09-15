---
name: performance-reviewer
description: Reviews code changes for database, async, rendering, polling, memory, bundle, worker, cache, scalability, and Core Web Vitals risks. Use when the user asks for a performance review, scalability review, efficiency review, bottleneck review, or a performance lens without a full multi-lens review.
---

# Performance Reviewer

Plan and run a read-only performance review as a standalone skill, or return approved-shape assignments for a combined review.

## Read before planning

- [Performance lens contract and checklist](reference.md)
- [Shared execution contract](../../review-workflows/review-contract.md)
- [Performance review memory](memory.md)

Read each applicable file completely. The lens contract preserves the existing query, async, rendering, polling, memory, bundle, worker, caching, scalability, and Core Web Vitals checks.

## Standalone procedure

1. **Resolve the review basis.** Identify the repository root, requested files/diff/branch/work folder, comparison base, run mode, usable plans/tasks, and output path. Completion: every changed file and expected workload is listed or explicitly unknown; a grand review continues even when all files have no runtime effect.
2. **Name the evidence.** Read relevant plans, performance budgets, architecture and deployment docs, schemas/indexes, query paths, metrics/traces, benchmarks/profiles, tests, adjacent hot-path code, conventions, and performance-memory entries. Record exact paths and absent evidence classes. Completion: supported claims have source-proven current cost plus change-linked impact or a concrete contract contradiction; unsupported workload or measurement hypotheses are mapped to gaps, not findings.
3. **Apply the lens.** Use `reference.md` to map query count/bounds, async concurrency, rendering, polling, memory lifetime, bundle boundaries, worker behavior, caching, Core Web Vitals, and scale assumptions. Treat pattern checks as investigation prompts until caller/consumer evidence proves current cost and change impact. Completion: every changed file and applicable focus area is accounted for, including explicit not-relevant results for a grand review with no runtime path.
4. **Design assignments.** Partition by cohesive hot path or resource domain: database, async/worker, client rendering/bundle, memory/lifecycle, or caching. Keep producers/consumers and benchmark/test evidence together. Assign one primary reviewer per file. Use `reviewer-thorough` for cross-system or scale-model work, `reviewer-staff` for ordinary cohesive cross-file hot paths, and `reviewer-shallow` for a narrow deterministic pattern check; choose the model and thinking effort separately. Completion: each file, hot path, and evidence source has one owner.
5. **Build self-contained prompts.** Include the shared assignment fields, exact lens path or full contents, workload/scale assumptions, Block/Human Review/Suggestion states, required severity, the finding evidence threshold and required `costEvidence` / `changeImpact` or `contractContradiction` / `verificationMeasurement` fields, performance gaps, explicit not-relevant accounting, and positive findings. Completion: an agent with no conversation history can execute each assignment without converting an unsupported hypothesis into a finding.
6. **Display the proposal.** Show scope, plan status, workload assumptions, exact evidence, every assignment's role/model/effort, grouping rationale, total agents/parallelism, output path, merger, and verified model choices. Completion: the proposed review can be inspected before launch.
7. **Obtain approval.** Pause for approval unless autonomous execution was explicitly requested. Autonomous runs still display and record the proposal. Completion: scope is approved or autonomous mode is explicit.
8. **Run the workflow.** Launch `../../review-workflows/review.js` with the approved assignments unchanged. Treat any missing or failed assignment as a terminal incomplete run. Completion: every assignment returns a schema-valid result.
9. **Merge and publish.** Follow the shared workflow rules. Validate reviewer results, run the dedicated merger, and write its validated cohesive artifact preserving lens, action state, bucket, and severity. Completion: the artifact accounts for every file and does not present partial evidence as complete.
10. **Surface results.** Report counts by action state/severity, the highest-impact bottlenecks, measurement gaps, limitations, and output path. Propose memory updates only after human confirmation.

## Reusable worker contract

When the requested output is assignments for a combined review, perform Steps 1–5 and return an assignment manifest with:

- Stable `id`, `label`, `lens: performance`, selected workflow `role`, model/thinking effort, and complete `instructions`.
- Assigned files, hot path/resource domain, workload assumptions, evidence, relevant memory, and grouping rationale.
- Explicit not-applicable files and focus areas.

Stop at the manifest. `code-review-manager` handles the one proposal, approval gate, workflow launch, merger, and final artifact; this mode starts no nested approval or workflow.
