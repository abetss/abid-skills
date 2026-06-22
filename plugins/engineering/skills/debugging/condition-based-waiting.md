# Condition-Based Waiting

Replace arbitrary timeouts with condition polling to fix flaky tests.

## Core Principle

Wait for the actual condition you care about, not a guess about how long it takes.

```
// BAD: guessing at timing
await sleep(300);
expect(result).toBeDefined();

// GOOD: waiting for the condition
await waitFor(() => getResult() !== undefined);
expect(result).toBeDefined();
```

## When to Use

- Tests use `setTimeout`, `sleep`, or arbitrary delays
- Tests are flaky (pass sometimes, fail under load or in CI)
- Tests timeout when run in parallel
- Waiting for async operations to complete

## The Pattern

A generic polling function:
1. Check if the condition is true
2. If true, return
3. If not, wait a short interval (10ms) and check again
4. If timeout exceeded, throw with a descriptive error

Use whatever waiting primitives your project already has:
- **React Testing Library**: `waitFor(() => ...)`
- **Playwright**: `expect(locator).toBeVisible()`
- **Vitest/Jest**: `waitFor` from testing utilities
- **Python**: `tenacity` library or custom polling
- **Generic**: Write a `waitFor` helper with polling + timeout

## Quick Patterns

| Scenario | Pattern |
|----------|---------|
| Wait for DOM element | `waitFor(() => screen.getByText('Done'))` |
| Wait for state change | `waitFor(() => store.getState().status === 'ready')` |
| Wait for event count | `waitFor(() => events.length >= 5)` |
| Wait for file | `waitFor(() => fs.existsSync(path))` |
| Wait for API response | `waitFor(() => fetchResult !== undefined)` |

## When Arbitrary Timeout IS Correct

Sometimes you genuinely need a fixed delay -- when testing timed behavior (debounce, throttle, animation duration). When this is the case:

1. First wait for the triggering condition (not arbitrary)
2. Then wait the specific duration based on known timing
3. Comment explaining WHY: `// 200ms = 2 ticks at 100ms interval`

## Common Mistakes

- **Polling too fast** (1ms): wastes CPU. Use 10ms intervals.
- **No timeout**: loops forever if condition never met. Always include a timeout.
- **Stale data**: checking a cached value. Call the getter inside the loop for fresh data.
- **Too-short timeout**: 100ms works locally but fails in CI. Use 5000ms default.
