---
name: executing-task
description: When executing a single task
---

# Executing a Plan Task

## Overview

Execute the task given. Read the task's context, follow its Implementation steps exactly, run every Verification check, and report completion by updating the task checkboxes and reporting back.

## Inputs

Task: could be a file, a task list with reference to the target task, or a description of a task
Walkthrought: Preceeding related work contex, this is usually in the file `walkthrough.md` withing the same work/session folder

---

## The Process

### Step 1: Understand
1. mark task to in progress by changing its [ ] to [x]
2. Read task in full
3. Read walktrhough in full
4. Check the state of the work env (usually the repo(s))
5. Review critically — identify any questions or concerns. If any, raise
6. Summarize understanding (to yourself, not to the user unless asked)
   - Why (business reason)
   - Current State → Desired State delta
   - Files to create/modify/delete
   - Patterns to follow (from similar files)

### Step 2: Execute

If a task has implementation section follow it in order.
If its instruction has [ ], mark them as [-] when in progress and [x] when done.

---

### Step 3: Verify
**Rules:**
- check verificaiotn step as done if they are fully done
- verifcaiton is done only when all of them are passed
- Have a subagenet complete the verifacation step
- If a task has verification section follow in order.
- If its steps has [ ], mark them as [-] when in progress and [x] when done. (responsibility of the subagent)
- Each verifiaction step is a gate — fail any and the task is not complete.






1. run the verification steps in parallel whenever execution step declares work compelte
2. if there is a failure, rest the verification steps status to todo (ex: [ ]), and report that to the execution step so that next time execution step finished, all the verification steps run again
3. When all steps are marked as pass, move to the next step

---

### Step 5: Report Completion

All steps of the task must be checked by their designated step. If not, invoke that step.

1. First clean up. That could mean deleteing any temporary left overs, or removing anything that doesn't need to be commited or be reivewed by the user.
2. Document in `walkthrough.md` (in the workfolder, same folder as `task-list.md`):
   - Decisions made and why
   - Learnings discovered
   - Deviations from plan (if any)
   - Files created/modified
   (Only document significant items — skip if nothing notable.)
3. Mark the task complete (on the task file, and if there is a task list, in the task list)
3. Commit the work.
4. Report task compelte
---

## When to Stop and Ask

**STOP immediately when:**
- Instruction is unclear or ambiguous
- Missing dependency or file not found
- Test fails and you can't figure out' why
- Convention file conflicts with task instructions
- Edge case not covered in task
- Dev server not running or crashes during browser QA, and you could not fix it yourself
- Browser QA reveals a bug that blocks verification
- A dependency task (`Depends on:` in `## Context`) is not yet marked `[x]` in `task-list.md`

**Ask for clarification rather than guessing.**

---

## Remember

- **Read context first** — Similar Files, Conventions, Skills before coding
- **Follow the task exactly** — Don't add features not in the task
- **Handle listed edge cases** — Everything in `## Context`'s Data Flow and in the QA cases must be covered
- **Run all verifications** — Don't skip checks, don't skip subsections
- **QA cases are inline** — They live in the task file, not in a separate qa.md
- **Adding a Post verification task resets Verification** — Any new item under `## Post verification tasks` means every `## Verification` checkbox goes back to `- [ ]` and must be re-run once the Post verification tasks are all `- [x]`
- **All three sections must be green to complete** — Implementation, Verification, and Post verification tasks must ALL be `[x]` simultaneously
- **Report honestly** — If something didn't work, say so
- **Document learnings** — Add significant decisions to `walkthrough.md`
- **One task only** — Don't start the next task without approval

## Common Mistakes

- **Mixing Implementation and Verification** — Implementation is what you build; Verification is what you run to confirm it works
- **Skipping context read** — Always read similar files and conventions first
- **Adding unlisted features** — Only implement what's in the task
- **Guessing on ambiguity** — Ask for clarification
- **Not updating `task-list.md`** — status must move `[ ]` → `[-]` → `[x]` as you progress

---

## Anti-Rationalization

These are excuses agents use to skip browser verification. None are valid:

- **"Tests pass, so it works"** — Unit tests verify logic, not wiring. A button with an empty `onClick` passes every test. Only a browser click catches it.

- **verifying means seeing the behaviour**: I checked the code and the behvours seems right, I don't need to QA, or run the tests.

- **"The server isn't running so I'll work around it"** — A broken server is a BLOCKER, not a workaround opportunity. Stop, fix it, then resume. There is no half-way QA.
