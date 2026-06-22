## Naming a skill

The skill's name is part of its identity. It influences Claude's mental model of what the skill does before the description is even read. Pick it carefully.

## Rules

- Lowercase kebab-case. No spaces, no underscores, no camelCase.
- Directory name must match the `name:` field in frontmatter exactly. A mismatch breaks loading.
- For process skills (ongoing activities), prefer gerund form: `creating-skills`, `documenting-features`, `reviewing-prs`.
- For action skills (one-shot operations), prefer verb+noun: `render-pdf`, `validate-schema`, `extract-entities`.

## Banned

- Reserved words in the name: `claude`, `anthropic`.
- Vague words: `helper`, `utility`, `manager`, `tool`, `handler`. They describe nothing.
- XML-like tags or angle brackets.

## Bad / good

| Bad | Why | Good |
|---|---|---|
| `csv` | too short, no verb | `processing-csv-files` |
| `data_processor` | underscores, vague noun | `processing-data` |
| `helper` | vague, means nothing | `generating-release-notes` |
| `claude-skill-helper` | reserved word + vague | `creating-skills` |
| `PDFTool` | PascalCase, vague noun | `rendering-pdf` |

## Why it matters

Names are the first thing both Claude and humans see in a skills directory listing. A vague or inconsistent name makes the skill harder to discover and harder to reason about when deciding whether to invoke it.
