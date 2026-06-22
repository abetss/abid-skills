# {Page or screen name}

**Route:** `{/em/timesheet/[id] — Sign tab}`
**Roles:** {manager, attendant}

## Overview

One paragraph describing what this screen is, who uses it, and where it sits in the user journey. Don't be exhaustive here — just orient the reader.

## Why it exists

The domain reason this screen was built. Link every justification back to the specific regulation or program rule (DF, ESA, PIPEDA, CILT, IL philosophy).

If the reason is purely UX or accessibility, say so explicitly.

## User flows

One H3 per flow. Title = role + goal in one sentence. Numbered steps covering what the user does, sees, and the resulting state.

### {Role} {does a specific thing}

1. ...
2. ...

## Business rules and validation

The complete catalog of every rule encoded on this screen. Be exhaustive. Use sub-headings to group related rules.

### {Rule group}

- Specific values, thresholds, formulas
- What triggers the rule
- What happens when it fires
- What happens when it doesn't

### {Another rule group}

- ...

## States

What the screen looks like in each state. Document each one explicitly.

- **Default / loaded** — ...
- **Loading** — ...
- **Empty** — ...
- **Error** — ...
- **Locked / signed / disabled** (if applicable) — ...
- **Role-specific states** (if applicable) — ...

## Role differences

Use this section when both roles access the same page but see different things. Skip if the page is single-role.

| Aspect | Manager | Attendant |
|---|---|---|
| Auth | ... | ... |
| Data scope | ... | ... |
| Available actions | ... | ... |

## Edge cases

Things that should rarely happen but the code handles. Race conditions, missing data, legacy values, etc. One bullet per edge case with the expected behavior.

- ...

## Screenshots

Embed all visuals for this screen. Captions should say what the screenshot demonstrates, not just "screenshot of X".

![{caption}](../screenshots/{file}.png)
*{What this screenshot demonstrates}*

## Relationships

Explicit cross-page linking.

- **Comes from:** which screens link or navigate to this one
- **Goes to:** which screens this one links or navigates to
- **Depends on:** other features whose data feeds this screen
- **Affects:** other features whose state changes when this screen does something

## Q&A

Page-specific user-facing questions an LLM might be asked about this screen.
Cross-screen questions for the whole feature go in the feature folder's `q-and-a.md` instead.

**Q: {Question}?**
A: {Answer with specific behavior, not a generic explanation.}

**Q: {Another question}?**
A: ...

## Technical notes

For developers and AI editing the code:

- **Files:** key file paths
- **API endpoints:** which APIs this screen calls
- **Data flow:** brief description of how data moves
- **Known tech debt / open issues:** anything worth flagging
