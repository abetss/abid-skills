---
chapter: 5
title: "Model Routing and Structured Output"
part: "II — Building an Agent"
source_pdf_pages: "18-19"
---

# Chapter 5: Model Routing and Structured Output
*Part II: Building an Agent*

It's useful to be able to quickly test and experiment with different models. Various libraries provide an abstraction known as *model routing*.

Let's pull up that example again from last chapter, which uses Mastra's built-in model routing.

```ts
import { Memory } from '@mastra/memory'
import { Agent } from '@mastra/core/agent'

export const agent = new Agent({
  name: 'my-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-5.1',
})

const result = await agent.generate("What is the weather today?");
```

The nice thing about structuring the code this way, whether you're using Mastra or something else, is that it's a one-line fix to swap in a different model and provider — instead of needing to rip out a provider SDK.

**Structured output**

When you use models as part of an application, you often want them to return data in JSON format instead of unstructured text. Most models support "structured output" to enable this.

Here's an example of requesting a structured response by providing a schema:

```ts
import { z } from 'zod'

const response = await agent.generate('Help me plan my day.', {
  structuredOutput: {
    schema: z.array(
      z.object({
        name: z.string(),
        activities: z.array(z.string()),
      }),
    ),
  },
})
```

Models are very powerful for processing unstructured or semi-structured text. Consider passing in the text of a resume and extracting a list of jobs, employers, and date ranges, or passing in a medical record and extracting a list of symptoms.

Structured output and model routing actually compose nicely together. You can usually route to a cheaper/faster model specifically for structured extraction tasks, since they tend to require less reasoning than open-ended generation.
