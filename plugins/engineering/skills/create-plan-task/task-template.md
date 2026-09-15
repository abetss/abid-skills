# Task File Template

Used by Step 4 of `SKILL.md`. Dispatch a subagent with the prompt pattern below. The subagent writes ONE `task-NN.md` file matching this exact structure.

## Status convention (must be followed throughout the file)

Every actionable item in a task file is a checkbox that progresses through three states:

- `- [ ]` — todo
- `- [-]` — in progress
- `- [x]` — done

This applies to every bullet under `## Implementation → Tests (What to Test)`, every bullet under `## Implementation → Steps`, every present `## Verification` subsection, and every bullet added later to `## Post verification tasks`. **Never** use plain bullets or numbered lists for actionable items.

Top-level task status (the `[ ]/[-]/[x]` next to the task in `task-list.md`) lives in `task-list.md`, not in the task file.

## Reset rule (must be stated inside the task file)

Whenever a new item is added under `## Post verification tasks`, ALL checkboxes in `## Verification` MUST be reset to `- [ ]`. Once the fix lands and the Post verification task is `- [x]`, the full `## Verification` section is re-run. The task is only complete when every checkbox in `## Implementation`, `## Verification`, and `## Post verification tasks` is `- [x]` at the same time.

---

## Subagent prompt pattern

Send this as the subagent's `prompt` (general-purpose agent). Paste real context inline before dispatching — do not pass placeholders.

> "Create an implementation task file at `{work-folder}/task/task-NN.md` for: **[task name]**.
>
> **Context from planning:**
> [Paste relevant sections from plan-prep.md — the flow diagram for this task, technical details, reference files]
> [Paste from architecture-decisions.md if relevant]
> [Paste design artifacts if relevant — design-discovery-result.md, view-model-props.md, [design folder]/requirements.md, any component variants referenced in plan-prep.md's design artifact section]
> [Paste discussion outcomes if Step 3 of SKILL.md happened: agreed signature, paths, and targeted tests]
> [Paste task-level QA only when the user explicitly requested it; otherwise state that QA is omitted]
> [List the knowledge-base guides matched from the KB index for this task in Step 2, if any — the subagent must read each in full]
>
> **Before writing, consult the knowledge base.** Read the project's KB index (`a-kb/table-of-content.md`, or the repo's equivalent docs/KB table of contents). For every guide whose scope matches what this task touches — including any listed above — read it in full, cite it in the `Conventions / SOPs / Skills / Rules` block, add it to `Read for Context`, and make the Implementation follow it. Decide the relevant set from the index based on THIS task; do not assume a fixed list and do not skip the scan.
>
> **The task file must have exactly these four top-level sections, in this order:**
>
> 1. `## Context` — what the implementer needs to understand
> 2. `## Implementation` — how to build it
> 3. `## Verification` — the smallest checks needed to prove this task's isolated outcome; Code review is required and other subsections are conditional
> 4. `## Post verification tasks` — placeholder for artifacts produced during verification
>
> Do NOT include an `Implementation Steps` or `Verification Steps` section at the top level. Those belong inside `## Implementation` and `## Verification` respectively.
>
> Omit `### QA` unless the caller explicitly supplied task-level QA. Omit `### Automation tests` when no targeted automated check is necessary, and omit `### Others` when the caller supplied no additional check. Never invent QA or broad verification and never leave an empty placeholder.
>
> **Follow this task file structure exactly:**

```markdown
# Task NN: [Name]

## Context

**Why:** [Business reason — what user problem this solves]
**Current State:** [What exists now — brief summary]
**Desired State:** [What we're building — brief summary]

**Data Flow:**
[Relevant portion of the flow diagram from plan-prep.md]

**Files:**
- Create: `path/to/new_file.ts`
- Modify: `path/to/existing_file.ts`
- Delete: `path/to/obsolete_file.ts`
- Test: `path/to/test_file.test.ts`

**Depends on:** Task NN: Name (or "None — can start immediately")
- Use from dependency: [What this task needs from each listed dependency]

**Read for Context:**
- `path/to/relevant_file.ts` — [why]

**Similar Files (from plan-prep.md):**
- `path/to/similar_file.ts` — [why it's a good reference]
- `path/to/similar_test.test.ts` — [test pattern to follow]

**Conventions / SOPs / Skills / Rules:**
- `agents/conventions/naming.md` — [relevance]
- `agents/sops/relevant.md` — [relevance]
- `.claude/rules/transformers.md` — [relevance]
- `/Users/abtinghods/.claude/skills/relevant-skill.md` — [relevance]

---

## Implementation

**Interface Contracts:**

[Function signature with inline types + path comments describing what each path handles. Not implementation — just the shape.]

\```typescript
function transform_feature_data(
  data: {
    field_one: string
    field_two: number
    nested: { sub_field: string }
  }
): {
  display_field: string
  formatted_value: string
  status_info: { text: string; color: 'green' | 'yellow' | 'red' }
} {
  // Path 1: Normal case — formats and returns
  // Path 2: Missing nested — returns default
  // Path 3: Invalid field_two — throws ValidationError
}
\```

**Tests (What to Test):**

Only include tests necessary to prove this isolated outcome. Describe the behavior and example input — no assertions, no implementation. Omit this subsection when no new test is necessary. Each included test is a checkbox that progresses `[ ]` → `[-]` (writing) → `[x]` (written).

- [ ] handles normal case
  - input: `{ field_one: "test", field_two: 100, nested: { sub_field: "value" } }`
- [ ] handles missing nested gracefully
  - input: `{ field_one: "test", field_two: 100 }`
- [ ] throws ValidationError on negative field_two
  - input: `{ field_one: "test", field_two: -1, nested: { sub_field: "value" } }`

**Steps:**

Each step is a checkbox. Progress `[ ]` → `[-]` (working on it) → `[x]` (done).

- [ ] [task-specific implementation step]
- [ ] [task-specific implementation step]
- [ ] ...

---

## Verification

All verification checkboxes must be `- [x]` before this task is complete.

**Reset rule:** If a verification finding requires code changes — or any new item is added to `## Post verification tasks` below — reset ALL checkboxes in this section to `- [ ]` and re-run every present subsection from scratch. A previous pass is meaningless once code changes.

**Checkbox semantics:** `[ ]` = todo, `[-]` = in progress, `[x]` = done. A checkbox can only be marked `[x]` when fully verified. Failures are blockers — fix or raise them.

### Automation tests

Run only the smallest targeted commands needed for this task's changed unit and immediate integration seam. A package-wide, repository-wide, or feature-wide command appears only when the caller explicitly supplied it with a task-specific reason.

- [ ] `path/to/test_file.test.ts` — [specific behavior this task changes]
- [ ] `path/to/related_test.test.ts` — [immediate integration seam, only when applicable]

### Code review

- [ ] Run `code-style-reviewer` with exactly one assignment using role `reviewer-junior` over every file changed by this task; address its findings before checking this item

### Others

Include only caller-supplied checks that directly prove this isolated outcome and are not tests or code review. Omit this subsection when none apply.

- [ ] [targeted task-specific check and why it is necessary]

---

## Post verification tasks

Follow-up items surfaced during this task's verification. This section starts empty and is populated as verification runs. Each item is a checkbox: `[ ]` = todo, `[-]` = in progress, `[x]` = done.

**IMPORTANT — the moment any new item is added to this section:**

1. All checkboxes in `## Verification` above MUST be reset to `- [ ]`.
2. When every Post verification task is `- [x]`, re-run the full `## Verification` section from scratch.
3. The task is only complete when every checkbox in `## Implementation`, `## Verification`, AND `## Post verification tasks` is `- [x]` simultaneously.

**Code Review follow-ups:**
- (empty — populated when code review surfaces findings that need fixing)

Add a **QA follow-ups** block only when the user explicitly requested task-level QA.

Example after verification has surfaced follow-ups:

**Code Review follow-ups:**
- [x] Fix: contrast ratio on disabled button — `code-review.md#task-03-button-contrast`
- [-] Refactor: extract duplicated validation — `code-review.md#task-03-dup-validation`
- [ ] Review: confirm access policy — `code-review.md#task-03-access-policy`
```

> **Important rules the subagent must follow:**
>
> - Use the exact four top-level section headings (`## Context`, `## Implementation`, `## Verification`, `## Post verification tasks`) — do not rename, reorder, or add other top-level sections.
> - `### Code review` is always present and contains exactly one `code-style-reviewer` assignment using role `reviewer-junior` over every file changed by the task.
> - `### Automation tests` contains only the smallest necessary targeted commands and may be omitted when no automated check is needed.
> - `### QA` appears only when the caller states that the user explicitly requested task-level QA.
> - `### Others` appears only for caller-supplied, directly relevant checks. Never leave a subsection with just a placeholder.
> - **Every actionable item uses the `- [ ]` checkbox format.** This applies to every included test, every implementation step, every present Verification subsection, and every Post verification task. Never use plain bullets or numbered lists for actionable items.
> - All items start as `- [ ]`. The three states are: `- [ ]` (todo), `- [-]` (in progress), `- [x]` (done).
> - `## Post verification tasks` starts empty. When items are added later, the reset rule for `## Verification` applies (see below).
> - When the user explicitly requested task-level QA, keep those cases inline and limited to the supplied scope. Otherwise omit QA entirely.
> - All paths are project-relative (not absolute), except skill references under `/Users/abtinghods/.claude/skills/`.
> - Inline types in the `Interface Contracts` — do not invent separate type files.
> - Consult the KB index and cite every guide relevant to what this task touches in the `Conventions / SOPs / Skills / Rules` block — decide the set from the index per task, never a fixed list.

---

## How to Write Interface Contracts

Define **input**, **paths of logic**, and **output** inline:

```typescript
function transform_feature_data(
  data: {
    field_one: string
    field_two: number
    nested: { sub_field: string }
  }
): {
  display_field: string
  formatted_value: string
  status_info: { text: string; color: 'green' | 'yellow' | 'red' }
} {
  // Path 1: Normal case — formats and returns
  // Path 2: Missing nested — returns default
  // Path 3: Invalid field_two — throws ValidationError
}
```

## How to Write Tests (What to Test)

Describe WHAT to test with example input. No assertions, no implementation:

```typescript
describe('transform_feature_data', () => {
  // handles normal case
  const input = {
    field_one: "test",
    field_two: 100,
    nested: { sub_field: "value" }
  }

  // handles missing nested
  const input = {
    field_one: "test",
    field_two: 100
  }

  // throws on invalid field_two
  const input = {
    field_one: "test",
    field_two: -1,
    nested: { sub_field: "value" }
  }
})
```

## How to Write User-Requested QA Cases

Use this section only when the caller states that the user explicitly requested task-level QA. Each supplied case has Preconditions, numbered Steps, Expected outcome, and a single `[ ]` checkbox for Pass. Keep the cases within the user's requested scope; do not derive additional cases from Planning QA Scenarios.

---

## Verification checklist (run after the subagent returns)

Open the file and confirm:

- `## Context` has Why / Current State / Desired State, plus the reference blocks (Files, Depends on, Read for Context, Similar Files, Conventions)
- `## Implementation` has Interface Contracts and Steps; Tests (What to Test) appears between them only when targeted tests are necessary
- `## Verification` contains exactly one Code review assignment using role `reviewer-junior`; Automation tests and Others contain only caller-supplied targeted checks, and QA appears only when explicitly requested by the user
- `## Post verification tasks` exists with Code Review follow-ups, optional QA follow-ups only when QA was requested, and the reset rule
- Reset-on-change, reset-on-new-post-verification-task, and all-must-check rules are stated in the `## Verification` header and the `## Post verification tasks` header
- Any explicitly requested QA cases are inline and limited to the supplied scope
- Every actionable item across Implementation, Verification, and Post verification tasks uses the `- [ ]` checkbox format — not plain bullets or numbered lists
- Knowledge-base guides relevant to what this task touches (matched from the KB index) are cited in the `Conventions / SOPs / Skills / Rules` block and reflected in the Implementation

If anything is missing, send a targeted follow-up to the subagent — do not rewrite the file yourself.
