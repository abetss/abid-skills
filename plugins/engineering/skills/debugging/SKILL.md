---
name: debugging
description: Use when encountering any bug, test failure, unexpected behavior, performance problem, build failure, or production incident.
argument-hint: "[bug description, error message, or issue reference]"
---

# Debugging

Triages severity, investigates root cause, fixes with test-first verification, and escalates when needed.
Covers: functional bugs, flaky tests, performance issues, build failures, production incidents.

**Core principle:** Find root cause before fixing. Test-first verification. No guessing.

## Memory

Read `memory.md` in this directory before starting (if it exists). It contains learnings from past debugging sessions that prevent repeating mistakes.

### Reading memory
Before starting any debugging work, scan memory entries for:
- Bugs in the same area of the codebase
- The same bug type (functional, flaky, performance, build, production)
- Patterns that match the current symptoms
- Prevention steps that should have caught this bug

### Writing to memory
After every completed fix, evaluate whether the session produced a learning worth capturing. Write an entry if:
- The root cause was surprising or non-obvious
- You went down a wrong path that wasted time
- A technique or tool was particularly effective
- The fix revealed a systemic pattern (e.g., "spy-on-emit tests pass even when the consumer never ran — pair with an end-to-end assertion")
- A prevention step would have caught this earlier

**Discriminator:** would this entry help debug a different codebase? If no, it's a codebase fact — route it to that project's docs (PR description, project KB, troubleshooting docs), not here. Memory is project-agnostic.

Do NOT write obvious things or restate what's already in the code. Only capture what would save future debugging time.

Entry format:
```markdown
## [Date] -- [One-line summary]
**Bug type**: [functional | flaky | performance | build | production]
**Root cause**: [one sentence]
**What was surprising**: [what we didn't expect]
**Prevention**: [what would prevent this class of bug]
```

## Step 1: Triage

Assess the issue and determine the track:

### Trivial (root cause obvious, one-line fix)
Go directly to `fix.md`. Skip diagnosis.

### Standard (root cause unclear but localized)
Read `diagnose.md`. After root cause is confirmed, proceed to `fix.md`.

### Complex (multi-component, intermittent, flaky, performance, architectural)
Read `diagnose.md` with full investigation (all steps including pattern analysis and multi-component tracing).
- For deep call-stack bugs, also read `root-cause-tracing.md`.
- For flaky/timing bugs, also read `condition-based-waiting.md`.
- For test pollution, also read `find-polluter.md`.
- After diagnosis, proceed to `fix.md`.
- After fixing, consider reading `defense-in-depth.md` for hardening.

### Production Incident (critical, user-facing, revenue-impacting)
Before investigating, ask the user: "This looks like a critical production issue. Should we mitigate first (rollback, feature flag, circuit breaker) and investigate second?"
- If user says yes: mitigate, then follow Standard/Complex track for root cause.
- If user says no: follow Standard/Complex track directly.

## Anti-Patterns

If you catch yourself thinking any of these, STOP:

| You're thinking... | Reality |
|---|---|
| "Quick fix, investigate later" | First fix sets the pattern. Do it right. |
| "Just try changing X" | That's guessing, not debugging. |
| "It's probably X" | Probably != confirmed. Verify first. |
| "Skip the test, manually verify" | Untested fixes don't stick. |
| "Multiple fixes at once saves time" | Can't isolate what worked. |
| "One more fix attempt" (after 2+) | 3 failures = architectural problem. Read `escalate.md`. |
| "I don't fully understand but this might work" | Understanding IS the fix. Return to `diagnose.md`. |
| "I'll adapt the pattern differently" | Partial understanding guarantees bugs. Read the reference completely. |

## Rules

- NEVER write test and fix in the same step
- One bug at a time, in priority order
- For multiple bugs: each gets its own diagnose -> test -> fix cycle
- If the bug can't be reproduced in a test, explain why and describe the verification method
