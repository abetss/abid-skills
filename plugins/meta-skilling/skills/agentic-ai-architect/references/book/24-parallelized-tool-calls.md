---
chapter: 24
title: "Parallelized Tool Calls"
part: "VI — Multi-Agent Systems"
source_pdf_pages: "80"
---

# Chapter 24: Parallelized Tool Calls
*Part VI: Multi-Agent Systems*

In most of the workflows we've covered, tool calls are sequential by default.

Parallel tool calling lets the model batch those calls into a single step. If the results don't depend on each other, they can run simultaneously. You can imagine opening several URLs in parallel to complete research faster, or running several coding subagents in parallel to test different approaches.

Over the last several months, all three major providers have added support. OpenAI added it earliest; Anthropic has extended the idea the furthest.

Today, Claude models enable parallel tool calls by default. You can disable this if your workflow requires strict sequential execution — for instance, when earlier tool results need to gate what gets called next.
