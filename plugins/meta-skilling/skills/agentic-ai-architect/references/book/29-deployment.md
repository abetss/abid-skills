---
chapter: 29
title: "Deployment"
part: "VIII — Development & Deployment"
source_pdf_pages: "102-103"
---

# Chapter 29: Deployment
*Part VIII: Development & Deployment*

Most teams are wrapping their agents in a server, wrapping the server in a Docker container, and scaling that.

## The core agent loop

The core agent loop is long-running and stateful. Sure, you can model each "turn" as a separate request/response cycle.

But you still have to think about streaming a response back to the user, rather than simply sending a single JSON blob.

## Agentic workflows

Relatively speaking, similar to the workloads on durable execution engines like Temporal and Inngest. But they are still tied to a specific user request.

Agents can run on serverless platforms, but teams need to work through dealing with timeouts from long-running processes, bundle size issues, etc.

## Using a managed platform

The agent teams sleeping the soundest at night are the ones we see who figure out how to run their agents using auto-scaling managed services.

Teams using container services like AWS EC2, Digital Ocean, or equivalent seem to be all right as long as they have a B2B use case that won't have sudden usage spikes.
