## Arguments and dynamic context

How a skill receives inputs and how it pulls live data into its own prompt. Both happen
*before* the model reads the skill — they are preprocessing, not steps the model performs.

## Contents

- Declaring arguments (frontmatter)
- Referencing arguments in the body
- Bare `$name` vs backticked — the rule that bites
- Documenting arguments for the reader
- Injecting dynamic context with `` !`command` ``
- Injection gotchas
- Prefer injected values over hand-derived ones
- Source

## Declaring arguments

If a skill takes one or more inputs, declare them in frontmatter. Two fields work together:

- **`argument-hint`** — the shape shown in autocomplete when someone types `/skill-name`.
  List the arguments in order and mark optional ones so the caller knows what to pass.
- **`arguments`** — named positional arguments. Names map to positions in order, so the
  first name binds to the first argument passed. Accepts a YAML list or a space-separated
  string.

```yaml
---
name: translate
description: Translates text into a target language. Use when the user asks to translate a phrase, sentence, or document.
argument-hint: "[text] [target language]"
arguments: [text, target_lang]
---
```

Now `/translate "good morning" French` binds `$text` → `good morning` and `$target_lang` →
`French`. Mark optional arguments in the hint so the shape stays honest:

```yaml
argument-hint: "[file] [optional format]"
arguments: [file, format]
```

## Referencing arguments in the body

Inside the body, the declared names — plus a few built-ins — are substituted with the
caller's actual values before the model sees the content:

| Token | Expands to |
|---|---|
| `$name` | A named argument from `arguments` (e.g. `$text`, `$target_lang`) |
| `$ARGUMENTS` | The full argument string as typed |
| `$N` / `$ARGUMENTS[N]` | The Nth argument, 0-based (`$0`, `$1`, …) |
| `${CLAUDE_SESSION_ID}` | Current session id — for logging or session-scoped files |
| `${CLAUDE_EFFORT}` | Current effort level (`low`…`max`) — adapt instructions to it |
| `${CLAUDE_SKILL_DIR}` | The skill's own directory — use it to point at bundled scripts |

Prefer named `$name` over positional `$1` — names survive reordering and read clearly.

## Bare `$name` vs backticked — the rule that bites

Write a declared argument **bare**: `$text`. Never wrap it in backticks.

- `$text` → substituted with the runtime value (`good morning`).
- `` `$text` `` → the backticks are literal markup, so the model reads the *label* `$text`,
  not the value. You've shown the model a code-styled placeholder name instead of the data.

Rule of thumb: if you want the *value*, write it bare. Reserve backticks for when you are
genuinely talking *about* the placeholder (documenting it in a table, as this file does).

## Documenting arguments for the reader

Right after the title, give each argument one line — what it is and whether it's optional.
This is for the model reading the skill, separate from the autocomplete hint:

```markdown
## Input

- $text — the phrase or document to translate.
- $target_lang *(optional)* — the language to translate into; defaults to English.
```

## Injecting dynamic context with `` !`command` ``

When the skill needs live data, inject it. A line that starts with `` !`<command>` `` is run
by the harness before the model sees the skill; the command's output replaces the
placeholder. The model receives real data, never the command.

```markdown
## Current changes

!`git diff HEAD`

## Task

Summarize the changes above and flag anything risky.
```

For several commands, use a fenced block opened with `` ```! ``:

    ## Environment
    ```!
    node --version
    git status --short
    ```

## Injection gotchas

- **Line-start only.** The inline form runs only when `` ! `` is at the start of a line or
  right after whitespace. `` KEY=!`cmd` `` is left as literal text — the command does not run.
- **One pass.** Substitution runs once over the file. Command output is inserted as plain
  text and is *not* re-scanned, so a command cannot emit a placeholder for a later pass.
- **Only documented tokens expand.** `$name`, `$N`, `$ARGUMENTS`, the `${CLAUDE_*}` built-ins,
  and `` !`…` `` are the substitutions. An undocumented `{placeholder}` is just literal text —
  it reaches the model verbatim unless you inject its value.
- **It can be disabled.** The `disableSkillShellExecution` setting replaces each command with
  a notice instead of running it; don't make correctness depend on injection alone if the
  skill must also work with it off.

## Prefer injected values over hand-derived ones

If a value can be computed at load time, inject it rather than hardcoding it or telling the
model to go fetch or derive it. Injection keeps the skill correct as the underlying state
changes, removes a step the model would otherwise spend a tool call on, and grounds the
instructions in real data from the first token. A hardcoded value rots; a "go run this and
read the result" instruction burns a turn and can be skipped.

## Source

Claude Code skills docs — "Pass arguments to skills", "Available string substitutions", and
"Inject dynamic context": https://code.claude.com/docs/en/skills
