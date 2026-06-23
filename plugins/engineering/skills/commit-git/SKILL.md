---
name: commit-git
description: Use when the user wants to commit staged changes to git — "commit this", "commit-git", "make a commit", "commit with conventions". Writes a conventional commit message (prefix + optional ticket reference) and fixes any pre-commit hook errors before committing.
---

# Commit (git)

Commit the staged changes to git using your project's commit conventions. If the user named
a ticket/issue, include it; otherwise infer it from the branch name or omit it.

## Prefixes (required)
- `feat:` New feature
- `fix:` Bug fix
- `chore:` Maintenance, dependencies, config, refactor, docs etc

## Format
```
[<ticket>] <prefix>: <short description>

<optional body — what/why, not how>
```

> The `[<ticket>]` segment is optional — drop it if your project doesn't track work in an
> issue tracker.

## Rules
1. If pre-commit hooks (linters, formatters) report errors, fix them all properly before
   retrying the commit — never bypass hooks with `--no-verify`. If a fix is complex and
   needs clarification, ask the user.
2. Use third person present ("adds" not "add" or "added").

## Examples
```
[PROD-34] feat: adds user invite flow for managers

[PROD-201] fix: resolves auth race condition on mobile

chore: updates date-fns dependency
```
