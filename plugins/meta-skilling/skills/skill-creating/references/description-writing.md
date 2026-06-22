## Writing the skill description

The description is the primary triggering mechanism. Claude only sees the skill's `name` and `description` before deciding whether to invoke — the body isn't loaded yet. Every "when to use" signal has to live in the description, not the body.

## Structure

Anthropic's canonical pattern is **three parts in order**:

```
[What the skill does] + [When to use it] + [Key capabilities / trigger phrases]
```

Lead with capability, not with a trigger clause. Claude matches descriptions against the user's request, and a capability-first sentence gives Claude a clean hook to match on before the trigger details reinforce it.

### Good example (official — PDF processing)

> Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

### Good example (official — Figma handoff)

> Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

### Good example (official — Linear workflows)

> Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

## Rules

- **Capability first.** The first clause states what the skill does in third person. Not "Use when ..." as the opener.
- **Third person only.** Describes Claude's behavior, not Claude speaking.
  - Bad: "I help you process PDFs."
  - Bad: "You can use this to ..."
  - Good: "Processes PDFs ..."
- **Include a `Use when ...` clause.** After the capability sentence, name the specific phrases and contexts that should fire the skill.
- **10–1024 characters.** Too short and there's nothing to match on; too long and it gets truncated.
- **Name the trigger surface.** Capability alone is not enough — Claude needs to know what user phrases should fire it.
- **Be pushy.** Claude under-triggers skills by default. Enumerate specific phrases, keywords, file types, and contexts that should trigger the skill, even ones that feel redundant.
- **No XML angle brackets.** `<` and `>` are forbidden in frontmatter (security restriction).
- **No first-person.** (Repeating because this is the most common failure.)

## Why under-triggering happens

Claude decides whether to use a skill based only on the short description. If the description sounds narrow or literal, Claude silently handles the task directly instead of consulting the skill — and you never learn the skill was skipped. Pushiness plus named trigger phrases is the counter.

## Pushy example

- Under-triggering: "Build a dashboard for internal data."
- Pushy: "Creates dashboards for internal data including metrics views, chart layouts, and KPI summaries. Use when the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard'."

## The 4C principles

- **Clear** — one unambiguous capability, not a grab-bag.
- **Concise** — no filler; every phrase pulls weight toward triggering.
- **Contextual** — names the situations and user phrases that should fire it.
- **Complete** — covers the realistic trigger surface, not just the obvious case.

## Trigger-pattern taxonomy

Name at least two of these in the description:

- **Direct request** — user explicitly asks. E.g. "write a skill for X".
- **Keywords** — specific terms that imply the skill. E.g. "dashboard", "visualization", "metric".
- **Context** — situational cues. E.g. "user opened a CSV file with >1000 rows".
- **Task type** — category of work. E.g. "any data-cleanup task", "any release-notes task".

## Debugging a description

In a fresh session, ask Claude: *"When would you use the [skill name] skill?"* Claude will paraphrase the description back. If the paraphrase is missing a trigger context you care about, or includes one you don't want, adjust the description.

Signs of trouble and their fixes:

- **Under-triggers** → add more keywords, named phrases, and contexts. Add "even when the user doesn't explicitly say ..." clauses.
- **Over-triggers** → add a negative scope clause ("Do NOT use for ..., use the [other-skill] skill instead"). Be more specific about the domain.
