# Eval: skill-creating, measured on fixing `create-plan-task`

A single-target, diff-grounded output-quality eval. Instead of grading against a generic rule
checklist, we took one real skill with real issues, hand-built the **gold** fixed version, and
read the assertions off the **original → gold diff**. The assertions are in `assertions.json`.

## Layout

```
create-plan-task/
  EVAL.md            this file
  assertions.json    the checks, derived from the diff (mechanical + judgment)
  original/create-plan-task/   the broken skill the agent is handed (snapshot, frozen)
  gold/create-plan-task/       the reference fix (validates clean) — what "perfect" looks like
```

## The issues (and what the fix looks like)

| # | Issue in `original` | Rule | Fix in `gold` | Assertions |
|---|---------------------|------|---------------|------------|
| 1 | Description says "Invoked by `plan-prep` (Phase 2) …" | caller-agnostic (R1) | drop the caller clause; say *when* to use it instead | M4 |
| 2 | Body has a **Modes** table that detects "how the skill was invoked" and reads a `mode: from-plan-prep` marker the caller passes | caller-agnostic (R1) | decide from **observable state** — does a `task-list.md` entry already exist — not from the caller | **J1**, M5 |
| 3 | The rename must not break behavior or leave dangling mode references | — | Output/Steps/Rules/Common-Mistakes all updated consistently | **J2** |
| 4 | `argument-hint` present but no declared `arguments`; body says "First/Second positional arg" | declare args (R3) + bare `$name` (R4) | add `arguments:`; reference `$work_folder` / `$task_description` bare | M2, M3 |
| 5 | Broken link `](task-NN.md)` in an example (validate.py error) | structural | use placeholder `](task-{NN}.md)` | M1 |
| — | (guard) legitimate `plan-prep.md` prerequisite refs | — | **kept** — only caller-coupling removed, not every mention | **J3** |

The bolded assertions (J1–J3) are the ones a linter cannot see — they are the reason this skill
has value beyond `validate.py`, and the reason this target was chosen.

## Running it

For each arm, copy the frozen input into a run dir, then have an agent improve it in place:

- **with_skill:** agent reads `skill-creating/SKILL.md` + references first, then improves the copy.
- **baseline:** same prompt, no skill.

Prompt (both arms):
> Improve this Claude skill so it follows skill-authoring best practices. The skill folder is at
> `<run>/create-plan-task/`. Edit the files in place.

Then grade `<run>/create-plan-task/SKILL.md`:
- **Mechanical (M1–M5):** scripted PASS/FAIL.
- **Judgment (J1–J3):** a blind judge (arm hidden, order randomized) scores each against its
  rubric in `assertions.json`, quoting evidence, using `gold/` as reference.

The gold is a reference, **not** a required output — a correct fix worded differently still passes.
