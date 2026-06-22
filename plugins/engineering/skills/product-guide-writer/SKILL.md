---
name: product-guide-writer
description: Use when extracting product behaviors from feature development materials, conversations, code analysis, or browser testing into the product knowledge base. Triggers on "document product behavior", "write product guide", "extract feature specs", "update product knowledge", "document this feature", or "product knowledge".
---

# Product Guide Writer

Writes domain-expert reference docs into `a-kb/business-knowledge/product/pages-and-features/`. One canonical file per route, tab, or distinct screen. No `.short`/`.detailed` split.

## Always read these first (in this order)

1. `memory.md` (in this skill folder) — captured learnings from past sessions (see Memory section below)
2. `file-folder-structure.md` (in this skill folder) — where files live, how folders nest
3. `templates/page.md` — the literal page template
4. `templates/q-and-a.md` — the per-folder Q&A template

If a `domain-cheat-sheet.md` exists in the current task's `a-works/` folder, read it too — it contains domain rules every doc must align with.

## Memory

Read `memory.md` in this directory before starting. It contains learnings from past doc-writing sessions that prevent repeating mistakes — bugs found in older docs, mid-session user corrections, and anti-patterns from real failures.

### Reading memory

Before writing or updating any product doc, scan memory entries for:

- **Bugs in older docs for the same feature area** (e.g. wrong rate ranges, wrong sort orders) — anything you might be tempted to copy
- **User corrections that match your current task** (e.g. theme, naming, folder structure)
- **Anti-patterns** — common writing failures you should avoid in your own draft

If a memory entry contradicts what you find in the codebase, **trust the codebase** and update the doc accordingly. Then add a new memory entry capturing the new bug or correction.

### Writing to memory

After every completed doc, evaluate whether the session produced a learning worth capturing. Write an entry if:

- A user explicitly corrected you mid-session (theme, naming, structure, content)
- You found a bug or wrong value in an existing doc that you almost copied
- The same mistake or misunderstanding has happened more than once across sessions
- A technique or pattern was particularly effective (e.g. the three-agent code+chrome-1+chrome-2 pattern for a feature with both roles)
- A user preference came up that wasn't obvious from the existing rules

Do NOT capture:

- Things already in `SKILL.md`, `file-folder-structure.md`, or the templates
- Generic writing advice not tied to a real incident
- Project facts (those belong in the docs themselves, not in skill memory)
- Obvious do-better statements ("write better summaries")

Add a dated line under `## Updated by` whenever you append a new lesson.

## Process

1. Identify the route/tab being documented and its target file path (use `file-folder-structure.md`).
2. Gather evidence in parallel:
   - Read all source files for the route module (page.tsx, ui.tsx, transformer, actions, components)
   - Test the running app via **chrome-1 MCP** (manager role) and **chrome-2 MCP** (attendant role) when both roles access the page
   - Capture screenshots in **white theme** into `pages-and-features/screenshots/`
3. Cross-reference findings — code says X, browser confirms X, domain rule explains why X. If they disagree, investigate before writing.
4. Copy `templates/page.md` and fill it in. Section order is fixed.
5. Embed screenshots inline with relative paths.
6. Update the feature folder's `q-and-a.md` with any new cross-screen user-facing questions.
7. Update `pages-and-features/README.md` index if you added a new file.

## Hard rules

- Browser testing is mandatory. Never write from code alone.
- Verify every existing rule against current code — past sessions found bugs in older docs (wrong rate ranges, wrong sort orders, wrong multiplier values).
- Section order matches `templates/page.md` exactly.
- Q&A goes BOTH places: page-specific user questions in the page file's `## Q&A` section, cross-screen / feature-wide questions in the feature folder's `q-and-a.md`.
- Do NOT modify the in-app MDX guide (`apps/home/modules/guide/`) as part of this skill — that's hand-curated UI code.

## Out of scope

- Cross-cutting domain knowledge (DF rules, ESA, PIPEDA) → those live in `a-kb/business-knowledge/product/direct-funding/` and `a-kb/business-knowledge/compliance/`.
- User-facing in-app guide content → that's in `apps/home/modules/guide/content/*.mdx`, hand-curated UI code.
- Conventions, SOPs, troubleshooting docs → use `conventions-writer`, `sop-writer`, `troubleshooting-writer` instead.
