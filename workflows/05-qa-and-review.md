# QA & Review Workflow

This flow ensures that all code changes meet quality and security standards before being merged into the main branch.

```text
 [ Code Changes Ready ]
           │
           ▼
  ┌────────┴────────┐
  ▼                 ▼
[ Code Review ] [ Security Review ]
(review-code)   (security-review)
  │                 │
  └────────┬────────┘
           ▼
[ Generate Test Cases ]  <-- (Skill: manual-qa-case-writing)
           │
           ▼
 [ Execute QA Cases ]    <-- (Skill: qa-execution)
           │
           ▼
 [ Approve & Merge ]
```
