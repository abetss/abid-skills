# Evaluations — qa-execution

Three scenarios that test whether the skill stays in its lane (thin launcher) and correctly handles the four return statuses from qa-runner.

## Eval 1 — Happy path (COMPLETE return)

```json
{
  "skills": ["qa-execution"],
  "query": "run qa on work/2026-04-23-timesheet-approval",
  "files": [
    "work/2026-04-23-timesheet-approval/qa.md",
    "work/2026-04-23-timesheet-approval/spec.md",
    "CLAUDE.local.md"
  ],
  "expected_behavior": [
    "Does NOT read qa.md content (invariant)",
    "Dispatches qa-runner exactly once with the work folder path",
    "Parses the agent's JSON return",
    "Does NOT paste REPORT.md contents in the final response",
    "Surfaces: verdict (GO/NO-GO), pass rate, top 3 issues (titles only), report path, new bug IDs",
    "Announces at start per SKILL.md"
  ]
}
```

## Eval 2 — qa.md missing → auto-invoke case writing

```json
{
  "skills": ["qa-execution", "manual-qa-case-writing"],
  "query": "run qa on work/2026-04-23-new-feature",
  "files": ["work/2026-04-23-new-feature/spec.md"],
  "expected_behavior": [
    "Detects qa.md does not exist in the work folder",
    "Invokes manual-qa-case-writing with the work folder before dispatching",
    "Waits for qa.md to be written",
    "Then dispatches qa-runner in mode=fresh",
    "Does not attempt to run qa-runner with a missing qa.md"
  ]
}
```

## Eval 3 — Resume round (checkpoint + answers present)

```json
{
  "skills": ["qa-execution"],
  "query": "resume qa on work/2026-04-23-notifications",
  "files": [
    "work/2026-04-23-notifications/qa.md",
    "work/2026-04-23-notifications/checkpoint.json",
    "work/2026-04-23-notifications/ANSWERS.md"
  ],
  "expected_behavior": [
    "Detects checkpoint.json present → mode=continue",
    "Detects ANSWERS.md present → includes in dispatch prompt",
    "Does NOT reset qa.md checkboxes",
    "Does NOT restart from the beginning",
    "Presents only the delta summary on return (newly completed cases + any new bugs)"
  ]
}
```

## Baseline (pre-skill)

Without this skill, expect: Claude reads qa.md itself (leaks cases into main context), orchestrates test-by-test in main thread (pollutes with screenshots + evidence), pastes a long prose report back. This is exactly what the skill prevents.

## How to run

There is no built-in runner. Manual approach:
1. Set up the fixture files listed above in a scratch work folder
2. Send the query to Claude with this skill loaded
3. Observe behavior against expected_behavior criteria
4. Note any deviations
