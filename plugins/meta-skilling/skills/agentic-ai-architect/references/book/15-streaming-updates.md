---
chapter: 15
title: "Streaming Updates"
part: "IV — Graph-Based Workflows"
source_pdf_pages: "56-58"
---

# Chapter 15: Streaming Updates
*Part IV: Graph-Based Workflows*

> Summary (paraphrased, not a verbatim transcription). Code/API examples are transcribed exactly.

A key to making LLM applications feel fast and responsive is showing users what's happening while the model is still working — incrementally, in stages, when needed.

The author illustrates this with a 2024 trip-planning anecdote: planning a Hawaii trip, he compared OpenAI's o1 pro against Deep Research side by side. o1 pro showed only a spinning "reasoning" box for about three minutes with no feedback. Deep Research instead immediately asked clarifying questions (number of people, budget, dietary needs), then streamed back updates as it found restaurants and attractions. The model that streamed felt much snappier and kept the user in the loop throughout.

*Left: o1 pro (less good). Right: Deep Research (more good).*

## Streaming step completion

The most common thing to stream is the model's output — showing tokens as they're generated. But you can also stream updates from each step of a multi-step workflow or agent pipeline (for example, when an agent is searching, planning, and summarizing in sequence).

## Streaming within steps

Even when you're inside a function that has a defined return type (such as a workflow step), you can write to a stream as new results come in. In Mastra it looks like this:

```ts
import { createStep } from '@mastra/core/workflows'
import { z } from 'zod'

export const testStep = createStep({
  execute: async ({ inputData, mastra, writer }) => {
    const { city } = inputData

    const testAgent = mastra?.getAgent('testAgent')
    const stream = await testAgent?.stream(`What is the weather in London?`)

    await stream!.textStream.pipeTo(writer!)

    return {
      value: await stream!.text,
    }
  },
})
```

## Streaming tool calls

Tool-call streaming improved in March 2026: most major APIs now support streaming tool call results natively.

## Speed matters

As with web apps and mobile apps, perceived response time is crucial in agent engagement. There are no commercially successful agents that feel slow.

The chapter closes with a personal note about a hiking trip in Volcanoes National Park, where the author saw Mount Kilauea shooting lava hundreds of feet into the air — a reminder that nature sometimes delivers a different kind of streaming update.
