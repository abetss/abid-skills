# Fix -- Test-First Workflow

Fix the bug by first proving it exists in a test, then implementing the fix.

## Structural Guards (MANDATORY)

These are not suggestions. They are hard constraints that MUST be followed in order:

1. **Write the test FIRST.** Before any fix code exists.
2. **Run the test.** It MUST fail.
3. **Verify the failure reason.** The test must fail for the EXPECTED reason -- the same failure the bug produces. If it fails for a different reason, it's the wrong test. Rewrite it.
4. **If the test passes**, it does not capture the bug. The test is wrong. Rewrite it until it fails for the correct reason.
5. **Only after confirmed correct failure**, implement the fix code.
6. **NEVER write test and fix in the same step.** This is the single most important rule. A test written alongside its fix is likely reverse-engineered from the fix, not from the expected behavior.

## Step 1: Write a Failing Test

Write a test at the level that most directly exercises the root cause:

- **Unit test**: pure logic, single function, data transformation, regex, calculations
- **Integration test**: crosses module boundaries, needs real DB/routes/HTTP
- **Both**: when root cause is localized (unit test locks the fix) but symptom is user-facing (integration test proves it's resolved)

The test must:
- Use the project's existing test patterns and helpers
- Assert what the code SHOULD do, not what it currently does
- Be named clearly to describe the bug scenario

### For flaky/timing bugs
Read `condition-based-waiting.md` -- replace arbitrary timeouts with condition polling.

### For test pollution
Read `find-polluter.md` -- use bisection to find which test creates unwanted state.

### If the bug cannot be tested
Some bugs genuinely can't be reproduced in automated tests (pure visual/layout, environment-specific, timing-dependent Heisenbugs). When this is the case:
- Explain specifically WHY it can't be tested
- Describe the manual verification method
- Get user acknowledgment before proceeding without a test

## Step 2: Run the Test

Run the test. Confirm:
- It fails (if it passes, rewrite -- Step 1)
- It fails for the expected reason (if wrong reason, rewrite -- Step 1)
- The failure message clearly shows expected vs. actual behavior

## Step 3: Implement the Fix

- ONE change addressing the root cause
- No "while I'm here" improvements
- No bundled refactoring
- No additional features

## Step 4: Verify

1. Run the failing test -- it MUST pass now
2. Run the full test suite for the affected area -- no regressions
3. If the test still fails: iterate on the fix (NOT the test). Count your attempts.

## Step 5: Escalation Check

- **After 2 failed fix attempts**: Return to `diagnose.md`. Your hypothesis may be wrong. Re-investigate with the new information each failed attempt revealed.
- **After 3 failed fix attempts**: STOP. Read `escalate.md`. This is likely an architectural problem, not a localized bug.

## Step 6: Capture Learnings

After the fix is verified, evaluate if anything surprising or non-obvious happened. If so, append to `memory.md` in this directory.

Only write learnings that would prevent a future mistake. Don't write obvious things. Format:

```markdown
## [Date] -- [One-line summary]
**Bug type**: [functional | flaky | performance | build | production]
**Root cause**: [one sentence]
**What was surprising**: [what we didn't expect]
**Prevention**: [what would prevent this class of bug]
```
