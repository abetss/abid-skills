---
name: qa-exploratory
description: Runs time-boxed exploratory QA against a feature. Charter-driven (persona + goal + time box), not case-driven. Launches qa-runner in exploratory mode to find novel bugs, friction, and gaps that scripted cases miss. Use for pre-release sweeps, accessibility exploration, or when the user asks to "explore" a feature.
model: sonnet
---

# QA Exploratory — Charter-based Discovery

Exploratory finds what scripted cases miss. Give the agent a lens (persona + goal + time box), not a checklist. The agent wanders and reports.

**Announce at start:** "Starting exploratory QA with charter."

## Exploratory session checklist

Copy this into your response and check items as you go:

```
Session Progress:
- [ ] Charter received (persona + goal + constraints + focus + time)
- [ ] Charter incomplete? → ask user for missing components before dispatching
- [ ] Work folder and app URL confirmed
- [ ] Dispatch qa-runner with mode=exploratory + charter + FINDINGS.md output
- [ ] Parse agent's JSON return
- [ ] Surface findings summary (link FINDINGS.md — do NOT inline)
- [ ] Note candidate findings for promotion to qa.md (via manual-qa-case-writing)
```

## Inputs
- **Feature area** — what to explore (folder, URL, or component)
- **Charter** — persona + goal + constraints
- **Time box** — how long (default 30 min)

## Charter template

```
Persona: {who is using this — role, assistive tech, context}
Goal: {what they're trying to accomplish}
Constraints: {operating conditions — viewport, device, connectivity}
Focus: {what to pay attention to — friction, errors, surprises, a11y}
Time: {N minutes}
```

## Example charters

```
Persona: attendant using keyboard only, no mouse
Goal: complete onboarding + submit first timesheet
Constraints: Chrome at 1280×800, standard keyboard
Focus: unreachable elements, focus-trap bugs, missing shortcuts
Time: 30 min
```

```
Persona: manager on iPhone 12 (small screen)
Goal: review and approve three timesheets
Constraints: mobile viewport 390×844, touch only
Focus: target size, tap accuracy, scroll/pan friction, hidden actions
Time: 20 min
```

```
Persona: screen reader user (VoiceOver)
Goal: find and cancel a scheduled appointment
Constraints: desktop Safari + VoiceOver
Focus: live region announcements, heading structure, landmark nav
Time: 45 min
```

## What the agent does in exploratory mode

qa-runner in exploratory mode does NOT read qa.md. It:
1. Enters the app as the persona
2. Attempts the charter goal within the time box
3. Records every friction point, error, and surprise in FINDINGS.md
4. For each bug-like finding, writes a proposed 6-field test case
5. Returns a summary

## FINDINGS.md format (produced by agent)

```markdown
# Exploratory Findings — {date} — {charter persona summary}

## Charter
{full charter}

## Session summary
- Duration: {minutes}
- Goal achieved: yes | no | partial
- Friction count: N
- Potential bugs: N

## Findings

### Finding 1: {short title}
- Severity: P0/P1/P2
- Category: functional / a11y / usability / perf
- What I tried: {steps}
- What happened: {observed}
- What I expected: {expected}
- Evidence: {screenshot path, DOM snippet}
- Proposed test case: {6-field block, ready for promotion}

## Noted but not bug
- {friction that isn't a clear bug}
```

## When to run exploratory
- Before shipping a feature (pre-release sweep)
- After a big UI refactor (check assumptions)
- When a persona type hasn't been tested (e.g., switch-device user)
- Periodically on mature features (regression blind spots)

Not for: routine feature validation — use qa-execution.

## Return to main thread
Surface:
- Charter (persona + goal)
- Goal achieved: yes/no/partial
- Findings count by severity
- Top 3 findings (titles only)
- Path to FINDINGS.md

## Promoting findings into qa.md

Findings with a proposed test case are candidates for promotion:
1. User reviews FINDINGS.md
2. User selects which findings to promote
3. Invoke manual-qa-case-writing to append the proposed cases to qa.md

## Common mistakes

| Mistake | Fix |
|---|---|
| No charter — just "explore this" | Always have persona + goal + time box |
| Running exploratory on every task | Use for features, not tasks; or for persona gaps |
| Treating findings as noise | Promote good findings into qa.md |
| Over-long sessions | 45 min max — signal-to-noise drops after that |
| Exploring with no feature area | Exploration needs a target — specify page/flow/component |
