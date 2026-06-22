## Writing scripts bundled with a skill

Only read this if the skill bundles scripts in `scripts/`. Skills without executable code can skip it.

## Contents

- Degrees of freedom (pick the right one)
- Solve, don't punt
- No voodoo constants
- Execute vs read intent
- Error handling with helpful messages
- Verification scripts

## Degrees of freedom

Match instruction specificity to the task's fragility.

- **High freedom** (prose instructions) — multiple valid approaches, context-dependent heuristics. Example: "analyze the code structure and suggest improvements."
- **Medium freedom** (pseudocode or parameterized scripts) — preferred pattern exists, some variation fine. Example: `generate_report(data, format="markdown", include_charts=True)`.
- **Low freedom** (specific scripts, few or no params) — fragile, error-prone operations that must follow an exact sequence. Example: `python scripts/migrate.py --verify --backup` — and say "do not modify the command."

Analogy: narrow bridge with cliffs on both sides → low freedom. Open field → high freedom.

## Solve, don't punt

A script should handle expected error conditions itself, not fail and expect Claude to figure it out.

Good:
```python
try:
    with open(path) as f:
        return f.read()
except FileNotFoundError:
    print(f"File {path} not found, creating default")
    with open(path, "w") as f:
        f.write("")
    return ""
```

Bad:
```python
return open(path).read()  # punts to Claude on any error
```

## No voodoo constants

Every magic number in a script must be documented with its rationale. If you don't know the right value, how will Claude?

Good:
```python
# HTTP requests typically complete within 30 seconds.
# Longer timeout accounts for slow connections.
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed.
# Most intermittent failures resolve by the second retry.
MAX_RETRIES = 3
```

Bad:
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

## Execute vs read intent

In SKILL.md, tell Claude explicitly whether a script is for execution or reference:

- `Run scripts/analyze.py to extract fields` → execute; output consumes tokens, body does not
- `See scripts/analyze.py for the extraction algorithm` → read; whole file enters context

Most utility scripts are for execution. Reading is for when the script itself is the reference.

## Helpful error messages

When a script validates user input and fails, the message should name the problem AND list the valid options. Claude reads the error and decides what to fix next — vague errors cause wasted iteration.

Good: `Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed`

Bad: `Validation failed.`

## Verification scripts

For complex, open-ended operations: have Claude produce an intermediate plan (e.g. `changes.json`), then have a script validate the plan before executing. Pattern:

```
analyze → create plan → validate plan → execute → verify
```

Catches errors before destructive changes. Especially valuable for batch operations or anything irreversible.

## Dependencies

List required packages in SKILL.md — don't assume they're installed. State the install command if possible:

```
Install: `pip install pdfplumber`
Then: `python scripts/extract.py input.pdf`
```

On the Claude API, there is no network access at runtime, so any required packages must be available in the code-execution environment. On claude.ai, packages can be installed from npm/PyPI.
