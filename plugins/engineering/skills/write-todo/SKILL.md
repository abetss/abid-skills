---
name: write-todo
description: Create a scoped-out todo item when work should be deferred to a later session. Writes a markdown file to a-todo/ and optionally leaves code comments linking back to it.
user_invocable: true
---

# Write Todo

A todo is work that the AI or human decides should be scoped out of the current task and done later. It creates a traceable link between a deferred decision and the code it affects.

## When to Use

- You or the user identify something that should be done but is out of scope for the current work
- During code review, a finding is deferred rather than fixed now
- A follow-up action is needed after the current task completes
- An improvement is identified but not urgent enough to interrupt flow

## ADD to Jira
Create a ticket in Jira. Add a techdebt ticket to it

## File Naming

**Location**: `{repo}/a-todo/`

**Format**: `{jira-ticket-number}-{kebab-title}.md`

- `{jira-ticket-number}` — prod-123
- `{kebab-title}` — short descriptive kebab-case title

**Example**: `prod-123-add-retry-logic-to-email-sender.md`

## Todo File Template

```markdown
# {Title}

**Date**: {YYYY-MM-DD}
**Priority**: {High | Medium | Low}
**Related**: {link to work folder, plan, or PR if applicable}

## What

{what needs to be done}

## Why

{why this matters, what triggered it}

## AC

1. {concrete ac}
2. {concrete ac}
...
n. {concrete ac}
...

## Code References

{list each file:line where a todo comment was left, or "None" if no code comments}
```

## Code Comments

When the todo relates to specific code locations, leave a comment at each location:

```
// todo ({file-slug}): {brief description of what needs to change here}
```

Where `{file-slug}` is the filename without `.md` — e.g. `prod-123-add-retry-logic-to-email-sender`.

**Comment syntax by language:**
- TypeScript/JavaScript: `// todo ({slug}): {description}`
- CSS: `/* todo ({slug}): {description} */`
- HTML: `<!-- todo ({slug}): {description} -->`
- SQL: `-- todo ({slug}): {description}`

A todo may have **zero or multiple** code comments. Only add comments where they provide value — don't force them if the todo is purely about creating new files or infrastructure.

## Process

1. **Determine the next number**: List files in `a-todo/` matching today's date prefix, find the highest N, use N+1
2. **Write the todo file** with the template above
3. **Add code comments** at relevant locations (if any)
4. **List the code references** in the todo file's "Code References" section
5. **Tell the user** the todo was created with the filename and a one-line summary

## Example

File: `a-todo/prod-123-add-retry-logic-to-email-sender.md`

Code comment in `src/services/email/email-client.ts:47`:
```typescript
// todo (prod-123-add-retry-logic-to-email-sender): add exponential backoff with 3 retries
```

Todo file's Code References section:
```markdown
## Code References

- `src/services/email/email-client.ts:47` — add exponential backoff with 3 retries
```
