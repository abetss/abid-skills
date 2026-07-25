#!/usr/bin/env python3
"""Export the current Claude Code session transcript to markdown.

Locates the live session transcript via the CLAUDE_CODE_SESSION_ID env var
(set by Claude Code in the running session) and writes TWO markdown files:

  <dir>/<name>-local-<N>-with-tools.md   full deep archive: user/assistant
                                          text, model thinking, tool calls,
                                          and tool results. Nothing redacted.
  <dir>/<name>-local-<N>.md               clean read: user/assistant text only,
                                          tool calls/results/thinking stripped.

<N> auto-increments per <name> in <dir>. Both paths are printed at the end:

  WITH_TOOLS: /abs/path/<name>-local-<N>-with-tools.md
  CLEAN:      /abs/path/<name>-local-<N>.md

Usage:
  export-session.py --name <chat-name> [--dir <output-dir>]

Output dir defaults to ~/.claude/handoffs (durable; not purged like the OS
temp dir). Override with --dir.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def find_transcript():
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not sid:
        sys.exit(
            "error: CLAUDE_CODE_SESSION_ID is not set. This script must run "
            "inside the live Claude Code session whose transcript you want."
        )
    matches = list((Path.home() / ".claude" / "projects").glob(f"*/{sid}.jsonl"))
    if not matches:
        sys.exit(f"error: no transcript found for session {sid}")
    # If somehow more than one, the largest/most-recent is the real one.
    return max(matches, key=lambda p: p.stat().st_mtime)


def next_iteration(out_dir: Path, name: str) -> int:
    pat = re.compile(rf"^{re.escape(name)}-local-(\d+)\.md$")
    highest = 0
    for p in out_dir.glob(f"{name}-local-*.md"):
        m = pat.match(p.name)
        if m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def text_of(content) -> str:
    """Flatten a tool_result content value (str or list of blocks) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(b.get("text", ""))
                else:
                    parts.append(f"[{b.get('type', 'block')}]")
            else:
                parts.append(str(b))
        return "\n".join(parts)
    return str(content)


def render(entries, *, with_tools: bool) -> str:
    out = []
    for o in entries:
        etype = o.get("type")
        if etype not in ("user", "assistant"):
            continue
        msg = o.get("message") or {}
        content = msg.get("content")

        if etype == "user":
            blocks = content if isinstance(content, list) else [
                {"type": "text", "text": content or ""}
            ]
            for b in blocks:
                if not isinstance(b, dict):
                    continue
                bt = b.get("type")
                if bt == "text" and b.get("text", "").strip():
                    out.append(f"## User\n\n{b['text'].strip()}\n")
                elif bt == "tool_result" and with_tools:
                    flag = " (error)" if b.get("is_error") in (True, "True") else ""
                    body = text_of(b.get("content", "")).rstrip()
                    out.append(
                        f"### Tool Result{flag}\n\n```\n{body}\n```\n"
                    )

        else:  # assistant
            blocks = content if isinstance(content, list) else [
                {"type": "text", "text": content or ""}
            ]
            for b in blocks:
                if not isinstance(b, dict):
                    continue
                bt = b.get("type")
                if bt == "text" and b.get("text", "").strip():
                    out.append(f"## Assistant\n\n{b['text'].strip()}\n")
                elif bt == "thinking" and with_tools:
                    think = (b.get("thinking") or b.get("text") or "").strip()
                    if think:
                        out.append(f"### Thinking\n\n{think}\n")
                elif bt == "tool_use" and with_tools:
                    name = b.get("name", "tool")
                    try:
                        inp = json.dumps(b.get("input", {}), indent=2, ensure_ascii=False)
                    except (TypeError, ValueError):
                        inp = str(b.get("input"))
                    out.append(f"### Tool Call: {name}\n\n```json\n{inp}\n```\n")

    return "\n".join(out) if out else "_(no conversation content found)_\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="short kebab-case chat name")
    ap.add_argument(
        "--dir",
        default=str(Path.home() / ".claude" / "handoffs"),
        help="output directory (default: ~/.claude/handoffs)",
    )
    args = ap.parse_args()

    out_dir = Path(args.dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    transcript = find_transcript()
    entries = []
    with transcript.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    n = next_iteration(out_dir, args.name)
    clean_path = out_dir / f"{args.name}-local-{n}.md"
    full_path = out_dir / f"{args.name}-local-{n}-with-tools.md"

    header = f"# Session export: {args.name} (local-{n})\n\nSource: `{transcript}`\n"

    full_path.write_text(header + "\n" + render(entries, with_tools=True))
    clean_path.write_text(header + "\n" + render(entries, with_tools=False))

    print(f"WITH_TOOLS: {full_path}")
    print(f"CLEAN:      {clean_path}")


if __name__ == "__main__":
    main()
