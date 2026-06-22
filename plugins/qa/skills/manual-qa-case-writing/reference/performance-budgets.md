# Performance Budgets

## Contents
- Why performance is an accessibility concern
- Cold load (LCP)
- Interaction responsiveness (INP)
- Cumulative layout shift (CLS)
- Measurement approach

## Why this matters
For users with movement disabilities, latency IS an accessibility failure. Slow pages require patience and repeated input attempts. Every primary UI path needs a performance case.

## Cold load (LCP)
- Priority: P1
- Steps:
  1. Clear cache, cold-load the feature's primary page
  2. Measure LCP via `performance.getEntriesByName('largest-contentful-paint')`
- Observable: LCP < 2.5s on target viewport and network conditions
- Evidence: performance timeline; LCP value
- MUST NOT: LCP > 4s under any normal network condition

## Interaction responsiveness (INP)
- Priority: P1
- Steps:
  1. For each primary interaction (click, submit, tab change): measure response time
  2. Use `performance.now()` before/after
- Observable: response begins within 100ms (ideally < 50ms)
- Evidence: timing table per interaction
- MUST NOT: interactions with no visible feedback within 200ms

## Cumulative layout shift (CLS)
- Priority: P2 (escalate to P1 if touch users are affected)
- Steps:
  1. Load page, observe for 5 seconds as content resolves
  2. Trigger every dynamic content update
- Observable: CLS < 0.1 across the interaction
- Evidence: layout shift timeline
- MUST NOT: buttons moving after tap target established; image load pushing down interactive elements

## Measurement approach
The qa-runner agent injects a small probe via its chrome MCP that reads `performance.getEntriesByType('navigation')` and a `PerformanceObserver` for LCP/CLS. Record the raw values in evidence — not a pass/fail judgment.
