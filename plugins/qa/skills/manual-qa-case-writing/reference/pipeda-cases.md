# PIPEDA Compliance Test Cases

## Contents
- When to include
- Consent flow
- Sensitive input fields
- Right-to-access (data export)
- Right-to-erasure (data deletion)
- Breach notification path

This is a Canadian PIPEDA-compliant product. Features that touch personal data must include PIPEDA test cases. These are legal requirements — not optional.

## When to include
Any feature that:
- Collects personal data (name, email, phone, health info)
- Displays personal data of users other than the current user
- Exports, deletes, or modifies personal data
- Involves consent flows (terms, privacy, cookies)

If none of the above: mark N/A in qa.md with "feature does not touch personal data."

## Consent flow
- Priority: P0
- Steps:
  1. Visit consent flow (first-time or renewal)
  2. Attempt to reject using keyboard only
- Observable: reject as prominent as accept (same visual weight, same tab stops); keyboard-accessible
- Evidence: screenshot of consent UI; tab sequence log
- MUST NOT: reject buried in fine print; accept focused by default; dark-pattern wording

## Sensitive input fields
- Priority: P0
- Steps:
  1. For each sensitive field (password, SSN, health info): inspect attributes and network request
- Observable: correct `autocomplete` attribute (e.g., `current-password`, `off`); not logged in request bodies that don't need it; not echoed to console
- Evidence: DOM attributes of input; network request body; console log
- MUST NOT: sensitive data visible in any log; `autocomplete` missing or wrong

## Right-to-access (data export)
- Priority: P0
- Steps:
  1. Navigate to user settings → data export
  2. Request export
- Observable: export contains all personal data held about the user (JSON or CSV); delivered via secure channel (authenticated download, not emailed plaintext)
- Evidence: exported file contents; delivery mechanism
- MUST NOT: silent failure; partial export; export delivered to unauthenticated endpoint

## Right-to-erasure (data deletion)
- Priority: P0
- Steps:
  1. Navigate to user settings → delete account
  2. Complete deletion flow
- Observable: all personal data removed or anonymized within the timeframe stated in privacy policy; confirmation displayed; user logged out
- Evidence: DB query after deletion (via app admin interface); confirmation screenshot
- MUST NOT: data remains accessible after deletion; partial deletion; no confirmation

## Breach notification path
- Priority: P1
- Steps:
  1. If feature handles data subject to breach law: verify notification path exists
- Observable: breach notification UI/process documented; affected users identifiable
- Evidence: documented process in the feature's admin area
- MUST NOT: no plan for notification; affected users unidentifiable
