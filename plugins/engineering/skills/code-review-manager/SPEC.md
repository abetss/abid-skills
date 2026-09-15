# Code Review Manager — Specification

This is the human reference for `code-review-manager`. `SKILL.md` owns execution; keep both aligned.

## Purpose

Run specialized code-style, architecture, domain, security, and performance reviews in parallel, then pass their validated evidence to one dedicated merger that produces a cohesive review artifact. Every lens remains independently invokable and exposes a reusable assignment contract for manager runs.

The manager:

- Plans file/lens ownership and evidence before dispatch.
- Fixes code-style assignments to `reviewer-junior` with its Luna-high default; selects role, model, and thinking effort for other lenses.
- Shows the complete plan and asks once unless autonomous execution was explicit.
- Composes lens contracts without recursively starting their standalone approvals or workflows.
- Gives workflow agents self-contained prompts.
- Validates returned assignment identity and file coverage before merger execution.
- Publishes one merged artifact; partial reviewer or council output is never the final review.

## Skills and workflow roles

User-facing review skills:

- `code-style-reviewer` — focused convention/example/planned-test review.
- `code-review-manager` — multi-lens orchestration, model/effort selection, workflow execution, merger, and artifact publication.
- `architecture-reviewer`, `domain-expert-reviewer`, `security-reviewer`, and `performance-reviewer` — independently invokable specialist lenses.

Workflow-only roles:

- `reviewer-junior` — every code-style assignment; defaults to `junior-high` (Luna high).
- `reviewer-shallow` — bounded, direct, low-ambiguity non-code-style assignments; defaults to `junior-mid`.
- `reviewer-staff` — ordinary cohesive cross-file non-code-style assignments; defaults to `staff-high`.
- `reviewer-thorough` — broad, ambiguous, high-risk, architectural, or merger assignments; defaults to `principle-high`.

Roles define read-only review behavior and model defaults. Code-style assignments always use `reviewer-junior` without a model override. The manager may override another lens's role model with a verified alias or `provider/model:thinking` value when the proposal explains the quality/cost reason.

## Active lenses

| Skill | Default inclusion | Output semantics |
|---|---|---|
| `code-style-reviewer` | Every review | Block/Human Review/Suggestion; planned tests IMPLEMENTED/PARTIAL/MISSING only with a plan |
| `architecture-reviewer` | Grand; per-task for architecture-relevant changes | Introduced/Exposed/Observed + action state + severity |
| `domain-expert-reviewer` | Grand; per-task for product/domain behavior | Checklist bucket + action state; no severity |
| `security-reviewer` | Grand; per-task for security surfaces | OWASP/CWE bucket + action state + severity |
| `performance-reviewer` | Every grand review; per-task for performance surfaces | Focus bucket + action state + severity and measured/evidenced cost fields |

Explicit user overrides replace defaults. Record why every lens is selected or skipped.

## Code-style convention selection

The code-style lens selects one router:

1. `~/.agents/conventions/table-of-content.md` when present.
2. `{project}/.agents/conventions/table-of-content.md` only when the global router is absent.
3. If neither exists: `Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.`

Read the router before selecting documents; never load the entire library by default.

### Path pass

Use target paths/extensions and router summaries to identify `path-matched/` candidates. Read candidate frontmatter and select only exact `paths` metadata matches. Record the exact pattern and matched file.

### Content pass

Inspect the task, diff, imports, APIs, schemas, and changed behavior. Use router summaries and content metadata to identify `content-matched/` candidates. Select only when the change actually exercises a semantic trigger. Keywords and candidate paths narrow inspection but do not establish a match. Record the observed behavior that caused each selection.

Plan references are candidates only and pass through the same matching rules. Every selected convention is listed in the proposal with its exact path, match kind, specific reason, and code-style owner. Nonmatching or precedence-excluded references are accounted separately.

Each reviewed file has exactly one code-style owner. Use plan-named examples first; when none are named for a responsibility, discover the closest established repository example. With a plan, account for every promised test as IMPLEMENTED, PARTIAL, or MISSING.

## Architecture expertise routing

Before architecture assignments are proposed, `architecture-reviewer` follows the expertise-routing gate owned by `../architect-solution/SKILL.md`:

1. Inspect `../architect-solution/experts/` for local `*/expertise.md` entry points; absence is equivalent to an empty directory.
2. Compare every local trigger with the problem, proposed or implemented solution, changed system, requirements, likely failure modes, and scale/correctness boundaries.
3. Read materially relevant local entry points and every required relative reference.
4. Identify material concerns not covered by local expertise.
5. For those uncovered concerns, read `/Users/abtinghods/.agents/expertise/table-of-content.md` completely, consider every `ACTIVE` entry, and ignore every other status.
6. Read only materially relevant global entry points and every required relative reference.
7. List each selected local/global entry point, covered concern, required reference, and concrete reason in the review plan.
8. Record that no supplemental architecture expertise materially applies when none qualifies.

`architect-solution` is the canonical architecture owner. Local expertise controls plugin-specific guidance; the global index fills uncovered concerns. No review injects the complete passive library automatically.

## Assignment, model, and effort contract

Partition by cohesive context rather than raw file count. Every file has one primary owner per selected lens and exactly one code-style owner. Cross-lens overlap is expected.

For every assignment the manager records:

- Stable ID, label, lens, files, evidence, and grouping rationale.
- `reviewer-junior` for every code-style assignment; `reviewer-shallow`, `reviewer-staff`, or `reviewer-thorough` for other lenses.
- No model override for code-style; a verified model override for another lens only when its role default is not the best fit.
- Why the selected capability and thinking effort are sufficient without unnecessary cost.

Code-style execution always inherits Luna high from `reviewer-junior`. Use shallow execution for other direct bounded checks, staff execution for ordinary cohesive cross-file reasoning, and thorough execution for architecture, ambiguous invariants, security boundaries, cross-system performance models, and merger work. The merger normally uses the strongest justified thorough model.

Every prompt names project root, basis, files, lens/checklist/router, selected convention evidence, selected expertise entry points and required references, examples, plans/tests, relevant memory, output semantics, and accounting requirements.

## Proposal and approval

Before dispatch, show:

- Scope, mode, comparison base, artifact path, files, and plan status.
- Selected/skipped lenses and reasons.
- Every assignment's role, model/thinking effort, files, evidence, and grouping rationale.
- Each file's code-style owner.
- Every selected convention with exact path and path/content reason.
- Plan-named or discovered examples.
- Planned-test source and assignment, when present.
- Selected architecture expertise with entry points, required references, and reasons.
- Total assignments/parallelism, known gaps, and limitations.
- Merger role/model and optional council model choices.

Pause for approval unless autonomous execution was explicit. Autonomous runs still record the proposal.

## Workflow and merger

All reviewers use `../../review-workflows/review.js`. It validates the approved manifest, runs reviewer assignments in parallel, reconciles returned identity and code-style file coverage, applies lens-specific schemas, and launches one final merger.

- **Single mode:** validated reviewer packets go directly to the merger.
- **Council mode:** two independent thorough agents analyze the same immutable packet; their analyses and the original reviewer evidence then go to the merger for source-preserving adjudication.

The merger receives the approved manifest, reviewer packets, and any council analyses. It merges exact duplicates only within a lens, preserves cross-lens attribution, and returns one cohesive Markdown report. Missing, failed, or mismatched assignments block merger execution and publication.

## Artifact and memory

The manager validates the merged report and writes it to the approved artifact path. The artifact contains review metadata, executed plan, model/effort choices, selected conventions/experts, summary counts, findings by lens, not-relevant files, planned-test matrix or no-plan limitation, gaps, teaching moments, and positive findings.

Every reviewer skill owns its own `memory.md`. The manager reads [`memory.md`](memory.md) only for orchestration guidance and reads each selected specialist's local memory for lens-specific guidance. Add reusable entries only after human confirmation; never centralize specialist memory under the manager.
