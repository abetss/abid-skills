# Round 3: Design

> After discovery is complete, the team creates visual designs the user can review and approve.
> This round runs by default. The user can opt out -- they will tell you. Do not ask.

## Goal

Turn the discovery output (from Round 2's `discovery.md` sections) into visual designs the user reviews and approves in the browser. Discovery answered "what happens when?" -- Design answers "what does it look like?"

**Input:** Complete discovery document (roles, pages, states, flows, interactions, accessibility contracts).
**Output:** Approved visual direction with Storybook components per page/state/breakpoint.

---

## Step 1: Information Architecture

Designer proposes layout, hierarchy, and content priority per page.

```
Designer: "For [Page], the information architecture is:
  Primary:   [What dominates -- e.g., data table, form, detail card]
  Secondary: [Supporting -- e.g., filters, status summary, sidebar nav]
  Tertiary:  [Contextual -- e.g., help text, metadata, audit trail]
  Grouping:  [What's grouped together and why]"

Product:  "Does this serve AC-[N]? I expected [data] more prominent because [reason]."
User:     [Corrects priority, grouping, or placement]
```

Every page gets an IA proposal. No page proceeds to visual design without approved IA.

---

## Step 2: Responsive Strategy

Designer proposes what changes at each breakpoint.

```
Designer: "For [Page]:
  Desktop (1280px+): [Full layout -- sidebar + table + bulk action bar]
  Tablet  (768px):   [What reflows -- sidebar collapses, table condenses]
  Mobile  (375px):   [What stacks -- table becomes cards, filters become bottom sheet]
  Nothing hides -- all content accessible at all breakpoints."

Product:  "On mobile, can the manager still approve? Must work at every breakpoint."
```

---

## Step 3: Component Decomposition

Designer proposes the component tree.

```
Designer: "[PageName] [page]
    [LayoutName] [layout] -- [structure]
      [SectionA] [section] -- [purpose]
        [ComponentX] [component] -- [purpose]
      [SectionB] [section] -- [purpose]
        [CompositionZ] [composition] -- [composed of what]"

Product:  "Where does [business state] render? Missing component for [edge case]."
```

Types: `[page]`, `[layout]`, `[section]`, `[component]`, `[composition]`.
Every leaf must map to a state in the discovery state inventory.

---

## Step 4: Extract Design Brief (per component)

Before dispatching design-iterate, extract a focused **design brief** for each component being designed. The brief is a focused slice of `discovery.md` -- it contains ONLY what design-iterate and the rendering layers need for THIS specific component, not the full feature.

**Why a brief and not the full discovery.md:** Downstream skills must read context. discovery.md captures everything (every role, every page, every state, every flow). Forcing design-iterate, design-in-storybook, and design-in-asci to ingest the entire monolithic document bloats their context windows, slows iteration cycles, and degrades AI accuracy. The brief is a contract -- it carries forward only what's needed.

Write the brief to: `{work-folder}/design-brief-{component-name}.md`

**Brief contents (per component):**

```markdown
# Design Brief: {ComponentName}

## What we're designing
- Component name + intended location in the codebase
- One-paragraph purpose

## Roles
The role(s) that interact with this component, from the discovery role inventory.
For each role: their input methods (mouse, keyboard, switch, eye gaze, voice).

## Data shape
The view model fields this component displays. Slice from the discovery state inventory and convention sections -- only the fields RELEVANT to this component.

## States
The states this component can be in (from the discovery state inventory).
Format: `state name -- one-line description -- what triggers it -- what UI shows`.

## Flows
The flows this component participates in (from the discovery flow section).
Format: `[State A] --trigger--> [State B] -- who can trigger -- what fails look like`.

## Interactions + Accessibility
Per interactive element: click/tap, keyboard, ARIA role, focus management, screen reader announcement, touch target size.
Pull from the discovery interactions section.

## Acceptance Criteria
The AC IDs from requirements that apply to this component, with one-line descriptions.

## Conventions
The display/business rules from `discovery.md` conventions section that apply to this component.

## References
- Screenshots, Figma links, analogous components
- Pointer to the full discovery: `{absolute path to discovery.md}`
```

**Slicing rules:**

- **When in doubt, include it.** A slightly bloated brief is better than a missing constraint.
- Always include the pointer to the full discovery so the rendering layer CAN go deeper if needed.
- One brief per component being designed. If Round 3 designs 5 components, write 5 briefs.
- Briefs are written by design-discovery -- not by design-iterate.

## Step 5: Design Execution (per component)

For each component, dispatch design-iterate with the path to its brief:

Read and follow the `design-iterate` skill. It owns the full iteration lifecycle (variant planning, iteration folders, team internal review, user feedback, finalization) and dispatches the medium-specific rendering layers `design-in-asci` or `design-in-storybook` based on the user's choice.

When you dispatch, tell design-iterate: "Read `{absolute path to design-brief-{component-name}.md}` as the focused context for this iteration session. Do NOT read discovery.md unless the brief explicitly tells you to look something up."

When `design-iterate` finishes (the user has signaled "this is final" and a `final/` folder has been promoted), it writes a `design-result.md` summarizing the chosen variant and key decisions. The main thread returns here to complete Step 6 (Coverage Validation) and the Round 3 gate.

**Why a separate iteration skill:** design-discovery already runs long. By delegating the iteration lifecycle to design-iterate, this round stays focused on the design hand-off rather than re-implementing variant planning, folder management, and feedback loops. design-iterate is also reusable standalone outside of design-discovery.

---

## Step 6: Validate Coverage (after design-iterate finishes)

When design-iterate hands control back, Product Manager reads the `design-result.md` it produced and validates that the final/ folder covers all the discovered states and acceptance criteria for the component.

```
Product:  "Let me check the final/ folder against the discovery doc:
  - Every state from Round 2 has a corresponding story? [yes/no]
  - Every AC from requirements is visually represented? [yes/no]
  - Responsive behavior preserved at all breakpoints? [yes/no]"
```

If gaps exist, return to design-iterate for another iteration before advancing.

---

## Artifacts

The actual design artifacts (component variants, stories, sample data, user-feedback logs) live in the iteration folders managed by design-iterate's child skill, NOT in the work folder. Design-discovery's work folder only contains the discovery and progress files.

The iteration folders typically live at:
`{repo}/apps/home/modules/{module}/components/{component-name}-variations/`

with `iteration-1/`, `iteration-2/`, ..., `final/` subfolders.

---

## Gate

**Design direction approved by user** -- the user has explicitly said "this iteration is final" during design-iterate, and the chosen variant has been promoted to the `final/` folder. Product confirms every AC has visual representation. If any AC lacks coverage, return to design-iterate before advancing to Round 4: read `specify.md`.
