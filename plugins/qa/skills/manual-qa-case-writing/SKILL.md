---
name: manual-qa-case-writing
description: Produces qa.md with 6-field test cases covering functional, accessibility (WCAG 2.2 AA), PIPEDA compliance, and performance dimensions. Use when writing manual QA cases for a feature, user flow, or bug fix, or when a feature needs test coverage documentation.
model: sonnet
---

# Manual QA Case Writing

Staff QA engineer. Write cases that make shortcuts impossible: every case has a measurable observable and required evidence. Generate coverage — don't wait for someone to ask for edge cases.

**Announce at start:** "Writing QA cases for {feature}."

## Case writing checklist

Copy this into your response and check items as you complete them:

```
Progress:
- [ ] Read spec/requirements from work folder
- [ ] Draft traceability matrix (requirements → cases)
- [ ] Emit Role × Verb permission matrix
- [ ] Write functional cases (happy, negative, error, concurrency, state transitions)
- [ ] Emit boundary cases — see reference/bva-boundaries.md
- [ ] Emit accessibility cases — see reference/accessibility-templates.md
- [ ] If data-handling: emit PIPEDA cases — see reference/pipeda-cases.md
- [ ] For UI cases: add design-ref field
- [ ] Emit performance cases — see reference/performance-budgets.md
- [ ] Assign P0/P1/P2 priority to every case
- [ ] Verify traceability; flag UNCOVERED requirements
- [ ] Save to {work-folder}/qa.md
```

## When to Use
- User asks for manual QA test cases
- Feature implementation needs test coverage documentation
- User provides requirements or acceptance criteria to validate
- Bug fix needs regression test documentation

**Don't use for:**
- Automated test code (unit/integration tests)
- Performance or load testing infrastructure
- Exploratory charters (use qa-exploratory skill)

## Output: 6-field test case format

```
### TC-{ID} {Title}
- [ ]
- Role: {manager | attendant | anon}
- Priority: {P0 | P1 | P2}
- Steps:
  1. {action}
  2. {action}
- Observable: {measurable outcome — URL, DOM selector + value, network endpoint + response, measured px, text}
- Evidence: {screenshot of X + network log | DOM snapshot | API response body}
- Design ref: {Figma URL or mockup path, required for UI-changing cases; "N/A" otherwise}
- MUST NOT: {negative checks — specific things that must not be true}
```

### Examples

Good:
```
### TC-01 Valid login routes manager to dashboard
- [ ]
- Role: manager
- Priority: P0
- Steps:
  1. Navigate to /login
  2. Enter seed manager email + password; submit
- Observable: URL becomes /dashboard within 3000ms; h1 text matches seed fixture's full name; POST /api/login returned 200 with user.role="manager"
- Evidence: screenshot of /dashboard header; network log for /api/login
- Design ref: N/A (no visual change in this case)
- MUST NOT: any console error; "Sign in" text present on page; URL stays /login
```

Bad (vague observable, no evidence):
```
- [ ] Login page: enter valid creds → submit → dashboard loads, user name shown
```

## Required coverage

Every qa.md MUST include cases from every applicable category. Non-applicable → mark N/A with a one-line reason.

### Functional
- Happy path (every primary flow)
- Boundary values per input — see [reference/bva-boundaries.md](reference/bva-boundaries.md)
- Negative: every denied path
- Error recovery: network fail, 5xx, timeout, stale data, conflict
- State transitions: every legal edge + every illegal edge (for features with states)
- Concurrency: double-submit, rapid-fire, tab-in-two-windows, interrupted mid-flow

### Role × Verb permission matrix
Auto-emit at top of qa.md. Rows = roles, columns = verbs (view/create/edit/delete/approve). Every cell becomes a case. Denied cells test authorization failure.

### Accessibility (for any UI feature)
(only when user excplicitly asks)
Generate cases from [reference/accessibility-templates.md](reference/accessibility-templates.md) — 8 templates (keyboard, switch-device, voice, target size, error ID, reflow, live regions, reduced-motion). Each becomes a real 6-field TC block.

### PIPEDA compliance (for data-handling features)
(only when user excplicitly asks)
Generate cases from [reference/pipeda-cases.md](reference/pipeda-cases.md) — consent, sensitive inputs, right-to-access, right-to-erasure, breach notification.

### Performance (for disabled users, latency IS a11y)
(only when user excplicitly asks)
Generate cases from [reference/performance-budgets.md](reference/performance-budgets.md) — cold load (LCP), interaction responsiveness (INP), layout shift (CLS).

## Priority rules

- **P0** — data loss, auth bypass, core flow broken, a11y blocker, PIPEDA violation, blast radius = all-users
- **P1** — non-core flow broken, a11y degradation, performance miss, data correctness issue
- **P2** — polish, cosmetic, rare-condition edge cases

A11y and data-correctness default to P1 minimum.

Blast radius tag (enum): `auth | data-write | billing | a11y-only | cosmetic`.

## Adversarial rules (mechanical, not vibes)

For every:
- Text input → emit all boundaries from bva-boundaries.md
- Numeric input → emit all boundaries from bva-boundaries.md
- Action → emit a double-submit / rapid-fire variant
- Modal → emit a viewport-resize-mid-interaction variant
- Role-gated route → emit an attempted-access-as-wrong-role case
- State machine → emit one case per illegal edge

## Output structure

Save to `{work-folder}/qa.md`:

```markdown
# QA: {Feature Name}

## Traceability
| AC/Req | Covered by | Gaps |
|---|---|---|
| AC-1.1 | TC-01, TC-02 | — |
| AC-1.2 | — | **UNCOVERED** |

## Role × Verb Matrix
| | view | create | edit | delete | approve |
|---|---|---|---|---|---|
| manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| attendant | ✓ | ✓ (own) | ✓ (own) | ✗ | ✗ |

## A11y Not Applicable
- Voice control — feature has no buttons or links
(only this section if any templates are skipped)

## Test Cases

### Functional
### TC-01 ...
- [ ]
- Role: ...

### Accessibility
### TC-A11Y-01 ...

### PIPEDA
### TC-PIPEDA-01 ...

### Performance
### TC-PERF-01 ...
```

Any gap in the traceability matrix = you're not done. Flag it, don't suppress it.

## Scope
- Test desktop and mobile viewports unless specified otherwise
- Add intermediate viewports for layout-sensitive changes (1024px, 1280px)

## Reset protocol

If implementation changed after cases were written, reset ALL checkboxes to `- [ ]`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Vague observable ("dashboard loads") | Specific: "URL becomes /dashboard within 3000ms; h1 text matches seed user's full name" |
| Missing design ref on UI cases | Required for any case that asserts on visual layout |
| One-liner cases | Use the 6-field block |
| Skipping BVA | Mechanical — emit boundaries per input type, no judgment calls |
| Skipping a11y until last | Generate alongside functional cases |
| Pass/fail based on screenshot alone | Specify the measurable — selector + expected value |
| Gaps in traceability matrix hidden | Flag as UNCOVERED; don't suppress |
| Priority tag missing | Every case gets P0/P1/P2 — no untagged cases |

## Key Principles

- **Measurable observable** — every expected outcome must be machine-checkable
- **Required evidence** — every case specifies what artifact the executor must produce
- **Design ref for UI** — visual/layout cases must cite the design source
- **Adversarial by default** — boundaries, negative, concurrency, illegal transitions all generated
- **Coverage over cleverness** — use the matrices and generators; don't rely on judgment to remember edge cases
- **Living document** — checkboxes track state; reset on code change
