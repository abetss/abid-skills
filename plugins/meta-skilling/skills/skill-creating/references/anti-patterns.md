## Anti-patterns in skill authoring

Failure modes that repeat. The rules themselves live in SKILL.md and the topic references; this file keeps the ones worth a concrete example, plus a pointer for the rest.

## Worth an example

### Time-sensitive language

Instructions like *"If you're doing this before August 2025, use the old API"* become wrong as time passes. Preserve legacy context in a collapsed section instead:

```markdown
## Current method
Use the v2 endpoint: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used `api.example.com/v1/messages`. No longer supported.
</details>
```

### Unqualified MCP tool names

Reference an MCP tool as `ServerName:tool_name`. Without the server prefix Claude may fail to locate it, especially with multiple servers connected.

- Good: `Use the BigQuery:bigquery_schema tool`
- Bad: `Use the bigquery_schema tool`

### Offering too many options

"Use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, ..." paralyses. Pick a default; offer an escape hatch only when it's actually needed.

- Good: "Use pdfplumber for text extraction. For scanned PDFs that need OCR, use pdf2image with pytesseract instead."

### Backticked `$argument` in the body

`` `$target` `` renders the literal label `$target`; bare `$target` substitutes the value. Backticking a declared argument ships the placeholder name to the model instead of the data. See `arguments-and-dynamic-context.md`.

## Watch for (rules stated in full elsewhere)

- **Description leads with "Use when ..."** instead of the capability — capability-first matches Claude's selection better. `description-writing.md`
- **Under-triggering descriptions** — plain, literal, or workflow-summarizing; name the phrases that should fire it. `description-writing.md`
- **Coupling to the caller** — "when X calls this ..."; a skill can't know its caller. `description-writing.md`
- **Hardcoding an injectable value** — prefer `` !`command` ``. `arguments-and-dynamic-context.md`
- **Nested references** deeper than one level — `SKILL.md → a.md → b.md` causes partial reads. `progressive-disclosure.md`
- **Dumping everything into SKILL.md** — split detail into `references/` once a topic gets long. `progressive-disclosure.md`
- **Empty folders** "in case we need them" — add a folder only when you have content for it. `folder-structure.md`
- **`README.md` inside the skill folder** — the validator flags it; repo-level READMEs live outside the folder. `folder-structure.md`
- **Windows-style paths** — forward slashes only; `scripts\helper.py` breaks on Unix.
- **MUSTs/NEVERs in all caps** — explain *why* instead; reserve caps for genuine safety or data-loss rules.
- **Inconsistent terminology** — one term per concept; mixing "field" / "box" / "element" lowers accuracy.
- **Lines that don't change behavior** — defensive caveats and narration; the `agents/necessity-auditor.md` audit finds these.
