---
lens: domain
purpose: Full taxonomy of product-correctness concerns. Use as a lens, not a to-do list. The reviewer reads this, then decides which categories apply based on the diff, task intent, and product domain.
---

# Domain reviewer checklist

This is the superset of product-correctness concerns for a typical full-stack product. The reviewing agent reads through it and applies judgment:

- Skip categories the diff doesn't touch
- Go deep on categories the diff is centered on
- Look opportunistically at categories adjacent to the diff
- Flag gaps where a category *should* apply to the feature but isn't addressed in code or tests

Stack markers: `[H]` frontend, `[P]` backend/API, `[Both]`. (Adapt to your repo's app boundaries.)

> Some categories below (regulatory anchoring, patient/user safety, consent/disclosure/audit) only apply to products in regulated or safety-sensitive domains. If your product doesn't operate under those constraints, skip them. They're included because domain-correctness reviews in regulated domains depend on them.

## Contents

1. Business-rule correctness
2. State machines & transitions
3. Invariants
4. Business-layer data validation
5. Authorization at the business-logic layer
6. User flows & journeys
7. Test coverage of user flows & journeys
8. Feature-intent alignment
9. User-facing error handling
10. Consent, disclosure, audit (product layer)
11. Accessibility as a product requirement
12. Cross-feature interactions
13. Domain vocabulary & naming
14. Lifecycle events & side effects
15. Regulatory / compliance anchoring — product commitments
16. Safety-critical correctness
17. Effective dates & timezones at the business level
18. Onboarding & empty states
19. Cross-role & cross-tenant scenarios

---

## 1. Business-rule correctness [Both]

*"Does the code compute what the product actually requires?"*

- Formulas and calculations produce the right number (scheduling, billing, pay, hours, quantities)
- Precedence / order of operations matches the spec (taxes before discounts vs after, etc.)
- Rounding rules consistent (money to 2dp, hours to quarters)
- Signed values handled (credits vs debits, overtime vs undertime)
- Threshold-sensitive rules hit the threshold correctly (≥ vs >)

## 2. State machines & transitions [Both]

*"Are the legal paths through this entity's lifecycle enforced?"*

- Valid transitions defined and enforced (can't go Archived → Active without elevation)
- Illegal transitions rejected with a clear error, not silent no-op
- Transitions atomic — no half-states visible
- Transition history logged (who, when, why)
- Terminal vs resumable states distinguished
- Rollback / reversal path defined when reversible

## 3. Invariants [Both]

*"What must always be true about this data, and is it enforced?"*

- Cross-record invariants ("one active subscription per account", "bookings don't overlap for the same resource")
- Cross-field invariants within a record (end after start, completed-at after created-at)
- Accounting / balance invariants where relevant
- Tenant isolation at the business-logic layer, not relying solely on DB policies
- Uniqueness that the product requires but DB doesn't enforce

## 4. Business-layer data validation [Both]

*"Does the validation match product language, not just schema constraints?"*

- Required vs optional matches product truth (not just "column has a default")
- Value ranges business-meaningful (age ≥ 0, identifiers valid-format, postal code valid)
- Enumerations match domain vocabulary
- Conditional required (field X required if Y is true)
- Cross-field validation at the product level

## 5. Authorization at the business-logic layer [Both]

*"Can only the right actors do this action?"*

- Role-based action gating (admin-only, member-only, self-service)
- Ownership checks ("user can only act on their own records unless elevated")
- Consent verified before action that requires it
- Delegation / impersonation paths explicit and logged
- Distinct from schema-policy correctness (the access-control / authorization policy layer); here it's the *product intent* layer

## 6. User flows & journeys [Both]

*"Does the sequence of steps match what the product specified?"*

- Each product-required step exists in code
- No silent scope creep (extra steps not in the spec)
- No silent scope drop (missing steps from the spec)
- Navigation preserves required state across steps
- Cancel / save-and-continue / abandon paths defined
- Success states and failure states both designed

## 7. Test coverage of user flows & journeys [Both]

*"Are the journeys tested end-to-end — not just the functions?"*

- Frontend e2e covers golden path per persona / role
- Frontend e2e covers the key error paths and recovery
- Backend integration tests cover the business rules, not just handler plumbing
- Tests assert **behavior**, not implementation detail (no mocks-of-mocks)
- Cross-role scenarios covered (user A tries to do something user B owns)
- Cross-tenant scenarios covered (tenant A tries to see tenant B's data)
- Regression test exists for every past bug (no silent re-breaks)
- Test data factories speak domain language (`Booking`, `Account`) not primitive shapes

## 8. Feature-intent alignment [Both]

*"Does the code match the task file and the acceptance criteria?"*

- Every acceptance criterion in the task file is implemented
- No behavior added beyond the task's scope
- Copy matches the product voice (labels, buttons, errors)
- Product decisions referenced in task file are honored

## 9. User-facing error handling [H mostly]

*"When things fail, is the human the error reaches served well?"*

- Error messages humane, action-oriented ("We couldn't save. Try again, or contact support at …")
- Technical internals not leaked (stack traces, codes, vendor names)
- Partial-success states handled (saved some, not all)
- External service failures surfaced, not hidden as "something went wrong"
- Retry paths explicit where retry is safe

## 10. Consent, disclosure, audit (product layer) [Both, if applicable]

*"Does the feature respect the consent and audit model the product commits to?"*

- Consent captured before actions that require it; scoped to the action (not blanket)
- Consent revocation paths defined and honored
- Disclosure to third parties logged per the product's commitments
- Access distinctions between roles respected in data visibility
- The lens here is "does the product keep the promises it makes" — not the legal interpretation of any regulation

## 11. Accessibility as a product requirement [H mostly]

*"Can the primary user of this feature actually use it end-to-end?"*

- Key journeys work keyboard-only from start to finish
- Key journeys survive screen-reader traversal
- Where the user base needs it, accessibility affordances (debounce, large targets, auto-save) are built into the **flow**, not just individual components
- Distinct from the accessibility profile (which does per-component WCAG); here it's "does the journey work"

## 12. Cross-feature interactions [Both]

*"Does this feature play well with its neighbors?"*

- Does it break an existing flow? (new type affects scheduling, billing, reporting)
- Does it share data with adjacent features consistently?
- Does it respect assumptions other features make?
- Does it fire the events other features expect to hear?

## 13. Domain vocabulary & naming [Both]

*"Is the product's language reflected in the code a product person could read?"*

- Entity names match product terms (`Booking`, `Account`, not `Record`, `Entry`)
- Same concept uses the same name everywhere (UI, code, DB, docs)
- No inventing new terms for existing concepts
- Acronyms expanded where ambiguous

## 14. Lifecycle events & side effects [Both]

*"When this entity changes, what else should happen — and does it?"*

- Create-of-X triggers the right downstream effects (notifications, emails, linked records)
- Update-of-X triggers what the product requires (re-notify? re-validate? recompute billing?)
- Delete / archive triggers correct cascade (soft-delete, anonymize, retention countdown)
- Side effects are tested
- Idempotent where the product requires (duplicate creation, webhook replays)

## 15. Regulatory / compliance anchoring — product commitments [Both, if applicable]

*"Does the feature meet the regulatory / compliance promises the product makes?"*

- Privacy / data-protection commitments (right of access, right to correction, right to know disclosures)
- Purpose limitation (collected data used only for stated purpose), retention limits
- Consent-based messaging with working unsubscribe, where the product sends messages
- Jurisdictional nuances (regional vs national, cross-border data)
- The lens here is "does the product fulfill its commitment" — not "does the law permit this"

## 16. Safety-critical correctness [Both, if applicable]

*"Could a mistake here hurt a real person or cause material harm?"*

- Alerts fire at the right thresholds
- Overrides require sign-off and log the override reason
- Safety-relevant data double-validated where the consequences require it
- Escalation paths exist and are testable

## 17. Effective dates & timezones at the business level [Both]

*"Does the product honor 'as-of' vs 'now'?"*

- Retroactive changes honor the effective date, not the change date
- Schedules, pay periods, billing periods anchored to the right timezone
- Historical views show data as it was, not as it is now
- Future-dated records handled correctly

## 18. Onboarding & empty states [H]

*"What does this feature look like on day one, before there's data?"*

- New-tenant / new-user initial state defined
- Empty states designed for every list and view (not just "nothing here")
- Helpful first-step guidance where appropriate
- Migration path from existing state is handled

## 19. Cross-role & cross-tenant scenarios [Both]

*"Does the feature behave right when user A meets user B's data?"*

- User A can see what they should
- User A can do what they should
- User A *cannot* see what they shouldn't — and the failure mode is correct (404 vs 403 vs redacted)
- Tenant A never sees tenant B's anything
- Cross-tenant references (referrals, grants between tenants) handled deliberately
