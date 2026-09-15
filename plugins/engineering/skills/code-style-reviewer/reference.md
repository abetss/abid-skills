# Code Style Reviewer — Shared Reference

The selected branch procedure loads this file before planning. This file defines shared selection, ownership, evidence, and execution contracts; `with-plan.md` and `without-plan.md` define the complete ordered paths.

## Review boundary

Review only:

1. Compliance with applicable conventions.
2. Consistency with plan-named examples or, when none are named, similar repository files.
3. Test implementation promised by a plan, when a plan exists.
4. Convention gaps exposed by repeated or consequential patterns.

Leave architecture, product/domain correctness, security, and performance to their dedicated lenses. A shallow reviewer may report an obvious defect only when it directly demonstrates a convention, example, or explicit plan contradiction.

## Review memory

Before proposing assignments, read [`memory.md`](memory.md). Pass only entries relevant to each assignment. Add memory only after explicit human confirmation.

## Convention-library router

Select one convention root:

1. If `~/.agents/conventions/table-of-content.md` exists, use `~/.agents/conventions/`.
2. Otherwise, if `{project}/.agents/conventions/table-of-content.md` exists, use `{project}/.agents/conventions/`.
3. If neither router exists, report exactly: `Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.`

Read the selected `table-of-content.md` completely before selecting conventions. Do not inject or load the whole library. The global library currently routes 15 path-matched documents under `path-matched/` and 5 semantic documents under `content-matched/`; the router and each candidate's current metadata are authoritative if counts change.

### Path-selection pass

1. Start from every target file path and extension.
2. Use the router's path-matched summaries to identify candidates under `path-matched/`.
3. Read each candidate's frontmatter.
4. Select it only when the target path matches its exact `paths` metadata.
5. Record the exact matching pattern and owned file, for example: `path match: **/*.test.ts matched src/x.test.ts`.

A filename keyword or broad thematic similarity does not override exact `paths` metadata.

### Content-selection pass

Inspect the task, diff, imports, APIs, schemas, and changed behavior for semantic triggers. When no formal task exists, the user's request is the task context.

Use the router's content-matched summaries and candidate metadata to narrow inspection. Select a document under `content-matched/` only when the reviewed change actually exercises its semantic trigger. A keyword alone is insufficient. Path hints and `candidatePaths` identify candidates; they do not establish a semantic match.

Record the observed behavior that triggered selection, for example: `content match: changed code converts a local appointment time to UTC before API transmission`.

### Plan references and selection accounting

Plan-referenced conventions are candidates, not automatic matches. Evaluate them through the same path/content procedures. Keep nonmatching and precedence-excluded references out of applicable lists and record each exact path and reason separately.

For every selected convention, record:

- Exact convention path
- `path match` or `content match`
- Specific pattern or observed semantic behavior
- Files owned by the reviewer applying it

Read every selected convention completely before dispatch.

## Repository examples

Repository comparison is always required:

1. Use plan-named example files first.
2. For a file or responsibility with no plan-named example, discover the closest established implementation by responsibility, layer, framework, API shape, and directory.
3. Record each example and why it is comparable.
4. Treat examples as evidence of repository practice, not authority over an explicit convention.

## Assignment design and code-style ownership

Partition by cohesive context rather than raw file count.

- Every reviewed file has exactly one code-style owner.
- Keep implementation and its tests together.
- Keep tightly coupled types, adapters, callers, schemas, and APIs together when separating them would hide behavior.
- Split unrelated applications, layers, convention sets, or responsibilities.
- Give each owner all conventions and examples applicable to its files.
- Use role `reviewer-junior` for every code-style assignment and omit a model override. The role's `junior-high` default supplies Luna high regardless of whether this skill runs standalone or through `code-review-manager`.

Before dispatch, reconcile assignment ownership against the changed-file manifest. Missing or duplicate code-style ownership blocks launch.

## Review proposal

Show before dispatch:

- Scope, comparison base, output, and whether a usable plan exists
- Every reviewed file and its single code-style owner
- Every assignment's role, model/thinking effort, files, and grouping rationale
- Every selected convention with exact path and specific path/content match reason
- Every excluded plan convention with exact path and reason
- Plan-named examples or the repository examples discovered because none were named
- Planned-test source and each assigned test obligation, when applicable
- Evidence gaps and limitations
- Total agents, parallelism, verified reviewer models, and merger role/model

Pause for approval unless autonomous execution was explicit. Autonomous runs still record the complete proposal.

## Findings

Use `Block`, `Human Review`, or `Suggestion`. Every finding includes exact location, current code, the convention/example/plan evidence, concrete reasoning, suggested change, and references. The bucket names the governing convention path, `Repository consistency`, `Planned tests`, or `Convention gap`.

## Planned-test statuses

- **IMPLEMENTED** — every promised behavior and condition is exercised.
- **PARTIAL** — a test exists but omits promised behavior, conditions, assertions, or failure paths.
- **MISSING** — no test exercises the promised behavior.

Cite both the plan requirement and test evidence. Without a plan, do not infer completeness.

## Execution and merger

Launch `../../review-workflows/review.js` only after approval. Independent assignments run in parallel. A council may supply two independent analyses for broad or conflicting work, but every path ends with one dedicated `reviewer-thorough` merger. Validate the merged Markdown against all immutable reviewer evidence before publishing the cohesive artifact.
