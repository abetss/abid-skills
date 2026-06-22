---
name: qa-execution
description: Runs a full QA round on a feature. Launches the qa-runner agent with a work folder; agent writes evidence + REPORT.md; skill surfaces only the terse summary. Auto-invokes manual-qa-case-writing if qa.md is missing. Use when user says "run qa", "execute qa", "do qa", or a qa.md file needs to be validated.
model: sonnet
---

# QA Execution — Launcher

Launches `qa-runner` and surfaces its return. Does NOT read qa.md content, write evidence, or inspect per-case state. If you find yourself doing those, stop — that's the agent's job.

**Announce at start:** "Launching qa-runner for this work folder."

## Orchestration checklist

Copy this into your response and check items as you go:

```
QA Round Progress:
- [ ] Work folder identified
- [ ] qa.md exists (else invoke manual-qa-case-writing, then continue)
- [ ] checkpoint.json present? → mode=continue; else mode=fresh
- [ ] Dispatch qa-runner with work folder path + mode
- [ ] Parse agent's JSON return
- [ ] Handle by status:
  - [ ] COMPLETE       → present summary
  - [ ] NEEDS_INPUT    → surface questions, write ANSWERS.md, re-dispatch
  - [ ] BLOCKED        → report blocker to user
  - [ ] CONTEXT_LIMIT  → auto-re-dispatch with mode=continue (no user)
- [ ] Present summary (link REPORT.md — do NOT inline)
```

## Invariants
- Never reads qa.md content
- Never opens evidence/*
- Only: validates inputs, dispatches agent, parses JSON return, presents summary

## Dispatch prompt template

```
Run QA round {N} against the app. Work folder: {path}.
Mode: {fresh|continue}.
Read qa.md, spec.md (if present), known-issues.yaml (if present),
CLAUDE.local.md for creds + URL.
{if continue: Read checkpoint.json and ANSWERS.md to resume.}
Execute per your standard contract. Return JSON only.
```

## Handling NEEDS_INPUT
1. Surface questions to user verbatim
2. Collect answers
3. Write answers to `<work>/ANSWERS.md`
4. Re-dispatch qa-runner with mode=continue

## Handling CONTEXT_LIMIT
Re-dispatch automatically with mode=continue. Agent resumes from checkpoint.json. No user involvement.

## Present the summary

From the agent's JSON return, tell the user:
- Verdict (GO / NO-GO)
- Pass rate (X/Y)
- Top 3 issues (titles only — link REPORT.md for details)
- Report path
- New bug IDs

Do NOT paste REPORT.md contents. Link to it.

## Example invocation

```
User: "run qa on work/2026-04-23-notifications"

Skill announces: "Launching qa-runner for work/2026-04-23-notifications"
Skill verifies qa.md exists; yes.
Skill checks checkpoint.json; absent → mode=fresh.
Skill dispatches qa-runner.

qa-runner runs 14 cases, writes evidence/TC-001..014/,
updates qa.md checkboxes, writes REPORT.md, returns:
{
  "status": "COMPLETE",
  "round": 2,
  "passed": 12, "failed": 2, "unknown": 0,
  "new_bugs": ["BUG-2026-04-23-001", "BUG-2026-04-23-002"],
  "report_path": "work/2026-04-23-notifications/REPORT.md"
}

Skill presents to user:
  Verdict: NO-GO
  Pass rate: 12/14
  Top issues:
    - BUG-2026-04-23-001 (P0) Attendant toast never renders (Firefox)
    - BUG-2026-04-23-002 (P1) Toast missing role=status (a11y)
  Report: work/2026-04-23-notifications/REPORT.md
```

## Reset protocol

If implementation changed since last round, reset ALL checkboxes in qa.md to `- [ ]` before dispatching. A previous pass is meaningless after a code change.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reading qa.md in the skill | Agent's job — dispatch and trust the contract |
| Pasting REPORT.md into the response | Link to it, don't inline |
| Asking user mid-run for clarifications | Agent must return NEEDS_INPUT for this |
| Not resetting after code changes | Reset qa.md to all `[ ]` when code changed |
| Restarting the server unnecessarily | If server is up, use it — don't restart |
| Letting the skill grow past its job | No per-case logic in the skill; all in qa-runner |
