# abid-skills

A Claude Code **plugin marketplace**. One repo, a few domain plugins — each a grouped
toolkit of skills (and a few agents). Add the marketplace once, then install only the
toolkits you want. Skills installed by a plugin can also be toggled individually after
install via the `/plugin` UI (Installed → select plugin → enable/disable a component).

## Install

```text
/plugin marketplace add abetss/abid-skills         # add once
/plugin install engineering@abid-skills            # then install just the toolkits you want
/plugin install product@abid-skills
```

Browse everything interactively with `/plugin` (Discover tab). Disable a whole plugin
with `/plugin disable <name>@abid-skills`.

## Plugins

| Plugin | What's inside |
|--------|---------------|
| **product** | design-discovery, design-in-asci, design-iterate, design-in-storybook, write-requirements |
| **engineering** | plan-prep, create-plan-task, architect-solution, executing-single-plan-task, executing-all-tasks, write-review-guide, write-todo, view-model-props, product-guide-writer, code-simplifier, inline-code-review-responder, debugging, sop-writer, troubleshooting-writer, conventions-writer, document-kb, write-architecture-docs, changelog-generator, never-again, release, commit-git, code-review-manager, architecture-reviewer, code-style-reviewer, domain-expert-reviewer, security-reviewer, performance-reviewer + agents: code-reviewer, code-architect, code-explorer |
| **qa** | qa-execution, qa-exploratory, manual-qa-case-writing + agent: qa-runner |
| **meta-skilling** | skill-creating, find-skills, agentic-ai-architect, capture-findings, generating-html-artifacts |

## How to use these skills


### TLDR
1. Start work with writing requirements using the `write-requirements`.
2. Plan the work. `plan-prep`. (Discovers status quoue, the gaps and potentailly go through architecutre sessions and how to verify the work)
3. Complete the work `executing-all-tasks`
4. Create guide, docs and release note `release`.

### More in Debth


The skills compose into larger workflows. The [`workflows/`](workflows/) folder holds
cheat sheets showing how to chain them for common jobs — each shows the happy path first,
then alternates:

- [main-development.md](workflows/main-development.md) — requirements → design → plan → execute → release
- [design.md](workflows/design.md) — discovery → iterate → asci/storybook
- [qa.md](workflows/qa.md) — write cases → run a team of browser agents
- [debug.md](workflows/debug.md) — bug → fix → document
- [document-kb.md](workflows/document-kb.md) — knowledge base routing

See [workflows/README.md](workflows/README.md) for the full index.

## Structure

```text
.claude-plugin/marketplace.json   # the catalog
plugins/<name>/
  .claude-plugin/plugin.json      # plugin manifest
  skills/<skill>/SKILL.md         # bundled skills (full folders: references/, scripts/, assets/)
  agents/<agent>.md               # bundled agents (where applicable)
workflows/                        # cheat sheets: how to chain the skills
```
