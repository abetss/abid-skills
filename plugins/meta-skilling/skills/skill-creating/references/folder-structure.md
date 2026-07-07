## Skill folder structure

Only `SKILL.md` is required. Every subfolder below is optional — add one only when it pulls its weight.

## Optional folders

- **`scripts/`** — executable code for deterministic or repetitive work: validators, generators, linters, data transforms. Use when the task is rule-based enough that code is more reliable than prose instructions. Scripts can run without being loaded into context. See `script-quality.md` if you're writing one.
- **`references/`** — supporting markdown docs loaded on demand. Rule details, schemas, taxonomies, bad/good tables. Use when inlining the material would push SKILL.md past the 500-line budget. Keep them one level deep from SKILL.md.
- **`templates/`** — files the skill copies from: page scaffolds, output skeletons, starter structures. Use when the skill's output should follow a consistent shape each run.
- **`assets/`** — static files used in generated output: fonts, icons, images, HTML fragments, CSS. Use when the skill produces artifacts that need non-text resources.
- **`examples/`** — example inputs and expected outputs. Use sparingly. Usually better embedded in SKILL.md or in the relevant `references/` file, where they're read in context.

## Forbidden inside the skill folder

- **`README.md`** — per Anthropic's official guidance, don't include a README.md inside your skill folder. All documentation goes in SKILL.md or `references/`. If the skill is distributed via GitHub and needs a human-readable README, that README lives at the **repo level**, outside the skill folder. The validator flags a README.md inside the skill folder as an error.
- **Files with spaces or capitals in names** — folder and top-level filenames should be lowercase. `SKILL.md` is the one exception (it must be exactly `SKILL.md`, case-sensitive).

## Paths

Use forward slashes in all file paths, even on Windows. Windows-style backslash paths cause errors on Unix systems. Relative links (`references/naming.md`) only — no `@path/file.md` force-load syntax.

Failure modes for folder structure are collected in `anti-patterns.md` (empty folders, `@path` force-loads, `README.md` in the folder, dumping everything into SKILL.md).
