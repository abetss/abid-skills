---
chapter: 18
title: "Setting Up Your RAG Pipeline"
part: "V — Retrieval-Augmented Generation (RAG)"
source_pdf_pages: "65-69"
---

# Chapter 18: Setting Up Your RAG Pipeline
*Part V: Retrieval-Augmented Generation (RAG)*

RAG combines the strengths of pre-trained LLMs with the ability to retrieve and incorporate specific and relevant information from your own curated datasets in order to generate more accurate and detailed (and sometimes more up-to-date) responses. Setting up a RAG pipeline involves loading data, creating embeddings, indexing, retrieving relevant information based on a query, and then generating a response using the LLM with the retrieved context.

## Chunking

Chunking is the process of breaking down large documents into smaller, manageable pieces for processing.

The key thing you'll need to choose here is a **strategy** and an **overlap window.** Good chunking balances context preservation with retrieval granularity.

Strategies for doing the actual chunking itself include recursive, character-based, token-aware, and format-specific corpus splitting like Markdown, HTML, JSON, or LaTeX. Mastra supports all of these.

## Embedding

Embeddings are numerical representations of text that capture semantic meaning. These vectors allow us to perform similarity searches. Mastra supports multiple embedding providers like OpenAI and Cohere, with the ability to generate embeddings for both individual chunks and arrays of text.

## Upsert

Upsert operations allow you to insert or update vectors and their associated metadata in your vector store. This operation is essential for maintaining your knowledge base, combining both the embedding vectors and any additional metadata that might be useful for retrieval.

## Indexing

An index is a data structure that optimizes vector similarity search. When creating an index, you specify parameters like dimension size (matching your embedding model) and similarity metric (cosine, euclidean, dot product). This is a one-time setup step for each collection of vectors.

## Querying

Querying involves converting user input into an embedding and finding similar vectors in your vector store. The basic query returns the most semantically similar chunks to your input, based on a similarity score. Under the hood, this is a bunch of matrix multiplication to find the closest point in "n-"dimensional space (think about a geo search with lat/lng, except in 1536-dimensions instead).

The most common algorithm that does this is called *cosine similarity* (although you can use other instead).

**Hybrid Queries with Metadata.** Hybrid queries combine vector similarity search with traditional metadata filtering. This allows you to narrow down results based on both semantic similarity and structured metadata fields like dates, categories, or custom attributes.

## Reranking

Reranking is a post-processing step that improves result relevance by applying more sophisticated scoring methods. It considers factors like semantic relevance, vector similarity, and position bias to reorder results for better accuracy.

It's a more computationally intense process, so you typically don't want to run it over your entire corpus for latency reasons — you'll typically just run it on a code example.

## Code Example

Here's some code using Mastra to set up a RAG pipeline. Mastra includes a consistent interface for creating indexes, upserting embeddings, and querying, while offering their own unique features and optimizations, so while this example uses PgVector, you could easily use another DB instead. This illustrates a common pattern for building context-aware AI responses with proper fallback handling.

```ts
import { Mastra } from "@mastra/core";
import { MDocument, PgVector } from "@mastra/rag";
import { embedMany, embed } from "ai";
import { openai } from "@ai-sdk/openai";

// Initialize document and create chunks
const doc = MDocument.fromText("Your text content here...");
const chunks = await doc.chunk({
  strategy: "recursive",
  size: 512,
  overlap: 50,
});

// Generate embeddings
const { embeddings } = await embedMany({
  values: chunks.map(chunk => chunk.text),
  model: openai.embedding("text-embedding-3-small"),
});

// Initialize vector store and Mastra
const pgVector = new PgVector(process.env.POSTGRES_CONNECTION_STRING);
const mastra = new Mastra({ vectors: { pgVector } });

// Store embeddings
await pgVector.createIndex("embeddings", 1536);
await pgVector.upsert(
  "embeddings",
  embeddings,
  chunks?.map(chunk => ({ text: chunk.text }))
);

// Query example
const query = "insert query here";
const { embedding } = await embed({
  value: query,
  model: openai.embedding("text-embedding-3-small"),
});

// Retrieve similar chunks
const results = await pgVector.query("embeddings", embedding);
const relevantContext = results
  .map(result => result?.metadata?.text)
  .join("\n\n");

// Generate response
const completion = await openai("gpt-4o-mini").generate(
  `Please answer the following question:
  ${query}

  Based on this context: ${relevantContext}
  If the context lacks sufficient information, please state that
  explicitly.`
);

console.log(completion.text);
```

This code:

1. Uses OpenAI's GPT-4o-mini model to generate a response

2. Constructs a prompt that includes a user query and relevant context

3. Instructs the model to explicitly state if there's insufficient information

4. Logs the generated text response

**Note:** There are advanced ways of doing RAG: using LLMs to generate metadata, using LLMs to refine search queries; using graph databases to model complex relationships. These may be useful for you, but start by setting up a working pipeline and tweaking the normal parameters — embedding models, rerankers, chunking algorithms — first.
