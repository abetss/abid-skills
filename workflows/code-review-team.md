# Code Review Team Workflow

Multi-agent code review orchestrated by the `code-review-team` skill. Spawns
specialized reviewers in parallel — one per **convention** and one per
**expert profile** — then compiles all findings into a single document.

## Happy Path

```
┌─────────────────────────┐
│    code-review-team     │   ← orchestrator (main thread)
└────────────┬────────────┘
             │
             ▼
   read learnings.md
             │
             ▼
   read task/ folder (task-list.md + task-NN.md)
             │
             ▼
   read a-kb/table-of-content.md
             │
             ▼
   collect .claude/rules/
             │
             ▼
   get changed files (git)
             │
             ▼
   build convention-to-files map
             │
             ▼
   build profile-to-files map
             │
             │   launch ALL agents in parallel
             │   (single wave, no sequencing)
             │
             ├──► convention agent 1
             ├──► convention agent 2
             ├──► convention agent N
             ├──► profile: designer
             ├──► profile: architect
             ├──► profile: domain-expert
             ├──► profile: code-expert
             ├──► profile: performance-expert
             ├──► profile: human-advocate
             └──► profile: accessibility
                          │
                          ▼
              orchestrator collects findings,
              asks agents to clarify or drop
              low-confidence items (resume)
                          │
                          ▼
              write accepted findings to
              code-review-raw.md
                          │
                          ▼
              compile + deduplicate into
              code-review.md (by severity)
                          │
                          ▼
              update learnings.md
                          │
                          ▼
┌─────────────────────────┐
│ respond-to-code-review  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   write-review-guide    │
└─────────────────────────┘
```

## Two kinds of reviewer

### Convention agents — one per convention doc
Use Sunnet model for these agents

```
  input      →  a convention doc from a-kb/ + applicable .claude/rules/
  scope      →  files that match the convention's domain frontmatter
                (home, platform-api, or shared)
  output     →  file:line violations with severity + suggestion
```

### Profile agents — one per expert lens
Use Opus model for these agents
```
  input      →  the profile's own markdown (its lens + priorities)
  scope      →  files that match the profile's domain frontmatter
  output     →  file:line violations + up to 5 positive findings
```

## The 7 expert profiles

```
  designer            →  UI/UX quality, visual consistency, composition
  architect           →  extensibility, coupling, scalability, boundaries
  domain-expert       →  business logic, compliance, data integrity
  code-expert         →  bugs, type safety, async correctness, edge cases
  performance-expert  →  N+1 queries, batching, memory, concurrency
  human-advocate      →  cognitive load, error recovery, UX for disabled users
  accessibility       →  WCAG 2.1 AA, ARIA, touch targets, keyboard nav
```

## Domain scoping

Both convention and profile agents have a `domain` frontmatter field that
limits which files they see:

```
  domain: home          →  only changes under apps/home/
  domain: platform-api  →  only changes under apps/platform-api/
  domain: shared        →  all changes
```

## Severity legend

```
  Critical   →  data loss, security breach, recurring user-visible bug
  Major      →  functional bug, design flaw, convention violation
  Minor      →  code quality, non-blocking improvement
  Nit pick   →  style preference, subjective suggestion
```

## Deduplication rules

When multiple agents flag the same file:line:

```
  1. Keep the highest severity
  2. Merge descriptions from different lenses
  3. Note which agents flagged it
```

## Learnings memory (persistent across runs)

```
  /Users/abtinghods/.claude/skills/code-review-team/learnings.md
```

Tracked categories:

```
  False Positives      →  findings agents should skip next run
  Accepted Trade-offs  →  known violations the team accepts
  Recurring Patterns   →  frequent violations → candidates for automation
  Convention Gaps      →  issues no convention covers yet
  Calibration Notes    →  severity overrides
```

## Inputs

```
  a-works folder       →  contains task/ subfolder (task-list.md + task-NN.md files)
                          or auto-detect from git
  output file name     →  default: code-review.md in the a-works folder
```

## Fallback — no task/ folder

```
  read a-kb/table-of-content.md
        │
        ▼
  match rules/conventions to changed files by domain/glob
        │
        ▼
  include any rule/convention whose scope matches ≥1 changed file
```

## Alternate Paths

### Findings indicate a process gap (not just a bug)

```
┌─────────────────────────┐
│   compiled findings     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       never-again       │   ← fix the process that allowed it
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ respond-to-code-review  │
└─────────────────────────┘
```

### Bug found during review → debug loop

```
┌─────────────────────────┐
│   compiled findings     │
└────────────┬────────────┘
             │
             ▼
        (see debug.md)
             │
             ▼
┌─────────────────────────┐
│ respond-to-code-review  │
└─────────────────────────┘
```
