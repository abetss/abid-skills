# Product Knowledge Base — File and Folder Structure

## Root location

All product knowledge lives under:

```
a-kb/business-knowledge/product/pages-and-features/
```

## Top-level layout

```
pages-and-features/
├── README.md                  # Index — list of all documented features
├── screenshots/               # All screenshots (flat folder, descriptive names)
├── timesheet/
│   ├── q-and-a.md             # Cross-screen Q&A for the timesheet feature
│   ├── overview/              # The /timesheet route group
│   │   ├── main.md            # The list view itself
│   │   └── report.md          # The Hours Summary panel (split out as a screen)
│   ├── review/                # The /timesheet/[id] route group with tabs
│   │   ├── review.md          # "Review Entries" tab
│   │   ├── sign.md            # "Sign Timesheet" tab
│   │   └── history.md         # "History" tab
│   ├── line-entry/
│   │   └── form.md            # The shared Add/Edit form
│   └── history.md             # Standalone /timesheet/history page
├── staff/
│   ├── q-and-a.md
│   ├── list.md
│   ├── detail.md
│   └── create.md
├── notifications/
│   ├── q-and-a.md
│   ├── settings.md
│   └── guide.md
└── profile/
    ├── q-and-a.md
    └── manager-profile.md
```

## File-per-screen rules

- **One file per route, tab, or distinct screen.**
- **Nested folders follow the route hierarchy**, not arbitrary categorization.
- A screen with **2+ big independent features** → split into sub-files in a sub-folder. Do NOT collapse them into one doc with sub-sections.
- Tabs on the same route → one file per tab. Don't try to guess which is "primary" — name each file after its tab so future tab additions don't require renames.
- Modal flows that have meaningful business logic → their own file in a sub-folder.

## Naming

- Filenames are lowercase **kebab-case**: `line-entry.md`, `review.md`, `q-and-a.md`.
- **No numbered prefixes** (no `01-`, `02-`).
- Folder names match the route segment when possible (`timesheet/`, `staff/`, `notifications/`).
- For tabs, name each file after its tab (`review.md`, `sign.md`) — never `main.md`, since default tabs may change.
- For a primary screen + supplementary sub-feature split into its own file (e.g. a panel large enough to warrant one), `main.md` is OK for the primary. Example: `timesheet/overview/main.md` + `report.md`.

## The `q-and-a.md` per feature folder

Every feature folder gets a `q-and-a.md` containing **cross-screen** user-facing questions for that feature. Page-specific questions stay inline in each page's own `## Q&A` section.

Use `templates/q-and-a.md` as the starting point.

## The `screenshots/` folder

All screenshots live in a single flat `pages-and-features/screenshots/` folder.

**Filenames must be self-describing:**
```
{feature}-{screen}-{state}-{role}.png
```

Examples:
- `timesheet-overview-mgr-full.png`
- `timesheet-review-signed-att.png`
- `staff-create-form.png`

**Embed in markdown with relative paths from the page file:**

For files at the feature root (e.g. `timesheet/history.md`):
```markdown
![Manager overview](../screenshots/timesheet-overview-mgr-full.png)
```

For files in a sub-folder (e.g. `timesheet/review/sign.md`):
```markdown
![Manager sign tab](../../screenshots/timesheet-review-mgr-sign.png)
```

## The `README.md` index

`pages-and-features/README.md` is the table of contents for the whole product KB.
Update it whenever you add a new file.

Format:
- Group by feature
- One row per documented file
- Columns: Document, Route(s), Roles
