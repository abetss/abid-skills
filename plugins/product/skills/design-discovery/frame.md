# Round 1: Frame

## Goal

Get everyone on the same page about what we're designing, for whom, and within what constraints. Establish the team, choose the walk-through approach, and dispatch research agents -- before any design work begins.

## Prerequisites

Requirements must exist. Check for `requirements.md` (or equivalent) in the work folder or provided by the user.

If no requirements exist:
> "We need requirements before starting design discovery. Use the `write-requirements` skill first, or provide a requirements document."

Stop here until requirements are provided.

## Step 1: Read Requirements

Read `requirements.md` and extract:
- **Problem statement**: What user problem are we solving?
- **Acceptance criteria**: Number each one (AC-1, AC-2, ...). These become the coverage checklist tracked through all rounds.
- **Roles involved**: Which user roles interact with this feature?
- **Scope boundaries**: What's explicitly in scope and out of scope?

Present a summary to the user for confirmation:

```
Lead Product Manager: "Here's what I understand from the requirements:

  Problem: [one sentence]
  Roles: [list]
  Scope: [in] / [out]

  I extracted [N] acceptance criteria:
    AC-1: [criterion]
    AC-2: [criterion]
    ...

  Does this capture the brief correctly?"
```

Wait for user to confirm or correct.

## Step 2: Read Memory

Read `memory.md` in this skill directory. Scan for:
- Previous discovery sessions for the same product area
- Patterns or decisions that should carry forward
- Mistakes to avoid

If relevant entries exist, mention them to the team:
> "From a previous session: [learning]. Keeping this in mind."

## Step 3: Assess Team Composition

The core team is always present:
- **Lead Product Manager** -- owns requirements coverage and business rules
- **Lead Designer** -- owns interaction design, states, accessibility

Assess whether optional team members are needed:

```
Lead Designer: "Before we start -- let me check if we need additional expertise:
  - Complex interaction patterns (tables, forms, drag-drop)? → Accessibility Specialist
  - New user personas or behavioral research? → UX Researcher
  - New or complex data model? → Data Architect
  - Significant copy, onboarding, or error messaging? → Content Strategist

  For this feature, I'd recommend adding: [list or none].
  What do you think?"
```

Read `perspectives.md` for full team member definitions. User confirms the team.

## Step 4: Dispatch Research Agents

Based on what exists, dispatch agents in the background. Read `research-agents.md` for dispatch templates.

**Schema Reader** -- dispatch if a database schema exists for this feature area.

**Feature Scout(s)** -- dispatch one or more in parallel:
- One to screenshot the current feature (if it exists in the app)
- One to read `a-kb/product-guide/` and `a-kb/` for domain context
- Additional scouts for analogous features if the team identifies them

Agents run in the background. Don't wait for results -- proceed to Step 5. Results will be available by Round 2.

## Step 5: Choose Walk-Through Approach

Present the four approaches. Default to A (Role-first):

```
"How should we walk through this feature? I recommend A for this product.

  A. Role-first (recommended) -- Start with roles, enumerate pages per role,
     then states, flows, interactions for each.
     First step: 'Let's list every role that touches this feature.'

  B. Page-first -- Start with pages, overlay role differences.
     First step: 'Let's list every page/screen in this feature.'

  C. Hybrid -- Quick role inventory, then page-by-page with role annotations.
     First step: 'Quick role list, then we go page by page.'

  D. Flow-first -- Start with the happy path, branch to variations.
     First step: 'Let's trace the primary user journey start to finish.'

  Which approach?"
```

Lock in the chosen approach:
> "You chose: [X]. Our path is locked in. Proceeding to Round 2."

## Step 6: Initialize Session

Create the progress file in the work folder:

```markdown
# Design Discovery Progress

**Feature**: [name from requirements]
**Date started**: [date]
**Approach**: [A/B/C/D]
**Team**: [list of active team members]

## Requirements
[AC checklist from Step 1]

## Progress
- [x] Round 1: Frame -- complete
- [ ] Round 2: Discovery Walk-through
  - [ ] Level 1: Roles
  - [ ] Level 2: Pages
  - [ ] Level 3: States
  - [ ] Level 4: Flows
  - [ ] Level 5: Interactions + Accessibility
- [ ] Round 3: Design
- [ ] Round 4: Specify

## Research Agents
- Schema Reader: [dispatched/not needed]
- Feature Scout(s): [dispatched N agents/not needed]
```

Write this to `{work-folder}/design-discovery-progress.md`.

## Gate

Round 1 is complete when:
1. Requirements are read and acceptance criteria extracted
2. User confirmed the brief summary
3. Team composition is decided
4. Research agents are dispatched (or noted as not needed)
5. Walk-through approach is chosen
6. Progress file is initialized

Proceed to Round 2: read `discover.md`.
