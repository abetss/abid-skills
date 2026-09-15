# Shared Review Execution Contract

All standalone reviewer skills and `code-review-manager` use [`review.js`](review.js) after their proposal is approved. `code-style-reviewer` and `code-review-manager` are the primary review skills. The manager or standalone review owner plans scope; the workflow executes only approved assignments and always finishes with one merger.

## Workflow roles

Choose the least expensive role and model effort that can exhaustively review the assignment:

| Role | Use for | Default tier |
|---|---|---|
| `reviewer-junior` | Every code-style assignment | `junior-high` (Luna high) with read-only tools |
| `reviewer-shallow` | Small, direct, low-ambiguity non-code-style checks | `junior-mid` with read-only tools |
| `reviewer-staff` | Ordinary cohesive cross-file non-code-style review | `staff-high` with read-only tools |
| `reviewer-thorough` | Broad, ambiguous, high-risk, architectural, or merger work | `principle-high` with read-only tools |

These are workflow roles, not skills. Every code-style assignment uses `reviewer-junior` and omits `model`, so the role supplies Luna high. Other lenses may use a verified model override when the proposal explains the capability, effort, and cost choice. The dedicated merger always uses `reviewer-thorough` plus the approved merger model.

## Self-contained assignment

Workflow agents inherit no main-thread conversation. Every `instructions` value therefore includes:

1. Repository root and working directory.
2. Review mode, comparison base, changed-file manifest, and output context.
3. Exactly assigned files plus the reason they form one cohesive scope.
4. The complete lens contract and checklist, either inlined or named by exact readable path with an instruction to read each file completely.
5. Every applicable evidence source: plans/tasks, requirements, selected conventions with exact path/content reasons, selected local/global architecture expertise entry points with covered concerns, required relative references, and exact relevance reasons, architecture/product/security docs, schemas, examples, tests, benchmarks, and relevant memory. State when an evidence class is absent.
6. Lens-specific output buckets, action states, severity rules, planned-test requirements, and required gaps/teaching/positive outputs. Architecture, security, and performance findings require severity. Domain findings omit severity. Security permits only `Block + Critical/Major`, `Human Review + Major/Minor`, and `Suggestion + Minor`. Performance findings also require `costEvidence`, `changeImpact` or `contractContradiction`, and `verificationMeasurement`; unsupported hypotheses go in gaps.
7. Instructions to use read-only tools, account for every assigned file, and submit one schema-valid `workflow_result`.

Never rely on a skill having been loaded in the workflow agent's context.

## Memory ownership

Every independently invokable reviewer skill owns and reads its own `memory.md`. The manager's memory contains orchestration guidance only. Assignment prompts receive relevant entries from the assignment lens's local memory; no specialist borrows the manager's memory or another reviewer's memory. Add reusable memory only after human confirmation.

## Proposal

Before launch, display one proposal containing:

- Scope, review mode, comparison base, artifact path, and whether a usable plan exists.
- Selected lens or lenses and why each applies or does not apply.
- One section per assignment: stable ID, lens, role, model/thinking effort, files, evidence paths, relevant memory, and grouping rationale.
- Exactly one code-style owner for every reviewed file.
- Every selected convention's exact path plus its specific path-match pattern or content-match behavior.
- Plan-named examples first, or discovered repository examples when none are named.
- Every selected local/global architecture expertise entry point, the concern it covers, required relative reference, and material relevance reason.
- Total assignments, maximum parallelism, merger role/model, optional council models, and the rationale for every model/effort choice.
- Known evidence gaps and review limitations.

Pause for approval unless autonomous execution was explicitly requested. Autonomous runs still display and record the proposal before launching.

## Workflow arguments

```json
{
  "reviewName": "short stable name",
  "reviewedFiles": ["src/example.ts"],
  "codeStyleOwnership": [
    {
      "file": "src/example.ts",
      "assignmentId": "style-example"
    }
  ],
  "assignments": [
    {
      "id": "style-example",
      "label": "Code style: example conventions",
      "lens": "code-style",
      "role": "reviewer-junior",
      "instructions": "Complete self-contained assignment prompt"
    }
  ],
  "consolidation": {
    "mode": "single",
    "mergerModel": "principle-xhigh"
  }
}
```

`model` is prohibited for code-style assignments and optional for other lenses; omission uses the role default. `reviewedFiles` and `codeStyleOwnership` are required whenever a code-style assignment is present. The workflow rejects a code-style role other than `reviewer-junior`, any code-style model override, and missing, duplicate, extra, or non-code-style ownership. Council mode additionally requires distinct `primaryModel` and `secondaryModel` values; after those analyses complete, `mergerModel` still produces the single final artifact. Resolve all names from the installed workflow catalog rather than guessing.

Run the workflow with `scriptPath` pointing to `plugins/engineering/review-workflows/review.js` or the correct installed-plugin path.

## Validation, merger, and publication

1. Reconcile every returned key and each result's `assignmentId` and `lens` against the approved assignment manifest.
2. Apply lens-aware required-field and action-state/severity validation.
3. For code-style assignments, reconcile `filesReviewed` plus `notRelevant` against approved ownership; every owned file appears exactly once and no worker accounts for another owner's file.
4. In council mode, obtain two independent analyses of the same immutable approved manifest and reviewer packet.
5. Launch one `reviewer-thorough` merger with the approved merger model. It receives the manifest, all reviewer packets, and any council analyses.
6. Preserve lens attribution, action state, bucket/provenance, severity where defined, evidence, file accounting, planned-test status, gaps, teaching moments, and positive findings. Merge only exact same-lens duplicates.
7. The main-thread owner validates the merged Markdown against the immutable packet, then writes it to the approved artifact path.

A failed, missing, extra, identity-mismatched, or coverage-mismatched assignment blocks the merger. Reviewer and council outputs are evidence, never publishable substitutes for the cohesive merged artifact.
