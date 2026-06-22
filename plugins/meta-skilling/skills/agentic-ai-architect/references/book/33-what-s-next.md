---
chapter: 33
title: "What's Next"
part: "X — Everything Else"
source_pdf_pages: "118-119"
---

# Chapter 33: What's Next
*Part X: Everything Else*

This book was intentionally written as a getting-started guide. We have a sequel, *Patterns for Building AI Agents*, that dives more into productionizing them.

*Patterns* includes more on context engineering, creating high-quality eval suites by working with domain experts and analyzing failure modes, plus more on agent security.

The agent space is moving incredibly quickly.

We don't have a crystal ball, but from our vantage point as a prominent agent framework, here's what we see:

- **Reasoning models will continue to get better.** Claude Opus 4.6 introduced "adaptive thinking," where the model dynamically allocates reasoning effort based on problem complexity. GPT-5.4 offers explicit reasoning effort controls (low through xhigh) so you can tune latency/depth per request. As the model does more planning, our job may shift from choreographer to architect.
- **We'll make progress on agent learning.** Agents emit traces, but right now the feedback loop to improve their performance runs through their human programmers.
- **Synthetic evals are becoming standard practice.** Generating evals automatically from production traces, with human approval, has moved from experimental to mainstream. People aren't going to hand code evals in the era of Claude Code.
- **Agent & MCP security will continue to be a challenge.** As agents ingest more data and take more actions, prompt injection attacks will multiply. And MCP's rapid adoption has created a large and fast-growing attack surface.
- **The eternal September of AI will continue.** Every month brings new developers who haven't learned how to write good prompts or how to do context engineering. Meanwhile, the rapid pace of model updates means even established teams are constantly adapting their implementations.

In a field where the ground shifts constantly, we're all perpetual beginners. To build something enduring, you have to stay humble.
