# Accessibility Test Case Templates

## Contents
- Applicability
- Keyboard-only full flow
- Switch-device friendliness
- Voice control
- Target size (WCAG 2.5.8)
- Error identification
- Reflow + zoom (WCAG 1.4.10)
- Live regions
- Prefers-reduced-motion

This is a Canadian PIPEDA-compliant product for users with movement disabilities. Accessibility is the product. WCAG 2.2 AA applies.

Each template below becomes a normal 6-field TC block in qa.md. Include only templates applicable to the page. Non-applicable templates get marked N/A with a one-line reason.

## Applicability
- Include every template with at least one applicable element on the page
- Skip only when genuinely non-applicable (e.g., "Voice control" skipped when there are no buttons on a purely static page)
- Any template skipped must be listed in qa.md under "A11y N/A" with the reason
- Default posture: include

## Keyboard-only full flow
- Role: any user role
- Priority: P0 (movement-disability product)
- Steps:
  1. Load page, place focus at top
  2. Use only Tab, Shift+Tab, Enter, Space, arrows, Esc to complete the primary flow
- Observable: every interactive element reachable; focus ring visible at every stop; activeElement sequence recorded
- Evidence: screenshot of focus indicator at each step; activeElement.id sequence log
- Design ref: {if design specifies focus state, cite}
- MUST NOT: any step require mouse; focus trap outside modals; focus lost to body after an action

## Switch-device friendliness
- Priority: P0
- Steps:
  1. Enable macOS Switch Control OR a keyboard-only simulation
  2. Attempt primary flow with single-switch scanning
- Observable: every interactive element reachable in < 20 tab stops; no hover-only affordance
- Evidence: focus traversal count; screenshot at each scan step
- MUST NOT: hover reveals critical UI; interactive-looking elements outside tab order

## Voice control
- Priority: P1
- Steps:
  1. For each interactive element, query accessibleName()
- Observable: every button/link accessibleName matches visible text (case-insensitive)
- Evidence: table of accessibleName vs visible text for all interactive elements
- MUST NOT: buttons named only by icon; generic names like "button"

## Target size (WCAG 2.5.8)
- Priority: P1
- Steps:
  1. Query bounding box of every interactive element (`[role=button]`, `a`, `input`, `select`)
- Observable: every element ≥ 24×24 CSS px (prefer 44×44); spacing ≥ 24px edge-to-edge unless separated by a non-clickable gutter
- Evidence: table of element → `getBoundingClientRect()`
- MUST NOT: any target below 24×24; two targets within 24px without gutter

## Error identification
- Priority: P1
- Steps:
  1. Submit a form with invalid values in every field
- Observable: every error has `role=alert`; programmatically associated to input (`aria-describedby`); includes correction guidance (not just "invalid")
- Evidence: DOM snippet of each error element
- MUST NOT: color-only error indication; generic "Something went wrong"

## Reflow + zoom (WCAG 1.4.10)
- Priority: P1
- Steps:
  1. Set viewport to 320 CSS px wide
  2. Set browser zoom to 400%
  3. Complete primary flow
- Observable: no horizontal scroll; no content loss; all actions reachable
- Evidence: screenshots at 320px and 400% zoom
- MUST NOT: content cropped; two-dimensional scroll required

## Live regions
- Priority: P1
- Steps:
  1. Trigger every dynamic announcement (save, error, toast, loading complete)
  2. Inspect DOM after each
- Observable: announcement lives in `aria-live` region with appropriate politeness (polite/assertive); cleared between announcements
- Evidence: DOM tree with aria-live attribute
- MUST NOT: visual-only announcements for state changes

## Prefers-reduced-motion
- Priority: P2
- Steps:
  1. Set `prefers-reduced-motion: reduce` in browser
  2. Trigger every animation on the page
- Observable: non-essential animation disabled or replaced with instant transition; essential motion preserved
- Evidence: comparison of animation behavior with flag on vs off
- MUST NOT: decorative transitions running under reduced-motion; content that only conveys meaning through animation
