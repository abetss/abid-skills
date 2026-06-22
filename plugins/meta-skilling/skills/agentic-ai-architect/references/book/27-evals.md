---
chapter: 27
title: "Evals"
part: "VII — Observability & Evals"
source_pdf_pages: "89–95"
---

# Chapter 27: Evals
*Part VII: Observability & Evals*

While traditional software tests have clear pass/fail conditions, AI outputs are non-deterministic — that is, an LLM can take the same input and produce different outputs. (You've seen how ChatGPT and Claude offer the option to regenerate the results of your query as soon as they finish spitting it out, right?)

**Evals** help bridge this gap by providing quantifiable metrics for measuring agent quality.

Think about evals sort of like including, say, performance testing in your CI pipeline. There's going to be some randomness in each result, but on the whole and over time there should be a correlation between application performance and test results.

When writing evals, it's important to think about what *exactly* you want to test.

There are different kinds of evals just like there are different kinds of tests.

Unit tests are easy to write and run but might not capture the behavior that matters; end-to-end tests might capture the right behavior but they might also be more flaky.

Similarly, if you're building a RAG pipeline or a structured workflow, you may want to test each step along the way — and then after that test the behavior of the system as a whole.

## Seeing evals over time

It's also nice to be able to see your evals (more on evals later) in a cloud environment with your team.

For each of their evals, people want to see a side-by-side comparison of how the agent responded versus what was expected.

They want to see the overall score on each PR (to ensure there aren't regressions), and the score over time, and to filter by tags, run date, and so on.

Eval UIs tends to look like this:

> *[Screenshot: Eval UI — A sample evaluation screen]*

* * *

## Offline vs. online evals

There are two modes teams run evals in.

**Offline** evals run against a fixed dataset before deploys. These tend to catch regressions.

**Online** evals run against live production traffic. You sample real requests, score them, and watch metrics over time. These can be noisy (your inputs vary over time). But real users break your agents in new and exciting ways.

Most teams start offline. Then teams add online evals once their agent is in production.

## Building your eval dataset

There are three ways to get a dataset of test cases.

**Hand-curate.** This is a good place to start because it forces you to think clearly about what good looks like. You may want to work with a subject-matter expert if you're working in an unfamiliar domain.

**Generate them synthetically.** This is fast, but you should check the output; models tend to generate easy cases.

**Mine production logs.** This only works when you're in production, but it's the highest-signal source.

A mature eval dataset is a mix of all three. Like normal code, as you find bugs, fix them and add test cases to prevent future regressions.

> *[Screenshot: Datasets in Mastra Studio]*

## LLM-as-judge for textual evals

For textual evals, the most common pattern is using a second model as the scorer.

You pass the output — and optionally the original input and retrieved context — to a judge model with a rubric. It returns a score and sometimes an explanation.

It works well. It scales. It handles cases where there's no single right answer. It also does well judging metrics like hallucination and faithfulness (whether responses accurately represent provided context).

It's not perfect: judges tend to prefer longer answers even when they're not better. Consider picking a judge from a different model family as your agent; a judge can favor outputs that sound like itself.

```ts
import { Agent } from '@mastra/core/agent'
import { createFaithfulnessScorer } from '@mastra/evals/scorers/prebuilt'

export const evaluatedAgent = new Agent({
  scorers: {
    relevancy: {
      scorer: createFaithfulnessScorer({ model: 'openai/gpt-5.1' }),
    },
  },
})
```
*Adding a LLM-as-judge for faithfulness in Mastra*

## Classification or labeling evals

Classification or labeling evals help determine how accurately a model tags or categorizes data based on predefined categories (e.g., sentiment, topics, spam vs. not spam).

This can include broad labeling tasks (like recognizing document intent) or fine-grained tasks (like identifying specific entities aka entity extraction).

## Tool calling evals

Tool usage evals for agents measure how effectively a model or agent calls external tools or APIs to solve problems.

For example, just like you would write `expect(fn).toBeCalled` in the JavaScript testing framework Jest, you would want to see similar functions for agent tool use.

## Multi-turn evals

Most textual evals are built around single-turn interactions. But agents are multi-turn by nature.

A multi-turn eval runs the agent through a full conversation or task sequence and grades the whole thing. Did it maintain context across turns? Did it recover when a tool failed? Did it stay on task after a tangent?

## Task completion

For agents doing things in the world, the most important eval is the simplest one: did it finish the job?

Did the support agent resolve the ticket? Did the coding agent pass the tests? Did the research agent return a usable answer?

## Prompt engineering evals

Prompt engineering evals explore how different instructions, formats, or phrasings of user queries impact an agent's (non-deterministic) results performance.

They look at both the **sensitivity** of the agent to prompt variations (whether small changes produce large differences in results) and the **robustness** to adversarial or ambiguous inputs.

All things "prompt injection" fall in this category.

## A/B testing

Leaders of larger consumer and developer tools AI companies like Perplexity and Replit joke that they rely more on A/B testing of user metrics than evals per se. This works if you have enough traffic that degradation in agent quality is quickly visible!

## Human data review

In addition to automated tests, high-performing AI teams regularly review production data. Typically, the easiest way to do this is to view traces which capture the input and output of each step in the pipeline.

Many correctness aspects (e.g., subtle domain knowledge, or an unusual user request) can't be fully captured by rigid assertions, but human eyes catch these nuances.

## Observability & evals are even more important than you think

This might be relatively long chapters, but observability is one of the most important pieces when shipping agents into production.

Teams can spend months staring closely at their observability tools as they move from prototype to production.

We've written a follow-up book covering much more on these topics: **Patterns For Building AI Agents.** We encourage you to read it, especially as you're pushing your agent into production.
