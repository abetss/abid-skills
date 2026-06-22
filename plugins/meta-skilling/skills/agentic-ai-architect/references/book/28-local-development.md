---
chapter: 28
title: "Local Development"
part: "VIII — Development & Deployment"
source_pdf_pages: "99-101"
---

# Chapter 28: Local Development
*Part VIII: Development & Deployment*

Agent development typically falls into two different categories: building the frontend vs. backend.

## Building an agentic web frontend

Web-based agent frontends tend to share a few characteristics: they're built around a chat interface, stream to a backend, autoscroll, and display tool calls.

We discussed the importance of streaming in an earlier chapter. Agentic interfaces tend to use a variety of different transport options like request/response, server-sent events, webhooks and web sockets, all to feed the sense of real-time interactivity.

There are a few frameworks we see speeding up development here, especially during the prototype phase: Assistant UI, Copilot Kit, and Vercel's AI SDK UI.

(And many agents are based on other platforms like WhatsApp, Slack, mobile apps, email, or voice and don't have a web frontend.)

It's important to note that while agentic frontends can be powerful, the full agent logic generally can't live client-side in the browser for security reasons — it would leak your API keys to LLM providers.

## Building an agent backend

So it's the backend where we typically see most of the complexity.

When developing AI applications, it's important to see what your agents are doing, make sure your tools work, and be able to quickly iterate on your prompts.

Some things that we've seen be helpful for local agent development:

- **Agent chat interface:** Test conversations with your agents in the browser, seeing how they respond to different inputs and use their configured tools.
- **Workflow visualizer:** Seeing step-by-step workflow execution and being able to suspend/resume/replay
- **Agent/workflow endpoints:** Being able to curl agents and workflows on localhost (this also enables using eg Postman)
- **Tool playground:** Testing any tools and being able to verify inputs / outputs without needing to invoke them through an agent.
- **Tracing & evals:** See inputs and outputs of each step of agent and workflow execution, as well as eval metrics as you iterate on code.

Mastra's local dev environment, which we call Mastra Studio, lives at `localhost:4111`:

In Mastra Studio, you can interact with your agents in real-time, observe their decision-making process, review prompts and responses, and debug function calls so you can iterate quickly on prompts, workflows, and integration logic.
