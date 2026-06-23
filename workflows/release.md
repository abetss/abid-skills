# Release Workflow

The full `release` command, end to end. Stops on any failure and reports.

## Happy Path

```
┌───────────────────────┐
│        release        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ product-guide-writer  │   ← document user-facing changes
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      commit-git       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    write-changelog    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│         push          │   ← rebase onto origin/main first
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    staging deploy     │   ← auto-triggered, monitor every 5min
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      prod deploy      │   ← manual trigger, requires confirmation
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│     monitor prod      │   ← every 5min until complete
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      close ticket     │   ← move Jira to Done + summary comment
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│       complete        │
└───────────────────────┘
```

## Alternate Paths

### Skip production (user said "don't deploy to prod")

```
┌───────────────────────┐
│    staging deploy     │
└───────────┬───────────┘
            │   (skip prod deploy + monitor)
            ▼
┌───────────────────────┐
│      close ticket     │
└───────────────────────┘
```

### Pre-commit hook fails

```
┌───────────────────────┐
│      commit-git       │
└───────────┬───────────┘
            │   (hook fails)
            ▼
       fix issues
            │
            ▼
   re-stage + new commit
            │
            ▼
   (continue happy path)
```

### Push rejected (rebase needed)

```
┌───────────────────────┐
│         push          │
└───────────┬───────────┘
            │   (origin/main ahead)
            ▼
   git rebase origin/main
            │
            ▼
    resolve conflicts
            │
            ▼
   (re-run push; continue)
```

### Staging deploy fails

```
┌───────────────────────┐
│    staging deploy     │
└───────────┬───────────┘
            │   (fail)
            ▼
       HALT + report
            │
            ▼
    await user guidance
```

### Production deploy fails

```
┌───────────────────────┐
│      prod deploy      │
└───────────┬───────────┘
            │   (fail)
            ▼
       HALT + report
            │
            ▼
    await user guidance
   (rollback / hotfix?)
```

## Step Reference

```
  1.  product-guide-writer   →  document user-facing changes
  2.  commit-git             →  prefixed message, jira ref
  3.  write-changelog        →  user-friendly release notes
  4.  push                   →  rebase first, then push -u
  5.  staging deploy         →  auto, monitored
  6.  prod deploy            →  manual gh workflow run
  7.  monitor prod           →  poll until complete
  8.  close ticket           →  Jira → Done + comment
  9.  complete               →  final summary to user
```
