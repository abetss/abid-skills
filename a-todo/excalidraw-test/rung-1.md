# rung-1 — Foundations: what retrieval is made of

**Status:** material-ready · generated 2026-07-20 · lab grounded at `local-bookmarks` `master@e8e308d0` (clean; verified at generation)

**Requirement (from `../brief.md`):** Command the mechanics vocabulary the rest of the block assumes — what an embedding is, how lexical and dense scoring differ and combine, what an ANN index trades away, what a cross-encoder adds, what chunking decides — well enough to explain each concept and locate it in the lab's own code and data.

**Provenance note:** every source dump in `../sources-raw/` is stamped with URL, fetch date, and a fidelity boundary. Most dumps are **excerpt + faithful reconstruction** (WebFetch condenses pages); text inside quotation marks is verbatim from the source, surrounding prose is reconstructed. Claims below inherit that caveat. App claims cite the lab's actual files, read in full at generation.

---

## Primer

### The one mental model: your search command is the whole field in miniature

Run `bm search "query"` and this happens ([src/search_cmd.ts:59-78](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/search_cmd.ts)):

```
                       your query text
                             │
             ┌───────────────┴────────────────┐
             │                                │
   embed(query, RETRIEVAL_QUERY)      toMatch(query) → "tok1" OR "tok2"
   → 768 floats                              │
             │                                │
   vectorSearch: cosine distance      keywordSearch: FTS5 bm25()
   over ALL rows, ORDER BY ASC        over full-body index, ORDER BY ASC
             │                                │
     ranked list #1 (pool)            ranked list #2 (pool)
             └───────────────┬────────────────┘
                             │
                  rrf([v, kw])  k=60 — fuse by RANK, not score
                             │
                   top `limit` hits printed
```

Two independent retrieval engines — **dense** (meaning-based) and **lexical** (word-based) — each produce a ranked list; **Reciprocal Rank Fusion** merges them by position. Everything in this rung is understanding why each box exists, what it's good and bad at, and what the two boxes you *don't* have (ANN index, cross-encoder reranker) would add. Hybrid is your default mode; `keyword` and `semantic` run each engine alone ([src/search_cmd.ts:64-68](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/search_cmd.ts)).

### What an embedding actually is

An embedding model takes a piece of text and returns "an array of floating point numbers" of **fixed length regardless of input size** — Willison: the array will "always be the same length, no matter how long the content is" ([Willison, *Embeddings*](https://simonwillison.net/2023/Oct/23/embeddings/) · [raw dump](../sources-raw/rung1-willison-embeddings.md)). Think of those numbers as "co-ordinates in a very weird multi-dimensional space" where "location…represents the semantic meaning" of the text. One property drives every use: **texts that are near each other in this space are semantically similar** — even when they share no words.

That's the entire trick behind what Willison calls "vibes-based search": his example query "sqlite backup tools" surfaces relevant posts that never contain the word "backups" ([same source](../sources-raw/rung1-willison-embeddings.md)). Contrast with keyword search, which can *only* match literal tokens — the complementary failure modes are the reason your lab runs both engines.

Your lab's concrete instance: `gemini-embedding-001`, asked for **768 dimensions** via `outputDimensionality` ([src/embed.ts:15-20](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/embed.ts), [src/config.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/config.ts) — `EMBED_DIMS = 768`), stored per note in a `F32_BLOB(768)` column ([src/db.ts:48](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts)). One vector per note — that granularity decision is the chunking section's subject.

### Cosine: how "near" is measured

Similarity between two vectors is almost always **cosine similarity**: the dot product of the two vectors divided by the product of their magnitudes — which measures the **angle** between them, not their lengths. Willison's reference implementation is exactly that formula: `dot_product / (magnitude_a * magnitude_b)` ([Willison](https://simonwillison.net/2023/Oct/23/embeddings/) · [dump](../sources-raw/rung1-willison-embeddings.md)). Identical direction → 1.0; his worked example scores ~0.88 for a strongly related article. Because only *direction* carries meaning, cosine ignores vector magnitude entirely — hold that thought for the normalization subtlety below.

Your lab computes **cosine distance**, not similarity: libSQL's `vector_distance_cos` is documented as "Cosine distance (1 - cosine similarity)" with range **0 → 2** — "close to 0 indicates vectors are nearly identical… close to 1… orthogonal… close to 2… opposite directions" ([Turso/libSQL docs](https://docs.turso.tech/features/ai-and-embeddings) · [dump](../sources-raw/rung1-libsql-vector.md)). Lower = more similar, which is why `vectorSearch` orders `ASC` ([src/db.ts:146-156](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts)) — the docs' own example does the same. When you read a `score=0.4123` line from `bm search --mode semantic`, you're reading a *distance*: similarity ≈ 1 − 0.4123.

### The normalization subtlety (a real almost-bug worth understanding)

Google trained `gemini-embedding-001` with **Matryoshka Representation Learning (MRL)** — the model "learn[s] high-dimensional embeddings that have initial segments (or prefixes) which are also useful, simpler versions," so you can keep just the first 768 of 3072 dimensions ([Gemini embeddings doc](https://ai.google.dev/gemini-api/docs/embeddings) · [dump](../sources-raw/rung1-gemini-embeddings-docs.md), near-verbatim excerpt). The documented quality cost at 768 is nearly nil: mean scores on MTEB (a standard benchmark suite that averages embedding quality across many tasks — higher is better) are 68.17 @ 1536 vs **67.99 @ 768**, degrading for real only by 256 (66.19) and 128 (63.31) (same dump). That's why your `EMBED_DIMS = 768` with the comment "plenty at this scale" is a well-supported choice ([src/config.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/config.ts)).

But the same doc says: the default 3072-dim output is unit-normalized, while **truncated dimensions are not** — "you must manually normalize non-3072 dimensions" (same dump). Your lab stores the 768-dim vectors raw — there is no normalization anywhere in [src/embed.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/embed.ts) or [src/db.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts).

Is that a bug? **No — and knowing *why* is the lesson** *(local inference, ours — premises above)*: cosine divides by both magnitudes, so scaling a vector changes nothing about its cosine distance to anything else. Google's "must normalize" matters for **dot-product** or Euclidean comparisons, where magnitude leaks into the score. Your pipeline is magnitude-immune because every comparison goes through `vector_distance_cos`. If anyone ever swaps that function for a dot product (a common "optimization" — dot of unit vectors *equals* cosine, but only for unit vectors), the missing normalization becomes a live bug. You'll verify this empirically in the build.

### Task types: queries and documents are different kinds of text

Your `embed()` takes a `TaskType` — documents are embedded with `RETRIEVAL_DOCUMENT` at index time ([src/index_cmd.ts:61](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/index_cmd.ts)), queries with `RETRIEVAL_QUERY` at search time ([src/search_cmd.ts:67,72](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/search_cmd.ts)). Why: a query ("best sqlite backup approach?") and a document (three paragraphs about a backup tool) are different *shapes* of text that should land near each other when they're about the same thing. Gemini exposes this as task types and warns "it is important that the task is used consistently" ([Gemini doc dump](../sources-raw/rung1-gemini-embeddings-docs.md)); the full table also pairs `QUESTION_ANSWERING` and `FACT_VERIFICATION` query-side types with `RETRIEVAL_DOCUMENT` corpus embeddings. This is the same idea as the `query:` / `passage:` prefixes Willison used with E5-large-v2 ([Willison dump](../sources-raw/rung1-willison-embeddings.md)) — your `embed.ts` header comment even says so ("the Gemini equivalent of getting nomic's prefixes right", [src/embed.ts:1-3](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/embed.ts)). Asymmetric embedding is the norm in retrieval, and mixing the sides up silently degrades ranking.

### Lexical scoring: TF-IDF → BM25, the 50-year-old engine that still matters

First, the name in the header: **TF-IDF** scores a document by **t**erm **f**requency (how often a query word appears in it) weighted by **i**nverse **d**ocument **f**requency (how rare that word is across the corpus); BM25 is its refined successor — the same two ideas plus term-frequency saturation and length normalization. Keyword search ranks documents by combining three signals ([Elastic, *Practical BM25 Part 2*](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) · [dump](../sources-raw/rung1-elastic-bm25.md), excerpt+reconstruction — the formula on the page is an image, reconstructed to standard form in the dump):

1. **IDF — rare words carry the signal.** `IDF(qᵢ) = ln((docCount − f(qᵢ) + 0.5)/(f(qᵢ) + 0.5))`. Elastic's worked example: a term appearing in *all* 4 docs scores IDF ≈ **0.074** — nearly nothing — while a term in only 2 of 4 docs scores higher. A word every bookmark contains ("the", or in your corpus probably "AI") contributes almost zero ranking signal.
2. **Term-frequency saturation — k1.** More occurrences help, with diminishing returns approaching an asymptote. Elastic's increments with k1=10: 1st occurrence +0.0741, 2nd +0.0618, 3rd +0.0523 (slow saturation); with k1=0.01 the 2nd occurrence adds only +0.00037 (instant saturation). k1 sets how fast "mentions it a lot" stops mattering.
3. **Length normalization — b (0→1).** b=1 fully penalizes documents longer than the average; b=0 ignores length. With b high, *match density* (matched terms ÷ length) drives ranking, so a short note that's all about your query beats a long note that mentions it once.

Your lab gets all of this from SQLite FTS5's built-in `bm25()` with **k1 = 1.2 and b = 0.75 hard-coded** ([SQLite FTS5 docs](https://sqlite.org/fts5.html) · [dump](../sources-raw/rung1-sqlite-fts5-bm25.md), high-fidelity excerpt). One quirk you must know to read your own output: FTS5 "multiplies the result by -1 before returning it, ensuring that better matches are assigned numerically lower scores" — so **BM25 scores in your lab are negative, best-first means `ORDER BY … ASC`** ([src/db.ts:170-174](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts) does exactly that), and a `score=-8.1` beats a `score=-2.3`.

Two lab-specific details ([src/db.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts)): the FTS index covers `title, author, summary, tags, body` (path is unindexed), all columns at default weight 1.0; and `toMatch()` (lines 160-163) lowercases the query, strips punctuation, and joins tokens with `OR` inside quotes — because FTS5's MATCH syntax treats bare punctuation as operators and would otherwise throw. Cost of that choice *(app fact + local inference)*: an OR-of-tokens query matches documents containing *any* query word, leaning on BM25's IDF to keep common-word matches from ranking high — a phrase like "context rot" matches every note containing just "context".

### Dense vs lexical: complementary failure modes, hence hybrid

Neither engine dominates. Dense retrieval finds **vocabulary-mismatched** content (the "backups" example) but is weak at exact identifiers, names, and rare tokens — and your corpus is full of those (tool names, personal names, `bm`, `FTS5`). Lexical BM25 nails exact tokens and fails at synonyms/paraphrase. Weaviate's framing of why hybrid exists: combine "the accuracy of keyword-based search with the semantic understanding of vector search" ([Weaviate, *Hybrid Search Explained*](https://weaviate.io/blog/hybrid-search-explained) · [dump](../sources-raw/rung1-weaviate-hybrid-search.md), excerpt+reconstruction). This is capability Q4's seed: *when* should you use which — and the honest foundations-level answer is "keyword for identifier-shaped queries, semantic for concept-shaped queries, hybrid when you don't know" — which you will test on your own corpus in the build, and study properly in rung-3.

### RRF: fusing two rankings without comparing their scores

The two engines' scores are incomparable — BM25 emits negative unbounded numbers, cosine distance lives in [0,2]. RRF sidesteps normalization entirely by using only each document's **rank position** in each list:

```
RRF score(d) = Σ over lists 1/(k + rank(d))
```

([Weaviate dump](../sources-raw/rung1-weaviate-hybrid-search.md), formula attributed to Benham & Culpepper 2018.) Weaviate's worked example, with k=0: doc A = BM25 rank 1 + dense rank 3 → 1/1 + 1/3 = **1.33**; doc B = rank 2 + rank 1 → **1.5**; doc C = rank 3 + rank 2 → **0.83**; final order **B > A > C**. The lesson in those three numbers: RRF rewards documents that rank *decently in both lists* over documents that top one list and miss the other.

Your `rrf()` is thirteen lines implementing exactly that with **k = 60** — the conventional smoothing constant *(the article's k=0 is pedagogical; that k=60 is the default in common implementations such as Elasticsearch is general-practice knowledge, ours to flag — not from the cited page)* — as `1/(k + i + 1)` with zero-indexed `i`, i.e. rank 1 contributes 1/61 ([src/rrf.ts:7-19](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/rrf.ts)). Its file comment states the *why* precisely: "merge ranked lists by position, not by raw score (so BM25's negative scores and cosine distance never need to be normalized together)." What k does *(local inference from the formula)*: with k=60, ranks 1 and 5 contribute 1/61 vs 1/65 — a small gap — so k dampens how much winning the top slot matters; with k=0 rank 1 is worth 3× rank 3. Note also `search_cmd.ts` widens the candidate pool before fusing — `pool = max(limit*3, 20)` per engine ([src/search_cmd.ts:70-77](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/search_cmd.ts)) — because a doc at rank 15 in both lists may still deserve a top-10 hybrid slot.

One fidelity flag: Weaviate's page also offers `relativeScoreFusion` (score-normalizing fusion, and an `alpha` weight: 0 = pure keyword, 1 = pure vector, default 0.75); the dump could not capture its internals verbatim and marks them as to-verify — treat the *existence* of score-based fusion as sourced, its mechanics as unverified ([dump](../sources-raw/rung1-weaviate-hybrid-search.md)).

### ANN: the index you deliberately don't have

Your `vectorSearch` is a brute-force scan: cosine distance against **every** row, `ORDER BY` — O(N) per query, with the in-code comment "trivially fast at this scale, no ANN index needed" ([src/db.ts:145-156](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts)). At ~450 notes that's the right call, and Willison agrees at much larger scale: brute-force in SQLite is fine to ~20k items, "I'm not convinced you need an entirely new database" ([Willison dump](../sources-raw/rung1-willison-embeddings.md)).

What an **Approximate Nearest Neighbor** index buys when N grows: sublinear query time, paid for with *recall* — it may miss true neighbors. Pinecone's HNSW numbers make the trade concrete: recall ranging from ~80% at 1ms up to 100% at 50ms per 1,000 queries (Sift1M; the dump's phrasing leaves ambiguous whether those times are per query or per 1,000-query batch), with memory scaling in the graph's connectivity parameter M ([Pinecone, *HNSW*](https://www.pinecone.io/learn/series/faiss/hnsw/) · [dump](../sources-raw/rung1-ann-hnsw.md), excerpt+reconstruction). HNSW's intuition: a layered graph with "longer edges in the highest layers (for fast search) and shorter edges in the lower layers (for accurate search)" — enter at the sparse top, greedily hop toward the query, drop a layer, repeat to the dense bottom. Global-first, then local-refine; built from skip-list + navigable-small-world ideas with (poly)logarithmic search complexity.

When your corpus outgrows brute force, the upgrade is one function away in the same database: libSQL ships `libsql_vector_idx` + `vector_top_k` ([Turso docs dump](../sources-raw/rung1-libsql-vector.md)) — the day you reach for it, you accept the recall/speed trade above and it becomes a versioned component of your pipeline (rung-6's territory).

### Cross-encoders: the judge your pipeline doesn't have yet

Everything above is **bi-encoder** retrieval: query and document are embedded *independently*, and similarity is computed between the two frozen vectors — SBERT: sentences pass through the model separately, producing "sentence embeddings u and v… compared using cosine similarity" ([SBERT cross-encoder docs](https://sbert.net/examples/applications/cross-encoder/README.html) · [dump](../sources-raw/rung1-sbert-cross-encoders.md)). A **cross-encoder** instead reads *both texts at once*: "we pass both sentences simultaneously to the Transformer network. It produces then an output value between 0 and 1" — and crucially "does not produce a sentence embedding." Joint attention over the pair lets it judge relevance far more accurately than two independently-compressed vectors ever can.

The catch is cost: with nothing cacheable, every (query, candidate) pair is a fresh model forward pass. SBERT's scale example: scoring all pairs among 10k sentences ≈ "50 Million sentence combinations… about 65 hours" for a cross-encoder versus ~5 seconds to embed the same set with a bi-encoder (same dump). Hence the universal pattern, verbatim from SBERT: "First, you use an efficient Bi-Encoder to retrieve e.g. the top-100 most similar sentences for a query. Then, you use a Cross-Encoder to re-rank these 100 hits." Cheap-recall-then-expensive-precision. Your lab stops after stage one — RRF's output goes straight to the screen. What a reranker would judge that your current scoring can't (Q17's seed): BM25 sees token overlap, cosine sees direction between two *independently* summarized vectors, but only a cross-encoder reads the query *against* the document's actual text. Whether that's worth the latency on your corpus is rung-3's measured experiment — this rung only needs you to command the concept. *(Forward pointers, parked to rung-3: Clavié's "MVP++" pattern, `rerankers` library, measured rerank lift.)*

### Chunking: what "one note = one vector" preserves and destroys

Chunking is deciding **what unit of text gets its own vector**. Your lab's answer today: the whole note — title, summary, metadata, and body joined into one string ([src/parse.ts:48-50](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/parse.ts)) — with a hard cap: anything past **8,000 characters is silently cut from the embedding** (with a warning at index time), because "gemini-embedding-001 takes up to ~2048 tokens" ([src/parse.ts:47-58](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/parse.ts)).

Why unit size matters ([Pinecone, *Chunking Strategies*](https://www.pinecone.io/learn/chunking-strategies/) · [dump](../sources-raw/rung1-chunking-strategies.md), excerpt+reconstruction): a single vector must represent *everything* in its text — a long, multi-topic document averages into a vector that matches *no* specific query sharply *(that dilution mechanism is the dump's labelled teaching gloss, not Pinecone's own wording)* — and over-limit text is simply "truncated, or thrown away." Small chunks (~128–256 tokens) give sharp, granular matches but lose surrounding context; large chunks (~512–1024) keep context but risk dilution; overlap preserves ideas cut at boundaries at the cost of duplicate tokens. The page's serviceable heuristic: "if the chunk of text makes sense without the surrounding context to a human, it will make sense to the language model as well," and its honest bottom line — "there's no one-size-fits-all solution."

Two lab-specific consequences you'll demonstrate in the build:

1. **The truncation asymmetry** *(app fact, verified in code)*: FTS5 indexes the **full** body (`upsertNote` writes `n.body` into `notes_fts` — [src/db.ts:110-114](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/db.ts)), but the embedding sees only the first 8,000 chars of the joined text. Content in a long note's tail is findable by keyword search and **invisible to semantic search**. That's a stage-attribution trap: a "semantic search missed it" symptom whose root cause is corpus processing, not retrieval — exactly the distinction Q10 will formalize.
2. **Your `embedText` is a proto-enrichment** *(local observation)*: prepending title/summary/tags to the body before embedding is a home-grown version of the context-prepending idea that rung-3's Contextual Retrieval source systematizes. You already do a naive form of it — worth knowing when you read the fancy version.

### Where each concept lives in your lab (orientation table)

| Concept | Your code | The gap it exposes |
|---|---|---|
| Embedding call, task types, 768 dims | `src/embed.ts` · `src/config.ts` | truncated-dim normalization skipped (harmless under cosine) |
| Vector storage + brute-force cosine | `src/db.ts` `F32_BLOB(768)`, `vectorSearch` | no ANN (correct at this scale) |
| FTS5/BM25 keyword engine | `src/db.ts` `notes_fts`, `keywordSearch`, `toMatch` | OR-semantics; k1/b fixed |
| RRF hybrid fusion | `src/rrf.ts` (k=60) + `search_cmd.ts` pool widening | rank-only; no reranker after fusion |
| Chunking decision + 8K cap | `src/parse.ts` (`embedText`) | whole-note vectors; tail invisible to semantic; no provenance |
| Index lifecycle (preview of rung-6) | `src/index_cmd.ts` content-hash sync, `DB_MARKER` rebuild | versioning is marker-only ("L0-ish" — Safjan's L0–L4 levels are rung-6's material) |

### Learning coverage

`cov-retrieval-foundations` — evidence the learner must produce (all eight rows, no skips):

| Sub-skill | Evidence |
|---|---|
| Embeddings & cosine | Explain fixed-length semantic coordinates + why cosine ignores magnitude; state what a `score=0.41` semantic hit means in the lab |
| Normalization subtlety | Explain why the lab's unnormalized 768-dim vectors are safe under cosine and when they wouldn't be |
| Task-type asymmetry | Explain why docs and queries embed differently; point to both call sites |
| BM25 | Explain IDF/k1/b in own words; read a negative FTS5 score correctly |
| Hybrid + RRF | Hand-compute an RRF fusion and predict the hybrid order before running it |
| ANN | State the recall/speed/memory trade and why the lab correctly skips it; name the libSQL upgrade path |
| Cross-encoders | Explain bi-vs-cross architecturally and the retrieve-then-rerank pattern; state what stage the lab lacks |
| Chunking | Explain dilution + size/overlap trades; demonstrate the lab's 8K truncation asymmetry live |

---

## Reading

### Core

- **Simon Willison — [Embeddings: What They Are and Why They Matter](https://simonwillison.net/2023/Oct/23/embeddings/)** (Oct 2023) · ⏱ **24 min** · **Why:** the best zero-baseline entry to embeddings, written engineer-to-engineer; the primer's embedding sections are assembled from it. **Extract:** the fixed-length/semantic-space mental model; cosine as direction; vibes-based search; the related-content and RAG applications. *(Raw: [dump](../sources-raw/rung1-willison-embeddings.md), faithful reconstruction + quotes.)*
- **DLAI RAG (Zain Hasan) — foundations lesson subset** (~**85 min** video, Modules 1–3 named lessons: Intro-to-IR → TF-IDF → BM25 → semantic search → embedding deep-dive → hybrid → evaluating retrieval → ANN → vector DBs → chunking ×2 → cross-encoders/ColBERT → reranking) · **Why:** the only professionally sequenced from-zero video treatment of the rung's foundation topics; reinforces this primer through a second channel. **Extract:** visual intuition, esp. for ANN and cross-encoders. **Access (verified 2026-07-20, [dump](../sources-raw/rung1-dlai-access-check.md)):** Module 1 free with signup (preview by "accessing the entire first module at no cost"); M2–M3 free-audit unconfirmed on public pages — check the Coursera enroll modal for the audit link; fallback = $25 Pro month or skip (this primer + optional reads carry the content). *Gated: listed from the public outline only.*
- **Weaviate — [Hybrid Search Explained](https://weaviate.io/blog/hybrid-search-explained)** (Jan 2025) · ⏱ **7 min** · **Why:** the RRF walkthrough with actual arithmetic — the fastest route to owning the fusion step. **Extract:** the B>A>C worked example; rank-based vs score-based fusion; alpha. *(Raw: [dump](../sources-raw/rung1-weaviate-hybrid-search.md).)*

**Core subtotal: ~31 min reading + ~85 min video** (video conditional on the access check).

### Optional / go deeper

- **Elastic — [Practical BM25 Part 2](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)** · ⏱ **11 min** · marginal benefit: the worked IDF/k1/b numbers the primer quotes, in full context — read if BM25's ingredients don't feel owned. *(Primer-basis source.)*
- **Pinecone — [HNSW](https://www.pinecone.io/learn/series/faiss/hnsw/)** · ⏱ **15 min** · marginal benefit: the actual layered-graph mechanics + recall/latency/memory curves behind the primer's ANN section. *(Primer-basis.)*
- **Pinecone — [Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/)** · ⏱ **12 min** · marginal benefit: the named strategy families (fixed/recursive/semantic/contextual) before rung-3 evaluates them empirically. *(Primer-basis; bridge to rung-3.)*
- **SBERT — [Cross-Encoders](https://sbert.net/examples/applications/cross-encoder/README.html)** · ⏱ **2 min** · marginal benefit: the canonical two-paragraph statement of bi-vs-cross from Reimers' own docs. *(Primer-basis.)*
- **Google — [Gemini Embeddings API](https://ai.google.dev/gemini-api/docs/embeddings)** · ⏱ ~7 min (est. — measurer blocked by JS rendering; based on captured excerpt) · marginal benefit: the primary source for MRL truncation, the MTEB-by-dimension table, task types, and the normalization warning — the primer's claims about *your own embedding model*. *(Primer-basis; [dump](../sources-raw/rung1-gemini-embeddings-docs.md).)*
- **LLM Zoomcamp — [Module 2: Vector Search](https://github.com/DataTalksClub/llm-zoomcamp)** · hands-on notebooks (NumPy-from-scratch → minsearch → SQLite → pgvector, [dump](../sources-raw/rung1-zoomcamp-m2.md)) · marginal benefit: build-it-yourself reinforcement if concepts stay abstract after the build exercise; same FAQ corpus reimplemented across four backends.
- **Vicki Boykis — [What Are Embeddings?](https://vickiboykis.com/what_are_embeddings/)** · long-form PDF · marginal benefit: the rigorous depth reference behind Willison's intro, for after the block.

**Full-list subtotal: ~78 min reading + ~85 min video + notebooks/reference.**

---

## Build

*(Pure-study rung with a hands-on trace: the application here is reading and predicting your own system, not writing product code. Code policy per case — the one script below is yours to write.)*

### Current app context

Lab at `~/Ork/tools/local-bookmarks`, `master@e8e308d0`, clean. Corpus ≈ 450 notes in `BOOKMARKS_DIR`. Commands: `bm search "<query>"` (hybrid default) with `--mode keyword|semantic|hybrid`, `--limit N`, `--json` ([src/search_cmd.ts](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/search_cmd.ts)); `bm sync-all` re-indexes incrementally. DB: `bookmarks.db` (libSQL) next to the tool. Requires `GOOGLE_API_KEY`/`GEMINI_API_KEY` for semantic/hybrid modes.

### Exercise A — predict the engines' disagreement

Pick **two real queries** against your own corpus: one *identifier-shaped* (an exact tool/person name you know appears verbatim) and one *concept-shaped* (a paraphrase you'd never have typed into the note). **Before running anything**, write down: which mode wins each query and why, in the primer's vocabulary. Then run all three modes per query (`--limit 5`) and annotate: where did keyword/semantic/hybrid agree, where did they diverge, and does your explanation survive contact with the output? Read the scores as what they are (negative BM25; cosine distance; RRF sums).

### Exercise B — hand-compute one RRF fusion

For the concept-shaped query: run `--mode keyword --json --limit 20` and `--mode semantic --json --limit 20`. On paper (or in a scratch file), take the top ~6 of each list, apply your lab's actual formula — `1/(60 + rank)` with rank starting at 1 — sum per doc across lists, and **predict the hybrid top-5 in order**. Then run `--mode hybrid --limit 5` and compare. Watch-out you should hit: the hybrid command fuses *pool-sized* lists (`max(limit*3, 20)`), so a doc outside your top-6 slice can sneak in — explain any mismatch through that lens.

### Exercise C — cosine with your own hands

Write a **small throwaway script** (yours — any style) that: pulls two note embeddings straight from `bookmarks.db` (`SELECT path, embedding FROM notes` — the column is a float32 blob), computes cosine similarity from raw floats (dot product over magnitudes), and cross-checks that `1 − similarity` matches `vector_distance_cos` for the same pair (compare against a `--mode semantic --json` score for a query, or query the function directly in SQL). Then scale one vector by 10× in memory and recompute: the cosine must not move. That's the normalization subtlety made empirical.

### Exercise D — demonstrate the truncation asymmetry

**Setup first — no existing note qualifies** *(app fact, verified 2026-07-20: the longest joined `embedText` in the corpus is 7,554 chars — "Claude Code Auto Mode - permission-free operation.md" — so 0 of ~450 notes exceed the 8,000-char cap and the oversize warning ([src/parse.ts:53-57](file:///Users/abtinghods/Ork/tools/local-bookmarks/src/parse.ts)) never fires today)*. Create one that does: write a new bookmark note whose joined text exceeds 8,000 chars (e.g. paste a long article as its body — the content is yours to write), making sure a distinctive phrase that appears nowhere else in the corpus sits in its **tail**, past the 8,000-char mark. Run `bm sync-all` and confirm the oversize warning fires for your note. Then, predicting before running: search that tail phrase in `--mode keyword` (should hit — FTS indexes the full body) and `--mode semantic` (should miss or rank low — the tail never reached the embedding). Record the pair of outputs as your evidence. State, in one sentence, which *pipeline stage* caused the semantic miss.

### Artifact to produce

A short trace log (markdown, anywhere you like — it feeds the rung checkpoint): per exercise, your **written prediction**, the observed output (paste the relevant lines), and a one-paragraph explanation in primer vocabulary. Plus the throwaway cosine script.

### Success criterion

Predictions made *before* runs; mismatches explained rather than ignored; the RRF hand-computation reproduces the hybrid order (or the pool-width explanation covers the gap); the cosine cross-check matches to float precision and survives the 10× scaling; the truncation asymmetry demonstrated with the oversized note you created (warning observed at sync; keyword finds the tail phrase; semantic misses it).

### Hints / rubric

- Stuck picking queries? Your corpus is heavy on AI-tool bookmarks — an author name or CLI name is identifier-shaped; "that technique where you retrieve before generating" is concept-shaped.
- RRF math sanity check: a doc at rank 1 in one list only = 1/61 ≈ 0.0164; a doc at rank 4 in *both* lists = 2/64 ≈ 0.0313 — the double-appearance doc wins. If your prediction disagrees with the tool, recount ranks (the code is zero-indexed, `i + 1` restores 1-based).
- Blob decoding friction in Exercise C is mechanics, not learning — if stuck >10 min, ask the companion to unblock the decode, then do the math yourself.

---

## Verify

From the brief (gate, not weakened):

- **Explain-back interview** across all eight coverage rows — the companion probes with the Learning coverage table above until gaps close; fluency raises challenge, never skips.
- **Applied trace exercise passes** — the artifact exists, predictions precede runs, all four exercises done to the success criterion.
- **No written-answer set for this rung** (no owned Q-numbers; foundations vocabulary is checkpointed via explain-back).

Additional evidence-grounded checks:

- He can point at `src/{embed,db,rrf,parse,search_cmd}.ts` and say what each contributes to a single `bm search` invocation without opening the primer.
- He reads one real hybrid output line (`score=…`) and correctly identifies what the number is and is not.
- Coverage ledger: `cov-retrieval-foundations` flips to `demonstrated` only on the companion's checkpoint, recorded in `progress.md` §Learnt.
