---
name: code-style-reviewer
description: Plans and runs a parallel code-style review against applicable global or project conventions, repository examples, and planned tests when a plan exists. Use for shallow review, convention review, code-style review, rules review, or focused plan-conformance review without the full multi-lens review.
---

# Code Style Reviewer

Plan a focused read-only review in the main conversation, show file ownership and every selected convention before dispatch, then run the approved assignments in parallel and merge one report.

## Route to one procedural source

1. Resolve the requested files, diff, branch, or work folder.
2. Determine whether a usable implementation plan or task file was supplied or exists in the supplied work folder.
3. If a plan exists, read and follow [with-plan.md](with-plan.md).
4. Otherwise, read and follow [without-plan.md](without-plan.md).

The selected branch is the complete procedural source of truth. Each branch explicitly loads [reference.md](reference.md), [memory.md](memory.md), the selected convention-library router, and the [shared execution contract](../../review-workflows/review-contract.md).

## Reusable worker contract

When `code-review-manager` requests assignments, follow the selected branch only through assignment design and return:

- Stable `id`, `label`, `lens: code-style`, fixed workflow `role: reviewer-junior`, no model override, and complete self-contained `instructions`.
- Exactly owned files: every reviewed file has one code-style owner.
- Every selected convention with its exact path and a specific path-match or content-match reason.
- Excluded plan-referenced convention candidates with exact paths and reasons.
- Plan-named examples first; repository-discovered examples only where the plan names none.
- Every planned test and its source when a plan exists; the explicit no-plan limitation otherwise.
- Relevant memory, evidence gaps, and grouping rationale.

Stop at the assignment manifest. `code-review-manager` owns the combined proposal, approval gate, workflow launch, merger, and final artifact. This mode starts no nested approval or workflow.

## Files

```text
SKILL.md
reference.md
with-plan.md
without-plan.md
memory.md
```

Execution is shared at `../../review-workflows/review.js`.
