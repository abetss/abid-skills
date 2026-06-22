# Discovery Phase -- Product Manager Section

> This section defines what the Product lead does during Rounds 1-3 of design-discovery.
> It runs BEFORE any visual design. Its output feeds into `ui-design-iterate-storybook` or `ui-ascii-design`.

---

## Prerequisites

Before starting discovery, Product MUST have:

1. **A requirements document.** If `requirements.md` does not exist, stop and say:
   > "I need requirements before starting design discovery. Use the `write-requirements` command first, or provide a requirements document."
2. **A work folder** for this feature (e.g., `work/feature-name/`). All discovery artifacts go here.

---

## Round 1: Frame (Product Leads)

### 1.1 Parse Requirements into a Working Checklist

Read `requirements.md` and extract every acceptance criterion into a numbered checklist. This checklist is the source of truth for coverage validation throughout the entire process.

**Format the checklist in the work folder as `acceptance-criteria.md`:**

```markdown
# Acceptance Criteria Checklist

Source: [path to requirements.md]

## Functional Requirements
- [ ] AC-1: [Exact text from requirements]
- [ ] AC-2: [Exact text from requirements]
...

## Non-Functional Requirements
- [ ] NF-1: [Performance, compliance, accessibility requirements]
...

## Implicit Requirements (discovered during framing)
- [ ] IR-1: [Requirement that is implied but not stated -- added during discovery]
...
```

Rules for parsing:
- Every "should", "must", "when...then" statement becomes a numbered AC.
- If requirements use user stories, extract the acceptance criteria from each story.
- If requirements are informal (Slack messages, meeting notes), rewrite them as testable ACs and get user confirmation.
- Flag any AC that is ambiguous or contradictory. Present these to the user immediately -- do not guess.

### 1.2 Present the Problem Frame

Summarize what you learned from requirements in this structure:

```
PROBLEM FRAME
=============
Feature:      [Name]
Core problem:  [One sentence: what user pain does this solve?]
Success looks like: [Observable outcome when this feature works]

Roles involved: [List every role that touches this feature]
Primary role:   [The role whose workflow this feature primarily serves]

Scope boundary: [What is explicitly OUT of scope per requirements]

Compliance:     [Any regulatory constraints: PIPEDA, labor law, WCAG, etc.]
```

**What to look for when framing:**
- Requirements that mention permissions or "only X can" -- these define roles
- Requirements that mention data from other systems -- these define integration boundaries
- Requirements that mention time-based rules (deadlines, expiry, pay periods) -- these create lifecycle states
- Requirements that mention "if...then" conditions -- these are business rules to track

### 1.3 Assess Team Composition

Present the team composition question to Designer and User:

| Question | If Yes, Add |
|----------|-------------|
| Complex user personas or behavioral research needed? | UX Researcher |
| Complex keyboard/screen-reader interactions? (tables, forms, drag-drop, multi-step) | Accessibility Specialist |
| New data model or cross-service data? | Data Architect |
| Significant copy, onboarding, or error messaging? | Content Strategist |

### 1.4 Dispatch Research Agents

While the user reviews the problem frame, dispatch research agents in parallel:

| Agent | Dispatch when | Returns |
|-------|--------------|---------|
| **Schema reader** | DB/API schema exists | Fields, relationships, enums, nullable columns, constraints |
| **Code reader** | Existing UI exists | Current component tree, data shapes, patterns already in use |
| **Doc reader** | Product docs exist beyond requirements | Additional context, previous decisions, related feature docs |
| **Pattern finder** | Similar features exist in codebase | Analogous patterns, conventions already established |

Each agent writes its findings to the work folder (e.g., `research/schema-findings.md`). The main thread does NOT block on these -- it continues with framing while agents work.

**Gate: Round 1 passes when** the user confirms: problem understood, team composed, scope agreed, no ambiguous ACs remaining.

---

## Round 2: Approach Selection (Product Presents)

Present the discovery approach options. Recommend A unless you have reason not to.

```
How should we walk through this feature?

  A. Role-first (recommended)
     Roles -> pages per role -> states -> flows -> interactions -> accessibility
     Best for: permission-heavy features, multi-role workflows

  B. Page-first
     Pages -> overlay role differences -> states -> flows
     Best for: features where most content is shared across roles

  C. Hybrid
     Quick role inventory, then page-by-page with role annotations
     Best for: moderate role differences, many pages

  D. Flow-first
     Happy path first, branch to edge cases and other roles
     Best for: linear workflows, single-role features, quick exploration
```

The user picks. The choice determines the walk-through order in Round 3.

---

## Round 3: Discovery Walk-through (Product + Designer, Iterative)

This is the core of discovery. Product's job at each level of the hierarchy is to ensure **business completeness** -- that every requirement, edge case, and business rule is surfaced and documented.

### Product's Role at Each Level

Product does NOT design. Product ensures the designer has everything needed to design correctly.

---

### Level 1: Roles

**Product proposes:**

```
ROLE INVENTORY
==============
Role: [Name]
  Goal: [What this role is trying to accomplish]
  Permissions: [What they can see and do]
  Frequency: [How often they use this feature -- daily? weekly? once?]
  Input method: [Desktop only? Mobile? Assistive technology?]

Role: [Name]
  ...
```

**What Product checks:**
- Every role mentioned in requirements is listed
- Roles that are implied but not stated (e.g., "admin" is often implicit)
- Roles that interact indirectly (e.g., a person whose data appears but who may not use the feature)
- Cross-role interactions: when Role A acts, what does Role B see change?

**What Product documents in `conventions.md`:**
- Permission rules: "[Role] can/cannot [action]"
- Visibility rules: "[Role] sees/does not see [data]"
- Cross-role constraints: "When [Role A] does [X], [Role B]'s view updates to show [Y]"

---

### Level 2: Pages

**Product proposes (per role, or per page depending on approach):**

```
PAGE INVENTORY FOR [ROLE]
=========================
Page: [Name]
  Purpose: [What the user accomplishes here]
  Entry points: [How the user gets here]
  Key data: [What data is displayed]
  Key actions: [What the user can do]
  Requirements covered: [AC-1, AC-3, AC-7]
```

**What Product checks:**
- Every AC maps to at least one page. If an AC has no page, something is missing.
- Entry points are complete: can the user get here from every place they need to?
- No orphan pages: every page is reachable from somewhere.
- Navigation context: does the user know where they are and how to get back?

**What Product documents in `conventions.md`:**
- Page-level business rules: "This page is only visible when [condition]"
- Data scoping rules: "[Role] sees only their own [data], [Other role] sees all [data]"

---

### Level 3: States (Per Page)

This is where Product adds the most value. Designers think about visual states. Product ensures every BUSINESS state is accounted for.

**Product proposes the systematic state inventory:**

For EVERY page, walk through this checklist. Not every state applies to every page, but every state must be explicitly considered and either included or marked N/A with a reason.

```
STATE INVENTORY FOR [PAGE]
==========================

Data states:
  [ ] Empty (first-time ever -- no data has ever existed)
  [ ] Empty (filtered -- data exists but current filter shows none)
  [ ] Empty (permission -- data exists but this role cannot see it)
  [ ] Single item
  [ ] Typical (representative sample)
  [ ] Full/maximum (pagination threshold, performance boundary)
  [ ] Stale (data exists but is outdated -- last sync was [when])

Loading states:
  [ ] Initial load (skeleton/spinner)
  [ ] Refresh (data visible, updating in background)
  [ ] Partial load (some sections loaded, others pending)
  [ ] Optimistic update (action taken, server not yet confirmed)

Error states:
  [ ] Network error (offline, timeout)
  [ ] Server error (500, unexpected)
  [ ] Validation error (user input rejected)
  [ ] Conflict error (another user modified this data)
  [ ] Rate limit error (too many requests)

Permission states:
  [ ] Authorized (normal)
  [ ] Read-only (can see but not act)
  [ ] Denied (cannot see this page at all -- redirect or message?)
  [ ] Degraded (partial permissions -- can see some actions but not others)
  [ ] Expired session (was authorized, session timed out mid-action)

Lifecycle states (if the data has a workflow):
  [ ] Draft
  [ ] Submitted / Pending review
  [ ] Approved
  [ ] Rejected (with reason)
  [ ] Expired / Archived
  [ ] [Other states specific to this domain]

Temporal states:
  [ ] Before deadline (normal operation)
  [ ] Near deadline (warning threshold)
  [ ] Past deadline (locked? degraded? different actions available?)
  [ ] Outside business hours (if relevant)
```

**What Product checks:**
- Every "when" and "if" in the requirements maps to a state
- The distinction between similar-sounding states is clear (empty-first-time vs. empty-filtered is a common one)
- Impossible state combinations are identified and documented

**What Product documents in `conventions.md`:**

```markdown
## Impossible States
- [Page] cannot be in [State A] and [State B] simultaneously because [reason]
- [Data] cannot be [value] when [condition] because [business rule]

## State Transition Rules
- [State A] -> [State B]: triggered by [action], only when [condition], by [role]
- [State B] -> [State A]: NOT ALLOWED because [reason]
```

---

### Level 4: Flows

**Product proposes flow maps as structured text (NOT Graphviz -- it wastes tokens and Claude cannot render it):**

```
FLOW: [Name] (e.g., "Timesheet Submission")
=============================================
Actor: [Role]
Precondition: [What must be true before this flow starts]

1. [State A] -- user sees [description]
   -> Action: [what user does]
   -> Success: go to step 2
   -> Failure: [error state] -- user sees [description]
   -> Permission check: [who can trigger this]

2. [State B] -- user sees [description]
   -> Action: [what user does]
   ...

Cross-role effect:
  When Actor completes step [N], [Other Role] sees [change] on [their page]

Undo/recovery:
  Step [N] is reversible by [action] within [time window]
  Step [M] is NOT reversible because [reason]
```

**What Product checks:**
- Every flow has an error path, not just a happy path
- Every destructive action has a recovery mechanism (undo toast, edit, revert)
- Cross-role effects are documented: "when A submits, B's dashboard updates"
- Concurrent modification: what if two users act on the same data simultaneously?
- Fatigue analysis for multi-step flows: count total interactions, identify where auto-save or batch operations reduce effort

**What Product documents in `conventions.md`:**
- Flow-level business rules: "[Action] can only be performed when [condition]"
- Timing constraints: "[Action] must happen within [time] of [trigger]"
- Batch rules: "Can [action] be performed on multiple items? How many at once?"

---

### Level 5: Interactions

Product's role at this level is lighter -- Designer leads interaction design. But Product validates:

**What Product checks:**
- Every destructive action (delete, submit, approve, reject) has been identified
- Each destructive action has a defined recovery mechanism
- Actions that affect other users are identified (and those users are notified how?)
- Keyboard-only operability is possible for every action (no hover-dependent functionality)
- No timed interactions that could exclude users with motor disabilities

**What Product documents in `conventions.md`:**
- Destructive action inventory with recovery mechanisms
- Notification rules: "When [action], notify [role] via [channel]"

---

### Level 6: Accessibility

Product's role here is compliance and requirements validation, not design:

**What Product checks:**
- WCAG level required by the project (typically AA)
- Any regulatory accessibility requirements (ADA, Section 508, EN 301 549)
- User population characteristics: are assistive technology users expected? (switch access, screen readers, voice control)
- Interaction modality feasibility: can every flow be completed with keyboard only? With voice only? With switch access?

**What Product documents in `conventions.md`:**
- Accessibility requirements tier: "This feature must meet [WCAG AA / AAA / custom standard]"
- Known assistive technology requirements: "[User group] uses [technology]"

---

## Product Artifacts

By the end of Round 3, Product has produced or contributed to these files in the work folder:

### 1. `acceptance-criteria.md` (created in Round 1, updated throughout)

The numbered checklist of every AC. Updated during discovery as implicit requirements are found.

### 2. `conventions.md` (built incrementally during Round 3)

Complete format:

```markdown
# Conventions -- [Feature Name]

## Roles and Permissions
- [Role]: can [actions], sees [data]
- [Cross-role rule]

## Business Rules
- [Rule name]: [Description]
  - Applies to: [pages/flows]
  - Source: AC-[N] / discovered during [round]

## Impossible States
- [State combination that cannot exist] because [reason]

## State Transition Rules
- [From] -> [To]: triggered by [action], by [role], when [condition]
- [From] -> [To]: NOT ALLOWED because [reason]

## Display Rules
- [Data condition] -> display as [format]
- [Null/empty] -> show [fallback]

## Timing and Lifecycle Rules
- [Deadline/expiry rule]
- [Batch operation rule]

## Destructive Actions and Recovery
- [Action]: recovery via [mechanism] within [window]
- [Action]: NOT recoverable because [reason]

## Compliance
- [Regulatory requirement]: addressed by [design decision]

## Domain Assumptions (Validated)
- [Assumption] -- confirmed by user (Round [N])
- [Assumption] -- CORRECTED: actually [correction] (Round [N])
```

### 3. `state-inventory.md` (produced during Level 3)

```markdown
# State Inventory -- [Feature Name]

## [Page Name]

### Data States
| State | Applies? | Description | AC Coverage |
|-------|----------|-------------|-------------|
| Empty (first-time) | Yes | No timesheets ever created | AC-4 |
| Empty (filtered) | Yes | Timesheets exist but date filter shows none | AC-12 |
| ... | | | |

### Loading States
| State | Applies? | Description | AC Coverage |
|-------|----------|-------------|-------------|
| Initial load | Yes | Skeleton while fetching | NF-2 |
| ... | | | |

[Repeat for Error, Permission, Lifecycle, Temporal states]

## [Next Page]
...
```

### 4. `flow-maps.md` (produced during Level 4)

Structured text flow maps as described in Level 4 above. One flow per major user journey.

### 5. `coverage-matrix.md` (produced at the end of Round 3)

This is the final validation artifact. Every AC must map to at least one design artifact.

```markdown
# Coverage Matrix -- [Feature Name]

| AC | Description | Covered By | State/Flow/Page | Status |
|----|-------------|------------|-----------------|--------|
| AC-1 | User can submit timesheet | flow-maps.md: Timesheet Submission | Submission flow, step 3 | Covered |
| AC-2 | Manager sees pending approvals | state-inventory.md: Dashboard | Populated state, manager role | Covered |
| AC-3 | Rejected timesheets show reason | state-inventory.md: Timesheet Detail | Rejected lifecycle state | Covered |
| NF-1 | Page loads in under 2s | state-inventory.md: All pages | Loading states | Covered |
| IR-1 | Concurrent edit conflict | state-inventory.md: Edit page | Conflict error state | Covered |
```

**Coverage rules:**
- Every AC-N must appear in the matrix with status "Covered"
- If an AC cannot be covered by design artifacts alone (e.g., a backend performance requirement), mark it "Out of scope -- engineering" and note why
- If an AC is ambiguous and the user has not clarified, mark it "Blocked -- needs clarification" and flag it

---

## Gate: Round 3 Complete

Round 3 is complete when ALL of the following are true:

1. **State inventory is exhaustive:** Every page has been walked through the full state checklist. Every state is either included with a description or explicitly marked N/A with a reason.

2. **Flows cover all user journeys:** Every multi-step interaction has a flow map with happy path, error paths, cross-role effects, and recovery mechanisms.

3. **Coverage matrix has no gaps:** Every AC maps to at least one artifact. No "Blocked" items remain.

4. **Conventions doc is complete:** All business rules, impossible states, display rules, and domain assumptions are documented and validated with the user.

5. **User confirms:** "Nothing is missing."

Only then does the process advance to Round 4 (Design), where the Designer takes the lead and uses these artifacts to produce visual designs.

---

## How Product Interacts with Designer During Discovery

Product and Designer are peers, not a handoff. During Round 3:

- **Product proposes business states and rules.** Designer challenges whether they matter visually ("that distinction doesn't need a different UI state") or identifies states Product missed ("what about the first-time-ever empty state?").

- **Product validates Designer's proposals against requirements.** When Designer proposes a layout or interaction, Product checks: "Does this cover AC-7? I don't see how [edge case] is handled."

- **When they disagree, they present both perspectives to the user with trade-offs.** Neither overrides the other. Example:
  - Product: "We need a confirm dialog for this destructive action per AC-15."
  - Designer: "A confirm dialog adds friction. An undo toast for 10 seconds is more accessible for switch users and less disruptive."
  - User decides.

- **Product catches scope creep.** If Designer proposes features not in requirements, Product flags it: "That's not in scope. Should we add it as a new AC, or save it for later?"

- **Product catches missing coverage.** If the team moves to the next level without covering an AC, Product stops the conversation: "We haven't addressed AC-11 yet. Which page/state/flow covers [requirement]?"
