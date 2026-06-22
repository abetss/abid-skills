## Anti-patterns in skill authoring

Failure modes we've seen repeat. Each is one the canonical docs or real sessions flagged as costly.

## Contents

- Description that leads with "Use when ..." instead of capability
- Under-triggering descriptions
- README.md inside the skill folder
- Time-sensitive language
- Inconsistent terminology
- Windows-style paths
- Offering too many options
- Unqualified MCP tool names
- Nested references (deeper than one level)
- Heavy-handed MUSTs/NEVERs in all caps
- Empty folders "in case we need them"

## Description leads with "Use when ..."

Wrong order. Every official example leads with what the skill **does**, then adds "Use when ..." for triggers. Capability-first matches Claude's matching model better. See `description-writing.md`.

## Under-triggering descriptions

Plain, literal, or workflow-summarizing descriptions cause Claude to silently handle the task instead of loading the skill — and you never find out. Name the specific phrases, keywords, file types, and contexts that should fire the skill. Be pushy.

## README.md inside the skill folder

Official rule: don't include a README.md inside the skill folder. Human-facing docs go in the **repo-level** README, outside the skill folder. The validator flags this as an error.

## Time-sensitive language

Instructions like *"If you're doing this before August 2025, use the old API"* become wrong as time passes.

Pattern to use instead — an "old patterns" collapsed section:

```markdown
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`. No longer supported.
</details>
```

The legacy context is preserved without cluttering the main flow.

## Inconsistent terminology

Mixing "field" / "box" / "element" / "control" for the same thing makes Claude less accurate. Pick one term per concept and use it everywhere in the skill.

## Windows-style paths

Forward slashes only, even on Windows. `scripts\helper.py` breaks on Unix; `scripts/helper.py` works everywhere. The validator flags backslash paths in markdown links.

## Offering too many options

"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, ..." → confusing. Pick a default and offer escape hatches only when they're actually needed.

Good: "Use pdfplumber for text extraction. For scanned PDFs that need OCR, use pdf2image with pytesseract instead."

## Unqualified MCP tool names

When referencing an MCP tool, use the fully-qualified `ServerName:tool_name`. Without the server prefix, Claude may fail to locate the tool, especially when multiple MCP servers are connected.

Good: `Use the BigQuery:bigquery_schema tool`
Bad: `Use the bigquery_schema tool`

## Nested references

`SKILL.md → a.md → b.md → c.md` causes partial reads. Keep references one level deep from SKILL.md. See `progressive-disclosure.md`.

## MUSTs/NEVERs in all caps

Heavy-handed shouting is less effective than explaining *why* the rule exists. "NEVER do X" becomes "Don't X — here's what goes wrong when you do." Reserve ALL CAPS for the rare case where a rule is truly non-negotiable (safety, data loss).

## Empty folders "in case we need them"

Add `scripts/`, `references/`, `templates/`, `assets/` only when you have actual content for them. Empty folders signal "this skill isn't done yet" and create noise.
