# Defense-in-Depth Validation

After fixing a bug, consider whether additional validation layers would make the bug structurally impossible to recur.

**This is optional post-fix hardening.** Not every bug needs it. Use when the bug class is dangerous enough to warrant prevention at multiple layers.

## Why Multiple Layers

Single validation: "We fixed the bug."
Multiple layers: "We made the bug impossible."

Different layers catch different cases -- different code paths bypass entry validation, mocks bypass business logic, edge cases on different platforms need environment guards.

## The Four Layers

### Layer 1: Entry Point Validation
Reject obviously invalid input at the API/function boundary.
```
if (!workingDirectory || workingDirectory.trim() === '') {
  throw new Error('workingDirectory cannot be empty');
}
```

### Layer 2: Business Logic Validation
Ensure data makes sense for this specific operation.
```
if (!projectDir) {
  throw new Error('projectDir required for workspace initialization');
}
```

### Layer 3: Environment Guards
Prevent dangerous operations in specific contexts.
```
if (process.env.NODE_ENV === 'test' && !path.startsWith(tmpdir())) {
  throw new Error('Refusing operation outside temp dir during tests');
}
```

### Layer 4: Debug Instrumentation
Capture context for forensics when other layers fail.
```
logger.debug('About to perform operation', { directory, cwd, stack });
```

## When to Apply

Ask after fixing any bug:
- Could this class of bug happen through a different code path?
- Would a mock or test bypass my fix?
- Is this operation dangerous enough to warrant environment guards?

If the answer to any is yes, add the relevant layers. If no, skip this -- not every typo fix needs four layers of validation.
