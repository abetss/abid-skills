# Research Agent Prompts

The skill spawns 3-5 research agents in parallel before writing any docs. This file is the template library — when you launch them, fill in the system-specific blanks and send all the agents in one message so they run concurrently.

## The pattern

Each agent has:
- A specific scope (one surface, one infra, one corpus)
- A structured prompt that names the focus areas in priority order
- An expected output format (so synthesis is mechanical)

You synthesize their reports into `raw-context.md` — the source of truth that backs every other doc. The other docs are written FROM the raw context, not from re-running research.

## Standard agent set

For a typical full-stack system, spawn 4 agents in parallel:

1. **Code A — primary surface** (often the backend service that owns the data)
2. **Code B — secondary surface** (often the frontend or a sibling service)
3. **Infra inventory** (cloud CLI sweep — what's deployed, what isn't)
4. **Docs digest** (existing design docs, work folders, knowledge base)

For a backend-only system, drop Code B. For a system with no cloud surface, drop Infra. For a system with no prior docs, drop Docs but say so explicitly in the brief.

## Agent 1 — Code A (primary surface)

**Subagent type:** `code-explorer` (use the project's deep-analysis agent if available; otherwise `general-purpose`).

```
Deep-dive {system_name} in `{primary_code_path}`. This is for architecture documentation —
I need to understand the WHY of design decisions, not just WHAT exists.

Focus areas, in priority order:

1. **Entry point / contract**: how does the system get invoked? Read the top-level
   service file. What's the function signature, what's the payload shape, what's the
   error contract (throw vs swallow), what's the threading/async model?

2. **Core engine**: read the main processor / handler / orchestrator file fully. Map
   the exact flow from input → output. Note any anti-N+1 batch fetches, error isolation
   boundaries, retry semantics.

3. **Pluggability / extensibility**: how is the system extended? Is there a registry,
   a discriminated union, a plugin interface? Find 2-3 example "plug-ins" and read them
   to understand what a contributor would change to add a new instance. Quantify: "adding
   a new X = N file touches."

4. **Schema / data model**: find the Prisma/Drizzle/Sequelize/SQL schema. Capture all
   fields, relations, enums, indexes (especially partial indexes). Note where types come
   from (DB enum vs application enum vs free-form string) and why that's load-bearing.

5. **Queue / async infrastructure**: what library, what backend store, what concurrency,
   what retry policy, what DLQ strategy?

6. **Cross-cutting**: search for these terms and report what you find:
   - `outbox`, `transactional outbox` — delivery guarantee pattern
   - `idempotency`, `dedup`, `dedupe` — duplicate-handling
   - `event_bus`, `pubsub`, `subscribe` — pub/sub presence
   - `feature_flag`, `growthbook`, `ld_client` — feature gating
   - `audit`, `audit_log` — audit pipeline

7. **Tests**: read the integration tests. Tests double as documentation — they reveal
   intent and edge cases the code doesn't.

8. **Anything that looks impressive or particularly challenging** from a staff-engineer
   perspective. Toggle reversals, sophisticated dedup, custom DI hacks, etc.

For each area, capture:
- Concrete file paths and line numbers
- Key code excerpts (function signatures, schema fields, enum values, queue names)
- The DESIGN INTENT (why is it shaped this way — read tests + comments + git log if helpful)
- Tradeoffs visible in the code (the "we chose X over Y because…" comments and structural choices)

Return a structured report organized by the 8 focus areas. Be thorough — this becomes
the "raw context" for architecture documentation. Aim for ~2000-3000 words of dense
findings. Code excerpts welcome. Include exact file paths and line numbers everywhere.
```

## Agent 2 — Code B (secondary surface)

**Subagent type:** `code-explorer` or `general-purpose`.

```
Explore {system_name}'s surface in `{secondary_code_path}` ({frontend|sibling-service}).
This is for architecture documentation — focus on architecture-level concerns, not
pixel-level details.

Find and report on:

1. **Where the surface lives**: directory structure, key components.

2. **Data fetching strategy**: how does the surface get data from the primary surface?
   REST? GraphQL? RPC? React Query? tRPC? Plain fetch? Server actions? What's the
   freshness strategy — polling, push, manual refetch?

3. **Real-time updates** (if applicable): WebSocket? SSE? Polling cadence? Tab-visibility
   awareness? Reconnect logic? If polling, what cadence and what informed that choice?

4. **State management**: where does data live in the client — useState, Zustand, Redux,
   React Query cache, context? Global or per-component?

5. **Write actions / mutations**: optimistic? Debounced? Rolled-back-on-error?
   Bulk vs per-item?

6. **Cross-surface coordination** (auth, deep links, push notifications, etc.): how do
   external entry points (email links, push) bring users back into the surface?

7. **Anything architectural worth noting**: service worker presence, scaffolding for
   future capability, accessibility-driven decisions that shaped the API contract, etc.

For each finding: file path + line number + 1-2 line excerpt where the architectural
decision is visible. ~1500 words.
```

## Agent 3 — Infra inventory

**Subagent type:** `general-purpose`.

For Azure systems (uses `az` CLI):

```
Inventory cloud resources used by {system_name}. The user is logged into Azure as
`{user_email}` on subscription `{subscription_name}`.

Run these `az` commands:

1. List resource groups: `az group list -o table`
2. For each production-looking group: `az resource list -g <group> -o table`
3. Specifically look for resources related to {system_name}:
   - Service Bus namespaces: `az servicebus namespace list -o table`
   - Storage accounts (queues): `az storage account list -o table`
   - Redis Cache: `az redis list -o table`
   - Communication Services (email/SMS): `az communication list -o table`
   - Notification Hubs: `az notification-hub namespace list -o table`
   - Function Apps: `az functionapp list -o table`
   - Container Apps: `az containerapp list -o table`
   - App Services: `az webapp list -o table`
   - Event Grid: `az eventgrid topic list -o table` and `az eventgrid system-topic list -o table`
4. For any Service Bus found, list queues/topics: `az servicebus queue list ...`
5. For Redis: SKU, persistence, network access (private endpoint?)
6. App Insights / Log Analytics: observability presence

For each resource: type, name, region, SKU/tier, role in the system (annotated with how
naming + tags suggest it ties to {system_name}). For resources NOT found (Service Bus,
Event Grid, etc. — anything that COULD have been used but wasn't), include them in a
"**What's NOT here**" section. The absence is as informative as the presence.

Read-only operations only. ~1000 words.
```

For AWS systems (uses `aws` CLI):

```
Inventory AWS resources for {system_name} using `aws` CLI. Profile: `{profile_name}`.
Region: `{region}`.

Check for:
- SQS queues: `aws sqs list-queues`
- SNS topics: `aws sns list-topics`
- EventBridge buses + rules: `aws events list-event-buses`, `aws events list-rules`
- Lambda functions: `aws lambda list-functions`
- ECS / Fargate / EC2 / EKS: per service
- ElastiCache (Redis): `aws elasticache describe-cache-clusters`
- RDS / Aurora: `aws rds describe-db-instances`
- SES (email): `aws ses list-identities`
- DynamoDB: `aws dynamodb list-tables`
- S3 buckets used by the system
- CloudWatch / X-Ray observability

Same output format as the Azure agent: per-resource (type, name, region, SKU, role) +
"What's NOT here" section. Read-only. ~1000 words.
```

For GCP, swap to `gcloud`. Pattern is the same.

## Agent 4 — Docs digest

**Subagent type:** `general-purpose`.

```
Read every file in these locations and produce a structured digest:

1. `{primary_work_folder_path}` (the team's in-progress work folder for this system)
2. `{secondary_work_folder_path}` (follow-up tickets, if any)
3. Any matching files in `{knowledge_base_path}` (search by grep for keyword `{system_name}`)
4. Any matching files in `{docs_path}` (search by grep)

For each file, capture:
- Purpose (plan? requirements? design doc? QA cases? task list? code review?)
- Key architectural decisions documented inside (rationale for X over Y, schema choices,
  pluggability approach, explicit tradeoffs)
- Anything that reads like "we considered X but chose Y because Z"
- Open questions or known limitations the author flagged
- Verbatim paragraph-length quotes where the design intent is captured — direct quotes
  from the design doc are gold for architecture documentation

This is for architecture documentation. The goal is to surface what the engineer was
thinking when they designed the system, not just what they built. Include direct quotes.

Output: structured digest organized by document, with cross-cutting themes summarized at
the end. ~2000 words.
```

## Calling them in parallel

When you launch, put all 4 (or 3) Agent calls in a single message so they run
concurrently. Example outline:

```
<Agent call 1: code A>
<Agent call 2: code B>
<Agent call 3: infra inventory>
<Agent call 4: docs digest>
```

Each returns a structured report. Synthesize them into `raw-context.md`. Don't lose
information — `raw-context.md` is the only place the raw findings live before they get
distilled into the other docs.

## Tuning the prompts

Adjust the focus-area lists per system:

- For a **data pipeline**, emphasize ingestion sources, transformation contracts, sink
  guarantees, replay/backfill — drop pluggability if it doesn't apply.
- For a **frontend feature**, swap Agent 1's "core engine" focus for "key components +
  state flow," and drop the schema focus.
- For a **library**, drop infra entirely and emphasize public API surface, versioning,
  consumer impact.

The pattern stays the same: 3-5 parallel agents, structured prompts, structured
outputs, synthesized into `raw-context.md`.
