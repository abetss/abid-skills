# Discovery Phase (Rounds 1-3)

This phase runs BEFORE any visual design. Its job is to produce a complete discovery document that contains everything needed to confidently design every page, every state, every interaction. The output feeds into either `ui-design-iterate-storybook` (preferred) or `ui-ascii-design`.

**Nothing gets designed until this phase gates as complete.**

---

## Required Input

A `requirements.md` (or equivalent) must exist before discovery starts. If it does not:

> "I need requirements before starting design discovery. Use the `write-requirements` skill first, or provide a requirements document."

Parse the requirements immediately for: acceptance criteria (as checklist), mentioned roles, mentioned pages/screens, stated business rules, compliance constraints (PIPEDA, labor law).

---

## Round 1: Frame the Problem

**Product leads. Designer asks about users and constraints.**

Product synthesizes from requirements:
1. Who are the users? (roles, goals, primary input methods)
2. What problem does this feature solve?
3. What does success look like? (measurable criteria)
4. What compliance rules apply? (data display, privacy, labor law)

Designer asks:
1. What input methods will these users rely on? (keyboard-only, switch access, eye gaze, voice control, standard mouse/touch)
2. Are there multi-step flows where fatigue is a concern?
3. Do any interactions involve time pressure, drag-and-drop, or hover-dependent functionality?

Jointly assess whether optional team members are needed:

| Question | If Yes, Add |
|----------|-------------|
| Complex user personas or behavioral research? | UX Researcher |
| Complex keyboard/screen-reader interactions? (tables, forms, drag-drop, multi-step) | Accessibility Specialist |
| New data model or crosses multiple services? | Data Architect |
| Significant copy, onboarding, or error messaging needs? | Content Strategist |

Present the team recommendation to the user. User confirms or adjusts.

**Dispatch research agents in parallel:**
- Schema reader (if DB/API exists) -- fields, relationships, enums, nullable columns
- Code reader (if existing UI exists) -- current components, data shapes, patterns
- Doc reader (if requirements/product docs exist) -- all mentioned states, events, rules
- Pattern finder (if analogous features exist in codebase) -- conventions to follow or break

**Gate:** Problem understood, team composed, scope agreed, research agents dispatched.

---

## Round 2: Choose the Walk-through Approach

Present all four options. Recommend A unless the user's feature clearly fits another.

> "How should we walk through this feature?"
>
> **A. Role-first** (recommended) -- Roles -> Pages per role -> States -> Flows -> Interactions -> Accessibility
> Best for: permission-heavy features, multi-role workflows
>
> **B. Page-first** -- Pages -> Role overlay -> States -> Flows -> Interactions -> Accessibility
> Best for: features where most content is shared across roles
>
> **C. Hybrid** -- Quick role inventory, then page-by-page with role annotations
> Best for: moderate role differences, avoids repetition
>
> **D. Flow-first** -- Happy path first, then branch to edge cases and other roles
> Best for: features centered on a single workflow (e.g., form submission, approval chain)

User picks. The walk-through in Round 3 follows the chosen approach, but all six hierarchy levels are always covered regardless of entry point.

**Gate:** Approach selected.

---

## Round 3: Discovery Walk-through

This is the core of the process. The team walks through six levels of the hierarchy. At EVERY level:

1. **Product proposes** based on requirements and research findings
2. **Designer proposes** based on UX patterns and accessibility constraints
3. **Agents disagree productively** -- each catches the other's blind spots
4. **User corrects** -- every correction is a rule discovery; write it down immediately
5. **Document before moving on** -- nothing advances to the next level undocumented

### The "Propose and Get Corrected" Method

At each level, do NOT ask open-ended questions like "what roles exist?" or "what states does this page have?" Instead:

1. **Propose a concrete, specific answer** -- even if you suspect it is wrong
2. **Present it to the user as a draft** -- "Here is what I think. What did I get wrong?"
3. **Record every correction** -- corrections ARE the discovery. Each one is a business rule, a constraint, or a domain fact
4. **Re-propose with corrections applied** -- iterate until the user says "that's right"

Wrong proposals are intentional and valuable. "We don't have a rejection state" teaches you more than "what states exist?" ever would.

---

### Level 1: Roles

**What to discover:**
- Every role that interacts with this feature (including system/automated actors)
- Each role's primary goal when using this feature
- Each role's likely input methods (keyboard, switch, eye gaze, voice, mouse/touch)
- Permission boundaries between roles (what each can see, what each can do)
- Whether any role acts on behalf of another (e.g., representative managing for person with disability)

**How to propose:**

Product proposes:
```
"The roles involved are:
  1. [Role A] -- goal: [X]. Can see: [Y]. Can do: [Z].
  2. [Role B] -- goal: [X]. Can see: [Y]. Can do: [Z].
  3. System -- triggers [automated actions] when [conditions]."
```

Designer proposes:
```
"For accessibility, I expect:
  - [Role A] primarily uses [input method]. Fatigue concern: [yes/no].
  - [Role B] primarily uses [input method]. Switch access likely: [yes/no]."
```

User corrects. Record every correction in the discovery document.

**What to document:**

```markdown
## Roles

### [Role Name]
- **Goal:** [What they are trying to accomplish]
- **Can see:** [What data/pages they have access to]
- **Can do:** [What actions they can perform]
- **Input methods:** [Primary input methods for this user population]
- **Fatigue concern:** [Yes/No -- if yes, note which flows are multi-step]
- **Acts on behalf of:** [Another role, if applicable]
```

**Do not advance to Level 2 until every role is documented and user confirms the list is complete.**

---

### Level 2: Pages

**What to discover:**
- Every page/screen in this feature (including pages only one role sees)
- What each page does (primary purpose, not layout yet)
- Which roles see each page (role-page matrix)
- What differs per role on shared pages (data visible, actions available, sections shown/hidden)
- Page-to-page navigation (how users get to each page and where they go next)

**How to propose (approach varies by chosen method):**

For **Role-first (A):** Walk through one role at a time.
```
Product:  "[Role A] needs these pages: [list]. Here's what each does."
Designer: "I'd also expect a [page] because [reason]. This other page might
           not be needed because [reason]."
User:     [Corrects]
```

For **Page-first (B):** List all pages, then annotate roles.
```
Product:  "The feature has these pages: [list]."
Designer: "For each page, which roles see it? What changes per role?"
User:     [Corrects]
```

For **Hybrid (C):** Role inventory is done, now page-by-page with role annotations.

For **Flow-first (D):** Pages emerge from the flow -- "this step happens on [page]."

**What to document:**

```markdown
## Pages

### [Page Name]
- **Purpose:** [What the user accomplishes here]
- **Roles with access:** [List]
- **Role differences:**
  - [Role A]: sees [X], can do [Y]
  - [Role B]: sees [X], can do [Y] (cannot see [Z])
- **Navigation:**
  - Reached from: [page/action]
  - Leads to: [page/action]
```

Also produce the **Role-Page Matrix** (even for non-role-first approaches):

```markdown
## Role-Page Matrix

| Page | Role A | Role B | Role C |
|------|--------|--------|--------|
| Dashboard | View + Edit | View only | No access |
| Detail | View + Approve | View + Submit | No access |
| Settings | Full access | No access | Full access |
```

**Do not advance to Level 3 until every page is documented, the role-page matrix is confirmed, and user says the list is complete.**

---

### Level 3: States (per page)

**What to discover:**

For EVERY page, systematically enumerate these state categories:

| State Category | Description | Always Check |
|---------------|-------------|--------------|
| **Default/Populated** | Normal state with data | What does the typical view look like? |
| **Loading** | Data is being fetched | Skeleton? Spinner? What's shown? |
| **Empty (first-time)** | No data has ever existed | Onboarding message? CTA? |
| **Empty (filtered)** | Data exists but filters exclude it | Different message than first-time empty |
| **Error (network)** | Request failed | Retry affordance? Cached data shown? |
| **Error (validation)** | User input is invalid | Inline errors? Summary? |
| **Error (server)** | Server returned business error | Specific message per error type? |
| **Permission denied** | Role lacks access | Redirect? Inline message? |
| **Degraded** | Partial data loaded, partial failed | What's shown vs hidden? |
| **Stale** | Data may be outdated | Indicator? Auto-refresh? |
| **Offline** | No network connection | What's available offline? |
| **First-use / Onboarding** | User has never seen this feature | Tutorial? Reduced UI? |
| **Busy / Optimistic** | Action submitted, awaiting confirmation | Disabled buttons? Optimistic update? |

Not every page will have every state. But you MUST explicitly consider each one and document whether it applies or not. "Not applicable" is a valid answer -- it prevents future ambiguity.

**How to propose:**

Designer proposes the full state list for a page:
```
Designer: "For [page], I think these states exist:
  - Default: [description]
  - Loading: skeleton with [X] placeholder shapes
  - Empty (first-time): message says '[Y]', CTA to [action]
  - Empty (filtered): message says 'No results match your filters', CTA to clear filters
  - Error: [description], retry button
  - Permission denied: [not applicable -- all roles access this page]"

Product: "Missing: when [business rule], there's a [special state] where
          [data is partially locked]. Also, the empty state differs for
          [Role A] vs [Role B] -- [Role A] sees a CTA to create, [Role B]
          sees a message that [Role A] hasn't created anything yet."
```

User corrects. Each correction is a business rule.

**What to document:**

```markdown
## States: [Page Name]

### Default (Populated)
- **Description:** [What the user sees with normal data]
- **Role variations:** [Differences per role, if any]
- **Data requirements:** [What must be present for this state]

### Loading
- **Pattern:** [Skeleton / spinner / progressive]
- **Duration expectation:** [Fast <500ms / medium 1-3s / slow 3s+]
- **What's shown:** [Skeleton shapes matching default layout]

### Empty (First-Time)
- **Headline:** "[Exact copy]"
- **Body:** "[Exact copy]"
- **CTA:** [Button text] -> [action]
- **Role variations:**
  - [Role A]: sees CTA to create
  - [Role B]: sees "[Role A] hasn't created any [items] yet"

### Empty (Filtered)
- **Message:** "[Exact copy]"
- **CTA:** "Clear filters" -> resets to default view

### Error
- **Network error:** [Message, retry affordance]
- **Business error [type]:** [Specific message]
- **Recovery:** [How the user gets back to a good state]

### [Business-Specific State: e.g., "Locked for Payroll"]
- **Trigger:** [What causes this state]
- **Appearance:** [How it differs from default]
- **Available actions:** [What the user can still do]
- **Exit condition:** [When/how this state ends]

### States NOT applicable to this page:
- Permission denied: [reason -- e.g., all roles have access]
- Offline: [reason -- e.g., feature requires real-time data]
```

**Content decisions happen HERE, not in visual design.** Empty state copy, error messages, button labels, tooltips -- all are documented at this level. If a Content Strategist is on the team, they lead these decisions.

**Do not advance to Level 4 until every page has its state inventory confirmed by the user.**

---

### Level 4: Flows (between states and between pages)

**What to discover:**
- Every state transition: what triggers it, who can trigger it, what happens on success, what happens on failure
- Multi-step workflows: the full sequence from start to end, with every branching point
- Cross-role effects: when one role acts, what changes for another role's view
- Lifecycle flows: entity state machines (e.g., draft -> submitted -> approved -> paid)
- Error recovery: for every failure, how does the user get back on track
- Destructive actions: what can be undone, how, and for how long

**How to propose:**

Designer proposes the flow:
```
Designer: "The approval flow is:
  1. [Role A] opens timesheet (Default state)
  2. [Role A] clicks 'Submit' -> Busy state (button disabled, spinner)
  3. Success -> transitions to 'Submitted' state (read-only view, status badge)
  4. Failure -> Error state (inline error, Submit button re-enabled)
  5. [Role B] sees notification, opens timesheet in 'Pending Approval' state
  6. [Role B] clicks 'Approve' -> Busy -> 'Approved' state
  7. [Role A] sees status update to 'Approved'"

Product: "Missing: what if [Role B] clicks 'Request Changes'? The timesheet
          goes back to [Role A] in an 'Amendments Requested' state with
          [Role B]'s comments attached. Also, [Role A] can withdraw the
          submission before [Role B] acts."
```

User corrects transitions and adds constraints.

**What to document:**

For simple flows (single action):
```markdown
## Flow: [Action Name] (e.g., "Submit Timesheet")

- **Trigger:** [User action -- e.g., clicks Submit button]
- **Who can trigger:** [Roles]
- **Preconditions:** [What must be true -- e.g., all required fields filled]
- **On trigger:** [Immediate UI feedback -- e.g., button disabled, spinner shown]
- **On success:** [New state -- e.g., read-only view, status badge "Submitted"]
- **On failure:** [Error state -- e.g., inline error, button re-enabled]
- **Cross-role effect:** [What changes for other roles -- e.g., notification appears]
- **Undo:** [Can this be undone? How? Time limit?]
```

For lifecycle flows (multi-step):
```markdown
## Lifecycle: [Entity] (e.g., "Timesheet")

| State | Who sees it | Available actions | Next states |
|-------|------------|-------------------|-------------|
| Draft | Role A | Edit, Delete, Submit | Submitted |
| Submitted | Role A (read-only), Role B (actionable) | Approve, Request Changes, (Role A: Withdraw) | Approved, Amendments Requested, Draft |
| Amendments Requested | Role A (editable + comments) | Edit, Resubmit | Submitted |
| Approved | Both (read-only) | -- | Paid (system) |
| Paid | Both (read-only) | -- | -- |
```

For destructive actions:
```markdown
## Destructive Actions

| Action | Undo mechanism | Time limit | Accessibility note |
|--------|---------------|------------|-------------------|
| Delete draft | Undo toast | 10 seconds | Toast auto-focuses, Enter to undo |
| Withdraw submission | Confirmation with single-action undo | Immediate | No confirm dialog (switch user hostile); use undo toast instead |
```

**Fatigue analysis for multi-step flows:**
```markdown
## Fatigue Analysis: [Flow Name]

- **Total steps:** [N]
- **Total interactions (clicks/keypresses):** [N]
- **Auto-save:** [Yes/No -- required if > 5 steps or > 3 minutes expected duration]
- **Batch operations:** [Can multiple items be processed at once?]
- **Progress indicator:** [Yes/No -- required if > 3 steps]
- **Early exit:** [Can the user save and come back later?]
```

**Do not advance to Level 5 until all flows are documented and user confirms transitions are correct.**

---

### Level 5: Interactions (per element, per page)

**What to discover:**
- Every interactive element on every page (buttons, links, form fields, toggles, menus, tables)
- Per element: what happens on click, keyboard activation, focus, blur, hover (if any)
- Tab order within each page (the sequence a keyboard/switch user follows)
- Focus management: where focus moves after actions (submit, delete, modal open/close, error)
- Feedback: what the user sees/hears after each interaction (visual change, screen reader announcement, toast)
- Timing: no timed interactions; auto-save intervals; debounce on search/filter

**How to propose:**

Designer proposes per page, walking through elements in tab order:
```
Designer: "On the Timesheet Detail page, tab order is:
  1. Back link -> navigates to list
  2. Status badge (read-only, not focusable)
  3. Date range display (read-only)
  4. [For each time entry row]: hours input -> notes input -> delete button
  5. 'Add Row' button -> inserts new row, focus moves to new hours input
  6. 'Save Draft' button -> saves, shows success toast, focus stays
  7. 'Submit' button -> submits, transitions to Submitted state, focus moves to status badge

  Keyboard: Enter/Space activates all buttons. Escape closes any open dropdown.
  No hover-dependent functionality anywhere.
  Delete button: undo toast for 10 seconds (no confirm dialog)."

Product: "The hours input needs validation: max 24 per day, must be in
          0.25 increments. Error appears inline below the field."
```

User corrects.

**What to document:**

```markdown
## Interactions: [Page Name]

### Tab Order
1. [Element] -- [role if not obvious]
2. [Element]
3. [Repeating group: for each [item]]: [element] -> [element] -> [element]
4. [Element]

### Element Details

#### [Element Name] (e.g., "Submit Button")
- **Type:** button / link / input / select / toggle / etc.
- **Click/Activate:** [What happens]
- **Keyboard:** [Keys that activate -- e.g., Enter, Space]
- **Focus behavior:** [What happens when element receives focus]
- **After action:** [Where focus moves, what's announced]
- **Disabled when:** [Conditions]
- **Validation:** [Rules, error message copy, when validation runs]

#### [Element Name] (e.g., "Hours Input")
- **Type:** number input
- **Constraints:** min 0, max 24, step 0.25
- **Validation:** on blur; error message: "[exact copy]"
- **Error display:** inline below field, `role="alert"`
- **Auto-save:** triggers 2 seconds after last edit (no manual save needed for drafts)

### Feedback Patterns
- **Success actions:** undo toast, 10 second timeout, auto-focus toast on appear
- **Validation errors:** inline per field, summary at form top if > 3 errors
- **Destructive actions:** undo toast (NOT confirm dialog -- confirm dialogs are hostile to switch users)
- **Loading feedback:** button shows spinner, disabled during request
```

**Accessibility constraint reminders for interaction design:**
- No hover-dependent functionality. Tooltips on focus, not just hover.
- No timed interactions. If a toast has an undo action, the timer pauses on focus.
- Touch targets: 48px minimum, 60px for primary actions.
- No content shift after load (stable layouts). Reserve space for error messages.
- Undo over confirm dialogs (confirm dialogs require multiple precise interactions; undo requires one).

**Do not advance to Level 6 until every page has its interaction inventory confirmed by the user.**

---

### Level 6: Accessibility (per interaction, architectural)

**What to discover:**
- ARIA roles and patterns for each interactive component (combobox, dialog, tabpanel, grid, etc.)
- Keyboard patterns per component (arrow keys for tabs, Enter for buttons, Escape to close)
- Focus management plan (where focus goes after every state transition)
- Screen reader announcements (what's announced after actions, live regions)
- Switch access feasibility (can every flow be completed with a single switch?)
- Reduced motion behavior (what animations are removed or replaced)
- High contrast readiness (does the design rely on color alone for any meaning?)

This is NOT a verification checklist applied after design. This is **architectural input that shapes design decisions.** Every choice made in Levels 2-5 must be compatible with these constraints.

**How to propose:**

Designer proposes the accessibility contract per component:
```
Designer: "The Timesheet Table uses a grid pattern:
  - ARIA role: grid with row/gridcell
  - Keyboard: arrow keys navigate cells, Enter to edit, Escape to exit edit
  - Focus management: focus ring visible on active cell, 3px solid blue
  - Screen reader: announces cell coordinates and content on focus
  - Switch access: linear tab through cells in reading order (no 2D navigation required)
  - Reduced motion: no cell transition animations"

Accessibility Specialist (if present): "Switch users can't use arrow key
  navigation efficiently. Provide a linear tab-through mode as the DEFAULT,
  with arrow-key grid nav as an enhancement for keyboard power users."
```

User confirms.

**What to document:**

```markdown
## Accessibility Contracts

### Page-Level
- **Landmark structure:** [main, nav, complementary, etc.]
- **Heading hierarchy:** h1: [text], h2: [text], h3: [text]
- **Skip links:** [What skip links exist and where they go]
- **Page title pattern:** "[Page Name] - [Feature] - [App Name]"

### Component: [Name]
- **ARIA role:** [role]
- **ARIA attributes:** [aria-label, aria-describedby, aria-live, etc.]
- **Keyboard pattern:** [Full keyboard interaction spec]
- **Focus management:**
  - On open: focus moves to [target]
  - On close: focus returns to [trigger]
  - On action: focus moves to [target]
- **Screen reader announcements:**
  - On [action]: announces "[text]" via [aria-live="polite" / role="alert"]
- **Switch access mode:** [How a single-switch user completes this interaction]
- **Reduced motion:** [What changes when prefers-reduced-motion is active]
- **High contrast:** [Does this rely on color alone? If so, add icon/text indicator]

### Interaction Modality Matrix

| Flow | Mouse | Keyboard | Switch | Eye Gaze | Voice |
|------|-------|----------|--------|----------|-------|
| Submit timesheet | Click button | Enter/Space on focused button | Scan to button, activate | Dwell on button | "Click Submit" |
| Navigate table | Click cell | Arrow keys / Tab | Linear tab through cells | Dwell on cell | "Go to row 3" |
| Delete row | Click X | Enter/Space on focused X | Scan to X, activate | Dwell on X | "Click Delete" |
```

**Architectural accessibility rules (non-negotiable):**
1. No hover-dependent functionality
2. 48px minimum touch targets (60px for primary actions)
3. Complete keyboard operability for every flow
4. No timed interactions (timers pause on focus)
5. Stable layouts (no content shift after load; reserve space for dynamic content)
6. Forgiving interactions (undo over confirm dialogs)
7. Sequential navigation support (switch devices traverse in reading order)
8. `prefers-reduced-motion` support (no animation when set)
9. High contrast readiness (no meaning conveyed by color alone)
10. Error recovery over error prevention (let users make mistakes and fix them easily)

**Gate:** Complete Roles -> Pages -> States -> Flows -> Interactions -> Accessibility map documented. User confirms nothing is missing.

---

## Discovery Output Document

When all six levels are complete, the discovery document is assembled. This document is the **sole input** to visual design (Round 4). It must be complete enough that the designer never has to ask "what happens when...?" during design.

The document lives in the work folder and is structured as follows:

```
{work-folder}/
  discovery/
    discovery.md          # The main document (below)
    conventions.md        # Business rules, impossible states, display rules
    state-inventory.md    # All states per page per role
    flow-diagrams.md      # State transitions with triggers and actors
    coverage-checklist.md # Requirements ACs mapped to discovered artifacts
```

### discovery.md Structure

```markdown
# Design Discovery: [Feature Name]

## Meta
- **Date:** [date]
- **Requirements source:** [path to requirements.md]
- **Team:** [list of agents present]
- **Approach used:** [A/B/C/D]

---

## 1. Problem Frame
- **Users:** [roles and goals]
- **Problem:** [what this feature solves]
- **Success criteria:** [measurable]
- **Compliance:** [applicable regulations]
- **Accessibility context:** [input methods, fatigue concerns, special considerations]

---

## 2. Roles
[Full role documentation from Level 1]

---

## 3. Role-Page Matrix
[Matrix from Level 2]

---

## 4. Pages
[Full page documentation from Level 2, in the order a user would navigate them]

---

## 5. State Inventory
[Per page, every state from Level 3, including content/copy decisions]

---

## 6. Flows
[All flows from Level 4: simple flows, lifecycle flows, destructive actions, fatigue analysis]

---

## 7. Interactions
[Per page, tab order + element details + feedback patterns from Level 5]

---

## 8. Accessibility Contracts
[Per component contracts + interaction modality matrix from Level 6]

---

## 9. Conventions
[Link to conventions.md -- business rules, impossible states, display rules, domain assumptions]

---

## 10. Open Questions
[Anything unresolved -- these MUST be resolved before design begins]

---

## 11. Requirements Coverage
[Checklist: every AC from requirements.md mapped to a section in this document.
 Any AC not covered is flagged as a gap.]
```

### What the Design Phase Needs From This Document

The `ui-design-iterate-storybook` or `ui-ascii-design` skill will consume this document and needs to find:

1. **For layout decisions:** Roles (who), Pages (what), Role-Page Matrix (what differs), Information hierarchy within each page (from State Inventory default state)
2. **For component identification:** Interaction inventory per page (every interactive element), State inventory (what each component looks like in each state)
3. **For story creation:** State inventory (one story per state per page), Role variations (one story variant per role difference), Flow endpoints (before/after states for each transition)
4. **For responsive design:** The page purposes and information hierarchy (what's primary vs secondary, what can collapse)
5. **For accessibility implementation:** Accessibility contracts per component, Tab order per page, Focus management plan, ARIA patterns
6. **For content:** All copy decisions (empty states, errors, labels, tooltips, toasts) already made in this document

### Completeness Check Before Handoff

Before declaring discovery complete, verify:

- [ ] Every role from requirements is documented with goals and input methods
- [ ] Every page is documented with purpose, role access, and navigation
- [ ] Every page has a complete state inventory (all 13 categories addressed)
- [ ] Every state has its content/copy decided (not "TBD")
- [ ] Every state transition has a flow with trigger, success, failure, and cross-role effects
- [ ] Every destructive action has an undo mechanism documented
- [ ] Multi-step flows have fatigue analysis
- [ ] Every page has a tab order and interaction inventory
- [ ] Every interactive component has an accessibility contract
- [ ] The interaction modality matrix covers all primary flows
- [ ] Every acceptance criterion from requirements maps to a discovery section
- [ ] Open questions list is empty (all resolved)
- [ ] User has explicitly confirmed: "Discovery is complete, nothing is missing"
