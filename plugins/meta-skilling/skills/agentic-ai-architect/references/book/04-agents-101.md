---
chapter: 4
title: "Agents 101"
part: "II — Building an Agent"
source_pdf_pages: "15-17"
---

# Chapter 4: Agents 101
*Part II: Building an Agent*

You can use direct model calls for one-shot transformations: "*Given a video transcript, write a draft description.*"

But for ongoing, complex interactions with models, you typically need to build an agent on top.

Think of agents as AI employees rather than contractors: they maintain context, have specific roles, and can use tools to accomplish tasks.

**Levels of Autonomy**

In September 2025 Simon Willison distilled a fundamental definition of agents that we think is pretty solid: *An agent calls tools in a loop to achieve a goal.*

Agency is a spectrum. Like self-driving cars, there are different levels of agent autonomy.

- At a low level, agents make binary choices in a decision tree
- At a medium level, agents have memory, call tools, and retry failed tasks
- At a high level, agents do planning, divide tasks into subtasks, manage their task queue, manage multiple parallel sub-agents, and self-correct across long task horizons.

**Creating a basic agent**

In Mastra, agents have persistent memory, consistent model configurations, and can access a suite of tools and workflows.

The **agent** class is the foundation for creating AI agents in Mastra. It provides methods for generating responses, streaming interactions, and handling voice capabilities.

Here's how to create a basic agent:

```ts
import { Memory } from '@mastra/memory'
import { Agent } from '@mastra/core/agent'

export const agent = new Agent({
  name: 'my-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-5.1',
})
```

Running this code creates a configured AI agent that can:

- Accept user inputs/conversations
- Respond according to the 'helpful assistant' instructions
- Use GPT-5.1 as the underlying language model
- Be integrated into larger applications or workflows

It's worth noting that unlike a single model call, agents accumulate tokens quickly. Tool results, memory, and conversation history all add up.

This make context management and cost key things you'll need to figure out — not necessarily when you're initially building, but certainly as you begin rolling out your agent to users.
