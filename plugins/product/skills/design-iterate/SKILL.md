---
name: design-iterate
description: Use when designing or refining a UI component or page through multiple iterations of variants and feedback rounds.
argument-hint: "[feature or component name]"
---

# Design Iterate

Owns the full design iteration lifecycle: planning variants, managing iteration folders, team internal review, user feedback, and finalization. The actual rendering of variants (ASCII wireframes or Storybook components) is delegated to the medium-specific child skills `design-in-asci` and `design-in-storybook`.

**Core principle:** The user never sees half-baked work. Team reviews internally first, the rendering layer verifies output, then the user reviews polished variants.

## Memory

Read `memory.md` in this directory before starting (if it exists). It captures patterns and decisions from past iteration sessions worth carrying forward.

## Team voices

Read `/Users/abtinghods/.claude/skills/design-discovery/perspectives.md` for the Lead Product Manager and Lead Designer voices. The team internal review uses these voices in a meeting transcript format. You speak as named characters, not as a narrator.

## Step 1: Detect invocation mode

Before asking the user anything, determine which mode you are in.

- **Look for a design brief**: if the caller passed a path to a `design-brief-{component}.md` file (or one is in the work folder), you are in **design-discovery mode** and the brief is your single source of truth. Read the brief fully. Do NOT read `discovery.md` unless the brief explicitly tells you to look something up there.
- **No brief provided**: you are in **standalone mode**. You will gather inputs from the user directly.

```
Product:  "Checking for a design brief..."
[looks for design-brief-{component}.md path passed by caller, or in the work folder]
Product:  "Found design-brief-shift-card.md -- design-discovery mode. The brief
           tells me the component, data shape, states, flows, interactions, and
           accessibility constraints. I only need to ask about medium, variant
           count, and variant directions."
```

**Why a focused brief and not the full discovery.md:** discovery.md captures everything across the whole feature -- every role, every page, every state. Reading it all would bloat your context window, slow down iteration cycles, and degrade your ability to make accurate decisions about THIS component. The brief is the contract -- it carries forward only what's needed for the component you're designing right now.

## Step 2: Gather inputs

Ask only the questions whose answers are NOT already known. In design-discovery mode, the brief answers most questions already -- skip any input that the brief covers.

Required:

1. **What are we designing?** -- feature or component name (from discovery: feature section)
2. **Where does it live?** -- target admin repo, module, component name. If not obvious, look at cwd, git remote, or discovery's component tree. ASK if ambiguous.
3. **Existing component vs new** -- search the module for a matching component file. ASK if in doubt.
4. **Reference designs** -- screenshots, Figma, analogous features, code to match
5. **How many variants for iteration-1** -- never assume. ASK.
6. **Variant directions** -- what hypotheses are we exploring? (e.g. "info-dense vs minimal vs timeline-first")
7. **Medium: ASCII or Storybook?** -- see Step 3
8. **Ticket / namespace** -- for story title or wireframe title. Often in discovery.

## Step 3: Choose ASCII or Storybook

Always ask unless the user already specified. Give a short recommendation.

- **ASCII (`design-in-asci`)** -- fastest for layout, information architecture, motor-accessibility checks. Best when structure is still being debated. Cheap to throw away.
- **Storybook (`design-in-storybook`)** -- real components in the browser with real theme, tokens, and states. Best for color, spacing, interaction, responsive behavior. Closer to production.

```
Designer: "Recommendation: Storybook. This is an upliv project and you prefer
           iterating in real components. ASCII is still available if you want
           wireframes first."
User:     [picks]
```

Lock in the choice. The variations folder structure will be the same regardless of medium -- only the file format inside differs.

## Step 4: Locate or create the variations folder

The folder pattern (matching the canonical `shift-card-variations` example):

```
{project root}/apps/home/modules/{module}/components/{component-name}-variations/
```

Steps:

1. Glob for an existing `{component-name}-variations/` folder under `apps/home/modules/**/components/`. If found, use it. If multiple modules could host it, ASK.
2. If not found, create it. The parent `components/` folder must already exist -- verify before creating.
3. Read any existing `iteration-*/` folders to understand history.

## Step 5: Determine the iteration number

- **Default**: the next iteration is `iteration-{N+1}` where N is the highest existing iteration number.
- **First time ever**: create `iteration-1/`.
- **Update in place**: if the user explicitly says "stay in the same folder" or "tweak this one", overwrite files inside the current `iteration-N/`.
- **Never delete earlier iterations.** They are history. Only `final/` gets promoted at the end.

If iteration-{N+1} is a refinement of iteration-N, seed it from the previous iteration's strongest variant. Iterations are refinements, not blank-slate redraws, unless the user explicitly asks for a fresh start.

## Step 6: Plan the variants (with the user)

Propose the variants to the user before any building happens. Each variant is a hypothesis, not a cosmetic tweak.

```
Designer: "For iteration-{N}, I propose {count} variants:
           - V1 {name}: {one-line hypothesis}
           - V2 {name}: {one-line hypothesis}
           - V3 {name}: {one-line hypothesis}
           Naming is descriptive. Fine?"
Product:  "V2 needs to still show {business field} per AC-{X}."
User:     [confirms or adjusts]
```

Naming convention: keep variants distinct and meaningful. Do NOT formalize a rule -- just make sure each variant's name describes its philosophy.

## Step 7: Write the iteration brief

Before dispatching the rendering layer, write `iteration-brief.md` inside the current iteration folder. This is the focused context the rendering layer reads -- it does NOT read `discovery.md`, `design-brief.md`, or any other upstream document.

**Why a brief and not the full design context:** The rendering layer's job is small -- scaffold files, verify they render. It does not need the entire feature context. Forcing it to ingest the design-brief or discovery.md would bloat its context window and slow down each iteration cycle.

Path: `{variations folder}/iteration-{N}/iteration-brief.md`

**Iteration brief contents:**

```markdown
# Iteration {N} Brief

## Target
- **Folder:** {absolute path to this iteration folder}
- **Component name:** {kebab-case base name, e.g. shift-card-variations}
- **Component status:** {existing | new}
- **Path of existing component (if existing):** {absolute path}

## Variants to build
For each variant:
- **{Variant name}** -- {one-line hypothesis}
  - {2-3 lines of specific design direction}

## Medium
{ASCII | Storybook}

## Story title namespace (Storybook only)
{e.g. Exploration/PROD-111 Scheduling/Week Overview/Manager}

## Data shape
The view model fields the variants must display. Pull only what's relevant from the design brief.
```typescript
type {ComponentName}Props = {
  // only the fields actually used
}
```

## Critical states
The states the variants must support (default, loading, empty, error, etc.). Just the must-haves -- not every state from the discovery state inventory.

## Critical accessibility constraints
The accessibility rules that must be enforced. Examples:
- Touch targets >= 48px
- Keyboard operable (Tab, Enter, Escape)
- ARIA role: {role}
- Focus management: {behavior}
Skip the entire 13-category checklist -- just the must-haves for this component.

## Design system pointers
- `cn` utility import: {path}
- shadcn primitives expected: {list}
- Icon library: {lucide-react | other}
- Tailwind class style: {pointer to a neighboring component}

## Seed variant (if refining)
- Path: {path to the previous iteration's chosen variant}
- What worked: {one-line carry-forward}
- What feedback to apply: {one-line summary from user-feedback.md of the previous iteration}

## What the team internal review will check
The rendering layer should self-check before returning so the team review goes smoothly:
- {checklist item 1}
- {checklist item 2}

## Pointer to design brief (if more context needed)
{absolute path to design-brief-{component}.md, if one exists}
```

Keep the brief tight -- 30-80 lines is the target. When in doubt about what to include, lean toward the must-haves. The pointer to the design brief lets the rendering layer go deeper if needed.

## Step 8: Dispatch the rendering layer

Hand control to the medium-specific child skill to actually build the files.

- If the user chose **ASCII**, read `/Users/abtinghods/.claude/skills/design-in-asci/SKILL.md` fully and follow its instructions for the current task.
- If the user chose **Storybook**, read `/Users/abtinghods/.claude/skills/design-in-storybook/SKILL.md` fully and follow its instructions for the current task.

Tell the rendering layer: "Read `{absolute path to iteration-brief.md}` for everything you need. Do NOT read the design brief or discovery.md unless the iteration brief tells you to."

The rendering layer will scaffold files inside the target folder and verify rendering. It does NOT manage the iteration folder structure, user feedback, team review, or finalization -- those are owned here.

Do NOT spawn a Task/agent. The child skill runs in the same thread.

## Step 8: Team internal review (CRITICAL -- before user sees anything)

After the rendering layer returns, the Lead Product Manager and Lead Designer review the variants among themselves. The user does NOT participate in this step. Present it as a short meeting transcript inside your own response.

```
Designer: "V1 leads with the timeline because {rationale}. V2 hides backup
           availability behind an expand, trading density for clarity."
Product:  "V2 loses the backup count at a glance -- managers scan that first.
           Can you pull the count up into the header?"
Designer: "Fair. I will bring it forward in V2."
```

Rules for the internal review:

- Critique against discovery conventions (in design-discovery mode), accessibility rules (48px+ targets, no hover-only interactions, keyboard-operable), and the user's stated design direction.
- If either voice finds something broken, return to Step 7 -- have the rendering layer fix the variant -- before the user ever sees it.
- Only stop internal review when both voices agree the iteration is presentable.
- Catch obvious issues yourself. The user should not have to tell you V2 is missing a button.

Do NOT write the team review to disk. It is a runtime conversation, not an artifact.

## Step 9: Create user-feedback.md

Before handing off to the user, create `user-feedback.md` inside the current iteration folder with an empty template:

```
# Iteration {N} -- User Feedback

<!-- Feedback is appended below in order. Multiple rounds of feedback in the
     same iteration get stacked. -->
```

## Step 10: Hand off to the user

Once team review and rendering verification are done, say exactly this (adjusted for the actual title):

```
Ready for review -- iteration-{N} at {target folder}.
{Storybook only: Story namespace: Exploration/{TICKET} {Feature}/{Page}/{Role}/}
```

Do NOT paste screenshots. Do NOT paste URLs. Do NOT summarize variants again in detail. The user navigates and reviews. Wait for feedback.

## Step 11: Capture feedback

When the user gives feedback, append it to `user-feedback.md` in the CURRENT iteration folder. Multiple rounds during the same iteration stack on the bottom.

```
## Round 1 -- {date}
{user's words}

## Round 2 -- {date}
{user's follow-up}
```

## Step 12: Apply feedback

- **Default behavior**: ANY substantive feedback starts a new iteration. Return to Step 5 (increment iteration number), then Step 6 (plan variants based on feedback), then Step 7 (dispatch rendering), then Step 8 (team review), then Step 10 (hand off). Seed the new iteration from the previous iteration's strongest variant.
- **Exception**: If the user explicitly says "stay in the same folder", "update in place", or "tweak this one", update the CURRENT `iteration-N/` files and append feedback rounds to the existing `user-feedback.md`.

The new variant count may change if the user asks. After applying feedback, repeat Steps 7-10.

## Step 13: Finalize

When the user says "this is final", "approved", "ship it", or similar:

1. Create `final/` in the variations folder if it does not exist.
2. Copy the chosen variant(s) into `final/` with clean file names (drop the `-variations` suffix if it reads better as a real component name).
3. For Storybook: create a `final.stories.tsx` titled `Exploration/{TICKET} {Feature}/{Page}/{Role}/Final`.
4. For ASCII: copy the chosen variant's subfolder into `final/`.
5. Leave all `iteration-*/` folders in place. They are history.
6. Write `design-result.md` at the variations folder root (next to iteration-*/ and final/).
7. Announce completion in one line.

### `design-result.md` contents

This is the focused handoff document the caller (design-discovery Round 4 or whoever invoked design-iterate) reads to know what was decided. The caller does NOT need to dig through every iteration folder.

```markdown
# Design Result: {ComponentName}

## Final iteration
- **Iteration number:** {N}
- **Folder:** {absolute path to final/}

## Chosen variant
- **Name:** {variant name}
- **Hypothesis it explored:** {one-line}
- **Why this one:** {one-line summary of why the user picked it}

## Key design decisions (during iteration)
- {decision 1 -- e.g. "Used undo-toast pattern instead of confirm dialog"}
- {decision 2 -- e.g. "Backup attendant count moved to header for at-a-glance scan"}
- {decision 3}

Each decision should be a one-liner. Focus on what the next phase (engineering, view-model-props, plan-prep) needs to know.

## Deviations from the design brief (if any)
List anything that ended up different from the original design brief, with reason.
- {deviation -- reason}

## Iterations summary
- iteration-1: {one-line direction explored, why we moved on}
- iteration-2: {one-line}
- iteration-3 (final): {one-line}

Skip if there's only one iteration.

## Pointers
- Final code: {path to final/}
- View model props: `view-model-props.md` (in this folder, produced after design-discovery Round 4 if applicable)
- Design brief (if discovery mode): {path to design-brief-{component}.md}
- discovery.md: {path, if discovery mode}
```

Keep `design-result.md` tight -- aim for under 50 lines. The point is a fast handoff, not another full document.

## Step 14: Return to the caller

- **Standalone mode**: print a short summary -- what was designed, where the artifacts live, how many iterations -- and exit cleanly.
- **Design-discovery mode**: print the summary AND this exact line:

  ```
  Return to design-discovery Round 4: read design-discovery/specify.md
  ```

## Anti-patterns

If you catch yourself thinking any of these, STOP.

| You're tempted to... | Reality |
|---|---|
| "I'll show V1 to the user while I build V2" | No. The user sees nothing until the whole iteration is built, team-reviewed, and verified. |
| "Team review is overhead, skip it" | Team review catches obvious bugs so the user does not have to. Never skip. |
| "Feedback is minor, I'll update in place" | Default is a new iteration. Only update in place if the user explicitly says so. |
| "I'll let the rendering layer handle iteration folders" | No. Iteration folder logic is YOURS. The rendering layer just writes inside the folder you give it. |
| "I'll let the rendering layer manage user-feedback.md" | No. That file is yours. |
| "I'll let the rendering layer hand off to the user" | No. The rendering layer returns to you. You hand off to the user. |
| "Variants 1 and 2 look similar -- the user can pick anyway" | Variants must be hypotheses, not cosmetic tweaks. If two variants explore the same idea, redesign one. |
| "I'll start iteration-N+1 without feedback" | Never. Iterations are driven by feedback. No feedback, no new iteration. |

## Rules

- ALWAYS read `perspectives.md` before starting -- you need the team voices
- ALWAYS run team internal review before user handoff
- ALWAYS create `user-feedback.md` in every iteration folder
- ALWAYS create a new iteration folder for substantive feedback (unless user says otherwise)
- ALWAYS keep past iterations -- history is the point
- NEVER touch the file rendering details inside iteration folders -- delegate to `design-in-asci` or `design-in-storybook`
- NEVER skip team internal review
- NEVER hand off half-built work to the user
- NEVER let the rendering layer manage iteration state
