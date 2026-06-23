# Code Review Team — Memory

Cross-run memory for the `code-review-team` skill. Active profiles read this file before reviewing. Entries should be scoped to a single profile; prefix with the profile name (e.g. `architect:`, `code-style-guide-expert:`, `domain-expert:`, `security-expert:`).

What belongs here:
- False positives the human has confirmed across runs
- Severity / action-state calibration adjustments the team has accepted
- Recurring gaps (convention, doc, product, security) the team has *consciously deferred* — so reviewers stop re-flagging them every run

What does NOT belong here:
- One-off findings from a specific feature → live in the review document, not memory
- Project-specific architecture notes → your project's architecture docs
- Conventions → your project's convention / style-guide docs
- Product knowledge → your project's product / business-knowledge docs

## False positives

<!-- Findings the human dismissed. Reviewers skip these in future runs. -->
<!-- Format: - <profile>: `file_pattern_or_rule` — reason dismissed -->

_None yet._

## Accepted trade-offs

<!-- Known violations the team has consciously accepted. -->
<!-- Format: - <profile>: `description` — rationale -->

_None yet._

## Calibration notes

<!-- Severity / action-state adjustments based on reviewer feedback. -->
<!-- Format: - <profile>: `finding_type` — profile says X, team calibrates to Y, reason -->

_None yet._

## Deferred gaps

<!-- Recurring gaps (convention, doc, product, security) consciously deferred. Re-flag only if the current change worsens the gap. -->
<!-- Format: - <profile>: `gap` — deferred until <trigger>, source: <run/feature where it was logged> -->

_None yet._
