# Escalate -- Question the Architecture

## When to Read This

You're here because 3+ fix attempts have failed, or each fix reveals problems in a different place.

**This is NOT a failed hypothesis. This is a wrong architecture.**

## The Pattern

Recognize these signals:
- Each fix reveals new shared state, coupling, or dependency that wasn't visible before
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere
- You're "sticking with the approach through sheer inertia"

## What to Do

### 1. STOP Fixing

Do not attempt Fix #4. More fixes on a broken architecture make things progressively worse.

### 2. List What You Learned

Write down what each failed attempt revealed about the system:
- Attempt 1: revealed that...
- Attempt 2: revealed that...
- Attempt 3: revealed that...

Each failure taught you something. What's the pattern across them?

### 3. Question Fundamentals

Ask yourself:
- Is this pattern fundamentally sound for what we're trying to do?
- Are we treating symptoms of a structural problem?
- Would a different approach avoid the entire class of issue?
- Is the cost of refactoring less than the cost of continued patching?

### 4. Discuss with the User

Present your findings:
- "I've attempted 3 fixes and each revealed a different underlying issue."
- "The pattern suggests this is structural, not a localized bug."
- Here's what I think is fundamentally wrong: [explanation]
- Here are the options: [refactor / accept and document / different approach]

Do NOT proceed without the user's decision on direction.

### 5. If Refactoring is Chosen

This is now a planned change, not a bug fix. Consider:
- Using `plan-prep` to properly scope the refactoring
- Breaking it into incremental steps
- Ensuring each step has its own tests
