---
name: design-in-storybook
description: Build UI component variants in the project's Storybook. Scaffolds .tsx and .stories.tsx files for the variants in a given folder, applies the project's design system, and verifies visual rendering via Chrome MCP.
argument-hint: "[component or feature name]"
---

# Design in Storybook

Given a target folder, a component name, a list of variants to build, and design context, this skill produces working Storybook components with stories and verifies they render correctly in Chrome.

This skill does ONE thing: build the requested variants in the given folder and verify them. It does not manage iterations, collect user feedback, run reviews, or finalize anything -- it only renders.

## Memory

Read `memory.md` in this directory before starting. It contains learnings specific to building Storybook variants in this project. Append a learning at the end if the session produced something worth keeping.

## Inputs

Follow the context passed to you. If any of the following is missing, ASK before starting.

Required:

1. **Target folder** -- absolute path where files should be written
2. **Component / variations name** -- the kebab-case base name
3. **Component status** -- existing or new. If existing, the path to the current component file.
4. **Variants to build** -- a list of variants with: name, one-line hypothesis, 2-3 lines of design direction per variant
5. **Story title namespace** -- the prefix for Storybook story titles
6. **Data shape** -- the view model fields the variants must display, typed
7. **Critical states** -- the must-have states for these variants (default, loading, empty, error, etc.)
8. **Critical accessibility constraints** -- the must-haves (touch target sizes, ARIA roles, keyboard patterns)
9. **Design system pointers** -- cn utility import path, shadcn primitives expected, icon library, Tailwind class style reference

Optional:

10. **Seed variant** -- path to a previous iteration's chosen variant + notes on what to carry forward
11. **Self-check items** -- things to verify before returning

## Step 1: Discover the design system

Before writing any code, read 2-3 neighboring components in the same module. Look for:

- The `cn` utility import path (`@/core/utils` or similar)
- shadcn primitives used (`@/components/shadcn/card`, `@/components/shadcn/badge`, etc.)
- `lucide-react` icon usage and import style
- Tailwind class patterns
- Project type imports (e.g. `../../../types`)
- `'use client'` directive usage
- Function vs arrow component style

Copy the import style of a nearby component. Do NOT guess.

## Step 2: Build the variants

Create two files inside the target folder:

### File 1: `{name}.tsx`

Exports one React function per variant. Reuse shared helper functions at the top so each variant stays readable. All variants typed with project types. Use the project's design system primitives discovered in Step 1.

**Page wrapper requirement:** If the variant is a **page** or a **page-wide component** (something that occupies the full page width in production — e.g. a full page view, a full-width header/hero/banner, a page-level layout shell), wrap its top-level output in `<div className="body-container">`. This mirrors how it will be embedded in the real app layout and ensures Storybook renders use the same page padding/width constraints as production. Example:

```tsx
export function V1Timeline(props: Props) {
  return (
    <div className="body-container">
      {/* variant content */}
    </div>
  )
}
```

If the variant is NOT a page or page-wide component (e.g. a card, badge, button, form field, modal body, or any sub-component that lives inside a larger layout), do NOT add the wrapper. Those render as-is so they can be composed freely by their parents.

### File 2: `{name}.stories.tsx`

- Imports all variants from `./{name}`
- Declares shared sample data at the top, typed with project types, deterministic values, realistic narrative (e.g. coherent shift schedules, not lorem ipsum)
- Exports one story per variant
- Story `title` follows the namespace pattern: `{Story Title Namespace}/{VariantName}`

Example story title: `Exploration/PROD-111 Scheduling/Week Overview/Manager/V1 Timeline`

### Index file at the variations folder root (only if it does not already exist)

Create `{name}.stories.tsx` ONE LEVEL UP from the iteration folder (at the variations root, alongside `iteration-*/`). It is a stub whose only purpose is satisfying Storybook's glob:

```tsx
// Redirect -- active stories live in iteration-*/ subfolders.
import type { Meta } from '@storybook/nextjs-vite'

const meta = {
  title: '{Story Title Namespace}/_Index',
  tags: ['!autodocs', '!snapshot'],
} satisfies Meta

export default meta
```

If an index file already exists at the variations root, leave it alone.

### Build all variants in one pass

Build every variant in the iteration before stopping. No "here is V1, what do you think?" mid-build. The caller will run team review and user review afterward.

## Step 3: Chrome MCP UI verification

Verify each variant renders correctly in Storybook. This is for the agent, not the user.

1. Check if Storybook is running. If not, start it in the background using the project's command (typically `pnpm storybook` from the `apps/home` workspace inside the admin repo). Wait until it serves a port.
2. Use Chrome MCP to navigate to each variant's story URL (derived from the story title namespace).
3. For each variant, view at:
   - Mobile viewport (~375 wide)
   - Desktop viewport (~1280 wide)
4. Confirm the UI paints and no primary element is visually broken.
5. **IGNORE** TypeScript warnings and runtime console errors. This step is pure visual rendering verification -- type errors get addressed during implementation, not during exploration.

If a variant does not render at all (blank, infinite loop, structural failure), fix it silently and re-verify. Do not surface rendering failures to the caller -- fix them.

**Note:** Chrome MCP tools come from the `claude-in-chrome` MCP server. Load them via ToolSearch before first use.

## Step 4: Return to caller

Once all variants are built and verified, return to the caller with:

```
Built and verified {count} variants in {target folder}.
Story namespace: {Story Title Namespace}
Variants: {comma-separated variant names}
```

This skill is done. Anything beyond rendering -- team review, user handoff, feedback capture, new iterations, finalization -- is the caller's responsibility, not this skill's.

## Anti-patterns

| You're tempted to... | Reality |
|---|---|
| Create iteration folders yourself | No. The caller passes you the target folder. You write inside it. |
| Manage `user-feedback.md` | No. The caller owns that file. |
| Decide when to start a new iteration | No. The caller decides. You build into whatever folder you were given. |
| Promote a variant to `final/` | No. The caller does that on user signal. |
| Hand off to the user directly | No. Return to the caller, which handles the user handoff. |
| Skip Chrome verification | No. Visual rendering is the one verification this skill MUST do. |
| Guess at design system imports | No. Read a neighboring component first. |
| Show partial builds to the caller | No. Build all variants in this iteration before returning. |

## Rules

- ALWAYS write inside the target folder the caller provided -- never outside it
- ALWAYS read neighboring components for design system conventions before writing code
- ALWAYS wrap pages and page-wide components in `<div className="body-container">` so Storybook matches real app layout constraints — do NOT wrap sub-components (cards, badges, form fields, modals, etc.)
- ALWAYS verify rendering in Chrome MCP before returning to the caller
- NEVER touch iteration folder structure, user-feedback files, or final/ folder -- those are caller concerns
- NEVER hand off to the user directly -- return to the caller
