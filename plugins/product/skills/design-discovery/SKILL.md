---
name: design-discovery
description: Team-based design process that discovers all roles, pages, states, flows, interactions, and accessibility contracts for a UI feature before any visual design begins.
argument-hint: "[feature name or requirements path]"
---

# Design Discovery

Orchestrates a team-based design process: Frame, Discovery Walk-through, Design, Specify.
Produces a complete discovery document so the designer never has to ask "what happens when...?" during design.

**Core principle:** Wrong proposals surface hidden rules faster than open-ended questions.

## Memory

Read `memory.md` in this directory before starting. It contains learnings from past sessions.

## Session Persistence

Check for `design-discovery-progress.md` in the work folder. If it exists, read it and resume where the session left off. Update it after every completed level.

## Prerequisites

`requirements.md` (or equivalent) must exist before starting. If it does not:

> "I need requirements before starting design discovery. Use the `write-requirements` command first, or provide a requirements document."

Parse requirements immediately for: acceptance criteria, roles, pages, business rules, compliance constraints.

## Process: 4 Rounds

| Round | Lead | Read | Purpose |
|-------|------|------|---------|
| 1. Frame | Product | `frame.md` | Understand brief, choose approach, assemble team, dispatch research agents |
| 2. Discovery | Product + Designer | `discover.md` | Walk through Roles, Pages, States, Flows, Interactions+Accessibility |
| 3. Design | Designer | `design.md` | Visual design via Storybook iteration or ASCII wireframes |
| 4. Specify | Engineering | `specify.md` | Component tree, types, fixtures, coverage matrix, handoff |

Read the corresponding file for each round. Read `perspectives.md` for team voice definitions. Read `research-agents.md` when dispatching agents in Round 1.

## Presentation Format

Distinct voices in meeting transcript format. Each team member speaks as a named character. The user participates as themselves. This is a facilitated team discussion, not a unified voice.

## Opt-out

Any round can be opted out by the user -- they will tell you. Do not ask. Default is to run all 4 rounds.

## Artifact Rule

Write artifacts to disk after every level. Team reviews, then user reviews. Three steps: write, team review, user review. Everything goes into a single `discovery.md` under section headings, except specialized Round 4 outputs.

## Anti-Rationalization

If you catch yourself thinking any of these, STOP:

| You're thinking... | Reality |
|---|---|
| "Let's skip states, the page is simple" | Simple pages still have loading, empty, error. Enumerate all 13 categories. |
| "This role probably sees the same thing" | Probably != confirmed. Propose both views, get corrected. |
| "We covered enough states, let's move on" | 5 states per page is the MINIMUM. Find ALL of them. |
| "The accessibility part is straightforward" | Accessibility is architectural input, not a checklist. Every component needs a contract. |
| "I'll ask what states exist" | Don't ask. Propose a concrete list and get corrected. |
| "This flow only has a happy path" | Every flow has failure branches. Every destructive action has a recovery path. |
| "Mobile is the same as desktop" | State it explicitly, even if true. Implicit "same" means QA skips it. |
| "The error state just shows an error" | Which error? Network, validation, conflict, permission, rate limit -- each is different. |
| "We can figure out accessibility later" | Later means never. Accessibility shapes design decisions NOW. |
| "One more quick proposal without waiting for user" | Every correction is a rule discovery. Do not skip the correction step. |

## Rules

- NEVER skip the propose-and-correct loop -- corrections ARE the discovery
- One level at a time, in order. Do not advance until user confirms current level
- Every business rule the user corrects goes into conventions immediately
- Batch per page: present the full spec for an entire page at once, not element by element
- All four walk-through approaches (A-D) are presented to user; A (Role-first) is default
- Research agents dispatch in parallel during Round 1; main thread does not block on them
