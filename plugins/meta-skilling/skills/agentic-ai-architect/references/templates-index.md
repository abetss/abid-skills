# Mastra Templates Index

These are the 12 official Mastra templates from https://mastra.ai/templates, cloned under
`/Users/abtinghods/Ork/interviews/koplar/templates/`. Each is a working repo that demonstrates a
**best-practice starting point** for a given agent capability. They are the **second grounding
tier**: after the book, consult these for *how a pattern is actually wired up in code*. (If that
directory isn't present in the current environment, treat this index's descriptions as the
template reference and note that the code wasn't available to open.)

**How to use this file:** find the row whose concept matches the decision at hand, open the
listed template's key files to see the concrete pattern, and when a recommendation draws on a
template, **say so explicitly** (e.g. "the deep-search template wires this as a nested
workflow"). Templates are Mastra/TypeScript — the book is too, so they're consistent.

All key-file paths below are relative to
`/Users/abtinghods/Ork/interviews/koplar/templates/<template-name>/src/`.

| Template | Demonstrates (architectural concept) | Complements book ch. | Key files |
|---|---|---|---|
| `template-text-to-sql` | Single agent + **tool calling**; tools that introspect a schema and execute generated code; conversational DB access | 6, 4 | `mastra/agents/sql-agent.ts`, `mastra/tools/introspect-database.ts`, `mastra/tools/execute-sql.ts` |
| `template-browsing-agent` | **Computer use / web automation** as tools (Stagehand); act/observe/extract/navigate tool decomposition | 11, 6 | `mastra/agents/web-agent.ts`, `mastra/tools/page-*.ts`, `lib/stage-hand.ts` |
| `template-chat-with-youtube` | **Tool composition + persistent memory**; fetch metadata for context, then transcript for detail | 6, 7 | `mastra/agents/youtube-agent.ts`, `mastra/tools/youtube-*.ts` |
| `template-github-review-agent` | **Workspace/sandbox-backed agent**; handles arbitrarily large PRs; agent + workflow split; typed schemas | 31, 6, 12 | `mastra/agents/code-review-agent.ts`, `mastra/workflows/pr-review-workflow.ts`, `mastra/lib/schemas.ts` |
| `template-chat-with-pdf` | **RAG pipeline**: chunk → embed → vector store → query tool; indexing as a workflow | 16, 17, 18 | `mastra/workflows/index-pdf.ts`, `mastra/lib/vector-store.ts`, `mastra/tools/pdf-query-tool.ts` |
| `template-flash-cards-from-pdf` | **PDF parsing tool + image generation** (multimodal output) | 32, 18 | `mastra/tools/extract-pdf-text.ts`, `mastra/tools/generate-image.ts`, `mastra/agents/flash-card-agent.ts` |
| `template-docs-chatbot` | **MCP server + client**; building your own MCP server and connecting an agent to it | 10 | `mcp-server/server.ts`, `mcp-server/tools/docs-tool.ts`, `mastra/mcp/mcp-client.ts` |
| `template-csv-to-questions` | **Workflow chaining agents**; large-context summarization layer before generation to control tokens | 13, 12, 19 | `mastra/workflows/csv-to-questions-workflow.ts`, `mastra/agents/csv-summarization-agent.ts` |
| `template-deep-search` | **Multi-agent orchestration**: nested workflows, suspend/resume for human-in-the-loop, self-evaluating research loop, specialized agents | 20, 21, 14, 25 | `mastra/workflows/deep-search-workflow.ts`, `mastra/agents/*-agent.ts` (planner, clarifier, evaluator, answerer) |
| `template-customer-feedback-summarization` | **Memory across sessions + scorers/evals** wired into an agent | 7, 27 | `mastra/agents/feedback-summarizer.ts`, `mastra/scorers/feedback-scorers.ts`, `mastra/tools/get-feedback.ts` |
| `template-google-sheets` | **Third-party integration** via Composio (external data access) | 11 | `mastra/agents/financial-modeling-agent.ts`, `mastra/index.ts` |
| `template-slack-agent` | **Deployment surface / integration**: agent behind a Slack app, streaming, request verification, routing; workflow-as-handler | 29, 15, 9 | `mastra/slack/routes.ts`, `mastra/slack/streaming.ts`, `mastra/slack/verify.ts`, `mastra/workflows/reverse-workflow.ts` |

## Concept → template quick lookup

- **Tool design / single agent** → text-to-sql, chat-with-youtube
- **RAG** → chat-with-pdf (full pipeline), flash-cards-from-pdf (parsing)
- **MCP (build a server)** → docs-chatbot
- **Workflows (chaining, summarization layer)** → csv-to-questions
- **Multi-agent + suspend/resume + nested workflows** → deep-search
- **Memory across sessions** → customer-feedback-summarization, chat-with-youtube
- **Evals/scorers in code** → customer-feedback-summarization
- **Sandboxes / large inputs** → github-review-agent
- **Computer use / browser** → browsing-agent
- **Third-party data integration** → google-sheets, slack-agent
- **Multimodal (image gen)** → flash-cards-from-pdf
- **Deployment / chat surface + streaming** → slack-agent

## Caveat

Templates show *one* working approach, not the only one. They are starting points. If a
template's choice conflicts with the book, prefer the book and note the difference. If both
are silent on something, fall back to general best practice and flag it as such.
