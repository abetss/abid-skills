---
name: release
description: Use when the user wants to run a full release or ship a branch end to end — "release this", "ship it", "do the release", "cut a release", "deploy this". Walks through documenting product behavior, committing, generating a changelog, pushing, deploying to staging then production, and closing the tracking ticket. Stops and reports on any failure.
---

# Release

Execute the full release workflow for the current branch and the changes on it. If the
user named a ticket, scope, or constraints (e.g. "skip prod"), honor them.

Follow each step in order. **If any step fails, stop, report the failure to the user, and
await guidance before proceeding.** Never skip steps or continue blindly.

## Step 1: Document product behaviors

Before committing, check whether the changes introduce or modify user-facing behavior that
should be reflected in your product knowledge base (if you maintain one).

Build a short context summary (2–4 sentences):
- WHAT the change does from a user's perspective
- WHY it was made (the product intent — pull from the ticket and conversation)
- WHICH roles/pages/flows it affects

Then dispatch an agent that pulls in the `product-guide-writer` skill, hand it the summary,
and ask it to:

1. Gather the file changes — run `git status` and `git diff`, building a list of changed
   files with attention to user-facing surface area (route modules, components, server
   handlers, new screens).
2. Invoke `product-guide-writer` with the changed-files list and context summary. The skill
   decides whether docs need creating/updating, reads the relevant source (verifying in the
   browser if local dev is running), and writes the docs in place.

> Skip this step if your project has no product knowledge base.

## Step 2: Commit

Stage all relevant changes (including any docs from Step 1) and commit using your project's
commit conventions. A reasonable default:
- Prefix: `feat:`, `fix:`, or `chore:`
- Format: `[<ticket>] <prefix>: <short description>`
- Third person present tense ("adds" not "add")
- If pre-commit hooks (linters, formatters) report errors, fix them properly before
  retrying — never bypass hooks.
- Commit autonomously — the release invocation is explicit authorization to commit.

## Step 3: Changelog

Generate a changelog using the `changelog-generator` skill:
- Analyze commits since the last release/tag
- Categorize into features, improvements, bug fixes
- Transform technical commits into user-friendly language
- Present to the user for review and iterate until approved

## Step 4: Push

1. Fetch latest: `git fetch origin`
2. If `origin/<default-branch>` is ahead, rebase onto it (`git rebase origin/<default-branch>`).
   Resolve conflicts and re-run hooks if they fail. **Strategy: always rebase, never merge.**
3. Push with upstream tracking: `git push -u origin HEAD`
4. If the push is rejected (e.g. non-fast-forward), diagnose and report to the user.

## Step 5: Staging deployment

If your project deploys on push:
1. Tell the user staging deployment was triggered.
2. Poll the deployment status (e.g. `gh run list --branch <branch>` then `gh run view <run-id>`).
3. Report progress at each check.
4. If staging fails, report details and await guidance.

## Step 6: Production deployment

- **Skip condition**: if the user said "don't deploy to prod" / "skip prod", skip to Step 9.
- Otherwise trigger production (e.g. `gh workflow run <prod-workflow> --ref <branch>`). The user's release command (or "to production") is authorization to trigger deployment.

## Step 7: Monitor production

1. Poll production deployment status until it completes.
2. Report progress at each check.
3. If it fails, report details and await guidance.

## Step 8: Close ticket

When production is confirmed successful:
1. Move the tracking ticket to "Done".
2. Add a comment summarizing the release (changelog, commit hash, key decisions).
3. Confirm closure with the user.

## Step 9: Complete

Provide a summary:
- Product docs written/updated (or "none — no user-facing changes")
- Commit hash and message
- Changelog highlights
- Branch pushed
- Staging status
- Production status (or "skipped")
- Ticket status

## Important notes

- **Fail gracefully**: stop and report on any failure; do not skip steps.
- **User opt-out**: the user can skip production by saying "don't deploy to prod" / "skip prod".
- **Rebase strategy**: always rebase, never merge; resolve conflicts properly.
- **Hooks**: if pre-commit/CI hooks fail, fix the underlying issue — never bypass them.
