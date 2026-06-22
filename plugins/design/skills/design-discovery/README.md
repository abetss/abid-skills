# Design Discovery Skill -- README

A team-based design process that discovers everything about a UI feature **before** any visual design begins. Instead of the AI guessing at data variations and jumping to mockups, a simulated team of Lead Product Manager and Lead Designer walks through the feature with you, surfacing roles, pages, states, flows, interactions, and accessibility requirements through structured proposals and corrections.

---

## Why This Skill Exists

The previous version of this skill was a "data discovery" tool -- it produced TypeScript types and fixtures but skipped most of the actual design process. It missed:

- Problem framing before touching data
- Task flows with decision points
- Systematic state enumeration (loading, empty, error, permission-denied, etc.)
- Role-based view matrices
- Accessibility as architectural input, not a verification checklist
- Component decomposition with proper prop layers

This version is a complete redesign based on input from 7 experts (Lead Product Manager, Lead Designer, Claude Code Expert, AI Prompt Expert, Frontend Engineer, QA Strategist, Usability Critic) and every decision you made during the redesign session. The complete discussion lives in `log.md`.

---

## Core Idea: Propose and Correct

**Wrong proposals surface hidden rules faster than open-ended questions.**

Instead of asking "what states does this page have?" (which misses things), the team proposes a specific answer -- sometimes deliberately including items marked with `[?]` to signal uncertainty -- and you correct it. Each correction is a rule discovery that gets written down immediately.

Example:
```
Lead Designer: "For the timesheet list page, I think these states exist:
  - Loading (skeleton with 5 placeholder rows)
  - Populated
  - Empty -- never created
  - Empty -- filtered to zero [?]
  - Error -- API failure
  - [?] Degraded -- partial data loaded
  Am I missing anything?"

User: "We don't have partial data loading. But you're missing the
  'locked' state -- past-period timesheets are read-only."
```

The `[?]` markers explicitly invite correction. You never have to feel like you're rejecting the AI's work.

---

## File Architecture

```
skills/design-discovery/
├── README.md                     ← this file
├── SKILL.md                      ← the orchestrator (entry point)
├── frame.md                      ← Round 1: Frame
├── discover.md                   ← Round 2: Discovery Walk-through (the big one)
├── design.md                     ← Round 3: Design
├── specify.md                    ← Round 4: Specify (engineering handoff)
├── perspectives.md               ← team voice definitions
├── research-agents.md            ← agent dispatch templates
├── memory.md                     ← learnings from past sessions
├── log.md                        ← full redesign history (reference)
├── discovery-phase.md            ← Lead Designer's original analysis (reference)
└── discovery-phase-product.md    ← Lead Product Manager's original analysis (reference)
```

**How the files work together:**

`SKILL.md` is the orchestrator -- when the skill triggers, this is read first. It contains the overview, anti-rationalization table, and routing instructions. It tells the AI which round file to read next.

The four round files (`frame.md`, `discover.md`, `design.md`, `specify.md`) contain the full procedure for each round. They're loaded on demand -- the AI reads only the round it's currently in. This keeps the context window small.

`perspectives.md` and `research-agents.md` are referenced from multiple rounds. Team voice definitions are in perspectives; agent dispatch templates are in research-agents.

`memory.md` is read at the start of every session and written at the end. It captures important decisions and ways of thinking about the product that carry forward across sessions.

The reference files (`log.md`, `discovery-phase.md`, `discovery-phase-product.md`) are historical documentation -- they contain the redesign rationale and the original expert analyses. The AI doesn't read these during normal operation, but they're valuable for understanding why the skill is structured the way it is.

---

## The Four Rounds

### Round 1: Frame

**Goal:** Get everyone on the same page about what we're designing, for whom, and within what constraints.

What happens:
1. Read requirements.md (hard prerequisite -- if it doesn't exist, the skill stops and asks you to use write-requirements first)
2. Extract acceptance criteria as a numbered checklist (AC-1, AC-2, ...) that tracks through all rounds
3. Identify roles involved and scope boundaries
4. Assess whether optional team members are needed (UX Researcher, Accessibility Specialist, Data Architect, Content Strategist)
5. Choose the walk-through approach: role-first (default), page-first, hybrid, or flow-first
6. Dispatch research agents in the background: Schema Reader for database context, one or more Feature Scouts for product/knowledge base context
7. Initialize the progress file for session persistence

**Gate:** You confirm the framing summary, team composition, and approach choice.

### Round 2: Discovery Walk-through

**Goal:** Map the complete design surface -- every role, page, state, flow, and interaction -- through structured proposals that you correct.

This is the core of the skill. The team walks through five levels using the approach you chose in Round 1:

1. **Roles** -- who interacts with this feature, their goals, permissions, input methods
2. **Pages** -- what each role sees, primary actions, role-page matrix
3. **States** -- a systematic 21-category sweep per page (13 standard states plus 8 resilience states from QA)
4. **Flows** -- state transitions, lifecycle flows, destructive actions with undo, cross-role flows
5. **Interactions + Accessibility** (combined) -- per page, batched: click/tap, keyboard, ARIA role, focus management, screen reader announcement, touch targets, feedback

At each level, the team proposes and you correct. Each level has a gate: the team writes the artifact to disk, reviews it among themselves, then hands it to you for review. Nothing advances until you approve.

Everything goes into one `discovery.md` file under different section headings, with ASCII diagrams where helpful. No separate files for states/flows/interactions -- it's all one document.

**Gate:** Complete discovery document, you confirm nothing is missing.

### Round 3: Design

**Goal:** Turn the discovery document into visual designs you can review in the browser.

What happens:
1. Lead Designer proposes information architecture per page (layout, hierarchy, primary/secondary content)
2. Responsive strategy per page (what changes at each breakpoint)
3. Component decomposition tree (what's a component, layout, composition)
4. Dispatch an agent with `ui-design-iterate-storybook` skill to build designs in Storybook (preferred), or use `ui-asci-design` for quick ASCII wireframes
5. You review in the browser, give feedback, iterate until approved

**Gate:** Visual direction approved. Product Manager confirms every acceptance criterion has visual representation.

### Round 4: Specify

**Goal:** Produce everything engineering needs to build the feature.

What happens:
1. **Three-layer type system:**
   - Domain types (what the API returns)
   - View model types (transformed for UI, with computed fields like `can_edit`, `display_status`)
   - Component props (per-component slice + callbacks)
2. **Fixture data** per component per state
3. **Story plan** (Default, Empty, Loading, Error, With{Feature}, As{Role}, Mobile, Tablet)
4. **Coverage matrix** -- every acceptance criterion mapped to a specific artifact. No gaps allowed.
5. **Testability map** -- for QA downstream: every state/flow/interaction with entry condition, action, and verifiable assertion
6. **Storybook handoff document** -- the 7-section spec package engineering consumes

**Gate:** Coverage matrix complete. Product Manager confirms every AC is addressed. You sign off.

---

## Team Model

The team uses distinct voices in meeting transcript format. You're participating in a meeting, not reading a report.

### Core Team (Always Present)

**Lead Product Manager**
- Owns "what" and "why"
- Draws from requirements, acceptance criteria, business rules, role permissions, compliance
- Catches missing coverage and scope creep
- Speaks with specific AC references: "AC-3 says managers can approve..."

**Lead Designer**
- Owns "how"
- Draws from accessibility heuristics, interaction patterns, state completeness, responsive strategy
- Proposes layouts, interactions, states
- Speaks with principles: "For switch users, confirm dialogs cost 3 extra interactions..."

### Optional Team Members (Assessed in Round 1)

The core team decides during Round 1 whether additional expertise is needed. You confirm:

- **UX Researcher** -- when personas need deeper analysis or user behavior data exists
- **Accessibility Specialist** -- when interaction patterns are complex (forms, tables, drag-drop, multi-step flows)
- **Data Architect** -- when the data model is new or crosses multiple services
- **Content Strategist** -- when labeling, tone, empty state copy, or error messages need special attention

### How the Team Disagrees Productively

When Lead Product Manager and Lead Designer disagree, they present both sides with trade-offs and let you decide. Example:

```
Lead Product Manager: "AC-7 requires confirmation before destructive actions.
  I'd expect a confirm dialog on timesheet deletion."

Lead Designer: "Confirm dialogs add 3 interactions per deletion. For a user
  who deletes 20 timesheets per day, that's 60 extra clicks. The undo-toast
  pattern is more accessible -- delete immediately, show a 10-second undo."

Options:
  1. Confirm dialog -- simpler, matches AC-7 literally
  2. Undo toast (10s) -- better for switch users, requires soft-delete backend
  3. Undo toast for single deletes, confirm dialog for bulk deletes

Which fits?"
```

You make the call. The team documents your decision in the conventions section of `discovery.md`.

---

## Research Agents

Dispatched during Round 1, they run in the background while you continue with approach selection. Results are ready by the time Round 2 begins.

### Schema Reader
One agent that reads the database schema (ZenStack/Prisma models) and reports fields, relationships, enums, and access policies. Facts only, no opinions.

### Feature Scout
One or more agents (dispatched in parallel if multiple features to examine) that:
- Take screenshots of the current feature in the browser using Chrome MCP
- Read `a-kb/product-guide/` and `a-kb/` knowledge base for domain context
- Look at analogous features in the app, take screenshots if useful
- Report back with screenshots, domain knowledge, and patterns found

Each Feature Scout reports facts and observations, not design proposals. The team uses their findings during the walk-through to make better proposals.

---

## Session Persistence

Design discovery is a long process. If you get interrupted, you can resume.

A progress file lives in the work folder:

```
{work-folder}/design-discovery-progress.md
```

It tracks:
- Current round and level
- Gates passed / pending
- Which artifacts have been written
- Chosen approach and team composition

When you re-invoke the skill, it reads this file and offers to resume from where you stopped.

---

## Anti-Patterns the Skill Guards Against

The SKILL.md contains an anti-rationalization table (inspired by the debugging skill) that lists thoughts the AI should recognize as signals it's cutting corners. Examples:

| You're thinking... | Reality |
|---|---|
| "We already covered states implicitly when discussing pages" | Implicit coverage means no one checked. Make it explicit. |
| "Accessibility can be added later" | Accessibility is architecture. Retrofitting costs 10x. |
| "This is a simple feature, we can go faster" | Simple features have the most undiscovered edge cases. |
| "I'll propose what I think is right" | Propose what might be WRONG. Corrections are more valuable. |

---

## Integration With Other Skills

**Upstream (before design-discovery):**
- `upliv:product:write-requirements` -- hard prerequisite. Design discovery requires `requirements.md`.

**Downstream (after design-discovery):**
- `ui-design-iterate-storybook` -- dispatched during Round 3 to build designs in Storybook (TO BE CREATED)
- `ui-asci-design` -- alternative for quick ASCII wireframes during Round 3
- `upliv:product:plan-prep` -- consumes the discovery document and `view-model-props.md` for planning
- `view-model-props` -- produced during Round 4 as part of the handoff document

---

## Outputs Written to Disk

The skill produces one main document and several supporting artifacts in the work folder:

```
{work-folder}/
├── discovery.md                      ← main document (grows incrementally through Round 2)
├── design-discovery-progress.md      ← session state (for resuming)
└── view-model-props.md               ← Round 4: component prop interfaces + prop values per state
```

Round 3 (Design) produces Storybook components directly, or ASCII wireframes in `ui-design/` if that path is chosen.

---

## Memory

The skill captures important learnings from each session to `memory.md`:

- Important design decisions and their rationale
- Important ways of thinking about the product
- Important ways of thinking about the users

Not everything -- only what would change how you approach the next discovery session. Memory is read at the start and appended to at the end.

---

## Prerequisites Checklist

Before invoking this skill, make sure:

- [ ] `requirements.md` exists (use `upliv:product:write-requirements` if not)
- [ ] You have 45-60 minutes available (this is a deep process, though you can resume later)
- [ ] You know which feature you're designing
- [ ] The current state of the feature is available in the browser (for Feature Scout to screenshot), if it exists
- [ ] The knowledge base at `a-kb/product-guide/` is up to date with current domain knowledge

---

## Known Limitations

1. **`ui-design-iterate-storybook` does not exist yet.** Round 3 references it as the preferred path, but the skill itself has not been created. Until it exists, Round 3 falls back to `ui-asci-design`.
2. **The process is always Deep.** Light and Standard tracks (for simple features) were discussed but deferred to future work.
3. **Performance and build failure debugging are out of scope.** Use the `debugging` skill for those.
4. **This skill is opinionated about accessibility.** The product serves people with movement disabilities, so accessibility is treated as architectural input, not a verification checklist. If you're designing for a different audience, adjust accordingly.

---

## Getting Started

1. Ensure `requirements.md` exists for the feature
2. Invoke the skill: `/design-discovery [feature name]`
3. Follow the meeting -- the team will propose, you correct, and everything gets documented
4. Each gate is a natural stopping point if you need to pause

The skill is designed to be thorough. Don't rush it. Most features take 45-60 minutes through all four rounds.
