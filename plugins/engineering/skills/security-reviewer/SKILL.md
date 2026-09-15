---
name: security-reviewer
description: Reviews code changes through OWASP, CWE, attack-surface, threat-model, and defense-in-depth lenses. Use when the user asks for a security review, AppSec review, vulnerability review, threat review, or a security lens without a full multi-lens review.
---

# Security Reviewer

Plan and run a read-only application-security review as a standalone skill, or return approved-shape assignments for a combined review.

## Read before planning

- [Security lens contract](reference.md)
- [Security checklist](checklist.md)
- [Shared execution contract](../../review-workflows/review-contract.md)
- [Security review memory](memory.md)

Read each applicable file completely. The lens contract and checklist preserve the OWASP/CWE and attacker-minded review substance.

## Standalone procedure

1. **Resolve the review basis.** Identify the repository root, requested files/diff/branch/work folder, comparison base, run mode, usable plans/tasks, and output path. Completion: every changed file and intended security-sensitive behavior is listed.
2. **Name the evidence.** Read relevant plans, threat models, auth and middleware configuration, schemas and authorization policies, environment contracts, dependency manifests/lockfiles, tests, security docs, and security-memory entries. Record exact paths and absent evidence classes. Completion: each trust claim and security control has named evidence or a documented gap.
3. **Map the attack surface.** Use `reference.md` and all 22 checklist categories to identify entry points, attacker-controlled inputs, trust boundaries, sinks, assets, defenses, and negative tests. Completion: every changed file, applicable category, and introduced/modified surface is accounted for.
4. **Design assignments.** Partition by cohesive attack surface or trust boundary. Keep entry points, policies, sinks, and negative tests together. Assign one primary reviewer per file. Use `reviewer-thorough` for auth, cross-tenant, cryptographic, or multi-boundary work, `reviewer-staff` for ordinary bounded cross-file surfaces, and `reviewer-shallow` only for a narrow deterministic control check; choose the model and thinking effort separately. Completion: each file, surface, and evidence source has one owner.
5. **Build self-contained prompts.** Include the shared assignment fields, exact lens/checklist paths or full contents, attack walkthrough requirement, Block/Human Review/Suggestion states, Critical/Major/Minor severities, security-doc gaps, negative-test checks, and teaching moments. Completion: an agent with no conversation history can execute each assignment.
6. **Display the proposal.** Show scope, plan status, attack surfaces, exact evidence, every assignment's role/model/effort, grouping rationale, total agents/parallelism, output path, merger, and verified model choices. Completion: the proposed review can be inspected before launch.
7. **Obtain approval.** Pause for approval unless autonomous execution was explicitly requested. Autonomous runs still display and record the proposal. Completion: scope is approved or autonomous mode is explicit.
8. **Run the workflow.** Launch `../../review-workflows/review.js` with the approved assignments unchanged. Treat any missing or failed assignment as a terminal incomplete run. Completion: every assignment returns a schema-valid result.
9. **Merge and publish.** Follow the shared workflow rules. Validate reviewer results, run the dedicated merger, and write its validated cohesive artifact preserving lens, action state, bucket, and severity. Completion: the artifact accounts for every file and does not present partial evidence as complete.
10. **Surface results.** Report counts by action state and severity, the highest-risk attacks, evidence gaps, limitations, and output path. Propose memory updates only after human confirmation.

## Reusable worker contract

When the requested output is assignments for a combined review, perform Steps 1–5 and return an assignment manifest with:

- Stable `id`, `label`, `lens: security`, selected workflow `role`, model/thinking effort, and complete `instructions`.
- Assigned files, attack surface, trust boundaries, security evidence, relevant memory, and grouping rationale.
- Explicit not-applicable files and checklist categories.

Stop at the manifest. `code-review-manager` handles the one proposal, approval gate, workflow launch, merger, and final artifact; this mode starts no nested approval or workflow.
