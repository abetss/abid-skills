# Root Cause Tracing

Trace bugs backward through the call chain to find the original trigger. Fix at the source, not where the error appears.

## When to Use

- Error happens deep in execution, not at the entry point
- Stack trace shows a long call chain
- Unclear where the invalid data originated
- You're tempted to fix where the error appears (that's the symptom, not the cause)

## The Process

### 1. Observe the Symptom
What's the actual error? Note the exact message, file, and line.

### 2. Find the Immediate Cause
What code directly produces this error? Read that function.

### 3. Ask: What Called This?
Who passed the bad value to this function? Read the caller.

### 4. Keep Tracing Up
Repeat step 3. At each level ask: "Is the value wrong here, or was it already wrong when it arrived?"

### 5. Find the Original Trigger
You've found the source when you reach the point where the value was CREATED wrong (not just passed wrong).

## Adding Stack Traces

When you can't trace manually, add instrumentation:

```
// Before the problematic operation
const stack = new Error().stack;
console.error('DEBUG [operation-name]:', {
  suspectValue,
  cwd: process.cwd(),
  stack,
});
```

**Tips:**
- Use `console.error()` in tests, not a logger (loggers may be suppressed)
- Log BEFORE the dangerous operation, not after it fails
- Include context: directory paths, environment variables, timestamps
- `new Error().stack` gives the complete call chain

## Worked Example

**Symptom:** `git init` runs in the source code directory instead of a temp directory.

**Trace:**
1. `git init` receives `cwd: ''` (empty string) -> resolves to `process.cwd()`
2. `WorktreeManager.createSessionWorktree(projectDir)` -- `projectDir` is empty
3. `Session.create()` passes empty string
4. Test accesses `context.tempDir` before `beforeEach` runs
5. `setupCoreTest()` returns `{ tempDir: '' }` initially

**Root cause:** Variable accessed before initialization in test setup.
**Fix:** Made `tempDir` a getter that throws if accessed before `beforeEach`.

**Key insight:** The error appeared in `git init` (level 1) but the bug was in test setup (level 5). Fixing at level 1 would have masked the real problem.

## Principle

NEVER fix just where the error appears. Trace back to find the original trigger. Then also add validation at intermediate layers (see `defense-in-depth.md`).
