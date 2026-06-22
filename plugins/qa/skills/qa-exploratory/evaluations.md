# Evaluations — qa-exploratory

Three scenarios that test whether the skill enforces charters, dispatches correctly in exploratory mode, and handles missing inputs gracefully.

## Eval 1 — Complete charter, dispatches cleanly

```json
{
  "skills": ["qa-exploratory"],
  "query": "Do exploratory QA on the scheduling feature as a keyboard-only attendant for 30 minutes. Work folder: work/2026-04-23-scheduling",
  "files": ["work/2026-04-23-scheduling/spec.md"],
  "expected_behavior": [
    "Constructs a complete charter (persona + goal + constraints + focus + time)",
    "Persona = keyboard-only attendant",
    "Time box = 30 minutes",
    "Dispatches qa-runner with mode=exploratory (not scripted)",
    "Does NOT read or execute a qa.md",
    "Does NOT dispatch manual-qa-case-writing",
    "Surfaces findings summary linking to FINDINGS.md",
    "Does NOT paste FINDINGS.md contents inline"
  ]
}
```

## Eval 2 — Incomplete charter, ask for missing components

```json
{
  "skills": ["qa-exploratory"],
  "query": "Explore this feature",
  "files": [],
  "expected_behavior": [
    "Does NOT dispatch agent with an incomplete charter",
    "Asks user for missing components: persona, goal, constraints, focus, time",
    "Asks user for feature area if not specified",
    "Only dispatches after charter is complete"
  ]
}
```

## Eval 3 — Compound mobile charter, pre-release sweep

```json
{
  "skills": ["qa-exploratory"],
  "query": "Pre-release exploratory sweep of the notifications feature for 45 min as an iPhone manager. Work folder: work/2026-04-23-notifications",
  "files": ["work/2026-04-23-notifications/spec.md"],
  "expected_behavior": [
    "Constructs charter with persona = manager on iPhone 12 (or similar)",
    "Constraints include mobile viewport and touch-only interaction",
    "Time box = 45 min",
    "Focus includes target size, tap accuracy, scroll friction (per mobile persona)",
    "Dispatches qa-runner in exploratory mode",
    "Agent uses chrome MCP with mobile viewport",
    "Surfaces findings count broken down by severity (P0/P1/P2)",
    "Identifies candidates for promotion to qa.md"
  ]
}
```

## Baseline (pre-skill)

Without this skill, expect: Claude dispatches the agent with a vague "explore the feature" prompt, no persona context, no time box. The agent wanders without a lens and either reports generic observations or nothing actionable.

## How to run

1. Prepare fixtures
2. Send the query with this skill loaded
3. Compare dispatch prompt (to qa-runner) and final response against expected_behavior
4. Verify FINDINGS.md was written and linked (not inlined)
