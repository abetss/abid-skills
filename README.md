# abid-skills

A Claude Code **plugin marketplace**. One repo, a few domain plugins — each a grouped
toolkit of skills (and a few agents). Add the marketplace once, then install only the
toolkits you want. Skills installed by a plugin can also be toggled individually after
install via the `/plugin` UI (Installed → select plugin → enable/disable a component).

## Install

```text
/plugin marketplace add abtinghods/<this-repo>     # add once (use your GitHub owner/repo)
/plugin install engineering@abid-skills            # then install just the toolkits you want
/plugin install product@abid-skills
```

Browse everything interactively with `/plugin` (Discover tab). Disable a whole plugin
with `/plugin disable <name>@abid-skills`.

## Plugins

| Plugin | What's inside |
|--------|---------------|
| **product** | design-discovery, design-in-asci, design-iterate, design-in-storybook, view-model-props, product-guide-writer |
| **engineering** | plan-prep, create-plan-task, architect-solution, executing-single-plan-task, executing-plan-task-list-sequential, execute-all-supervised, write-review-guide, write-todo, code-simplifier, inline-code-review-responder, debugging, sop-writer, troubleshooting-writer, conventions-writer, write-architecture-docs, changelog-generator + agents: code-reviewer, code-architect, code-explorer |
| **qa** | qa-execution, qa-exploratory, manual-qa-case-writing + agent: qa-runner |
| **meta-skilling** | skill-creating, find-skills, agentic-ai-architect, capture-findings, generating-html-artifacts |

## Structure

```text
.claude-plugin/marketplace.json   # the catalog
plugins/<name>/
  .claude-plugin/plugin.json      # plugin manifest
  skills/<skill>/SKILL.md         # bundled skills (full folders: references/, scripts/, assets/)
  agents/<agent>.md               # bundled agents (where applicable)
```

## Not included (repo-specific)

These skills are tied to a specific codebase shape (ZenStack/Prisma `schema.zmodel`,
`@@allow` policies, PIPEDA, an `apps/e2e` Page-Object-Model layout) and were left out
until generalized:

- `security-review-upliv`, `review-db-schema`, `writing-e2e-tests`
- `code-review-team` (its sub-reviewers reference the ZenStack/monorepo stack)

## Notes / caveats

- Some skill descriptions reference other skills by bare name (e.g. capture-findings →
  generating-html-artifacts). Co-dependent skills are bundled in the same plugin so they
  resolve together. A few cross-plugin references may need namespacing review.
- Several design skills assume **Storybook**; `manual-qa-case-writing` includes a
  **PIPEDA** compliance dimension. These are portable but opinionated — adapt as needed.
