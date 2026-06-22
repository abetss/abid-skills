---
chapter: 19
title: "Alternatives to RAG"
part: "V — Retrieval-Augmented Generation (RAG)"
source_pdf_pages: "70-71"
---

# Chapter 19: Alternatives to RAG
*Part V: Retrieval-Augmented Generation (RAG)*

Great, now you know how RAG works. But does it matter? Or, put like a Twitter edgelord, is RAG dead?

Not yet, we think. But there are some simpler approaches you should reach for first.

## Give your agent search tools

Instead of pre-parsing all your documents, start by giving your agent a relevant set of search tools to search through its corpus of data.

One of our investors built a variety of tools to query her website, and then bundled them into a MCP server she could give to an agent.

She then asked the agent about her favorite restaurants (it recommended Flour + Water in San Francisco) and her favorite portfolio companies (it said she likes all of her companies equally).

## Let your agent run code

Opus 4.6 and GPT 5.4 are really good at writing code. Consider solving your search problem by giving your model a code writing tool and running it in a loop. (*What would Claude Code do?*)

## Feed the model full context

Gemini has 1m tokens now. Maybe you should just load all the relevant content directly into the context.

The downsides: cost and "context rot" (recall can drop far before hitting context window limits.)

## Extract entities and relationships

Use a model to extract rich semantic information (section references, entity names, etc), and then throw those into the context window as well.

## Conclusion

We're engineers. We can over-engineer things.

Unless you're sure this is a pure document processing problem, build an agent first. Use RAG as a fallback.
