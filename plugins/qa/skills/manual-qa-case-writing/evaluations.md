# Evaluations — manual-qa-case-writing

Three scenarios that test whether the skill produces complete, unshortcut-able test cases across required coverage categories.

## Eval 1 — Full coverage for a UI feature

```json
{
  "skills": ["manual-qa-case-writing"],
  "query": "Write QA cases for the new timesheet approval feature. Requirements are in work/2026-04-23-timesheet-approval/spec.md",
  "files": ["work/2026-04-23-timesheet-approval/spec.md"],
  "expected_behavior": [
    "Reads spec.md before writing cases",
    "Emits a Traceability table at top of qa.md mapping each AC to its covering TC(s)",
    "Emits a Role × Verb permission matrix (rows include manager and attendant)",
    "Writes functional cases (happy, negative, error, concurrency, state transitions)",
    "Generates boundary cases referencing reference/bva-boundaries.md",
    "Generates 8 accessibility cases referencing reference/accessibility-templates.md (or marks applicable ones N/A with reason)",
    "Generates PIPEDA cases (personal data is involved)",
    "Generates performance cases (LCP, INP, CLS)",
    "Every case uses the 6-field block (Role, Priority, Steps, Observable, Evidence, Design ref, MUST NOT)",
    "Every UI case includes a design ref (not N/A)",
    "Every case has a P0/P1/P2 priority tag",
    "Flags any uncovered requirement as UNCOVERED in the traceability matrix",
    "Writes output to work/2026-04-23-timesheet-approval/qa.md"
  ]
}
```

## Eval 2 — BVA boundaries generated mechanically

```json
{
  "skills": ["manual-qa-case-writing"],
  "query": "Add QA cases for boundary conditions on the email input field (max 254 chars). Write to work/2026-04-23-email/qa.md",
  "files": [],
  "expected_behavior": [
    "Loads reference/bva-boundaries.md",
    "Emits separate 6-field cases for: empty, whitespace-only, 1-char, 253-char, 254-char, 255-char, emoji, RTL, script payload",
    "Each case has a specific, measurable Observable (not 'error shown' — the exact error element and text)",
    "No judgment-call skipping of boundaries",
    "Priority is P1 minimum for data-correctness boundaries"
  ]
}
```

## Eval 3 — Accessibility cases for a new modal

```json
{
  "skills": ["manual-qa-case-writing"],
  "query": "Write a11y cases for the new 'Create shift' modal in the scheduling feature",
  "files": [],
  "expected_behavior": [
    "Loads reference/accessibility-templates.md",
    "Emits keyboard-only full-flow case",
    "Emits switch-device friendliness case",
    "Emits voice-control accessible-name case",
    "Emits target-size and spacing case",
    "Emits error-identification case (if modal has a form)",
    "Emits live-region case (modal open/close announcements)",
    "Emits reflow case at 320px + 400% zoom",
    "Each case has Priority P0 or P1 (not P2 for this product)",
    "Any template marked N/A includes a one-line reason",
    "Cases follow the 6-field format"
  ]
}
```

## Baseline (pre-skill)

Without this skill, expect: one-line cases like `- [ ] Modal: open it, looks good`, no accessibility coverage, no BVA, no traceability, no PIPEDA, no priority tags. Reports end up passing superficially but missing most categories.

## How to run

1. Prepare the work folder fixtures
2. Send the query with this skill loaded
3. Compare emitted qa.md against expected_behavior
4. Note any category skipped without N/A justification — that's a failure
