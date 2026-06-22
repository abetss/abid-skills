---
chapter: 7
title: "Agent Memory"
part: "II — Building an Agent"
source_pdf_pages: "24-28"
---

# Chapter 7: Agent Memory
*Part II: Building an Agent*

Memory is crucial for creating agents that maintain meaningful, contextual conversations over time. While LLMs can process effectively individual messages, they need help managing longer-term context and historical interactions.

There are three established types of agent memory:

- "working memory" (relevant long-term characteristics of users, eg how ChatGPT store what it knows about you)
- "semantic recall" (embedding text as vectors and using semantic search, or RAG, to find similar results to the query string).
- "observational memory" — a more agentic approach that compresses sessions into structured observations."

**Observational memory**

If you step outside on a busy street, your brain processes millions of pixels, but distills down to one or two observations. That blue SUV just ran a red light. Your neighbor's pit bull is off their leash.

In the context of a coding agent, observational memory might compress a user session down to something like this:

```
Date: 2026-01-15
  - 🔴 12:10 User is building a Next.js
app with Supabase auth, due in 1 week
(meaning January 22nd 2026)
  - 🔴 12:10 App uses server components
with client-side hydration
  - 12:12 User asked about middleware
configuration for protected routes
  - 12:15 User stated the app name is
"Acme Dashboard"
```

The core message format uses **formatted text, not structured objects.** (text is the universal interface and it's optimized for LLMs), **a three-date model** (observation date, referenced date, and relative date) and **emoji based log levels.**

In observational memory, the context window is broken into two blocks. The first block is the list of observations (like above). The second block is new messages that haven't yet been compressed. Typically 30k tokens are reserved for the first block and 40k for the second block.

When new messages come in, they are appended to the end of the second block. When these messages overflow, a separate "observer agent" compresses messages into new observations; when observations overflow a separate "reflector agent" garbage collects.

```ts
import { Memory } from '@mastra/memory'
import { Agent } from '@mastra/core/agent'

export const agent = new Agent({
  name: 'my-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-5-codex',
  memory: new Memory({
    options: {
      observationalMemory: true,
    },
  }),
})
```

**Memory processors**

Sometimes increasing your context window is not the right solution. It may seem counterintuitive, but sometimes you want to deliberately prune your context window (or just have more control over it).

Memory processors allow you to modify the list of messages retrieved from memory *before* they are added to the agent's context window and sent to the LLM. This is useful for managing context size, filtering content, and optimizing performance (not mention saving tokens).

Mastra provides some built-in memory processors:

**`TokenLimiter`**

This processor is used to prevent errors caused by exceeding the LLM's context window limit. It counts the tokens in the retrieved memory messages and removes the oldest messages until the total count is below the specified limit.

```ts
import { Memory } from "@mastra/memory";
import { TokenLimiter } from
"@mastra/memory/processors";
import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

const agent = new Agent({
  model: openai("gpt-4o"),
  memory: new Memory({
    processors: [
      // Ensure the total tokens from memory don't exceed ~127k
      new TokenLimiter(127000),
    ],
  }),
});
```

**`ToolCallFilter`**

This processor removes tool calls from the memory messages sent to the LLM. It saves tokens by excluding potentially verbose tool interactions from the context, which is useful if the details aren't needed for future interactions. It's also useful if you always want your agent to call a specific tool again and not rely on previous tool results in memory.

```ts
import { Memory } from "@mastra/memory";
import { ToolCallFilter, TokenLimiter } from
"@mastra/memory/processors";

const memoryFilteringTools = new Memory({
  processors: [
    // Example 1: Remove all tool calls/results
    new ToolCallFilter(),

    // Example 2: Remove only noisy image generation tool calls/results
    new ToolCallFilter({ exclude: ["generateImageTool"] }),

    // Always place TokenLimiter last
    new TokenLimiter(127000),
  ],
});
```

You can also create more custom memory logic by extending the base **MemoryProcessor** class.

**Prompt caching**

Most major APIs now let you cache a static prefix, like a long system prompt, a knowledge base, or a set of examples. This reduces token cost significantly while keeping frequently used context available, and plays nicely with observational memory.
