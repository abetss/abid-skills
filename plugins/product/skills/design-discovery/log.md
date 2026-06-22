# Design Discovery -- Redesign Log

## Date: 2026-04-01

## Team

- **Lead Designer**
- **Lead Product Manager**
- **Principal Frontend Engineer**
- **Engineering Lead** (coordinator)

---

## What Each Expert Needs

### Lead Product needs:
1. Requirements.md as formal first-class input (parse acceptance criteria as checklist)
2. State inventory per page (loading, empty, error, permission-denied, degraded -- systematically)
3. Role-based view matrix (what each role sees and can do per page/component)
4. Workflow state diagrams for lifecycle features (draft -> submitted -> approved -> paid)
5. Coverage matrix mapping every acceptance criterion to a design artifact
6. Product sign-off gate before handoff to engineering
7. Compliance checkpoint (PIPEDA, labor law data display rules)
8. Interaction modality analysis (switch access, eye gaze, voice control feasibility per flow)
9. Fatigue analysis for multi-step flows (total interaction count, auto-save needs, batch operations)
10. Error recovery audit (every destructive action and its undo mechanism)

### Lead Designer needs:
1. Problem framing BEFORE touching data (who, what problem, success criteria)
2. Task flows with decision points and branching (user journeys, not just data shapes)
3. Information architecture (content hierarchy, grouping, visual priority)
4. Interaction specs per component (click, focus, blur, submit, escape, transitions)
5. State mockups -- not just data variations but UI states (empty, loading, error, first-use)
6. Responsive strategy per page (what reflows, collapses, hides, reorders at each breakpoint)
7. Accessibility as architectural input, not verification checklist:
   - No hover-dependent functionality
   - 48px+ touch targets (60px for primary actions)
   - Complete keyboard operability
   - No timed interactions
   - Stable layouts (no content shift after load)
   - Forgiving interactions (undo over confirm dialogs)
   - Sequential navigation support (switch devices)
   - prefers-reduced-motion support
   - High contrast readiness
   - Error recovery over error prevention
8. Content and labeling decisions (button text, empty state messages, tone)
9. The "propose and get corrected" method extended to interactions, states, and layouts (not just data)
10. Agent dispatch model for research (schema reader, code reader, doc reader, pattern finder)

### Principal Frontend Engineer needs:
1. Component decomposition tree (what's a component, layout, composition)
2. Three type layers:
   - Domain types (what API returns)
   - View model types (transformed for UI, with computed fields like `can_edit`)
   - Component props (per-component slice + callbacks)
3. Per-component interaction inventory (callbacks, events, keyboard handlers)
4. Per-component accessibility contract (ARIA role, keyboard pattern, focus management plan)
5. Per-component responsive behavior (what changes at each breakpoint)
6. Storybook as primary development environment with workflow:
   - Phase 1: Scaffold (component files + stories + fixtures)
   - Phase 2: Structure (semantic HTML, ARIA roles, keyboard nav)
   - Phase 3: Style (Tailwind against design, responsive)
   - Phase 4: Interact (callbacks, state, play() tests)
   - Phase 5: Verify (axe scan, visual regression, screen reader)
7. Story patterns: Default, Empty, Loading, Error, With{Variation}, Mobile/Tablet
8. Fixture data in `__fixtures__/` alongside stories
9. Every story must pass axe-core scan (zero violations)
10. Keyboard-only interaction tests in play() functions

---

## Current Skill Assessment

**What works well (KEEP):**
- "Wrong proposals surface hidden rules faster than open-ended questions" methodology
- Agent dispatch model (research agents parallel, main thread interactive)
- Conventions doc format (business rules, impossible states, display rules)
- TypeScript discriminated unions approach
- Story fixture guidelines (realistic narratives, actor constants, coverage table)
- Common mistakes table

**What's missing (ADD):**
- Problem framing / user goal definition
- Task flow mapping
- Systematic state enumeration
- Role-based view matrix
- Information architecture
- Interaction design specs
- Responsive strategy
- Accessibility as input (not checklist)
- Content/labeling decisions
- Component decomposition
- Three-layer type system (domain, view model, props)
- Requirements coverage validation
- Product sign-off

**What's wrong (FIX):**
- Types conflate API data shapes with component props (single layer instead of three)
- Storybook treated as optional output instead of primary development environment
- Accessibility is absent from discovery (only appears downstream in QA)
- No formal input contract (requirements.md should be required)
- No formal output contract (plan-prep can't verify completeness)
- Graphviz diagrams waste tokens (Claude can't render them)

---

## Scope Discussion: The Hierarchy

User's mental model for the discovery hierarchy:

```
Roles (who)
  └── Pages (what they see)
       └── States (per page: loading, empty, populated, error, permission...)
            └── Flows (between states: transitions, triggers, who can trigger)
                 └── Interactions (per element: click, keyboard, focus, feedback)
                      └── Accessibility (per interaction: ARIA, focus management, switch nav)
```

### The question: How to walk through this hierarchy effectively?

**Option A: Top-down, role-first**
Start with roles -> enumerate pages per role -> enumerate states per page -> map flows -> detail interactions -> layer in accessibility.

Pros: Matches the user's mental model. Ensures nothing is missed per role. Natural for permission-based products.
Cons: Can be slow if many roles share pages. Repetitive for shared pages.

**Option B: Page-first with role overlay**
Start with pages (the feature scope) -> for each page, enumerate which roles see it and what differs -> then states, flows, interactions, accessibility.

Pros: Faster for features where most content is shared. Avoids repetition.
Cons: Can miss role-specific pages that only one role sees.

**Option C: Hybrid -- role inventory first, then page-by-page with role annotations**
1. First pass: quick role inventory (which roles interact with this feature? what are their goals?)
2. Second pass: page-by-page walkthrough, annotating per role what differs (visibility, actions, data)
3. Third pass: states, flows, interactions, accessibility per page

Pros: Gets the best of both. Role context is established early but pages aren't duplicated.
Cons: Three passes could feel slow.

**Option D: Flow-first**
Start with the primary user flow (the happy path for the primary role) -> branch out to other roles and edge cases.

Pros: Gets to something concrete fastest. Users can react to a flow before abstract matrices.
Cons: Can miss pages/states that aren't on the happy path.

### Decision (2026-04-01)

**Option A (role-first) is the default.** But all four options are presented to the user at the start of every discovery session. The user picks which approach fits their use case. The skill should say something like:

> "How would you like to walk through this feature? (A is recommended)"
> - **A. Role-first** (default): Start with roles → pages per role → states → flows → interactions
> - **B. Page-first**: Start with pages → overlay role differences
> - **C. Hybrid**: Quick role inventory, then page-by-page with role annotations
> - **D. Flow-first**: Start with the happy path, branch to variations

Rationale: Option A matches the user's mental model (roles → pages → states → flows → interactions → accessibility) and is natural for permission-heavy products. But some features are better served by other approaches, and the user knows best.

### Decision: Complexity Triage (2026-04-01)

**Always use the Deep (full) process.** The skill does not triage by complexity -- every feature gets the complete 5-round treatment.

**Future note:** Light (~15-20 min, single page, props-only types) and Standard (~30-40 min, multi-page, Storybook opt-in) tracks may be created later as separate variations. For now, one process that covers everything.

### Decision: Team Presentation Format (2026-04-01)

**Distinct voices in meeting transcript format.** Each team member speaks as a named character. The user participates as themselves in the meeting. This is NOT a unified voice -- it's a facilitated team discussion where perspectives are attributed.

Overrides the Usability Critic and Claude Code Expert recommendation for unified voice. User's rationale: "This is a meeting between me and all the team members."

### Decision: Level Skipping (2026-04-01)

**Default: no skipping.** The full process runs every level for every feature.

**But:** If the user explicitly asks to skip a level, allow it. If the user provides existing artifacts (e.g., state inventory, flow diagrams) in the context, the team should review them quickly rather than re-derive from scratch -- "touch on it and move on." Don't force re-discovery of work that's already done, but don't skip the validation either.

### Decision: Interactions + Accessibility Combined (2026-04-01)

**Combined into one level.** Accessibility is part of design, not a separate pass. Every interactive element gets its interaction spec AND accessibility contract together in one review.

### Decision: Opt-in / Opt-out (2026-04-01)

**Any round can be opted out of, but the user specifies.** Don't ask them -- they'll tell you if they want to skip a round. Default is to run everything.

### Decision: Session Persistence (2026-04-01)

**Yes.** Use a progress file (`design-discovery-progress.md` in work folder) for:
- Reference and logging
- Resuming later if session is interrupted
- Tracking what's been approved vs still in progress

### Decision: Batching (2026-04-01)
**Batch per page.** Present the full interaction+accessibility spec for an entire page at once. Don't go element by element. We want to move fast and think about everything together.

### Decision: Anti-Rationalization Table (2026-04-01)
**Yes, include it.** Similar to the debugging skill's table -- catches the AI cutting corners during discovery.

### Decision: Memory (2026-04-01)
**Yes, but selective.** Only capture the most important things:
- Important design decisions and their rationale
- Important ways of thinking about the product
- Important ways of thinking about the users
- NOT everything -- only what would change how you approach the next discovery session

### Decision: Gate Format (2026-04-01)
**Write to disk first.** After each level, write the artifact to disk. The team reviews it, exchanges feedback, improves it. Then hand it to the user to review. Three steps: write → team review → user review.

### Decision: Minimum Discovery Thresholds (2026-04-01)
**Use the proposed minimums as a base** (5 states per page, 3 flows per page, 4 interactions per element, 3 accessibility items per component). But suggest to the AI that there are usually more than these minimums -- find ALL of them, not just the minimum.

### Decision: Artifacts (2026-04-01)
**Everything in one `discovery.md` file under different section titles.** Use text and ASCII diagrams. No separate files for states, flows, etc. -- keep it all in one document with clear headings. Specialized files only for Round 4 outputs (types, fixtures, component tree, coverage matrix).

### Decision: Research Agents (2026-04-01)

Two types of research agents, dispatched during Round 1:

**1. Schema Reader** (one agent)
- Reads database models (ZenStack/Prisma schema) to understand what data exists
- Reports: fields, relationships, enums, access policies
- Model: Sonnet (read-only, fast)

**2. Feature Scout** (one or more agents -- dispatch multiple in parallel if multiple features/areas to examine)
- Takes screenshots of the current feature in the browser (uses Chrome MCP)
- Reads `a-kb/product-guide/` and `a-kb/` knowledge base to learn about the product domain
- Looks at analogous features in the app, takes screenshots of those too if useful
- Brings back: screenshots + domain knowledge + patterns found
- Model: Sonnet (read-only except for screenshots)

**Removed:**
- Doc Reader: not needed -- requirements.md is shared with all team members directly at the start of Round 1
- Code Reader: replaced by Feature Scout's visual approach (screenshots over code reading for design context)
- Pattern Finder: merged into Feature Scout
- Domain Knowledge Reader: merged into Feature Scout

### Decision: Flow is now 4 Rounds (2026-04-01)

Approach selection merged into Round 1. New structure:
- Round 1: Frame (understand brief + choose approach + assemble team)
- Round 2: Discovery Walk-through (Roles → Pages → States → Flows → Interactions+Accessibility)
- Round 3: Design (Storybook iteration / ASCII wireframes)
- Round 4: Specify (types, fixtures, component tree, handoff)

---

---

## Collaborative Process Design (2026-04-01)

### Team Model

**Core team (always present):**
- **Lead Product** (AI agent) -- owns "what" and "why", validates against requirements, ensures edge case coverage
- **Lead Designer** (AI agent) -- owns "how", proposes layouts/interactions/states, drives accessibility decisions
- **User** (human) -- domain expert, decision-maker, approves directions at every gate

**Optional members (assessed at kickoff, user confirms):**
- **UX Researcher** -- when personas need deeper analysis, competitive analysis exists, or user behavior data is available
- **Accessibility Specialist** -- when feature has complex interaction patterns (forms, data tables, drag-and-drop, multi-step flows)
- **Data Architect** -- when data model is new, complex, or crosses multiple services
- **Content Strategist** -- when labeling, tone, empty state copy, error messages, or onboarding copy matter

### Process: 5 Rounds of Structured Conversation

The process is a **facilitated conversation**, not a document generator. Agents play their roles, disagree productively, and surface things the others miss. Artifacts emerge from the conversation.

#### Round 1: Frame (Product Manager leads, ~5 min)

**Goal:** Get everyone on the same page about what we're designing, for whom, and within what constraints -- before any design work begins.

Specific objectives:
1. Read and summarize requirements so the team shares the same understanding of the brief
2. Identify which roles are involved (manager, attendant, admin, representative, etc.)
3. Establish scope boundaries (what's in, what's out)
4. Decide if additional expertise is needed at the table (Accessibility Specialist, UX Researcher, Content Strategist, Data Architect)
5. Choose the walk-through approach (A: Role-first, B: Page-first, C: Hybrid, D: Flow-first)
6. Dispatch research agents to scan the codebase in the background (schema, existing code, docs, patterns) so findings are ready by Round 2

Product Manager presents requirements summary. Designer asks about users and constraints. They jointly assess whether optional team members are needed.

```
Product:  "From requirements: [summary]. Roles: [X, Y]. Core problem: [Z]."
Designer: "Do we need a UX Researcher? Any complex interactions needing
           an Accessibility Specialist?"
User:     [Confirms framing, approves/adjusts team composition]
```

Gate: Problem understood, team composed, scope agreed.

Research agents dispatched in parallel:
- Schema reader (if DB/API exists)
- Code reader (if existing UI exists)
- Doc reader (if requirements/product docs exist)
- Pattern finder (if analogous features exist in codebase)

#### Round 2: Approach Selection (~1 min)

```
"How should we walk through this feature?"
  A. Role-first (recommended) -- roles → pages per role → states → flows
  B. Page-first -- pages → role overlay → states → flows
  C. Hybrid -- role inventory, then page-by-page with role annotations
  D. Flow-first -- happy path first, branch to variations
User:     [Picks approach]
```

#### Round 3: Discovery Walk-through (iterative, the core of the process)

The team walks through the hierarchy using the chosen approach. At each level, they PROPOSE and the user CORRECTS. Wrong proposals surface hidden rules faster than open-ended questions.

**Level 1: Roles**
```
Product:  "The roles involved are [list]. Their goals: [per role]."
Designer: "For accessibility, these roles likely use these input methods: [list]."
User:     [Corrects, adds roles, clarifies goals]
```

**Level 2: Pages (per role)**
```
Product:  "This role needs these pages: [list]. Here's what each page does."
Designer: "I'd expect these pages: [list]. This one might not be needed because [reason]."
User:     [Corrects -- "we don't have that page", "these two are actually one page"]
```

**Level 3: States (per page)**
```
Designer: "For [page], I think these states exist: default, loading, empty,
           error, permission-denied. The empty state message should say [X]."
Product:  "Missing: [first-time-ever empty vs. filtered-to-empty]. Also,
           when [business rule], there's a [special state]."
User:     [Corrects, each correction is a rule discovery]
```

**Level 4: Flows (between states)**
```
Designer: "The flow is: [state A] → user clicks [action] → [state B].
           If it fails, [error state]."
Product:  "Who can trigger this transition? Manager only, or both roles?
           What happens to the other role's view when this changes?"
User:     [Corrects transitions, adds constraints]
```

**Level 5: Interactions (per element)**
```
Designer: "This button does [X] on click. On keyboard: Enter/Space activates.
           Tab order is [sequence]. Hover shows [tooltip]."
Product:  "What about undo? This is a destructive action."
Designer: "Right -- undo toast for 10 seconds instead of a confirm dialog.
           For switch users, confirm dialogs are harder to dismiss."
User:     [Approves or adjusts interaction pattern]
```

**Level 6: Accessibility (per interaction)**
```
Designer: "ARIA role: [role]. Keyboard pattern: [pattern].
           Focus moves to [target] after action. Screen reader announces [text]."
Accessibility Specialist (if present): "Switch users need [X] here.
           Dwell time on this target should be [Y]."
User:     [Confirms]
```

Gate: Complete Roles → Pages → States → Flows → Interactions → Accessibility map documented. User confirms nothing is missing.

Artifacts produced during Round 3:
- `conventions.md` (business rules, impossible states, display rules -- built incrementally)
- `state-inventory.md` (all states per page per role)
- `flow-diagrams.md` (state transitions with triggers and actors)

#### Round 4: Design (Designer leads)

Designer produces visual designs using the discovered information.

```
Designer: "Here's the information architecture for [page].
           Primary: [X], Secondary: [Y]. Layout: [description]."
Product:  "Does this cover AC-3? I don't see [edge case]."
Designer: "Adding [state]. Responsive: mobile [collapses X], tablet [reflows Y]."
User:     [Approves direction or requests changes]
```

User prefers **iterating in Storybook** over ASCII mockups. The flow is:
1. Designer describes the design direction (layout, hierarchy, responsive approach)
2. Design-discovery dispatches an agent with the `ui-design-iterate-storybook` skill to build it in Storybook
3. User reviews in the browser, gives feedback
4. Iterate in Storybook until approved

Can optionally use `ui-ascii-design` skill for quick wireframes early on, but Storybook iteration is preferred.
Can optionally use Pencil (Figma MCP integration) if visual design tool output helps.

Gate: Visual direction approved by user (via Storybook review in browser).

Artifacts produced during Round 4:
- Storybook components with stories per page/state/breakpoint
- `interaction-specs.md` (per-component behavior, keyboard nav, focus management)
- `responsive-specs.md` (breakpoint behavior per page)

#### Round 5: Specify (Engineering handoff)

The team produces the technical specification for engineering.

```
Designer: "Component breakdown: [tree]"
Product:  "Each component needs these business properties: [list]"
[FE perspective]: "Types should be three layers:
  - Domain types (API shape)
  - View model types (transformed: can_edit, display_status)
  - Component props (per-component slice + callbacks)"
User:     [Approves decomposition]
```

Product builds coverage matrix: maps every acceptance criterion from requirements to a specific artifact (variation, state, fixture, mockup).

Gate: Coverage matrix complete. Product confirms every AC is addressed. User signs off.

Artifacts produced during Round 5:
- `component-tree.md` (decomposition with props per component)
- `types.ts` (three layers: domain, view model, component props)
- `fixtures.ts` (per-component, covering every state)
- `coverage-matrix.md` (ACs → artifacts mapping)
- `view-model-props.md` (component prop interfaces for plan-prep)

### How Agents Disagree Productively

The value of the team model is that agents catch each other's blind spots:

- **Product catches business rules Designer doesn't know:** "Actually, attendants can't see other attendants' timesheets"
- **Designer catches UX problems Product didn't consider:** "A confirm dialog for every approval is 3 extra clicks × 20 timesheets per day = 60 unnecessary clicks for a user with limited motor function"
- **User catches domain knowledge neither agent has:** "We also have a 'representative' role that manages on behalf of the person with disability"
- **Accessibility Specialist catches what all three miss:** "This drag-to-schedule interaction has no keyboard alternative"

When agents disagree, they present both perspectives to the user with trade-offs. The user decides.

### Per-Case Team Composition Decision

At kickoff, the core team evaluates:

| Question | If Yes → Add |
|----------|-------------|
| Does this feature involve complex user personas or behavioral research? | UX Researcher |
| Does this feature have complex keyboard/screen-reader interactions? (tables, forms, drag-drop, multi-step) | Accessibility Specialist |
| Is the data model new or crosses multiple services? | Data Architect |
| Does the feature have significant copy, onboarding, or error messaging needs? | Content Strategist |

User confirms the team before Round 2 begins.

---

## Resolved Design Questions (2026-04-01)

### 1. Replace vs orchestrate?
**Orchestrate.** Design-discovery is the orchestrator. It can dispatch agents that use:
- `ui-ascii-design` (renamed from ui-design) for quick wireframes if needed
- `ui-design-iterate-storybook` (NEW -- to be created) for Storybook-based design iteration
- `view-model-props` for component prop spec at handoff
- Pencil (Figma MCP) if visual design tool output helps

### 2. Token budget?
Not a concern -- the skill dispatches agents and produces artifacts in work folder files. The skill itself stays lean; the output lives in the work folder.

### 3. Storybook phase -- part of this skill or separate?
**Separate skill** (`ui-design-iterate-storybook`) that design-discovery dispatches via agent. Design-discovery owns the process; the Storybook skill owns the implementation iteration.

### 4. Figma?
Not a primary concern. Pencil integration is available if it helps, but Storybook iteration is the preferred design medium.

### 5. Missing requirements?
**Push back to the user.** If requirements.md doesn't exist, the skill should say: "I need requirements before starting design discovery. Use the `write-requirements` skill first, or provide a requirements document."

---

## New Skill Needed: `ui-design-iterate-storybook`

A skill for iterating on UI designs directly in Storybook. Design-discovery dispatches an agent with this skill during Round 4.

What it does:
- Takes design direction from design-discovery (layout, hierarchy, states, responsive rules, accessibility requirements)
- Scaffolds components with typed props
- Creates stories per state (default, empty, loading, error, per-role variants)
- Creates responsive stories (mobile, tablet, desktop)
- User reviews in browser, gives feedback
- Iterates until approved
- Follows the FE Engineer's workflow: scaffold → structure → style → interact → verify

This skill consumes the artifacts from design-discovery Rounds 1-3 and produces the visual implementation.

To be designed and created in a future session.

---

## TODO for Next Session

1. Write the actual `design-discovery/SKILL.md` rewrite based on this log
2. Create `ui-design-iterate-storybook` skill
3. Decide whether `view-model-props` should be absorbed into Round 5 or remain standalone
4. Test the redesigned skill against a real feature

---

## Principal Frontend Engineer: Storybook Handoff Document Specification (2026-04-01)

### The Problem This Solves

When `design-discovery` dispatches an agent to `ui-design-iterate-storybook`, that agent needs to START BUILDING immediately -- not spend 20 minutes re-reading conventions docs, guessing component boundaries, or figuring out types. The handoff document is the contract between the two skills. If it is incomplete, the Storybook agent asks questions instead of writing code. If it is ambiguous, the Storybook agent makes wrong guesses and the user wastes iteration cycles correcting them.

The document must answer one question exhaustively: **"What do I scaffold right now?"**

---

### Required Sections in the Handoff Document

The handoff document lives at `{work-dir}/storybook-handoff.md` and contains exactly seven sections. Every section is mandatory. If a section is empty, the design-discovery skill is not done.

---

#### Section 1: Feature Summary (context, not requirements)

Brief orientation so the Storybook agent understands what it is building without needing to read requirements.md.

```markdown
## 1. Feature Summary

**Feature:** {PROD-XXX Feature Name}
**Primary user goal:** {One sentence -- what the user is trying to accomplish}
**Roles involved:** {Role A (primary), Role B, Role C}
**Pages in scope:** {Page 1, Page 2}
**Tech stack notes:** {e.g., Next.js 16, Tailwind 4, shadcn, Radix primitives}
**Design system:** {path to global.css or tokens file if relevant}
```

This is a 5-line orientation, not a requirements doc. The Storybook agent does not own requirements -- it owns visual implementation.

---

#### Section 2: Component Decomposition Tree

This is the most critical section. It defines every component the Storybook agent needs to create, its position in the hierarchy, and its classification.

**Format: indented tree with annotations.**

Each node has: `ComponentName` -- `[type]` -- one-line purpose.

Types are:
- `[page]` -- top-level route component, composes layouts and sections
- `[layout]` -- structural wrapper (sidebar + main, header + content)
- `[section]` -- a visually distinct region within a page (card, panel, toolbar)
- `[component]` -- a reusable interactive unit (button group, status badge, form field)
- `[composition]` -- a component composed of other components (a table row that contains badges and actions)

```markdown
## 2. Component Tree

TimesheetOverviewPage [page]
  TimesheetPageLayout [layout] -- sidebar nav + main content area
    TimesheetFilters [section] -- date range, status filter, role filter
      DateRangePicker [component] -- start/end date selection
      StatusFilterChips [component] -- multi-select status chips
    TimesheetTable [section] -- main data table
      TimesheetTableHeader [component] -- sortable column headers
      TimesheetRow [composition] -- single timesheet entry row
        StatusBadge [component] -- visual status indicator
        RowActions [component] -- approve/reject/view actions per role
    TimesheetEmptyState [component] -- shown when no timesheets match filters
    TimesheetErrorState [component] -- shown on data fetch failure
  TimesheetBulkActionBar [section] -- floating bar for multi-select actions
```

**Rules:**
- Every leaf node MUST appear in Section 3 (types) and Section 5 (story plan).
- If a component is shared/existing (already in the codebase), annotate it: `StatusBadge [component] [EXISTING: src/components/ui/status-badge.tsx]`
- The tree is the source of truth for what gets scaffolded. If it is not in the tree, it does not get built.

---

#### Section 3: Three-Layer Type System

Types are structured in three layers. Each layer serves a different consumer. The Storybook agent needs all three because stories use fixtures built from domain types, transformed through view models, and consumed as component props.

```markdown
## 3. Types

### Layer 1: Domain Types (what the API returns)

These match the API/database shape. The Storybook agent does not invent these -- they come from schema research during discovery.

```typescript
// domain/timesheet.ts

type TimesheetStatus = 'draft' | 'submitted' | 'approved' | 'rejected' | 'paid'

type Timesheet = {
  id: string
  employee_id: string
  employee_name: string
  period_start: string  // ISO date
  period_end: string    // ISO date
  status: TimesheetStatus
  total_hours: number
  submitted_at: string | null
  approved_by: string | null
  approved_at: string | null
  rejection_reason: string | null
  entries: TimesheetEntry[]
}

type TimesheetEntry = {
  id: string
  date: string          // ISO date
  hours: number
  description: string
  category: 'regular' | 'overtime' | 'holiday'
}
```

### Layer 2: View Model Types (transformed for UI consumption)

These add computed/derived fields the UI needs. The transformation logic lives in a `toViewModel()` function. View models answer questions like "can this user do X?" and "what should the display string be?" so components never contain business logic.

```typescript
// view-models/timesheet.vm.ts

type TimesheetViewModel = {
  // Pass-through from domain
  id: string
  employee_name: string
  period_label: string          // COMPUTED: "Mar 1 - Mar 15, 2026"
  status: TimesheetStatus
  total_hours: number
  entries: TimesheetEntryViewModel[]

  // Computed display fields
  status_label: string          // COMPUTED: "Awaiting Approval" (not raw enum)
  status_color: 'green' | 'yellow' | 'red' | 'gray'  // COMPUTED: maps status to design token
  submitted_label: string | null // COMPUTED: "Submitted 2 days ago" or null

  // Permission flags (depend on current user role + timesheet state)
  can_edit: boolean
  can_approve: boolean
  can_reject: boolean
  can_delete: boolean
  can_submit: boolean

  // UI state flags
  is_overdue: boolean           // COMPUTED: past period_end and still draft
  is_selected: boolean          // UI state: multi-select checkbox
}

type TimesheetEntryViewModel = {
  id: string
  date_label: string            // COMPUTED: "Mon, Mar 3"
  hours: number
  description: string
  category: 'regular' | 'overtime' | 'holiday'
  category_label: string        // COMPUTED: "Regular Hours"
  is_editable: boolean          // COMPUTED: depends on parent timesheet status
}
```

### Layer 3: Component Props (per-component slice + callbacks)

Each component in the tree gets its own props type. Props are the MINIMUM data a component needs plus its callbacks. Components never reach into parent data -- they receive exactly what they render.

```typescript
// components/timesheet-row/timesheet-row.types.ts

type TimesheetRowProps = {
  // Data (slice of view model relevant to this component)
  employee_name: string
  period_label: string
  status: TimesheetStatus
  status_label: string
  status_color: 'green' | 'yellow' | 'red' | 'gray'
  total_hours: number
  is_overdue: boolean
  is_selected: boolean

  // Actions (available based on permissions -- absent means not shown)
  can_approve: boolean
  can_reject: boolean

  // Callbacks
  on_select: (id: string) => void
  on_view: (id: string) => void
  on_approve?: (id: string) => void   // only present when can_approve
  on_reject?: (id: string) => void    // only present when can_reject
}
```

```

**Rules for types:**
- Every component in the tree (Section 2) MUST have a corresponding props type in Layer 3.
- Discriminated unions for status/kind fields -- no string literals scattered across types.
- View model computed fields are annotated with `// COMPUTED:` and a brief derivation note.
- Permission flags (`can_X`) live in the view model, not in component props as raw role checks.
- Callbacks use `on_action` naming. Domain-specific actions use `on_{domain}_{verb}` (e.g., `on_timesheet_approve`).
- No `any`. No `as` casts. No `interface` (project convention is `type`).

---

#### Section 4: State Inventory Per Component

Every component that has visual states beyond "default with data" gets a state table. This directly drives which stories to create.

```markdown
## 4. State Inventory

### TimesheetOverviewPage [page]
| State | Trigger | What renders |
|-------|---------|-------------|
| Loading | Initial fetch in progress | Skeleton of table + filters |
| Empty (never used) | No timesheets exist for this employee, first time | Empty illustration + "No timesheets yet" + CTA |
| Empty (filtered) | Filters applied, no results | "No timesheets match your filters" + clear filters link |
| Populated | Data loaded, timesheets exist | Full table with rows |
| Error | Fetch failed | Error banner + retry button |
| Permission denied | Role lacks access to this page | "You don't have access" message |

### TimesheetRow [composition]
| State | Trigger | What renders |
|-------|---------|-------------|
| Default | Normal row | All fields, actions based on permissions |
| Selected | Checkbox checked | Highlighted background, included in bulk bar count |
| Overdue | is_overdue = true | Warning icon, amber text on period label |
| Actionable (approver) | can_approve = true | Approve + Reject buttons visible |
| Actionable (employee) | can_edit = true | Edit button visible |
| Read-only | can_edit = false, can_approve = false | No action buttons, view only |

### StatusBadge [component]
| State | Trigger | What renders |
|-------|---------|-------------|
| draft | status = 'draft' | Gray badge, "Draft" |
| submitted | status = 'submitted' | Yellow badge, "Awaiting Approval" |
| approved | status = 'approved' | Green badge, "Approved" |
| rejected | status = 'rejected' | Red badge, "Rejected" |
| paid | status = 'paid' | Green badge, "Paid" (different icon than approved) |
```

**Rules:**
- Every component with more than one visual state MUST have a state table.
- Simple components that only have a "default" state (e.g., DateRangePicker is always interactive) can be omitted -- but annotate in Section 5 that they only have a Default story.
- State names become story names (Section 5). Keep them short and descriptive.

---

#### Section 5: Story Plan

Explicit list of stories per component. No guessing. The Storybook agent creates exactly these stories and no others (unless iteration with the user reveals gaps).

```markdown
## 5. Story Plan

### TimesheetOverviewPage
| Story | Description | Key fixture data |
|-------|-------------|-----------------|
| Default | Populated table, 5 rows, mixed statuses | 5 timesheets: 1 draft, 2 submitted, 1 approved, 1 rejected |
| Loading | Skeleton state | No data, loading = true |
| EmptyFirstTime | No timesheets ever | Empty array, has_ever_had_timesheets = false |
| EmptyFiltered | Filters applied, no match | Empty array, active_filters present |
| Error | Fetch failed | error object with message |
| PermissionDenied | Unauthorized role | permission_denied = true |
| AsApprover | Manager viewing employee timesheets | role = 'manager', can_approve on submitted rows |
| AsEmployee | Employee viewing own timesheets | role = 'employee', can_edit on draft rows |
| Mobile | Responsive: stacked layout | Same as Default, viewport 375px |
| Tablet | Responsive: condensed table | Same as Default, viewport 768px |

### TimesheetRow
| Story | Description | Key fixture data |
|-------|-------------|-----------------|
| Default | Standard row, no special state | status = 'submitted', no actions |
| Selected | Checkbox active | is_selected = true |
| Overdue | Past-due draft | is_overdue = true, status = 'draft' |
| WithApproveActions | Approver view | can_approve = true, can_reject = true |
| WithEditAction | Employee view | can_edit = true |
| ReadOnly | No permissions | all can_* = false |

### StatusBadge
| Story | Description | Key fixture data |
|-------|-------------|-----------------|
| AllStatuses | All 5 statuses rendered side by side | Array of all status values |
| Draft | Single draft badge | status = 'draft' |
| Submitted | Single submitted badge | status = 'submitted' |
| Approved | Single approved badge | status = 'approved' |
| Rejected | Single rejected badge | status = 'rejected' |
| Paid | Single paid badge | status = 'paid' |
```

**Story naming conventions:**
- `Default` -- always first. Happy path with representative data.
- `Empty`, `Loading`, `Error` -- standard UI states (when applicable).
- `With{Feature}` -- variations that add something to Default (`WithApproveActions`, `WithBulkSelection`).
- `As{Role}` -- role-specific views at the page/section level.
- `Mobile`, `Tablet` -- responsive variants (only at page/section level, not leaf components).
- `AllStatuses` / `All{Variants}` -- gallery story showing all visual variations of a single-dimension component.

**Rules:**
- Every state in Section 4 MUST map to at least one story in Section 5.
- Every story MUST have a "Key fixture data" column describing what makes this story distinct. This is what the Storybook agent uses to write the fixture.
- Page-level components MUST have Mobile and Tablet stories.
- Every story will be verified against axe-core (zero violations). This is implicit -- do not list it per story.

---

#### Section 6: Accessibility Contract Per Component

Each component gets an accessibility specification. This is not a checklist to verify after the fact -- it is an architectural input that the Storybook agent uses when writing the semantic HTML.

```markdown
## 6. Accessibility Contracts

### TimesheetTable
- **ARIA role:** `table` (native `<table>` element, not `role="table"` on a div)
- **Keyboard pattern:** Navigable with Tab between interactive elements (checkboxes, action buttons). Arrow keys NOT required (not a grid/spreadsheet pattern).
- **Focus management:** After bulk action completes, focus returns to the first selected row (or the bulk action bar if still visible).
- **Screen reader:** Column headers use `<th scope="col">`. Status is conveyed via text, not color alone. Row count announced via `aria-describedby` on table: "{N} timesheets".
- **Sort interaction:** Sortable columns use `aria-sort="ascending|descending|none"`. Click toggles sort. Screen reader announces new sort order.
- **Minimum touch target:** All interactive elements 48px minimum (60px for primary actions like Approve).

### TimesheetRow
- **ARIA role:** `row` (native `<tr>`)
- **Keyboard pattern:** Tab reaches checkbox, then action buttons (left to right). Enter/Space activates.
- **Focus management:** After approve/reject action, focus stays on the row (which updates visually) -- do NOT move focus away.
- **Screen reader:** Row announced as "{employee_name}, {period_label}, {status_label}, {total_hours} hours". Selected state announced via `aria-selected`.
- **Overdue indicator:** Conveyed via text ("Overdue" label), not just the amber color. Uses `aria-label` on the warning icon.

### StatusBadge
- **ARIA role:** `status` (live region for dynamic updates) OR no special role if static display.
- **Keyboard pattern:** Not interactive (no keyboard handling needed).
- **Screen reader:** Badge text IS the accessible name. No additional aria-label needed. Color is supplementary, not the only indicator.
- **Contrast:** All badge colors meet WCAG AA contrast ratio against their background. Verified in the `AllStatuses` story.

### TimesheetBulkActionBar
- **ARIA role:** `toolbar` with `aria-label="Bulk actions"`.
- **Keyboard pattern:** Arrow keys navigate between buttons within the toolbar. Tab moves into/out of the toolbar as a single stop.
- **Focus management:** Bar appears when first row is selected -- focus does NOT automatically move to bar (user is still selecting). When bar disappears (all deselected), focus returns to the last interacted row.
- **Screen reader:** Announces "{N} timesheets selected" as a live region (`aria-live="polite"`) when count changes.
- **Reduced motion:** Bar appearance/disappearance uses `prefers-reduced-motion` -- instant show/hide instead of slide animation.
```

**Rules:**
- Every component in the tree MUST have an accessibility contract.
- Leaf components with no interactivity (pure display) get a minimal contract: role, screen reader behavior, contrast note.
- The contract specifies WHAT the behavior is, not HOW to implement it (e.g., "focus returns to the row" not "call `.focus()` on the `<tr>` ref").
- Keyboard patterns reference established WAI-ARIA patterns by name when applicable (e.g., "toolbar pattern", "grid pattern", "disclosure pattern").
- Touch target sizes are specified in the contract, not left to styling.

---

#### Section 7: Fixture Data Plan

Describes the fixture file structure and the actor constants. This section exists so the Storybook agent creates consistent, realistic fixture data across all stories.

```markdown
## 7. Fixture Data Plan

### Actor Constants
Reused across all fixtures for consistency.

```typescript
// __fixtures__/actors.ts

export const ACTORS = {
  employee_maria: {
    id: 'emp-001',
    name: 'Maria Santos',
    role: 'employee' as const,
  },
  manager_james: {
    id: 'mgr-001',
    name: 'James Chen',
    role: 'manager' as const,
  },
  admin_priya: {
    id: 'adm-001',
    name: 'Priya Patel',
    role: 'admin' as const,
  },
} as const
```

### Fixture File Structure
One fixture file per component, co-located with stories.

```
components/
  timesheet-overview-page/
    __fixtures__/
      timesheet-overview.fixtures.ts   -- page-level fixtures
    timesheet-overview-page.tsx
    timesheet-overview-page.stories.tsx
  timesheet-row/
    __fixtures__/
      timesheet-row.fixtures.ts
    timesheet-row.tsx
    timesheet-row.stories.tsx
  status-badge/
    __fixtures__/
      status-badge.fixtures.ts
    status-badge.tsx
    status-badge.stories.tsx
```

### Fixture Design Notes
- Each fixture file exports named constants matching story names: `export const DEFAULT_FIXTURE = { ... }`
- Fixtures use domain types (Layer 1), transformed via `toViewModel()` in the story file, then spread into component props. This proves all three type layers work together.
- Date values use deterministic dates (not `new Date()`) for visual regression stability.
- Fixture data tells a coherent narrative: Maria submitted her March timesheet, James needs to approve it. All fixtures share these same actors and this same scenario.
- Every fixture variation is annotated with which state (Section 4) it exercises.
```

---

### What This Document Does NOT Contain

These are explicitly out of scope for the Storybook handoff:

1. **Requirements or acceptance criteria** -- the Storybook agent does not validate against requirements. That is Product's job in Round 5 (coverage matrix).
2. **API integration details** -- Storybook uses fixtures, not real APIs. API integration happens during implementation, after Storybook iteration is complete.
3. **Routing or navigation logic** -- Storybook stories are isolated. Page-level stories mock navigation callbacks.
4. **State management approach** -- Redux/Zustand/context decisions happen during implementation. Storybook components receive props.
5. **Animation specifications** -- beyond `prefers-reduced-motion` notes in accessibility contracts, animation details are not needed to scaffold. They are added during the Style phase.

---

### Completeness Checklist

Before design-discovery dispatches the Storybook agent, it verifies:

- [ ] Every component in the tree (S2) has a props type in Layer 3 (S3)
- [ ] Every component with multiple states (S4) has a story per state (S5)
- [ ] Every component has an accessibility contract (S6)
- [ ] Actor constants are defined (S7)
- [ ] Fixture file structure matches the component tree (S7)
- [ ] No `TODO` or `TBD` placeholders remain in any section
- [ ] The user has approved the component tree and type layers

If any check fails, design-discovery continues iterating before dispatching.

---

### How This Connects to the Storybook Agent's Workflow

The Storybook agent (`ui-design-iterate-storybook`) receives this document and follows five phases:

| Phase | What happens | Uses which sections |
|-------|-------------|-------------------|
| **1. Scaffold** | Create all component files, story files, fixture files, type files | S2 (tree), S3 (types), S7 (fixture structure) |
| **2. Structure** | Write semantic HTML, ARIA roles, keyboard navigation | S6 (accessibility contracts) |
| **3. Style** | Apply Tailwind classes, responsive breakpoints, design tokens | S4 (states -- for conditional styling), S5 (responsive stories) |
| **4. Interact** | Wire callbacks, state transitions, `play()` tests | S3 Layer 3 (callbacks), S5 (story plan), S6 (keyboard patterns) |
| **5. Verify** | Run axe-core, test keyboard-only navigation, screen reader audit | S6 (accessibility contracts as verification criteria) |

The document is consumed linearly in Phase 1 (scaffold everything), then referenced per-component in Phases 2-5.

---

### Format Notes

- The entire document is a single markdown file. No external references except to the codebase.
- Type blocks use fenced TypeScript code blocks. They are copy-pasteable into `.ts` files.
- Tables use standard markdown. No HTML tables.
- The document should be 200-500 lines for a typical feature (1-3 pages, 5-15 components). If it exceeds 500 lines, the feature scope may be too large for a single Storybook iteration cycle -- consider splitting into sub-features.

---

## QA Strategist Review (2026-04-01)

### Role
QA Strategist -- reviewing the 5-round discovery process and its output artifacts for downstream testability. The question: if discovery misses something, QA will miss it too. What must discovery capture so that `manual-qa-case-writing` can produce thorough test cases without re-discovery?

---

### 1. Testability of Discovery Output

The current artifact set (conventions.md, state-inventory.md, flow-diagrams.md, interaction-specs.md, coverage-matrix.md) contains the raw material QA needs, but in a form that requires interpretation. The QA case writer has to read multiple files, mentally reconstruct flows, and infer what to test. This is where coverage gaps creep in.

**Recommendation: Add a `testability-map.md` artifact to Round 5 output.**

This document bridges discovery and QA directly. Structure:

```markdown
# Testability Map

## States (per page, per role)
| Page | Role | State | Entry condition | Exit condition | Verifiable assertion |
|------|------|-------|-----------------|----------------|---------------------|
| Timesheet list | Manager | Empty (no timesheets) | New org, no entries | Create first entry | "No timesheets yet" message visible, create button enabled |
| Timesheet list | Manager | Loading | Page navigation | Data loads | Spinner visible, table not rendered |
| Timesheet list | Manager | Error (API failure) | API returns 5xx | Retry or refresh | Error message with retry action visible |
| Timesheet list | Attendant | Permission denied | Direct URL, no role | N/A (dead end) | 403 page or redirect to allowed page |

## Flows (per role)
| Flow name | Actor | Precondition | Steps | Expected outcome | Failure outcome |
|-----------|-------|--------------|-------|-----------------|-----------------|
| Submit timesheet | Attendant | Timesheet in draft state | Open draft > fill hours > click submit | Status changes to "submitted", manager notified | Validation errors shown inline |
| Approve timesheet | Manager | Timesheet in submitted state | Open submitted > review > click approve | Status changes to "approved", attendant notified | If already approved by another manager, conflict message |

## Interactions (per component)
| Component | Interaction | Input | Expected behavior | Keyboard equivalent | Accessibility announcement |
|-----------|-------------|-------|-------------------|--------------------|-----------------------------|
| Approve button | Click | Mouse click / Enter / Space | Confirm toast, status updates | Enter or Space when focused | "Timesheet approved" announced to screen reader |
| Date picker | Open | Click input / Enter | Calendar overlay opens, today highlighted | Enter opens, arrows navigate days | "Calendar opened, [date] selected" |
```

The key insight: every row in this map is a test case waiting to be written. The QA writer does not need to re-discover -- they translate rows into checkbox format directly.

**Why this format works for `manual-qa-case-writing`:**
- Each row has a precondition (test setup), an action (what the tester does), and a verifiable assertion (what to check). This is exactly the structure QA needs.
- The role column lets QA group by profile, matching how `qa-execution` dispatches agents (one per role).
- The keyboard equivalent and accessibility announcement columns prevent the QA writer from having to guess what accessibility checks to write.

---

### 2. Coverage Gaps: What QA Typically Finds That Discovery Missed

Based on common failure patterns in QA execution, these categories are systematically under-discovered:

#### A. Permission boundaries and transitions

Discovery captures "what each role sees" (the role-based view matrix from Product's requirements). But QA consistently finds gaps at **permission boundaries**:

- User's role changes mid-session (e.g., promoted from attendant to manager while logged in)
- Cached permissions vs. server permissions diverge
- Deep links shared between roles (manager shares URL, attendant opens it -- what do they see?)
- Feature flags or plan-level gating (free vs. paid features visible but disabled)

**Recommendation for Round 3 (Discovery Walk-through), Level 1 (Roles):** Add a "permission boundary" sub-pass after roles are enumerated. For each role pair, explicitly ask: "What happens when Role A accesses something intended for Role B? What happens if a user's role changes while they are in an active session?"

#### B. Error recovery and retry semantics

The current process has Product requesting an "error recovery audit" (item 10 in Product's needs list), but it is not structurally embedded in the walk-through. Errors are discovered per-state ("error state exists"), but recovery paths are not.

**Recommendation for Round 3, Level 3 (States):** For every error state discovered, require these three follow-up questions:
1. What is the recovery action? (retry button, back navigation, re-enter data)
2. Is user data preserved during recovery? (form inputs retained, scroll position maintained)
3. Can the user reach a dead end with no recovery? (if so, what is the escape hatch?)

#### C. Concurrent user scenarios

The `qa-execution` skill already handles cross-role testing (manager creates, attendant sees). But discovery does not systematically enumerate concurrency cases. These are the bugs QA finds late:

- Two users edit the same entity simultaneously (optimistic locking, last-write-wins, conflict UI)
- One user deletes what another is currently viewing
- Real-time updates vs. stale cache (does the other user see the change without refreshing?)
- Notification timing (does the notification arrive before or after the UI reflects the change?)

**Recommendation for Round 3, Level 4 (Flows):** Add a "concurrency" sub-question for every state transition involving shared data: "What if another user has modified or deleted this entity between when the current user loaded the page and when they perform this action?"

#### D. Data boundary conditions

Discovery captures "data variations" through the propose-and-correct loop, but tends to focus on semantic variations (draft vs. submitted vs. approved) rather than volume and boundary conditions:

- Zero items, exactly one item, many items (pagination threshold, e.g., 25/50/100)
- Maximum field length (what happens to the UI when a name is 200 characters?)
- Decimal precision (currency displayed as $10 vs. $10.00 vs. $10.005)
- Date boundaries (timezone differences, daylight saving transitions, year boundaries)
- Unicode, RTL text, special characters in user-entered fields

**Recommendation for Round 3, Level 3 (States) and the conventions doc:** Add a "data boundaries" section per entity that lists: min/max counts, field length limits, numeric precision rules, date/time display rules including timezone handling. These become direct QA test cases.

---

### 3. QA-Specific States That Discovery Often Skips

These are states that exist in real user sessions but rarely appear in requirements or design conversations. Discovery must enumerate them explicitly, or QA will not test them.

**Add to Round 3 as a mandatory checklist -- the "Resilience States" pass.** After the standard states (loading, empty, error, permission-denied, populated) are enumerated per page, the team runs through this checklist:

| Resilience state | What to discover | Why QA needs it |
|-----------------|-----------------|-----------------|
| **Session timeout during multi-step flow** | What happens if the auth token expires between step 2 and step 3 of a multi-step form? Is draft data preserved? Does the user return to the correct step after re-auth? | Multi-step forms are common in this product (timesheet entry, schedule creation). A session timeout that loses data is a critical accessibility failure for users with motor disabilities who take longer to complete forms. |
| **Browser back button** | For every flow: what happens on back? Does the previous state load correctly? Is form data preserved? Are there any "are you sure?" guards? | Single-page apps frequently break back-button behavior. QA finds this in nearly every feature. |
| **Browser refresh mid-flow** | For every multi-step flow: what happens on F5/refresh at each step? Is state persisted (URL params, local storage, server-side draft)? | If refresh loses state, users with motor disabilities who accidentally trigger refresh lose all progress. |
| **Duplicate submission** | For every mutation (create, update, delete): what prevents double-submit? Is the button disabled after first click? Is there server-side idempotency? | Double-tap and accidental double-click are common with assistive input devices (switch access, eye gaze). |
| **Slow/degraded network** | For every async operation: what does the user see during a 5-second API call? 30-second? Timeout? Is there a loading indicator? Can the user cancel? | Users on institutional WiFi (care facilities) frequently experience degraded network. |
| **Large dataset / pagination edge cases** | If a list has exactly N items where N is the page size: is "load more" / "next page" shown? If items are added/removed during pagination, does the count stay consistent? | Pagination off-by-one errors are among the most common UI bugs. |
| **Interrupted file upload** | If the feature involves file upload: what happens if upload is cancelled mid-way? If the browser is closed during upload? If the file exceeds the size limit? | Relevant if any feature involves attachments or document upload. |
| **Stale tab** | User opens the app in two tabs. Performs action in Tab A. Switches to Tab B (which has old data). What happens when they interact with stale data in Tab B? | Real user behavior, especially for managers who keep the app open all day. |

**Recommendation:** This checklist becomes a structural part of Round 3. After the standard state enumeration at Level 3, the team walks through every row and asks: "Does this apply to this page? If yes, what is the expected behavior?" Answers go into the testability map.

---

### 4. The Bridge: Structuring Discovery Output for Direct QA Consumption

The goal is: `manual-qa-case-writing` should be able to read discovery artifacts and produce test cases without needing to ask the user for clarification or re-discover anything.

#### Current gap

Today, the QA case writer receives a work folder that might contain requirements, specs, and code. It has to do its own mini-discovery to understand states, flows, and interactions. This is where coverage drops -- the QA writer does not have the same depth of domain conversation that happened during discovery.

#### Recommended bridge structure

The discovery output folder should contain these files, in this order of QA consumption priority:

```
work-folder/
  requirements.md          -- (pre-existing, input to discovery)
  conventions.md           -- business rules, impossible states, display rules
  state-inventory.md       -- all states per page per role (from Round 3)
  flow-diagrams.md         -- state transitions with triggers and actors (from Round 3)
  testability-map.md       -- NEW: the QA-ready artifact described in section 1 above
  interaction-specs.md     -- per-component behavior, keyboard nav, focus management (from Round 4)
  responsive-specs.md      -- breakpoint behavior per page (from Round 4)
  coverage-matrix.md       -- ACs to artifacts mapping (from Round 5)
  component-tree.md        -- decomposition with props (from Round 5)
  types.ts                 -- three-layer types (from Round 5)
  fixtures.ts              -- per-component fixtures (from Round 5)
```

The `testability-map.md` is the primary QA input. It should be self-contained -- meaning a QA case writer should be able to produce comprehensive test cases from the testability map alone, referencing conventions.md and interaction-specs.md only for deeper detail.

#### Specific structural requirements for QA consumability

**A. Every state must have an entry condition and a verifiable assertion.**
Not just "empty state exists" but "empty state appears when [condition], shows [message], has [actions available]." Without this, the QA writer cannot construct test preconditions or verification steps.

**B. Every flow must have failure branches, not just happy paths.**
The flow diagrams should include: what triggers the flow, what the success path is, what every failure branch is, and where the user ends up on failure. QA cannot write negative test cases from happy-path-only flow diagrams.

**C. Role-based differences must be explicit, not implied.**
Instead of "Manager sees the approve button" (which implies attendant does not), state both: "Manager sees approve button. Attendant does NOT see approve button on submitted timesheets." QA needs the negative assertion to write the permission test.

**D. The testability map should tag each row with a test priority.**
Using: Critical (blocks core workflow), High (affects usability for target users), Medium (edge case that has workaround), Low (cosmetic or rare). This lets QA prioritize when time-constrained and matches how `qa-execution` handles stopping rules (3+ consecutive fails = stop).

**E. Cross-role flows must be documented as sequences, not separate per-role entries.**
For example:
```
Flow: Timesheet submission and approval
  Step 1: Attendant submits timesheet (precondition: draft state)
  Step 2: Manager receives notification (verify: notification appears)
  Step 3: Manager opens timesheet (verify: status shows "submitted")
  Step 4: Manager approves (verify: status changes to "approved")
  Step 5: Attendant receives notification (verify: notification appears)
  Step 6: Attendant opens timesheet (verify: status shows "approved", edit disabled)
```
This sequence maps directly to how `qa-execution` orchestrates cross-role testing with its `qa-manager` and `qa-attendant` agents, including the coordination cues ("tell attendant agent when to proceed after manager action completes").

---

### 5. Additions to Each Round

Summary of what should be added to the 5-round process to make QA thorough:

**Round 1 (Frame):**
- Add "QA complexity assessment" -- does this feature involve multi-step flows, cross-role interactions, real-time data, or file operations? If yes, flag for resilience state enumeration in Round 3.

**Round 2 (Approach Selection):**
- No changes needed. The approach choice does not affect QA.

**Round 3 (Discovery Walk-through):**
- Level 1 (Roles): Add permission boundary sub-pass (role transitions, deep link sharing, cached vs. server permissions).
- Level 3 (States): Add "Resilience States" checklist (session timeout, back button, refresh, duplicate submission, slow network, large datasets, stale tab). Add "Data Boundaries" section per entity (min/max counts, field lengths, numeric precision, timezone rules).
- Level 4 (Flows): Add concurrency sub-question for every state transition on shared data. Add explicit failure branches for every flow. Add cross-role flow sequences.
- Level 5 (Interactions): Add recovery path for every error-producing interaction (what is the undo? is data preserved? where does focus go after error?).
- New artifact: Begin populating `testability-map.md` incrementally during this round.

**Round 4 (Design):**
- Add responsive breakpoint edge cases to interaction-specs.md: what happens at exactly the breakpoint boundary? What happens when viewport is resized during an open modal/dropdown/tooltip?
- Storybook stories should include resilience states where feasible (error recovery state, loading timeout state).

**Round 5 (Specify):**
- Finalize `testability-map.md` with all states, flows, interactions, resilience states, and data boundaries.
- Coverage matrix should include a "QA coverage" column: for each acceptance criterion, which testability map rows cover it. This closes the loop -- requirements to discovery to QA.
- Add priority tags (Critical/High/Medium/Low) to every testability map row.
- Product sign-off should include: "Can every row in the testability map be turned into a pass/fail QA test case? If any row is ambiguous, clarify now."

---

### 6. Anti-Patterns to Call Out in the Skill

These are things that make discovery output untestable. The skill should explicitly warn against them:

| Anti-pattern | Why it hurts QA | Fix |
|-------------|-----------------|-----|
| "Error state exists" without specifying error type | QA cannot write specific assertions | Enumerate: API timeout, validation error, permission error, conflict error -- each with distinct UI |
| Flow diagrams with only happy path | QA cannot write negative tests | Every flow must show failure branches with where the user ends up |
| "Role X cannot see this" without listing what they see instead | QA cannot verify the alternative view | State both: what Role X sees AND what Role Y sees in the same scenario |
| States described without entry conditions | QA cannot set up the test | Every state needs: how to get there, what preconditions must hold |
| Interactions described without keyboard equivalent | QA skips keyboard testing | Every interaction must list mouse, keyboard, and assistive tech behavior |
| Implicit "same as desktop" for mobile | QA skips mobile-specific checks | Explicit responsive behavior per breakpoint, even if it is "no change" |
| Business rules in conversation but not in conventions doc | QA writer never sees them | Every correction from the user must be captured in conventions.md |

---

### Summary

The single most impactful change is introducing `testability-map.md` as a first-class discovery artifact. It transforms the discovery-to-QA handoff from "read all these files and figure out what to test" to "each row is a test case."

The second most impactful change is the Resilience States checklist in Round 3. These states (session timeout, back button, refresh, duplicate submission, slow network, stale tab) represent real user conditions that are almost never in requirements, rarely in design conversations, and frequently the source of bugs found in production.

Together, these two additions close the gap between what discovery knows and what QA tests.

---

## TODO for Next Session

1. Write the actual `design-discovery/SKILL.md` rewrite based on this log
2. Create `ui-design-iterate-storybook` skill
3. Decide whether `view-model-props` should be absorbed into Round 5 or remain standalone
4. Test the redesigned skill against a real feature
5. Integrate testability-map.md artifact into the Round 3/5 output specification
6. Add Resilience States checklist to Round 3 structure
7. Update `manual-qa-case-writing` skill to reference testability-map.md as primary input when available
