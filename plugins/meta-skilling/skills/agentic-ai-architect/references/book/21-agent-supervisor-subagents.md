---
chapter: 21
title: "Agent Supervisor & Subagents"
part: "VI — Multi-Agent Systems"
source_pdf_pages: "77"
---

# Chapter 21: Agent Supervisor & Subagents
*Part VI: Multi-Agent Systems*

Agent supervisors are specialized agents that coordinate and manage other "subagents".

The most straightforward way to do this is to pass in the other agents wrapped as tools.

For example, in a content creation system, a publisher agent might supervise both a copywriter and an editor:

```ts
const publisherAgent = new Agent({
  name: "publisherAgent",
  instructions: "You are a publisher agent that coordinates content creation. First call the copywriter for initial content, then the editor for refinement.",
  model: {
    provider: "ANTHROPIC",
    name: "claude-3-5-sonnet-20241022",
  },
  tools: { copywriterTool, editorTool },
});
```
