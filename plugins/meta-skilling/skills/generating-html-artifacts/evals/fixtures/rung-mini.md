# rung-mini — retrieval in one page

**Status:** fixture for the generating-html-artifacts evals · generated 2026-07-22

A tiny learning doc that exercises the component router: one ASCII diagram, one
comparison table, one command, one fold of extra depth.

## How the pieces fit

Your `bm search` command fans out to two engines and merges the results:

```
┌────────────┐      query       ┌────────────┐
│ web client │ ───────────────▶ │ API server │
└────────────┘                  └─────┬──────┘
                                      │ reads/writes
                                      ▼
                                ┌────────────┐
                                │  database  │
                                └────────────┘
```

The client never talks to the database directly — every read goes through the
API server, which is why auth lives in exactly one place.

## Two engines compared

| Engine    | What it scores            | Strength              | Weakness                |
|-----------|---------------------------|-----------------------|-------------------------|
| Lexical   | BM25 over terms           | Exact phrases, names  | Synonyms, paraphrase    |
| Dense     | Embedding cosine distance | Concepts, paraphrase  | Rare tokens, exact IDs  |

## Try it

```bash
bm search "sqlite backup approach" --limit 5 --explain
```

<!-- more -->
The `--explain` flag prints each engine's ranked list before fusion, plus the
RRF score contribution per document: `1 / (60 + rank)`. A document ranked 1st
by lexical and 4th by dense scores `1/61 + 1/64 ≈ 0.0320`. Use this when a note
you expected is missing — check which engine ranked it poorly and why.
<!-- /more -->

## Vocabulary

- **RRF** — Reciprocal Rank Fusion; merges ranked lists by position, not score.
- **ANN index** — approximate nearest-neighbor structure; trades recall for speed.
- **Chunk** — the unit of text one embedding vector represents.
