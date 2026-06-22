# Find Test Polluter

When tests fail only when run together (not in isolation), one test is polluting shared state for another. Use bisection to find which test is the polluter.

## The Technique

1. Run each test file one at a time, in order
2. After each test, check if the pollution exists (unwanted file, corrupted state, leaked process)
3. The first test that produces the pollution is the polluter

## How to Apply

```
For each test file in the suite:
  1. Run the test in isolation
  2. Check for the pollution artifact
  3. If pollution appeared: THIS is the polluter
  4. If no pollution: continue to next test
```

The agent should write a project-specific script or loop when this technique is needed. Adapt to the project's test runner (pnpm test, npm test, pytest, etc.).

## What to Check For

Common pollution artifacts:
- Files created outside test directories (`.git` in source root, temp files not cleaned up)
- Database rows not rolled back
- Environment variables set and not restored
- Global state modified (singletons, caches, registries)
- Processes spawned and not killed
- Port bindings not released

## After Finding the Polluter

1. Read the polluting test -- find where it creates/modifies shared state
2. Fix the test to clean up after itself (afterEach, afterAll, try/finally)
3. Consider adding environment guards (see `defense-in-depth.md`) to prevent the pollution from causing damage even if cleanup is missed
4. Run the full suite to confirm the fix
