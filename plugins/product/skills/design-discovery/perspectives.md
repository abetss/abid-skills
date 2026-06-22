# Team Perspectives

This file defines the team voices used throughout all rounds of design discovery. Every round that involves team discussion reads this file.

## Core Team (Always Present)

### Lead Product Manager

Owns "what" and "why." Speaks first when framing problems, proposing role inventories, validating coverage.

**Draws from:** requirements, acceptance criteria, business rules, role permissions, compliance constraints (PIPEDA, labor law, WCAG), scope boundaries.

**Responsibilities:**
- Parse requirements into numbered acceptance criteria checklist
- Propose role inventories with goals, permissions, and cross-role effects
- Propose page inventories with AC coverage mapping
- Propose state inventories focused on business states (lifecycle, temporal, permission)
- Catch missing coverage: "We haven't addressed AC-11 yet"
- Catch scope creep: "That's not in requirements. Add it as a new AC, or save it for later?"
- Build conventions.md incrementally (business rules, impossible states, display rules)
- Build coverage matrix mapping every AC to a discovery artifact
- Validate that every flow has failure branches and recovery paths

**Does NOT:** design layouts, propose interaction patterns, make accessibility decisions. Product ensures the designer has everything needed to design correctly.

---

### Lead Designer

Owns "how." Speaks first when proposing layouts, interaction patterns, state visuals, and accessibility contracts.

**Draws from:** accessibility heuristics, interaction design patterns, state completeness checklists, responsive strategy, content hierarchy, WAI-ARIA patterns.

**Responsibilities:**
- Propose page layouts with information hierarchy (primary, secondary, tertiary)
- Propose the full state inventory per page (all 13 state categories)
- Propose interaction specs per element (click, keyboard, focus, blur, feedback)
- Propose tab order per page
- Propose accessibility contracts per component (ARIA role, keyboard pattern, focus management, screen reader announcements)
- Propose responsive strategy per page (what reflows, collapses, hides, reorders)
- Challenge assumptions about user navigation and input methods
- Content decisions: empty state copy, error messages, button labels, tooltips

**Non-negotiable accessibility rules (enforced by Designer):**
1. No hover-dependent functionality
2. 48px minimum touch targets (60px for primary actions)
3. Complete keyboard operability for every flow
4. No timed interactions (timers pause on focus)
5. Stable layouts (no content shift after load; reserve space for dynamic content)
6. Forgiving interactions (undo over confirm dialogs)
7. Sequential navigation support (switch devices traverse in reading order)
8. `prefers-reduced-motion` support
9. High contrast readiness (no meaning conveyed by color alone)
10. Error recovery over error prevention

---

## Optional Team Members

Assessed during Round 1 (Frame). The core team jointly evaluates whether each is needed, then the user confirms.

| Question | If Yes, Add |
|----------|-------------|
| Complex user personas or behavioral research needed? | **UX Researcher** |
| Complex keyboard/screen-reader interactions? (tables, forms, drag-drop, multi-step) | **Accessibility Specialist** |
| New data model or crosses multiple services? | **Data Architect** |
| Significant copy, onboarding, or error messaging needs? | **Content Strategist** |

### UX Researcher

**When present:** Personas need deeper analysis, competitive analysis exists, or user behavior data is available.

**Contributes:** User behavior insights, persona details beyond role definitions, usage frequency analysis, competitive patterns, user mental models.

### Accessibility Specialist

**When present:** Feature has complex interaction patterns -- data tables, multi-step forms, drag-and-drop, real-time updates.

**Contributes:** Switch access feasibility analysis, screen reader interaction patterns, ARIA pattern selection (grid vs. table, combobox vs. select, disclosure vs. dialog), focus management plans for complex flows, reduced motion alternatives.

### Data Architect

**When present:** Data model is new, complex, or crosses multiple services.

**Contributes:** Entity relationship clarity, field-level constraints (nullable, enums, computed), access policy implications for UI states, data lifecycle that creates UI states (draft, submitted, approved).

### Content Strategist

**When present:** Labeling, tone, empty state copy, error messages, or onboarding copy are significant.

**Contributes:** All copy decisions during Level 3 (States) -- empty state messages, error messages, button labels, tooltip text, onboarding guidance. Ensures consistent voice across states and roles.

---

## How Team Members Disagree

Disagreements are productive and expected. Neither team member overrides the other. The pattern:

1. **Present both perspectives with trade-offs:**

```
Product: "We need a confirm dialog for this destructive action per AC-15."
Designer: "A confirm dialog adds friction. An undo toast for 10 seconds
           is more accessible for switch users and less disruptive.
           Trade-off: undo has a time window where the action can be
           reversed; confirm prevents it entirely."
```

2. **Frame as a tension with options:**

> "There's a tension here: Product perspective says X because [requirement]. Design perspective says Y because [accessibility principle]. Options: [1, 2, 3]. Which fits?"

3. **User decides.** The decision is recorded in conventions.md with the rationale.

When an optional team member disagrees with a core member, the same pattern applies. No hierarchy -- only trade-offs presented to the user.
