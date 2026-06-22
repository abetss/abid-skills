---
chapter: 26
title: "Tracing"
part: "VII — Observability & Evals"
source_pdf_pages: "85–88"
---

# Chapter 26: Tracing
*Part VII: Observability & Evals*

There are two uniquely hard parts of building AI applications, that are typically the barrier for teams shipping agents into production: accuracy and token cost.

The answer for both: observability.

Let's dive in.

## Why accuracy and token cost matter

**Accuracy.** AI applications are built on top of non-deterministic models. Teams that have shipped agents into production typically building systems to detect regressions and look at production data every day. Agents can regress while still returning `200 OK`.

**Token cost.** Agents burn tokens. Opus 4.6 and GPT 5.4 can run in the background, in loops, generating multiple potential responses. But this can be costly.

We know several startups that raised $5m seed rounds, went viral, and ended up with a $500k token bill the next month. You can make something people want, but if your tokens cost 10x your revenue, you still have a big problem.

## Observability

*Observability* is a word that gets a lot of airplay, but since its meaning has been largely diluted and generalized by self-interested vendors let's go to the root.

The initial term was popularized by Honeycomb's Charity Majors in the late 2010s to describe the quality of being able to visualize application traces.

To debug a function, it would be really *nice* to be able to see the input and output of every function it called. And the input and output of every function *those* functions called. (And so on, and so on, turtles all the way down.)

This kind of telemetry is called a *trace*, which is made up of a tree of *spans*. (Think about a nested HTML document, or a flame chart.)

The standard format for traces is known as Open-Telemetry, or OTel for short.

When monitoring vendors began supporting tracing, each had a different spec — there was no portability. Lightstep's Ben Sigelman helped create the common Otel standard, and larger vendors like Datadog (under duress) began to support Otel.

## Visualizing traces

There's a large number of observability vendors, both older backend and AI-specific ones, but the UI patterns converge:

> *[Screenshot: Tracing UI — A sample tracing screen]*

What this sort of UI screen gives you is:

- **A trace view.** This shows how long each step in the pipeline took (e.g., parse_input, process_request, api_call, etc.)
- **Input/output inspection.** Seeing the exact "Input" and "Output" in JSON is helpful for debugging data flowing into and out of LLMs
- **Call metadata.** Showing status, start/end times, latency, etc.) provides key context around each run, helping humans scanning for anomalies.

## Setting this up on a project

Typically you'll want a cloud observability provider so you can point your production traces at it, though some teams prefer to self-host within their environments.

It's also nice to be able to look at this data locally when you're developing. Here's a screenshot of how this looks in Mastra Studio:
