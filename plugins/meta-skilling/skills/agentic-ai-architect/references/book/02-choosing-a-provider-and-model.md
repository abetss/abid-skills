---
chapter: 2
title: "Choosing a Provider and Model"
part: "I — Prompting a Large Language Model (LLM)"
source_pdf_pages: "5-7"
---

# Chapter 2: Choosing a Provider and Model
*Part I: Prompting a Large Language Model (LLM)*

One of the first choices you'll need to make building an AI application is which model to build on.

Here are some considerations:

## Hosted vs open-source

The first piece of advice we usually give people when building AI applications is to start with a hosted provider.

For text modality use cases — including text, code, structured output, tool calls (but not images, voice, or video), the state-of-the-art hosted model providers in March 2026 are OpenAI, Anthropic, or Google Gemini. We recommend you start there.

Perhaps you eventually move some of your workload to SoTA open-source providers like Qwen, Kimi, Deepseek, Minimax. But *make it work, make it right, make it fast/cheap* — in that order. Don't make yourself debug infra issues right off the bat.

To give yourself flexibility later, use a model routing library (more on that later).

## Model size: Accuracy vs cost/latency

Every provider has larger, medium, and small models (Anthropic's Claude 4.6 Opus vs Sonnet vs Haiku, OpenAI's GPT-5, GPT-5 mini, GPT-5 nano).

The larger a model is, the more mathematical operations (matrix multiplication) it has to perform to generate your answer. That makes it higher quality, but also more expensive and slower.

Again, *make it work, make it right, make it fast/cheap* — in that order.

Start with the larger models, when you need to worry about cost saving during scaling, then figure out how to move workloads to cheaper models.

## Context window size

One variable you may want to think about is the "context window" of your model. How many tokens can it take?

As of March 2026, the longest context window is offered by Google. Gemini 3.1 supports a one million token context window (roughly 2,000 pages of text), with Anthropic offering the same for Sonnet 4.6 (but only in the API, in beta)

This allows some interesting applications; we know a developer who built a support assistant for an iOS app and simply dumped the entire 800,000-token codebase in its context window.

## Reasoning models

Another type of model is what's called a "reasoning model." Starting in late 2024, models began to do a lot of logic internally before returning a response.

It might take seconds, or minutes, to give a response, and it will return a response all at once (while streaming some "thinking steps" along the way).

Today most state-of-the-art models like GPT 5.4 are reasoning models — though most let you can turn down `effort` to low when using them in an API to reduce latency. For lower-complexity tasks, you could also use pre-reasoning models like GPT-4o.

## Providers and models (March 2026)

| Provider | Form Factor(s) | Default Model | Cheap / Fast Model | Reasoning Model(s) |
| --- | --- | --- | --- | --- |
| OpenAI | Hosted | **GPT-5.4** | GPT-5 mini, GPT-5 nano | Reasoning built into GPT-5.4 with effort controls; GPT-5.2 Thinking / Pro |
| Anthropic | Hosted | **Claude Sonnet 4.6** | Claude Haiku 4.5 | Claude Opus 4.6 |
| Google Gemini | Hosted | **Gemini 3 Flash** | Gemini 3.1 Flash-Lite | Gemini 3.1 Pro |
| DeepSeek | OSS | **DeepSeek V3.2** | Efficient by default (MoE architecture) | DeepSeek R1 series |
| Alibaba (Qwen) | OSS | **Qwen 3.5** | Qwen3-30B-A3B | QwQ-32B |
