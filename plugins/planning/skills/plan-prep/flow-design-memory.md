# Flow Design — Memory

Learnings about designing execution flows. Read this before starting any flow design.

## When to write

When the user corrects a flow you designed — a missing branch, a wrong assumption about how data moves, an edge case you didn't consider, a side effect you missed. Record the pattern so you don't make the same mistake on similar flows.

## Entry Format

```markdown
## [Date] -- [One-line summary]
**Flow type**: [e.g., CRUD form submission, list with filters, background job]
**What the user corrected**: [what you got wrong or missed]
**Design lesson**: [the pattern to follow next time — e.g., "when designing assignment flows, always include the notification branch because..."]
```

<!-- Add entries below -->
