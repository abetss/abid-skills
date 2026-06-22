---
chapter: 8
title: "Dynamic Agents"
part: "II — Building an Agent"
source_pdf_pages: "29-30"
---

# Chapter 8: Dynamic Agents
*Part II: Building an Agent*

The simplest way to configure an agent is to pass a string for its system prompt, a string for the LLM provider and model name, and an object/dictionary for a list of tools that they are provided.

But what if you want to change these things at runtime?

**What are Dynamic Agents?**

A dynamic agent is an agent whose properties—like instructions, model, and available tools—can be determined at runtime, not just when the agent is created.

This means your agent can change how it acts based on user input, environment, or any other runtime context you provide.

Choosing between dynamic and static agents is ultimately a tradeoff between predictability and power.

**Example: Creating a Dynamic Agent**

Here's an example of a dynamic support agent that adjusts its behavior based on the user's subscription tier and language preferences:

```ts
const supportAgent = new Agent({
  name: "Dynamic Support Agent",

  instructions: async ({ runtimeContext }) => {
    const userTier = runtimeContext.get("user-tier");
    const language = runtimeContext.get("language");

    return `You are a customer support agent for our SaaS platform.
    The current user is on the ${userTier} tier and prefers ${language} language.

    For ${userTier} tier users:
    ${userTier === "free" ? "- Provide basic support and documentation links" : ""}
    ${userTier === "pro" ? "- Offer detailed technical support and best practices" : ""}
    ${userTier === "enterprise" ? "- Provide priority support with custom solutions" : ""}

    Always respond in ${language} language.`;
  },

  model: ({ runtimeContext }) => {
    const userTier = runtimeContext.get("user-tier");
    return userTier === "enterprise"
      ? openai("gpt-4")
      : openai("gpt-3.5-turbo");
  },

  tools: ({ runtimeContext }) => {
    const userTier = runtimeContext.get("user-tier");
    const baseTools = [knowledgeBase, ticketSystem];

    if (userTier === "pro" || userTier === "enterprise") {
      baseTools.push(advancedAnalytics);
    }

    if (userTier === "enterprise") {
      baseTools.push(customIntegration);
    }

    return baseTools;
  },
});
```
