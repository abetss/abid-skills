---
chapter: 10
title: "Model Context Protocol (MCP): Connecting Agents and Tools"
part: "III — Tools & MCP"
source_pdf_pages: "37-41"
---

# Chapter 10: Model Context Protocol (MCP): Connecting Agents and Tools
*Part III: Tools & MCP*

LLMs, like humans, become much more powerful when given tools. MCP works like a USB-C port for AI applications, providing a standard way for models and tools to interact.

## What is MCP?

In November 2024, a small team at Anthropic proposed MCP as a solution to a real and growing problem: every AI provider and tool author had their own way of defining and calling tools.

It's an open protocol for connecting AI agents to tools, models, and each other. Think of it as a universal adapter: **if your tool or agent "speaks" MCP, it can plug into any other MCP-compatible system— no matter who built it or what language it's written in.**

But, as any experienced engineer knows, the power of any protocol is in the network of people following it.

While initially well-received, it took until March for MCP to hit critical mass after gaining popularity among prominent, vocal supporters like Shopify's CEO Tobi Lutke.

Then, in April 2025, OpenAI and Google Gemini announced they would support MCP, making it the functional default for connecting AI agents. At this point (March 2026) MCP is the established standard for connecting AI agents to third-party tools.

## MCP Primitives

MCP has two basic primitives: *servers* and *clients*.

*Servers* wrap sets of MCP tools. They (and their underlying tools) can be written in any language and communicate with clients over stdio (locally) and Streamable HTTP (for remote servers).

*Clients* such as models or agents can query servers to get the set of tools provided, then request that the server execute a tool and return a response.

As such, MCP is as a standard for remote code execution, like OpenAPI or RPC.

## The MCP Ecosystem

As MCP was gaining traction, a bunch of folks joined the fray.

- *Vendors* like Stripe began shipping MCP servers for their API functionality.
- *Independent developers* started making MCP servers for functionality they needed, like browser use or error tracking, and publishing them on Github
- *Frameworks* like Mastra started shipping MCP server and client abstractions so that individual developers didn't have to reimplement specs themselves.

## When to use MCP

Agents, like SaaS, often need a number of basic integrations with third-party services (calendar, chat, email, web). If your project roadmap has a lot of this type of features, it's worth looking at building an MCP *client* that could access third-party tools and services.

Conversely, if you're building a tool that you want *other* agents to use, you should consider shipping an MCP *server*.

When consuming third-party MCP servers, treat them with the same trust level as any third-party API — vet them carefully, especially for agents with access to sensitive data or the ability to take real-world actions.

## Building an MCP Server and Client

If you want to create MCP servers and give an agent access to them, here's how you can do that in Typescript with Mastra:

```ts
// --- weatherTool.ts ---
import { defineTool } from "@mastra/core/tool";

export const weatherTool = defineTool({
  name: "weatherTool",
  description: "Get the current weather for a city.",
  parameters: {
    city: { type: "string", description: "City name" },
  },
  async execute({ city }) {
    // Dummy implementation
    return `The weather in ${city} is sunny!`;
  },
});

// --- weather-server.ts ---
import { MCPServer } from "@mastra/mcp";
import { weatherTool } from "./weatherTool";

const server = new MCPServer({
  name: "Weather Server",
  version: "1.0.0",
  tools: { weatherTool },
});

await server.startStdio();

// --- agent.ts ---
import { MCPClient } from "@mastra/mcp";
import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

const mcp = new MCPClient({
  servers: {
    weather: {
      command: "npx",
      args: ["tsx", "weather-server.ts"],
    },
  },
  timeout: 30000,
});

const agent = new Agent({
  name: "Weather Agent",
  instructions: "You can answer weather questions using the weather tool.",
  model: openai("gpt-4"),
  tools: await mcp.getTools(),
});
```

Conversely, if you want to create a client with access to other MCP servers, here's how you would do that:

```ts
import { MCPClient, MCPServer } from "@mastra/mcp";

// Step 1: Create an MCP client that connects to other MCP servers
const mcp = new MCPClient({
  servers: {
    weather: {
      // Connect to a remote MCP server via HTTP/SSE
      url: new URL("http://localhost:1234/sse"),
    },
    stocks: {
      // Or connect to a local MCP server via stdio
      command: "npx",
      args: ["tsx", "stock-server.ts"],
    },
  },
  timeout: 30000,
});

// Step 2: Expose all tools from the connected MCP servers via a new MCPServer
const server = new MCPServer({
  name: "Proxy MCP Server",
  version: "1.0.0",
  tools: await mcp.getTools(), // Aggregate tools from all connected servers
});

// Step 3: Start the proxy MCP server (stdio)
await server.startStdio();
```
