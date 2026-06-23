# QA Workflow

From requirements to a verified feature. A single `qa-runner` agent owns
each round end-to-end — it reads cases, drives both chrome profiles,
writes evidence, and returns a summary.

## Scripted QA (happy path)

```
┌─────────────────────────┐
│     write-qa-cases      │   ← uses manual-qa-case-writing skill
└────────────┬────────────┘
             │   (writes qa.md with 6-field cases + traceability)
             ▼
┌─────────────────────────┐
│          do-qa          │   ← uses qa-execution (launcher)
└────────────┬────────────┘
             │   (dispatches qa-runner with work folder path)
             ▼
┌─────────────────────────┐
│       qa-runner         │   ← agent owns the whole round
│                         │
│  - logs in as manager   │      uses chrome-1
│  - logs in as attendant │      uses chrome-2
│  - runs every case      │
│  - writes evidence/     │
│  - updates qa.md        │
│  - writes REPORT.md     │
└────────────┬────────────┘
             │
             ▼
     JSON return to skill
     (verdict, counts, report path)
             │
             ▼
       user sees summary
```

## Exploratory QA

```
┌─────────────────────────┐
│   qa-exploratory skill  │
└────────────┬────────────┘
             │   (takes a charter: persona + goal + time box)
             ▼
┌─────────────────────────┐
│   qa-runner             │   ← same agent, exploratory mode
│   (charter, not qa.md)  │
│                         │
│  - wanders the feature  │
│  - records friction     │
│  - writes FINDINGS.md   │
└────────────┬────────────┘
             │
             ▼
     findings summary
```

## Alternate Paths

### qa.md already exists (skip writing)
Start straight at `do-qa`.

### Code changed mid-execution → reset
Reset all checkboxes in qa.md to `- [ ]`, then restart `do-qa`. Previous
pass is invalid after a code change.

### Agent returns NEEDS_INPUT (hard blocker)
```
qa-runner hits something it can't resolve
       │
       ▼
returns early with NEEDS_INPUT + questions
       │
       ▼
qa-execution surfaces questions to user
       │
       ▼
user answers → ANSWERS.md
       │
       ▼
qa-execution re-dispatches with --continue
       │
       ▼
qa-runner resumes from checkpoint.json
```

### Hit context limit mid-round
qa-runner writes checkpoint, returns `CONTEXT_LIMIT`, qa-execution
re-dispatches automatically with --continue. No user involvement.

### 3+ consecutive failures → halt
Agent stops the round, returns with partial results — likely a systemic
issue (server, infrastructure, broken build).

## Reference — what each piece does

```
  write-qa-cases           →  command; uses manual-qa-case-writing skill
  manual-qa-case-writing   →  skill that authors qa.md (6-field cases,
                              traceability, a11y, PIPEDA, perf)
  do-qa                    →  command; uses qa-execution skill
  qa-execution             →  launcher skill; dispatches the agent
  qa-runner                →  agent that OWNS a full round (scripted
                              or exploratory)
  qa-exploratory           →  skill for charter-based discovery
```

## Inside `qa-runner`

```
┌─────────────────────────┐
│       qa-runner         │
└────────────┬────────────┘
             │
             ├──► verify app URL reachable (else BLOCKED)
             ├──► read qa.md + spec + known-issues.yaml
             ├──► if checkpoint.json → reconcile, resume
             ├──► for each case:
             │       set role context (chrome-1 or chrome-2)
             │       execute steps
             │       gather evidence (deterministic or judgment)
             │       run adversarial probe if P0 / on fail
             │       write evidence/TC-NNN/evidence.json
             │       update qa.md checkbox
             │       append to checkpoint.json
             │       evict raw tool output from context
             ├──► every 5 cases: flush checkpoint
             ├──► dedup against known-issues.yaml
             ├──► write REPORT.md (light or full by round size)
             └──► return JSON summary
```

## Evidence layout

```
<work folder>/
  qa.md                         # cases + checkboxes
  spec.md                       # feature requirements
  known-issues.yaml             # bugs already tracked
  checkpoint.json               # state for --continue
  ANSWERS.md                    # only after NEEDS_INPUT round
  REPORT.md                     # round report (light or full)
  FINDINGS.md                   # only after exploratory round
  evidence/
    TC-001/
      evidence.json
      before.png
      after.png
      console.log
      network.har  (optional)
    TC-002/
      ...
```

## Bug IDs

Date-scoped: `BUG-YYYY-MM-DD-NNN`. Ordinal within today. No global
counter, no lock coordination.
