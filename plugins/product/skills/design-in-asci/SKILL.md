---
name: design-in-asci
description: Build UI mockups as ASCII wireframes (markdown) or HTML visual prototypes. Produces variants in the given folder. Both formats optimized for motor accessibility.
---
# Design in ASCII

## Overview

Given a target folder, a list of variants to build, and design context, this skill produces ASCII markdown wireframes (for layout and information architecture) or HTML visual prototypes (for color, spacing, and visual treatments) inside that folder.

This skill does ONE thing: build the requested variants in the given folder. It does not manage iterations, collect user feedback, run reviews, or finalize anything -- it only renders.

Both formats are optimized for motor accessibility.

## Inputs

Follow the context passed to you. If any of the following is missing, ASK before starting.

Required:

1. **Target folder** -- absolute path where files should be written
2. **Component / page name** -- the kebab-case base name
3. **Variants to build** -- a list of variants with: name, one-line hypothesis, 2-3 lines of design direction per variant
4. **Data shape** -- the relevant content the wireframes must depict
5. **Critical states** -- the must-have states for these variants (default, loading, empty, error, etc.)
6. **Critical accessibility constraints** -- the must-haves (touch targets, keyboard nav, no hover-only interactions, etc.)
7. **Format** -- ASCII or HTML

Optional:

8. **Reference material** -- screenshots, analogous features, current implementation

## Format Decision

ASCII (`.md` files) or HTML (`.html` files)?

- **ASCII** -- best for layout, information architecture, content hierarchy
- **HTML** -- best for colors, spacing, badges, visual treatments

**Ask the user** which format if unclear. Default to ASCII for full-page layouts, HTML for component-level iteration.

## Motor Accessibility (MANDATORY — Both Formats)

Users may have: no hand movement, limited dexterity, reliance on switch devices, eye-tracking, or voice control.

- **ALL interactive elements**: minimum 44x44px (11 chars wide in ASCII)
- **Spacing between targets**: minimum 8px (2 chars in ASCII)
- **NO hover-dependent interactions** (tooltips OK for supplementary info only)
- **Tab order**: sequential, logical, skip-to-content first
- **Keyboard shortcuts**: for ALL primary actions
- **Large form fields**: minimum 48px height
- **NO timed interactions** or auto-dismiss
- **Sticky navigation**: accessible without scrolling
- **Large click areas**: entire row/card clickable, not just icon

## Variants

The caller decides how many variants and what they explore. You build whatever the caller asks for. Do NOT impose your own A/B/C variation count.

When the caller passes variants, each one comes with a name and a one-line hypothesis (e.g. "V1 Maximum Simplicity -- 60px+ targets, switch-friendly"). Build that variant per its hypothesis.

## Output Structure

The caller (`design-iterate`) gives you a target folder. You write inside it -- you do NOT create or manage iteration folders yourself.

### ASCII Format

Inside the target folder, create one subfolder per variant. The variant names come from the caller.

```
{target-folder}/
  {variant-1-name}/
    desktop.md
    tablet.md
    mobile.md
  {variant-2-name}/
    desktop.md
    tablet.md
    mobile.md
  ...
```

### HTML Format

```
{target-folder}/
  {variant-1-name}/
    mockup.html
  {variant-2-name}/
    mockup.html
  ...
```

Each HTML file contains all 3 viewports stacked in one page: **desktop → mobile → tablet**. Width-constrained containers with dashed borders. Self-contained — open in any browser, no build step.

## ASCII Reference

### Viewport Specifications

| Viewport | Width      | Sidebar   | Content Width | ~Chars |
| -------- | ---------- | --------- | ------------- | ------ |
| Desktop  | 1280px+    | 400px     | 880px         | ~100   |
| Tablet   | 768-1023px | 400px     | 368-624px     | ~46-78 |
| Mobile   | <768px     | collapsed | ~343px        | ~43    |

### Template

Each `.md` file includes:

1. **Philosophy** — 1-2 sentences on accessibility approach
2. **Keyboard Shortcuts** table
3. **Layout** — ASCII box drawing with labeled regions
4. **Accessibility Annotations** — tab order, focus indicators, target sizes

Use `[*element*]` notation for focus indicators. Use `┌─┐│└─┘` for box drawing.

## HTML Reference

**CRITICAL: Tailwind CDN v3 + oklch colors gotcha.** See @html-reference.md for:

- Full HTML template
- Tailwind CDN color workaround (must define CSS utility classes manually)
- How to extract and use project theme variables

## Process

1. **Ask format** — ASCII or HTML (or decide based on what's being evaluated)
2. **Read existing components** — understand current markup/layout
3. For HTML: read `apps/home/core/style/globals.css` and follow @html-reference.md
4. **Build "Current State" first** — baseline for comparison
5. **Build 3 variations** (A/B/C) with distinct philosophies
6. **Label sections** with clear descriptions of what changed and why
7. **Verify accessibility** — touch targets, tab order, no hover-dependent interactions

## Common Mistakes

| Mistake                               | Fix                                      |
| ------------------------------------- | ---------------------------------------- |
| Small buttons/links                   | Enforce 44px minimum                     |
| Hover tooltips as primary info        | Use persistent labels                    |
| Modal dialogs                         | Use inline expansion or new page         |
| Carousel/slider                       | Use paginated list                       |
| Drag-and-drop only                    | Provide keyboard reorder alternative     |
| Auto-rotating content                 | Static content only                      |
| (HTML) Tailwind config for oklch      | Define CSS utility classes manually      |
| (HTML)`bg-color/30` opacity syntax  | Use raw `oklch(... / 0.3)` in CSS      |
| (HTML) Missing `:root` variables    | Always extract full set from globals.css |
| (HTML) Forgetting custom `--radius` | Override `rounded-lg/md/sm` in CSS     |
