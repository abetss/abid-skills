---
name: read-jira
description: read and understand a ticket. use when you are given a ticket or you have to read a ticket to undetand something
disable-model-invocation: false
---

To read jira use `acli` cli.
If user was not logged in, stop and ask the user to log in to `acli`

Read the description and all the comments fully.
Download any image in order to view and understand them

## Script: `scripts/jira-clean.py`
Fetches a ticket via `acli` and strips the noise. Run:

`python3 .claude/skills/read-jira/scripts/jira-clean.py ID-1234`

Returns JSON: `bug-description` (summary), `body` (`text` + `attachments` URLs from the description), and `comments` (`author` name, plain-text `message`, `date`).
Prefer it over raw `acli ... --json`; it keeps bullet lists and @mentions that `acli comment list` drops.
