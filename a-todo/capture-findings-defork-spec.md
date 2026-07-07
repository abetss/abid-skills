# Fix: `capture-findings` cannot capture on-screen chat output (de-fork it)

**Status:** ready for implementation · **Skill:** `plugins/meta-skilling/skills/capture-findings/SKILL.md`
**Type:** bug fix + small redesign · **Owner:** unassigned

---

## Problem

The intended use of `capture-findings` is: the assistant prints an analysis/findings to the
terminal, the user says "capture this" / `/capture-findings`, and the skill turns **that on-screen
output** into a `<slug>/<slug>.md` + `<slug>/<slug>.html` pair. It does not do this reliably.

`capture-findings` is declared `context: fork` (+ `model: haiku`). A forked skill runs in an
isolated subagent whose **only input channel is `$ARGUMENTS`** — the Claude Code docs are explicit
that a forked skill "won't have access to your conversation history." So the fork literally cannot
see the chat. The content can only reach it if whoever invokes it copies the on-screen text into the
arguments.

That splits invocation into two paths:

1. **User types a bare `/capture-findings`** → the harness spawns the fork with `$ARGUMENTS` = the
   (empty) text after the command. The fork gets the skill body and nothing to capture. **Fails** —
   produces an empty/garbage artifact. This is the common path and the actual bug.
2. **The main agent invokes it** (because the user said "capture this" in natural language) → the
   main agent can see the conversation and *could* paste the analysis into the arguments. Only this
   path can work, and only if the agent remembers to forward the content.

## Evidence

Two real (end-to-end, not doc-following) eval runs already exist for this skill:

- `plugins/meta-skilling/skills/capture-findings/evals/evals.json`
  - **eval-0** (`capture-from-markdown-file`): content in a file on disk → passes.
  - **eval-1** (`capture-from-chat-context-inline`): content inline in the prompt → passed **only
    because the invoking agent manually pasted the analysis into `$ARGUMENTS`**. That proves the
    skill can *render forwarded content*, not that it can *grab chat content*.
- Fixture: `plugins/meta-skilling/skills/capture-findings/evals/files/proposal.md` (the sample
  analysis used by both evals).

Neither eval covers the failing path: a bare `/capture-findings` with the content only in the
conversation and nothing forwarded.

## Root cause

`context: fork` is the wrong choice for this skill. It was added to keep the heavy markdown+HTML
work out of the main context — but the **capture** step (reading what's on screen and composing the
markdown) is exactly the part that needs the conversation, and forking severs it. The genuinely
heavy/expensive part is the HTML render, which is **already delegated** to the separate
`generating-html-artifacts` skill (itself `context: fork` + `model: haiku`).

---

## Requirements (what the fix must achieve)

- **R1 — Capture on-screen output.** When the assistant has just produced findings in the
  conversation and the user invokes the skill (including a **bare `/capture-findings`** with no
  content in the arguments), the skill must capture that conversation content into the markdown. It
  must not depend on the caller pasting the content into `$ARGUMENTS`.
- **R2 — Faithful, lossless.** The markdown must preserve the full substance of the captured content
  (reasoning, options, tradeoffs, specifics, lists, tables) — no summarizing-away. (Same depth
  contract already documented in the skill body.)
- **R3 — Still produces the pair + opens it.** Output stays `<slug>/<slug>.md` +
  `<slug>/<slug>.html`; the HTML opens for the user. The three modes (Create / Update content /
  Re-render) are preserved.
- **R4 — Heavy render stays isolated.** The HTML generation continues to go through the
  `generating-html-artifacts` skill, which keeps the expensive, context-bloating work in a fork. The
  HTML skill needs only the `.md` path — no conversation — so it stays `context: fork`.
- **R5 — Progressive disclosure preserved.** The rendered HTML still uses progressive disclosure
  (TLDR/overview up front, detail behind folds/drill-down), as today.
- **R6 — No new caller obligations.** The fix must not require the user (or a calling agent) to do
  anything special beyond invoking the skill; "it reads what's on screen" should be true.

## Suggested changes (concrete)

All in `plugins/meta-skilling/skills/capture-findings/SKILL.md` unless noted.

1. **Frontmatter — remove the fork.** Delete `context: fork` and `model: haiku`. The skill then runs
   in the main agent, which already holds the conversation. (Optionally keep an explicit
   `model: inherit`, but omitting `model` already inherits the session model.)

2. **Rewrite the "How this skill runs" section.** It currently tells the *caller* to pass everything
   in `$ARGUMENTS` because the fork can't see the conversation. Replace with: the skill runs in the
   main agent and reads the content to capture **directly from the current conversation** (the
   findings the assistant just produced). `$ARGUMENTS` is now only for the optional slug/name and
   mode hints — not the content. Remove the "a fork does not inherit the conversation / pass the
   depth in arguments" framing.

3. **Update the dispatch step.** Keep "render the HTML by invoking the `generating-html-artifacts`
   skill," and make explicit that *that* skill is the forked/heavy step and is handed the `.md`
   **path** (no conversation). This is the isolation boundary that R4 relies on.

4. **Description cleanup.** The current `description` has a grammatical break ("Argument guide, Pass
   the content…" and "Use when the gives a name"). Rewrite to: capability + when-to-use only (per the
   house style), drop the now-obsolete "pass the content you'd print" caller-contract (the skill
   reads the conversation now), and keep the trigger phrases ("capture this", "write up your
   findings", "save this as a report/artifact", "turn this into a doc/page", plus the Update/Re-render
   triggers). Keep it under the 1,536-char description cap.

5. **Re-render mode note.** Re-render reads the user-edited `<slug>/<slug>.md` from disk (unchanged).
   Make sure the rewrite doesn't reintroduce "read from arguments" language there.

6. **Validate.** Run
   `python plugins/meta-skilling/skills/skill-creating/scripts/validate.py plugins/meta-skilling/skills/capture-findings`
   → must be clean.

## Rejected alternative

- **Keep it forked, make the forwarding contract explicit.** Even with a perfect description telling
  callers to forward content, the bare-`/capture-findings` path (no caller to forward) still gets an
  empty fork. Fragile and doesn't satisfy R1/R6. Rejected.

## Acceptance criteria / how to verify

Verify with **real, end-to-end invocations** (actually invoke the skill so it really writes files
and really calls `generating-html-artifacts`) — NOT by spawning a subagent that reads and
hand-follows `SKILL.md` (that tests "can an agent follow docs," which is meaningless here).

- **AC1 (the regression test — add as eval-2).** Simulate: the assistant has produced an analysis in
  the conversation (use the text in `evals/files/proposal.md` as that on-screen content), then the
  user sends a **bare** `/capture-findings skill-authoring-upgrade` with **no content in the
  arguments**. The skill must still produce `skill-authoring-upgrade/skill-authoring-upgrade.md`
  whose content faithfully matches the on-screen analysis (all 6 meta-instructions, the file-by-file
  plan, the two capabilities, the references, all 4 choices A–D). Add this as a third eval in
  `evals/evals.json`.
- **AC2.** eval-0 and eval-1 still pass (file input and inline input).
- **AC3.** For every produced HTML: `python plugins/meta-skilling/skills/generating-html-artifacts/scripts/validate_artifact.py <file>.html`
  → zero ERRORS; HTML contains everything the markdown does (incl. the `artifact-source` mirror); HTML
  uses progressive disclosure (`<details>` / folds).
- **AC4.** Skill structure validator clean (step 6 above).

## Affected files / references

- `plugins/meta-skilling/skills/capture-findings/SKILL.md` — the change.
- `plugins/meta-skilling/skills/capture-findings/evals/evals.json` — add eval-2 (AC1).
- `plugins/meta-skilling/skills/capture-findings/evals/files/proposal.md` — existing fixture.
- `plugins/meta-skilling/skills/generating-html-artifacts/` — unchanged; stays forked; is the heavy
  render step.
- Note: this reverses commit `2944e2a` "feat: run capture-findings in a forked haiku subagent" —
  reference its diff for exactly what to undo in the frontmatter and body.
- Live copies: after editing the source repo, the `~/.claude/skills/capture-findings` copy and the
  plugin cache are derivatives; sync/reinstall if the change should be live immediately.
