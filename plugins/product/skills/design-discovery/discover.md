# Round 2: Discovery Walk-through

## Goal

Map the complete design surface -- every role, page, state, flow, and interaction -- through structured proposals that the user corrects. Wrong proposals surface hidden rules faster than open-ended questions. Every correction is a rule discovery; write it down immediately.

---

## Before Starting

Read `perspectives.md` for team voice definitions used in this round.

The walk-through approach was chosen in Round 1 (check the progress file). Follow that approach, but all five levels are always covered regardless of entry point.

If the user provides existing artifacts (role lists, state inventories, flow diagrams), review them quickly rather than re-derive from scratch -- touch on it and move on. Do not force re-discovery of work that is already done, but do not skip validation either.

---

## Level 1: Roles

**Goal:** Identify every actor that interacts with this feature, what they can see, what they can do, and how they interact.

**What to discover:**
- Every role that touches this feature (including system/automated actors)
- Each role's primary goal when using this feature
- Permission boundaries: what each role can see vs. do
- Input methods per role (keyboard, mouse/touch, switch access, eye gaze, voice)
- Whether any role acts on behalf of another
- Cross-role effects: when Role A acts, what changes for Role B
- Permission boundaries between role pairs: what happens when Role A accesses something intended for Role B (deep link sharing, cached vs. server permissions, role changes mid-session)

**How to propose:**

```
Product: "Based on requirements, the roles involved are:
  1. Manager -- goal: review and approve timesheets.
     Can see: all employee timesheets for their team.
     Can do: approve, reject, request changes.
  2. Employee -- goal: submit hours for pay.
     Can see: only their own timesheets.
     Can do: create, edit drafts, submit.
  3. System -- auto-locks timesheets 48 hours after pay period ends. [?]"

Designer: "For input methods, I expect:
  - Managers primarily use desktop (mouse + keyboard). Fatigue concern: yes,
    if approving 20+ timesheets in a batch.
  - Employees may use mobile or tablet on shift. Touch targets matter. [?]"

User: "You're missing the Representative role -- they manage timesheets
       on behalf of employees with disabilities. They have the same access
       as the employee they represent, plus a role switcher."
```

Every correction is recorded. The [?] marker flags items the team is deliberately uncertain about to invite correction.

**What to document (written to `discovery.md` under `## Roles`):**

```markdown
## Roles

### Manager
- **Goal:** Review and approve employee timesheets
- **Can see:** All timesheets for their direct reports
- **Can do:** Approve, reject, request changes
- **Input methods:** Desktop (mouse + keyboard)
- **Fatigue concern:** Yes -- batch approvals of 20+ timesheets
- **Acts on behalf of:** No

### Employee
- **Goal:** Submit hours for pay
- **Can see:** Only their own timesheets
- **Can do:** Create, edit drafts, submit
- **Input methods:** Desktop and mobile/tablet
- **Fatigue concern:** No
- **Acts on behalf of:** No

### Representative
- **Goal:** Manage timesheets on behalf of employee with disability
- **Can see:** Same as represented employee
- **Can do:** Same as represented employee + role switcher
- **Input methods:** Desktop; may use assistive technology
- **Fatigue concern:** Yes -- multi-step flows with switch access
- **Acts on behalf of:** Employee (specific represented person)
```

**Gate:** Write to disk. Team reviews: Product checks every role from requirements is listed; Designer checks input methods and fatigue concerns are documented. User reviews and confirms the list is complete. Do not advance until every role is documented.

<!-- SELF-CHECK: At least 2 roles expected for any feature with permissions. If only 1 role found, probe harder. -->

---

## Level 2: Pages

**Goal:** Identify every page/screen in this feature, what it does, which roles see it, and how users navigate between pages.

**What to discover:**
- Every page in the feature (including pages only one role sees)
- Primary purpose of each page (what the user accomplishes)
- Which roles see each page and what differs per role (data visible, actions available, sections shown/hidden)
- Page-to-page navigation: entry points and exits
- Pages implied by requirements but not obvious (settings, confirmation screens, edge-case-only pages)

**How to propose (varies by chosen approach):**

For Role-first (A) -- walk one role at a time:
```
Product: "For Manager, I think the pages are:
  1. Team Dashboard -- see all employee timesheets, filter by status/period
  2. Timesheet Detail -- review a single timesheet, approve/reject
  3. Bulk Approval [?] -- batch approve multiple timesheets at once

  For Employee:
  1. My Timesheets -- list their own timesheets by period
  2. Timesheet Entry -- fill in hours for a period
  3. Timesheet Detail -- read-only view after submission"

Designer: "I'd merge Bulk Approval into the Team Dashboard -- a selection
  mode with a floating action bar, rather than a separate page. Less
  navigation for a repetitive task."

User: "Correct on the merge. Also, Employees need a Timesheet Entry page
       that's different from the Detail page -- Entry is editable,
       Detail is read-only after submission."
```

For Page-first (B), Hybrid (C), or Flow-first (D), adjust the proposal order accordingly, but always produce the same output.

**What to document (written to `discovery.md` under `## Pages` and `## Role-Page Matrix`):**

```markdown
## Pages

### Team Dashboard
- **Purpose:** Manager reviews all employee timesheets for their team
- **Roles with access:** Manager
- **Key data:** Employee name, period, status, total hours
- **Key actions:** Filter, sort, select for bulk approval, open detail
- **Navigation:**
  - Reached from: main nav
  - Leads to: Timesheet Detail

### Timesheet Entry
- **Purpose:** Employee fills in hours for a pay period
- **Roles with access:** Employee, Representative
- **Role differences:**
  - Employee: edits own timesheet
  - Representative: edits on behalf of another, sees role-switcher banner
- **Navigation:**
  - Reached from: My Timesheets (create new or edit draft)
  - Leads to: My Timesheets (after save/submit)

## Role-Page Matrix

| Page | Manager | Employee | Representative | System |
|------|---------|----------|----------------|--------|
| Team Dashboard | View + Approve/Reject | No access | No access | -- |
| My Timesheets | No access | View + Create | View + Create (on behalf) | -- |
| Timesheet Entry | No access | Edit | Edit (on behalf) | -- |
| Timesheet Detail | View + Approve/Reject | View (read-only) | View (read-only, on behalf) | -- |
```

**Gate:** Write to disk. Team reviews: Product checks every acceptance criterion maps to at least one page (if an AC has no page, something is missing); Designer checks navigation is complete and no orphan pages exist. User reviews and confirms. Do not advance until every page is documented and the role-page matrix is confirmed.

<!-- SELF-CHECK: Expect at least 2-3 pages per feature. If only 1, the feature may be underscoped or a single-page app section. Verify. -->

---

## Level 3: States

**Goal:** For every page, systematically enumerate every visual and business state so that no "what happens when...?" question remains unanswered.

**What to discover:**

Walk through this checklist for EVERY page. Not every state applies, but every category must be explicitly considered. "Not applicable" is a valid answer -- it prevents future ambiguity.

### State Checklist (13 standard categories)

| # | Category | Question to answer |
|---|----------|-------------------|
| 1 | **Default / Populated** | What does the typical view look like with data? |
| 2 | **Loading** | Skeleton? Spinner? What is shown during fetch? |
| 3 | **Empty (first-time)** | No data has ever existed. Onboarding message? CTA? |
| 4 | **Empty (filtered)** | Data exists but filters exclude it. Different from first-time? |
| 5 | **Error (network)** | Request failed. Retry affordance? Cached data? |
| 6 | **Error (validation)** | User input invalid. Inline errors? Summary? |
| 7 | **Error (server/business)** | Server returned business error. Per-error-type message? |
| 8 | **Permission denied** | Role lacks access. Redirect? Inline message? |
| 9 | **Degraded** | Partial data loaded, partial failed. What is shown vs hidden? |
| 10 | **Stale** | Data may be outdated. Indicator? Auto-refresh? |
| 11 | **Offline** | No network. What is available offline? |
| 12 | **First-use / Onboarding** | User has never seen this feature. Tutorial? Reduced UI? |
| 13 | **Busy / Optimistic** | Action submitted, awaiting confirmation. Disabled buttons? Optimistic update? |

### Resilience States (8 additional categories)

These represent real user conditions that rarely appear in requirements but frequently cause production bugs. Walk through each one after the standard states:

| # | Category | Question to answer |
|---|----------|-------------------|
| 14 | **Session timeout mid-flow** | Auth expires between steps of a multi-step form. Is draft data preserved? Does the user return to the correct step after re-auth? |
| 15 | **Browser back button** | What happens on back? Previous state loads correctly? Form data preserved? "Are you sure?" guard? |
| 16 | **Refresh mid-flow** | F5/refresh at each step of a multi-step flow. State persisted via URL params, local storage, or server draft? |
| 17 | **Duplicate submission** | What prevents double-submit? Button disabled after first click? Server-side idempotency? |
| 18 | **Slow / degraded network** | What does the user see during a 5-second API call? 30-second? Timeout? Can they cancel? |
| 19 | **Pagination edge cases** | Exactly N items where N is the page size. Items added/removed during pagination. Count consistency. |
| 20 | **Interrupted upload** | If file upload exists: cancelled mid-way, browser closed during upload, file exceeds size limit. |
| 21 | **Stale tab** | User has app in two tabs. Acts in Tab A. Switches to Tab B with old data. What happens when they interact with stale data? |

### Content Decisions Happen Here

Empty state copy, error messages, button labels, tooltips -- all documented at this level, not deferred to visual design. If a Content Strategist is on the team, they lead these decisions.

**How to propose:**

```
Designer: "For the Team Dashboard, I think these states exist:
  - Default: table with timesheets, filters at top, status chips
  - Loading: skeleton matching table layout, 5 placeholder rows
  - Empty (first-time): 'No timesheets to review yet. Employees will
    appear here once they create their first timesheet.' No CTA for manager.
  - Empty (filtered): 'No timesheets match your filters.' CTA: 'Clear filters'
  - Error (network): banner above table: 'Could not load timesheets. [Retry]'
  - Permission denied: N/A -- only managers reach this page [?]
  - Stale tab: if data changes while tab is inactive, show a subtle
    'Data updated' banner on tab focus with a refresh link [?]"

Product: "Missing: the 'Near deadline' state. When a pay period closes
  in 24 hours, unsubmitted timesheets show an amber warning badge.
  Also, the empty first-time message differs for Managers who have no
  direct reports assigned yet -- they see 'No employees assigned to
  you. Contact your administrator.' not the timesheet message."

User: "Also, we need a 'Locked' state -- after payroll runs, the entire
       period becomes read-only with a lock icon. No one can edit."
```

**What to document (written to `discovery.md` under `## States: [Page Name]`):**

For each page, document every applicable state with:
- Description of what the user sees
- Role variations (if any)
- Data requirements or trigger conditions
- Exact content/copy for messages, CTAs, labels
- Recovery path for error states (action, data preservation, dead-end escape)

Mark states that do not apply with a reason:
```
### States NOT applicable to Team Dashboard:
- Offline: feature requires real-time data, no offline mode
- First-use/Onboarding: no tutorial needed, standard table pattern
- Interrupted upload: no file upload on this page
```

**Gate:** Write to disk. Team reviews: Product checks every "when" and "if" from requirements maps to a state; Designer checks every page has content/copy decided (no "TBD" placeholders). User reviews and confirms. Do not advance until every page has its complete state inventory confirmed.

<!-- SELF-CHECK: Minimum 5 states per page expected. If fewer than 5, you likely missed loading, empty, or error variants. Go back through the checklist. -->

---

## Level 4: Flows

**Goal:** Map every state transition -- what triggers it, who can trigger it, what happens on success and failure, and what changes for other roles.

**What to discover:**
- Every state transition: trigger, actor, success outcome, failure outcome
- Multi-step workflows: full sequence from start to end with every branch point
- Cross-role effects: when one role acts, what changes for another role's view
- Lifecycle flows: entity state machines (e.g., draft -> submitted -> approved -> paid)
- Error recovery: for every failure, how does the user get back on track
- Destructive actions: what can be undone, how, and for how long
- Concurrency: what if another user modifies or deletes this entity between page load and action
- Fatigue analysis: for multi-step flows, count total interactions, identify auto-save and batch opportunities

**How to propose:**

```
Designer: "The timesheet submission flow:
  1. Employee opens draft timesheet (Default state, Entry page)
  2. Employee clicks 'Submit' -> Busy state (button disabled, spinner)
  3. Success -> 'Submitted' state (read-only view, status badge)
  4. Failure -> Error state (inline error, Submit button re-enabled)
  5. Manager sees new entry on Team Dashboard in 'Pending' status
  6. Manager clicks timesheet -> Detail page, 'Pending Approval' state
  7. Manager clicks 'Approve' -> Busy -> 'Approved' state
  8. Employee sees status update to 'Approved' on My Timesheets"

Product: "Missing branches:
  - What if Manager clicks 'Request Changes'? Timesheet returns to
    Employee in 'Amendments Requested' state with Manager's comments.
  - Employee can withdraw before Manager acts -- goes back to Draft.
  - Concurrent modification: what if Manager and Employee both have
    the timesheet open and Employee withdraws while Manager approves?
    We need a conflict state."

User: "On conflict: last action wins, but show a notification to the
       other user. 'This timesheet was withdrawn by [Employee] while
       you were reviewing it.'"
```

**What to document (written to `discovery.md` under `## Flows`):**

Simple flows (single action):
```markdown
## Flow: Submit Timesheet
- **Trigger:** Employee clicks Submit button
- **Who can trigger:** Employee, Representative (on behalf)
- **Preconditions:** All required hours filled, timesheet in Draft state
- **On trigger:** Button disabled, spinner shown
- **On success:** Page transitions to read-only view, status badge "Submitted"
- **On failure:** Inline error, button re-enabled, form data preserved
- **Cross-role effect:** Manager's Team Dashboard shows new "Pending" entry
- **Undo:** Employee can Withdraw (returns to Draft) until Manager acts
- **Concurrency:** If Manager acts while Employee withdraws, last action wins + notification
```

Lifecycle flows (state machine):
```markdown
## Lifecycle: Timesheet

Draft -> Submitted -> Approved -> Paid
                  \-> Amendments Requested -> Submitted (resubmit)
                  \-> Withdrawn (back to Draft)

| From | To | Trigger | Actor | Cross-role effect |
|------|----|---------|-------|-------------------|
| Draft | Submitted | Click Submit | Employee | Manager sees "Pending" |
| Submitted | Approved | Click Approve | Manager | Employee notified |
| Submitted | Amendments Requested | Click Request Changes | Manager | Employee sees comments |
| Submitted | Draft | Click Withdraw | Employee | Manager entry disappears |
| Amendments Requested | Submitted | Click Resubmit | Employee | Manager sees updated entry |
| Approved | Paid | Payroll runs | System | Both see "Paid" (read-only) |
```

Destructive actions:
```markdown
## Destructive Actions

| Action | Undo mechanism | Time limit | Focus after undo |
|--------|---------------|------------|------------------|
| Delete draft | Undo toast | 10 seconds | Toast auto-focuses, Enter to undo |
| Withdraw submission | Undo toast | 10 seconds | Focus returns to status badge |
```

Fatigue analysis (for multi-step flows):
```markdown
## Fatigue Analysis: Timesheet Entry

- **Total steps:** 7 (select period, enter hours x5 days, submit)
- **Total interactions:** ~15 clicks/keypresses minimum
- **Auto-save:** Yes -- drafts save after 2 seconds of inactivity
- **Batch operations:** Yes -- copy previous week's hours
- **Progress indicator:** Not needed (single page, all visible)
- **Early exit:** Yes -- draft auto-saves, user can return later
```

**Gate:** Write to disk. Team reviews: Product checks every flow has error paths (not just happy path), every destructive action has recovery, and cross-role effects are documented; Designer checks every failure state has a recovery path back to a good state. User reviews and confirms transitions are correct. Do not advance until all flows are documented.

<!-- SELF-CHECK: Minimum 3 flows per page expected. If fewer, you likely missed error recovery flows and cross-role effects. At least 1 lifecycle flow expected if the entity has status transitions. -->

---

## Level 5: Interactions + Accessibility

**Goal:** For every page, document what happens when the user interacts with each element -- via mouse, keyboard, switch, and screen reader -- and define the accessibility contract per component.

These are combined because accessibility is part of design, not a separate verification pass. Every interactive element gets its behavior spec and accessibility contract together.

**What to discover:**

Interactions:
- Every interactive element per page (buttons, links, inputs, toggles, menus, tables)
- Per element: what happens on click/tap, keyboard activation, focus, blur
- Tab order within each page
- Focus management: where focus moves after actions (submit, delete, modal open/close, error)
- Feedback: what the user sees/hears after each interaction (visual change, announcement, toast)
- Timing: no timed interactions; auto-save intervals; debounce on search/filter
- Validation: rules, when it runs, error message copy, error display pattern

Accessibility:
- ARIA roles and patterns per component (combobox, dialog, tabpanel, grid, etc.)
- Keyboard patterns per component (arrow keys, Enter, Escape, Tab)
- Screen reader announcements after actions (live regions)
- Switch access feasibility (can every flow be completed with a single switch?)
- Reduced motion behavior (what animations are removed or replaced)
- High contrast readiness (no meaning conveyed by color alone)

**How to propose (batched per page, not per element):**

```
Designer: "On the Team Dashboard, tab order is:
  1. Status filter chips (arrow keys between chips, Space toggles)
  2. Date range picker (Enter opens calendar, arrows navigate days)
  3. Search input (auto-filter after 300ms debounce)
  4. 'Select all' checkbox -> selects all visible rows
  5. [For each row]: checkbox -> employee name link -> status badge
     (read-only) -> approve button -> reject button
  6. Bulk action bar (appears on first selection, toolbar pattern)

  Keyboard: Enter/Space activates all buttons. Escape closes any
  dropdown. No hover-dependent functionality.

  ARIA: Table uses native <table>. Sort columns use aria-sort.
  Bulk action bar is role='toolbar' with aria-label='Bulk actions'.
  Row count announced via aria-describedby: '{N} timesheets'.

  Focus management:
  - After approve/reject: focus stays on the row (status updates)
  - After bulk approve: focus moves to confirmation toast
  - After filter change: focus stays on filter, table updates
  - After error: focus moves to error banner

  Screen reader:
  - Row announced as '{name}, {period}, {status}, {hours} hours'
  - Bulk bar announces '{N} timesheets selected' (aria-live='polite')
  - Sort announces 'Sorted by {column}, {direction}'

  Touch targets: 48px minimum, 60px for Approve/Reject buttons.
  Status conveyed via text label + color, never color alone."

Product: "The filter chips need an interaction spec: what happens when
  all chips are deselected? Does the table show everything or nothing?
  Also, the approve button should be disabled with a tooltip when the
  timesheet is already in 'Approved' state -- not hidden."

User: "All deselected means show everything. And add a 'Select period'
       dropdown before the status filters -- managers filter by pay
       period first, then by status."
```

### Accessibility Rules (Non-Negotiable)

These apply to every element at this level. Do not ask whether they apply -- they always do:

1. No hover-dependent functionality (tooltips on focus, not just hover)
2. 48px minimum touch targets (60px for primary actions)
3. Complete keyboard operability for every flow
4. No timed interactions (timers pause on focus)
5. Stable layouts (no content shift after load; reserve space for error messages)
6. Undo over confirm dialogs (confirm dialogs require multiple precise interactions; undo requires one)
7. Sequential navigation support (switch devices traverse in reading order)
8. `prefers-reduced-motion` support
9. High contrast readiness (no meaning by color alone)
10. Error recovery over error prevention

### Interaction Modality Check

For primary flows, verify each modality works. Document as a matrix:

```markdown
## Interaction Modality Matrix

| Flow | Mouse | Keyboard | Switch | Voice |
|------|-------|----------|--------|-------|
| Approve timesheet | Click button | Tab to button, Enter | Scan to button, activate | "Click Approve" |
| Filter by status | Click chip | Arrow to chip, Space | Scan to chip, activate | "Click Submitted" |
| Select multiple | Click checkboxes | Tab + Space per row | Scan + activate per row | "Click checkbox" per row |
```

**What to document (written to `discovery.md` under `## Interactions: [Page Name]` and `## Accessibility Contracts`):**

Per page:
- Tab order (numbered list of focusable elements)
- Element details (type, behavior on click/keyboard, focus after action, validation, disabled conditions)
- Feedback patterns (success toasts, error display, loading indicators)

Per component:
- ARIA role and attributes
- Keyboard pattern (reference WAI-ARIA patterns by name when applicable)
- Focus management plan (on open, on close, on action)
- Screen reader announcements (what, when, via which mechanism)
- Switch access mode
- Reduced motion behavior
- Touch target sizes

**Gate:** Write to disk. Team reviews: Designer checks every element has keyboard + screen reader behavior defined; Product checks every destructive action has a defined recovery mechanism and no hover-dependent functionality remains. User reviews and confirms. This is the final level -- thoroughness here prevents rework.

<!-- SELF-CHECK: Minimum 4 interactions per element, 3 accessibility items per component. If you are documenting fewer, you likely missed keyboard behavior, focus management, or screen reader announcements. Go back through. -->

---

## Round 2 Complete

When all five levels are documented and gated:

1. **Roles** -- every actor documented with goals, permissions, input methods
2. **Pages** -- every page documented with purpose, role access, navigation; role-page matrix confirmed
3. **States** -- every page has a complete state inventory (21 categories addressed: 13 standard + 8 resilience); all content/copy decided
4. **Flows** -- every state transition mapped with trigger, success, failure, cross-role effects, undo; lifecycle flows documented; fatigue analysis for multi-step flows
5. **Interactions + Accessibility** -- every page has tab order and element specs; every component has an accessibility contract; interaction modality matrix covers primary flows

All artifacts are written to `discovery.md` under section headings. The team does a final review:

```
Product: "I've checked every acceptance criterion against what we've
  documented. AC-1 through AC-14 are all covered. No gaps."

Designer: "Every page has states, every flow has error recovery, every
  element has keyboard + screen reader behavior. The accessibility
  contracts are complete."

User: [Confirms] "Discovery is complete, nothing is missing."
```

If open questions remain, they are listed under `## Open Questions` in `discovery.md`. These MUST be resolved before design begins.

Round 2 is complete. Advance to Round 3: read `design.md`.
