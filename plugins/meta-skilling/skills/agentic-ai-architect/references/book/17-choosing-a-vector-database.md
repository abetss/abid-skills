---
chapter: 17
title: "Choosing a Vector Database"
part: "V — Retrieval-Augmented Generation (RAG)"
source_pdf_pages: "63-64"
---

# Chapter 17: Choosing a Vector Database
*Part V: Retrieval-Augmented Generation (RAG)*

One of the biggest questions people having around RAG is how they should think of a vector DB.

There are multiple form factors of vector databases:

1. A feature on top of open-source databases (**pgvector** on top of Postgres)
2. Standalone open-source (**Chroma**)
3. Standalone hosted cloud service (**Turbopuffer**).
4. Hosted by an existing cloud provider (**Cloudflare Vectorize**).

Our take is that unless your use-case is exceptionally specialized, the vector DB feature set is mostly commoditized.

Back in 2023, VC funding drove a huge explosion in vector DB companies.

In 2026, many of these companies are doing layoffs (hint: any vector DB company that's done layoffs is also struggling with adoption).

Today, teams report wanting to prevent infra sprawl (yet *another* service to maintain). Our recommendation:

- If you're already using Postgres for your app backend, pgvector is a fine choice.
- If you're spinning up a new project, Chroma or Turbopuffer are great defaults.
- If your cloud provider has a managed vector DB service, start with that.
