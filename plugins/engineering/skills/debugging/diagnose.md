# Diagnose

Root cause investigation methodology. Complete this before attempting any fix.

**Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

If you haven't completed this process, you cannot propose fixes.

## Investigation Steps

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- Read stack traces completely -- they often contain the exact answer
- Note line numbers, file paths, error codes
- Read the FULL error, not just the first line

### 2. Reproduce Consistently

- Can you trigger it reliably? What are the exact steps?
- Does it happen every time?
- If not reproducible: gather more data, don't guess
- For intermittent issues: identify conditions that increase frequency

### 3. Check Recent Changes

- What changed that could cause this?
- `git log --oneline -20 -- <suspect-path>`
- New dependencies, config changes, environment differences
- If you can pinpoint the commit: `git bisect` to confirm

### 4. Multi-Component Evidence Gathering

**When the system has multiple components (API -> service -> database, CI -> build -> deploy):**

Before proposing fixes, add diagnostic instrumentation:

```
For EACH component boundary:
  - Log what data enters the component
  - Log what data exits the component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.
```

This reveals which layer fails (e.g., secrets -> workflow OK, workflow -> build FAILED).

### 5. Pattern Analysis

- Find similar WORKING code in the same codebase
- What works that's similar to what's broken?
- List every difference, however small -- don't assume "that can't matter"
- If implementing a pattern, read the reference implementation COMPLETELY. Don't skim.
- Understand dependencies: what settings, config, environment does this need?

### 6. Trace Data Flow

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing backward until you find the source
- Fix at the source, not at the symptom

For deep call-stack bugs with long chains, read `root-cause-tracing.md` in this directory for the complete backward tracing technique.

### 7. Form Hypothesis

- State clearly: "I think X is the root cause because Y"
- Be specific, not vague
- Make the SMALLEST possible change to test the hypothesis
- One variable at a time -- don't fix multiple things at once

### 8. Confirm Root Cause

- If hypothesis was correct: state the root cause and proceed to `fix.md`
- If hypothesis was wrong: form a NEW hypothesis based on what you learned. Don't stack fixes.
- If you don't understand: say so. Don't pretend. Research more or ask the user.

## Issue-Specific Guidance

### Performance Issues
- Profile before guessing -- use browser devtools, server profiling, or `console.time()`
- Check for N+1 queries (look at database query logs)
- Check for unnecessary re-renders (React Profiler)
- Check for memory leaks (heap snapshots)
- Measure before and after -- don't claim "faster" without numbers

### Build Failures
- Read the FULL error output, not just the last line
- Check Node/package versions match expectations
- Check for lockfile conflicts (`pnpm-lock.yaml` changes)
- Verify environment variables are set
- Try a clean install (`rm -rf node_modules && pnpm install`)

### Flaky Tests
- Is it timing-dependent? See `condition-based-waiting.md`
- Is it test-order-dependent? See `find-polluter.md`
- Is it data-dependent? Check for shared state between tests
- Run the test in isolation vs. with the full suite -- different results?

### When Investigation Reveals No Root Cause

If systematic investigation truly can't find the cause:

1. Document what you investigated
2. Implement appropriate handling (retry, timeout, error message)
3. Add monitoring/logging for future investigation
4. But: 95% of "no root cause" cases are incomplete investigation
