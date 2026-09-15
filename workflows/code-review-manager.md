# Code Review Manager Workflow

`code-review-manager` composes independently invokable reviewer skills, chooses each workflow role/model/thinking effort, asks for one combined approval, runs reviewers in parallel, and sends all validated evidence to one merger that produces the cohesive review artifact.

## Flow

```text
code-review-manager (main-thread owner)
  ├─ resolve diff, mode, plan, memory, and artifact path
  ├─ code-style-reviewer
  │    ├─ read convention router
  │    ├─ path-selection pass
  │    ├─ semantic content-selection pass
  │    ├─ one code-style owner per file
  │    ├─ plan examples or discovered examples
  │    └─ planned-test accounting when available
  ├─ select specialist lenses
  │    ├─ architecture-reviewer
  │    │    └─ local architect-solution expertise first,
  │    │       then ACTIVE global bundles for uncovered concerns
  │    ├─ domain-expert-reviewer
  │    ├─ security-reviewer
  │    └─ performance-reviewer
  ├─ choose reviewer-shallow/reviewer-staff/reviewer-thorough per assignment
  ├─ choose verified model + thinking effort per assignment and merger
  ├─ display files, lenses, agents, conventions, examples,
  │  planned tests, expertise, model choices, and merger
  ├─ ask once unless autonomous
  └─ launch plugins/engineering/review-workflows/review.js
       ├─ reviewer-shallow assignments  ─┐
       ├─ reviewer-staff assignments    ─┼─ parallel review
       └─ reviewer-thorough assignments ─┘
                                         │
                              validate identity + coverage
                                         │
                         optional two-model council analysis
                                         │
                           one reviewer-thorough merger
                                         │
                           cohesive Markdown review artifact
                                         │
                              owner validation + publication
```

## Skill and role boundary

`code-style-reviewer`, `code-review-manager`, and the specialist reviewer lenses are skills. `reviewer-shallow`, `reviewer-staff`, and `reviewer-thorough` are lens-neutral workflow roles with read-only tools. The manager selects a role and may override its default model with a verified alias or `provider/model:thinking` value when the proposal explains the capability, effort, and cost reason.

## Convention selection

`code-style-reviewer` reads `~/.agents/conventions/table-of-content.md` first. It uses `{project}/.agents/conventions/table-of-content.md` only when the global router is absent. If neither exists, it reports: `Convention files are needed under ~/.agents/conventions/ or {project}/.agents/conventions/.`

Path conventions are selected from target paths/extensions and exact `paths` metadata. Content conventions are selected only after inspecting the task, diff, imports, APIs, schemas, and changed behavior for an actual semantic trigger; a keyword alone is insufficient. The proposal names every selected convention and its specific path/content reason.

Every reviewed file has one code-style owner. Plan-named examples are used first; repository examples are discovered when none are named. Every planned test is marked IMPLEMENTED, PARTIAL, or MISSING.

## Architecture expertise routing

When architecture applies, its reviewer follows the canonical plugin `architect-solution` skill. It checks `architect-solution/experts/` first and treats an absent directory as empty. For every material concern still uncovered, it reads `/Users/abtinghods/.agents/expertise/table-of-content.md` completely, considers every `ACTIVE` semantic trigger, and selects only relevant global bundles. It reads each selected entry point plus required relative references. The proposal lists whether expertise is local or global, the concern it covers, and its concrete problem/solution reason. The complete library is never injected merely because it exists.

## Merger

The workflow validates every reviewer result before merger execution. In single mode, the complete packet goes directly to the merger. In council mode, two independent model families first analyze the same packet; their analyses and the original evidence then go to the merger.

The merger always uses `reviewer-thorough` with the manager-approved merger model and thinking effort. It preserves supported findings and lens semantics, merges only exact same-lens duplicates, resolves council disagreements from source evidence, and returns one cohesive Markdown artifact. Reviewer packets and council analyses are never published as final reviews.
