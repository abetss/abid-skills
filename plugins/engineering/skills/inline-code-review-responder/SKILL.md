---
name: inline-code-review-responder
description: 'Resolves inline code review comments the user left as `// code review: <feedback>` or `// todo human review: <feedback>` (or the equivalent in `#`, `/* */`, `<!-- -->`, etc.). Scoped to changed files only. For each marker, either applies the requested change and removes the marker, or — if the comment reads as a question or the agent has its own clarifying question — leaves a `code review ai response: <reply>` line directly beneath. Use when the user says "respond to my code reviews", "address my inline comments", "go through my code review notes", or invokes `/inline-code-review-responder`.'
---

# Inline Code Review Responder

The user leaves feedback for you inline by adding a comment with the `code review:` anchor — for example `// code review: rename this to userId`. Some users use `todo human review:` for the same purpose (e.g. `// todo human review: is this safe under concurrent writes?`) — treat it as an equivalent anchor with identical behavior. Your job is to find every one of those, in the changed files only, and resolve it.

## How to find the comments

Scope is **only changed files** in the working tree. Don't sweep the whole repo — that would pick up stale markers on unrelated branches and waste tokens.

1. List changed files: `git diff --name-only HEAD` (covers both staged and unstaged). If the user is mid-rebase or has untracked files they care about, also include `git status --porcelain` results — but ignore deleted files.
2. Within each changed file, grep for the literal anchors `code review:` and `todo human review:` (case-insensitive). The comment prefix varies by language — `//`, `#`, `/* */`, `<!-- -->`, `--`, `;`. Match the anchor, then walk back to the comment start to extract the feedback text.
3. Make sure you don't confuse `code review:` with `code review ai response:`. The response form is *your prior reply* — leave it in place; it's a record of an earlier round.

If there are no markers, say so plainly and stop. Don't hallucinate work.

## Deciding what to do with each marker

For every marker, you're choosing between three actions. Read the comment in context — the surrounding code is part of the message.

**Apply the fix and delete the marker.** Default to this when the feedback is a clear directive and you're confident about *both* the intent and how to do it. Examples: "rename this to X", "extract this into a helper", "use the existing util in lib/foo", "this should be async".

**Leave a response with `code review ai response:`.** Use this when:
- The comment is phrased as a question ("why are we doing X?", "is this safe under concurrent writes?", "do we still need this branch?"). Answer it.
- The comment is a directive but you have a real clarifying question — something the user genuinely needs to decide and you can't infer from the code. Don't manufacture clarifying questions to avoid making a call; if the answer is obvious from context, just do the work.
- You want to push back. If you think the suggested change is wrong or has a tradeoff the user might not have considered, say so in the response. Be direct, give your reasoning, and let them adjudicate. Don't silently apply something you disagree with, and don't silently refuse — leaving a response is how you put the ball back in their court.

**Format for responses:** insert a new line immediately below the original `code review:` line, using the same comment prefix and the same indentation. Keep the original `code review:` marker intact — the user's review comment stays as the anchor; your reply sits beneath it. Multi-line replies are fine; prefix every line with the comment syntax.

```ts
  // code review: should this also handle the empty-array case?
  // code review ai response: yes — added a guard above. empty input now returns null instead of throwing.
  return items[0] ?? null;
```

If the user later wants to continue the thread, they'll add another `// code review:` line below your response. That's the conversation pattern.

## Workflow

1. Find every marker in changed files.
2. Read each one *in context* — the surrounding 5–20 lines, sometimes the whole function. Comments often refer to "this", "above", "the loop" — you need to see what they're pointing at.
3. For each one, choose one of the three actions above and execute it. Apply edits with the file edit tool, not by rewriting the file.
4. Run any obvious local check after edits — type-check, the file's tests if they're fast, or a quick `git diff` review. You don't need to ship a full CI run; the user will do that. The point is to catch dumb mistakes you introduced (broken imports, syntax).
5. Report back: list every marker you found, what you did with each (applied / responded / asked), and the file:line. Group by file. If you applied a fix, one short sentence describing the fix is enough — the diff is the source of truth.

## Why this matters

The point of this skill is to make code review feel like a conversation in the file itself. The user's editing flow stays in their editor; they don't context-switch to a PR thread. That works only if you're disciplined about three things:

- **Don't lose the user's comment.** When you apply a fix, the marker goes away with it (the change is the answer). When you respond, the original stays so they can re-read what they asked.
- **Don't pretend certainty you don't have.** If you'd be guessing, ask. A 5-second clarifying question beats a 20-minute wrong-direction fix.
- **Don't be a yes-machine.** If the user is asking for something you think is wrong, the response form exists exactly for that. Use it.

## Edge cases

- **Marker inside a string literal or test fixture.** Skip it — it's data, not feedback. You can usually tell because it's quoted or the file is something like `fixtures/`, `__tests__/snapshots/`, etc.
- **Marker on a deleted line.** If `git diff` shows the line is being removed, the comment is going away anyway — no action needed.
- **Marker spanning multiple lines.** The user's feedback may continue on subsequent comment lines without a fresh `code review:` anchor. Read the contiguous comment block as one message.
- **No changed files.** Tell the user there's nothing to respond to. Don't fall back to scanning the whole repo unless they explicitly ask.
