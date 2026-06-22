# Task File Template

Used by Step 4 of `SKILL.md`. Dispatch a subagent with the prompt pattern below. The subagent writes ONE `task-NN.md` file matching this exact structure.

## Status convention (must be followed throughout the file)

Every actionable item in a task file is a checkbox that progresses through three states:

- `- [ ]` — todo
- `- [-]` — in progress
- `- [x]` — done

This applies to every bullet under `## Implementation → Tests (What to Test)`, every bullet under `## Implementation → Steps`, every bullet under all four `## Verification` subsections, and every bullet added later to `## Post verification tasks`. **Never** use plain bullets or numbered lists for actionable items.

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
> [Paste the Planning QA Scenarios for the relevant flow from plan-prep.md — these feed the QA subsection]
> [Paste discussion outcomes if Step 3 of SKILL.md happened: agreed signature, paths, tests, QA cases]
>
> **The task file must have exactly these four top-level sections, in this order:**
>
> 1. `## Context` — what the implementer needs to understand
> 2. `## Implementation` — how to build it
> 3. `## Verification` — how to know it's done (four fixed subsections)
> 4. `## Post verification tasks` — placeholder for artifacts produced during verification
>
> Do NOT include an `Implementation Steps` or `Verification Steps` section at the top level. Those belong inside `## Implementation` and `## Verification` respectively.
>
> Omit any subsection that is truly not applicable (e.g., no QA section for a pure internal-library task). Never leave a subsection empty with a placeholder — remove it entirely.
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

New tests to write for this task. Describe the behavior and example input — no assertions, no implementation. Each test is a checkbox that progresses `[ ]` → `[-]` (writing) → `[x]` (written).

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

**Reset rule:** If code review or QA findings require code changes — or any new item is added to `## Post verification tasks` below — reset ALL checkboxes in this section to `- [ ]` and re-run every subsection from scratch. A previous pass is meaningless once code changes.

**Checkbox semantics:** `[ ]` = todo, `[-]` = in progress, `[x]` = done. A checkbox can only be marked `[x]` when fully verified. Failures are blockers — fix or raise them.

### Automation tests

Tests to run in order as part of verifying this task. May include the newly written tests from the Implementation section, related existing tests impacted by this change, or a broader suite.

- [ ] `path/to/test_file.test.ts` — [specific scenario or "all tests in file"]
- [ ] `path/to/related_test.test.ts` — [what to verify still passes]
- [ ] [e.g., "Full suite: `pnpm test:unit` in affected package"]

### Code review

Code review agents to dispatch with their scope. Each item names a convention or profile AND the files it applies to.

- [ ] `code-review-team` agent — convention `agents/conventions/naming.md` on `path/to/file.ts`
- [ ] `code-review-team` agent — profile `accessibility` on `path/to/ui-component.tsx`
- [ ] All findings addressed in code or flagged in `code-review.md` under `## Task NN: [title]`

### QA

Manual QA cases for this task. Each case is written INLINE in detail using the `manual-qa-case-writing` skill format. Do not link out to `qa.md` — the cases live here in the task file.

**Case 1 — Happy path: [descriptive title]**
- Preconditions: [setup required, roles, state]
- Steps:
  1. Navigate to `/path/to/page`
  2. Click [element — specific selector or label]
  3. Fill [field] with [value]
  4. Submit
- Expected: [observable outcome — what the user sees, where they land, what message appears]
- [ ] Pass

**Case 2 — Edge case: [descriptive title]**
- Preconditions: [setup]
- Steps:
  1. ...
- Expected: [observable outcome]
- [ ] Pass

**Case 3 — Accessibility (REQUIRED for UI work):**
- Keyboard navigation: Tab order logical, all interactive elements reachable, focus indicators visible
- Screen reader: ARIA labels present and descriptive, semantic HTML, dynamic updates announced
- Color contrast: 4.5:1 for normal text, 3:1 for large text / UI controls
- Touch targets: minimum 44×44px, adequate spacing
- Motion: respects `prefers-reduced-motion`
- [ ] Pass

### Others

Other commands or checks to run for this task.

- [ ] `pnpm biome` (format + lint)
- [ ] `pnpm check:types`
- [ ] [task-specific: e.g., `pnpm db:migrate` + verify schema]

---

## Post verification tasks

Follow-up items surfaced during this task's verification (code review findings, QA bugs, etc.). This section starts empty and is populated as verification runs. Each item is a checkbox: `[ ]` = todo, `[-]` = in progress, `[x]` = done.

**IMPORTANT — the moment any new item is added to this section:**

1. All checkboxes in `## Verification` above MUST be reset to `- [ ]`.
2. When every Post verification task is `- [x]`, re-run the full `## Verification` section from scratch.
3. The task is only complete when every checkbox in `## Implementation`, `## Verification`, AND `## Post verification tasks` is `- [x]` simultaneously.

**Code Review follow-ups:**
- (empty — populated when code review surfaces findings that need fixing)

**QA follow-ups:**
- (empty — populated if QA surfaces issues beyond the inline cases above)

Example after verification has surfaced follow-ups:

**Code Review follow-ups:**
- [x] Fix: contrast ratio on disabled button — `code-review.md#task-03-button-contrast`
- [-] Refactor: extract duplicated validation — `code-review.md#task-03-dup-validation`
- [ ] Review: confirm access policy — `code-review.md#task-03-access-policy`

**QA follow-ups:**
- [ ] Fix: flaky test on slow networks — `qa.md#task-03-network-flake`
```

> **Important rules the subagent must follow:**
>
> - Use the exact four top-level section headings (`## Context`, `## Implementation`, `## Verification`, `## Post verification tasks`) — do not rename, reorder, or add other top-level sections.
> - Use the exact four subsection headings under `## Verification` (`### Automation tests`, `### Code review`, `### QA`, `### Others`).
> - Omit a subsection only when it is truly non-applicable (e.g., no QA for a pure internal refactor). Never leave a subsection with just a placeholder.
> - **Every actionable item uses the `- [ ]` checkbox format.** This applies to: every bullet under `## Implementation → Tests (What to Test)`, every bullet under `## Implementation → Steps`, every bullet under all four `## Verification` subsections, and every bullet added later to `## Post verification tasks`. Never use plain `- bullet` or `1. numbered` for actionable items — always `- [ ]`.
> - All items start as `- [ ]`. The three states are: `- [ ]` (todo), `- [-]` (in progress), `- [x]` (done).
> - `## Post verification tasks` starts empty. When items are added later, the reset rule for `## Verification` applies (see below).
> - QA cases live INLINE in the task file, in full detail. Do not summarize and link to `qa.md`. Each QA case ends with a single `- [ ] Pass` checkbox.
> - All paths are project-relative (not absolute), except skill references under `/Users/abtinghods/.claude/skills/`.
> - Inline types in the `Interface Contracts` — do not invent separate type files.

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

## How to Write QA Cases

Each case has: Preconditions, numbered Steps, Expected outcome (observable, not internal state), and a single `[ ]` checkbox for Pass. For UI work, ALWAYS include an Accessibility case covering keyboard, screen reader, contrast, touch targets, and motion.

Include:
- Happy path (at least one)
- Edge cases derived from Planning QA Scenarios in `plan-prep.md`
- Error/permission cases where relevant
- Accessibility case (required for UI)

---

## Verification checklist (run after the subagent returns)

Open the file and confirm:

- `## Context` has Why / Current State / Desired State, plus the reference blocks (Files, Depends on, Read for Context, Similar Files, Conventions)
- `## Implementation` has Interface Contracts, Tests (What to Test) as `- [ ]` checkboxes, and Steps as `- [ ]` checkboxes — in that order
- `## Verification` has the four subsections (Automation tests, Code review, QA, Others), each with task-specific `- [ ]` checkboxes
- `## Post verification tasks` exists as a placeholder with Code Review follow-ups / QA follow-ups structure, and states the reset rule
- Reset-on-change, reset-on-new-post-verification-task, and all-must-check rules are stated in the `## Verification` header and the `## Post verification tasks` header
- QA cases are inline and detailed (preconditions, steps, expected, `- [ ] Pass` checkbox)
- Every actionable item across Implementation, Verification, and Post verification tasks uses the `- [ ]` checkbox format — not plain bullets or numbered lists

If anything is missing, send a targeted follow-up to the subagent — do not rewrite the file yourself.
