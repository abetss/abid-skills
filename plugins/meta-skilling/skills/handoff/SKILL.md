---
name: handoff
description: Prepares a context for another LLM to take over what you have in progress. Use when user asks to initiate handoff or write handoff.
argument-hint: "What will the next session be used for?"
disable-model-invocation: false
---

## Step 1 — Dump the chat

Before writing the handoff, dump the conversation to disk so the next agent can retrieve detail if needed.

1. Determine a short `<chat-name>` from the conversation topic (kebab-case, ≤ 4 words, e.g. `auth-refactor` or `design-sprint`).
2. Run the export script from the live session (it reads $CLAUDE_CODE_SESSION_ID, finds the transcript, and writes the dumps to `~/.claude/handoffs/` with an auto-incrementing iteration number):
   ```bash
   python3 ~/.claude/skills/handoff/scripts/export-session.py --name <chat-name>
   ```
   It prints two paths — capture both:
   ```
   WITH_TOOLS: ~/.claude/handoffs/<chat-name>-local-<N>-with-tools.md
   CLEAN:      ~/.claude/handoffs/<chat-name>-local-<N>.md
   ```
   - **`-with-tools`** is the deep archive: every message plus model thinking, tool calls, and tool results. Nothing redacted.
   - The **clean** file is the same conversation with all tool/thinking noise stripped — use it when you just need the human-readable thread.

(If the script errors — e.g. `CLAUDE_CODE_SESSION_ID` not set or no transcript found — let the user know and continue with Step 2 without the dump.)

## Step 2 — Write the handoff to a file

Write the handoff document as a Markdown file in the same folder as the dumps, reusing the dump's `<chat-name>` and iteration `<N>`:
```
~/.claude/handoffs/<chat-name>-handoff-<N>.md
```
After writing it, report the path in chat (with a one-line summary). Do **not** paste the full handoff inline.

Retain anything you think a process without any of your content needs to know in order to succesfully accomplish or move forward what you have been working on. If often helps to include reference to any artificat relatede to your session, especailly any plans artificats.

Start the handoff file with this note:
```markdown
  > **Need more context?** Dispatch a subagent (model: `claude-sonnet-4-6`) to read the session dump and answer your question. Two dumps are available — use the one that fits:
  > - `<path-to-with-tools-dump>` — full archive with tool calls + results, when you need exactly what was run/returned.
  > - `<path-to-clean-dump>` — the conversation without tool noise, when you just need the human-readable thread.
  > The subagent must search the file and respond back accordingly.
```

## Rules
- Do not duplicate content already captured in other artifacts. Reference them instead.
