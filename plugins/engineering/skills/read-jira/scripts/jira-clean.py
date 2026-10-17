#!/usr/bin/env python3
"""Reduce `acli jira workitem view ... --json` output to just the useful content.

Usage:
    jira-clean.py ID-7767            # runs acli for you with the right fields
    acli jira workitem view ID-7767 --fields summary,description,attachment,comment --json | jira-clean.py

Output:
    {
      "bug-description": "<issue summary>",
      "body": {"text": "<description as plain text>", "attachments": ["<src>", ...]},
      "comments": [{"author": "<name>", "message": "<text>", "date": "<iso date>"}, ...]
    }

Note: `--fields comment` alone does not return summary/description/attachment,
so bug-description and body come out empty. Use the fields shown above.
"""

import json
import subprocess
import sys
from datetime import datetime

ACLI_FIELDS = "summary,description,attachment,comment"


def adf_to_text(node):
    """Flatten an Atlassian Document Format node into plain text."""
    if node is None:
        return ""
    if isinstance(node, list):
        return "".join(adf_to_text(n) for n in node)

    kind = node.get("type")
    attrs = node.get("attrs") or {}
    children = node.get("content") or []

    if kind == "text":
        text = node.get("text", "")
        for mark in node.get("marks") or []:
            if mark.get("type") == "link":
                href = (mark.get("attrs") or {}).get("href")
                if href and href != text:
                    return f"[{text}]({href})"
        return text
    if kind == "hardBreak":
        return "\n"
    if kind == "rule":
        return "---\n\n"
    if kind == "mention":
        return attrs.get("text", "")
    if kind == "emoji":
        return attrs.get("text") or attrs.get("shortName", "")
    if kind == "status":
        return f"[{attrs.get('text', '')}]"
    if kind == "inlineCard":
        return attrs.get("url", "")
    if kind == "date":
        ts = attrs.get("timestamp")
        if ts:
            return datetime.fromtimestamp(int(ts) / 1000).date().isoformat()
        return ""
    if kind in ("media", "mediaSingle", "mediaGroup", "mediaInline"):
        return ""  # attachments are reported separately

    inner = adf_to_text(children)
    if kind in ("paragraph", "heading"):
        return inner + "\n\n"
    if kind == "codeBlock":
        return f"```\n{inner}\n```\n\n"
    if kind == "blockquote":
        quoted = "\n".join(f"> {line}" for line in inner.strip().split("\n"))
        return quoted + "\n\n"
    if kind in ("bulletList", "orderedList"):
        lines = []
        for i, item in enumerate(children, start=1):
            marker = "-" if kind == "bulletList" else f"{i}."
            body = adf_to_text(item).strip().replace("\n\n", "\n").replace("\n", "\n  ")
            lines.append(f"{marker} {body}")
        return "\n".join(lines) + "\n\n"
    if kind == "tableRow":
        return " | ".join(adf_to_text(c).strip().replace("\n", " ") for c in children) + "\n"
    if kind == "table":
        return inner + "\n"
    # doc, panel, expand, listItem, tableCell, tableHeader, and anything unknown
    return inner


def clean_text(node):
    text = adf_to_text(node)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip()


def collect_media(node, found):
    """Collect `alt`/`id` of every media node, in document order."""
    if isinstance(node, dict):
        if node.get("type") == "media":
            attrs = node.get("attrs") or {}
            found.append(attrs.get("alt") or attrs.get("id"))
        for value in node.values():
            collect_media(value, found)
    elif isinstance(node, list):
        for value in node:
            collect_media(value, found)


def attachment_srcs(description, attachments):
    """Attachments referenced in the description, as src URLs.

    Media nodes only carry the filename (alt), so look the URL up in the
    attachment list. Falls back to the filename when there's no match.
    """
    by_filename = {a.get("filename"): a.get("content") for a in attachments or []}
    referenced = []
    collect_media(description, referenced)
    srcs = []
    for name in referenced:
        src = by_filename.get(name) or name
        if src and src not in srcs:
            srcs.append(src)
    return srcs


def format_date(raw):
    try:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S.%f%z").isoformat(timespec="seconds")
    except (TypeError, ValueError):
        return raw


def clean(data):
    fields = data.get("fields", {})
    description = fields.get("description")
    return {
        "bug-description": fields.get("summary") or "",
        "body": {
            "text": clean_text(description),
            "attachments": attachment_srcs(description, fields.get("attachment")),
        },
        "comments": [
            {
                "author": (c.get("author") or {}).get("displayName", ""),
                "message": clean_text(c.get("body")),
                "date": format_date(c.get("created")),
            }
            for c in (fields.get("comment") or {}).get("comments", [])
        ],
    }


def main():
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help")):
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) == 2:
        result = subprocess.run(
            ["acli", "jira", "workitem", "view", sys.argv[1], "--fields", ACLI_FIELDS, "--json"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.exit(result.stderr.strip() or f"acli exited with {result.returncode}")
        raw = result.stdout
    else:
        raw = sys.stdin.read()

    data = json.loads(raw)
    if "summary" not in data.get("fields", {}):
        print(
            "warning: input has no summary/description/attachment fields; "
            f"bug-description and body will be empty. Use --fields {ACLI_FIELDS}",
            file=sys.stderr,
        )
    json.dump(clean(data), sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
