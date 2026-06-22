# Skill Development Notes

Notes for future iterations of this skill. Not read during execution — only for skill development sessions.

## Pending Decisions

### Technical Analysis belongs in Task Breakdown
The old Step 3 (Technical Analysis — listing all transformers, API changes, DB changes) should be part of "How Does the Work Break Down?" component, not a separate step. The task breakdown naturally needs to enumerate technical changes to create tasks from them. Be careful not to duplicate this work across components.

## Design Principles

### Architecture opportunities must surface during every step
Any step that touches the system — flow design, codebase exploration, task breakdown — should actively look for architecture decisions that need resolution. This is not limited to the "Finding the Right Solution" component. When an architecture opportunity is found mid-step, pause, flag it to the user, and resolve it (possibly by delegating to architect-solution) before continuing.

### Skills should not know about their consumers
A skill should be standalone — it doesn't know who calls it or what happens with its output. The consumer (e.g., plan-prep) passes context and instructions when invoking it. Coupling lives in the caller, not the callee. Don't add "if plan-prep.md exists, do X" to a skill — instead, have plan-prep pass the relevant content as instructions.

### Each step must have a clear, non-overlapping goal
Be very careful that the goal of each step doesn't bleed into another. If two steps produce similar outputs, one of them is wrong. The test: can you explain in one sentence what this step achieves that no other step does?

## TODO

(none currently)
