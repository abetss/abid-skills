## Interviewing the user to capture skill intent

Before writing any skill file, gather intent. First scan the current conversation history — the user has often already given implicit answers to most of these questions. Only ask what's genuinely missing.

## The core four

1. **What should this skill enable Claude to do?** One sentence. Becomes the opening capability clause of the description.
2. **When should Claude invoke it?** What phrases, keywords, or contexts should trigger it? Becomes the "Use when ..." clause of the description (see `description-writing.md`).
3. **What does successful output look like?** Shapes `templates/` and the writing style inside SKILL.md.
4. **Should we set up test cases?** Objectively verifiable skills (file transforms, data extraction, code generation) benefit from tests. Subjective skills (writing style, visual design) usually don't — skip.

## Pin down 2–3 concrete use cases

Before drafting any files, write out 2–3 concrete use cases in this format. Anthropic's canonical format:

```
Use Case: [name]
Trigger: User says "[exact phrase 1]" or "[exact phrase 2]"
Steps:
1. [first action]
2. [second action]
3. [third action]
Result: [what the user ends up with]
```

This is the clearest single artifact for shaping the skill. If you can't fill one in, the skill's scope isn't clear enough yet.

## Follow-up probes

- Edge cases the skill must handle correctly.
- Example inputs — ask the user to attach files or paste snippets.
- Success criteria — how will the user know the skill is working? (Trigger rate? Output consistency? Reduced back-and-forth?)
- External dependencies or tools it needs (CLIs, APIs, libraries, MCP servers).

## Discovery questions for bundled resources

Each of these maps to one optional folder. Ask only if the answer isn't obvious from what the user already said.

- **Scripts** — "Will the skill need to do anything deterministic or repetitive: validation, code generation, data transforms, linting? If yes, that's a script."
- **Templates** — "Will the skill produce output in a consistent shape each time? If yes, that's a template."
- **References** — "Is there a large body of reference material — schemas, tables, taxonomies — that would bust the 500-line budget if inlined? If yes, that's a reference file."
- **Assets** — "Does the output include non-text files — HTML, fonts, icons, images? If yes, those are assets."
- **Memory** — "Will past sessions of this skill produce learnings that future sessions should remember? If yes, add opt-in memory."

## Closing the interview

Before writing any files, summarize what the skill will be — name, description draft, 2–3 use cases, folder layout, resources — and confirm with the user. Correcting direction now is much cheaper than after files are written.
