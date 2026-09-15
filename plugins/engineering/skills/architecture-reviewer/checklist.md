---
lens: architecture
purpose: Full taxonomy of architectural concerns. Use as a lens, not a to-do list. The reviewer reads this, then decides which categories apply to the current review based on the diff, feature intent, and exploration evidence.
---

# Architecture reviewer checklist

This is the superset of architectural concerns for a typical full-stack application (frontend + backend/API). The reviewing agent reads through it and applies judgment:

- Skip categories the diff doesn't touch
- Go deep on categories the diff is centered on
- Look opportunistically at categories the diff is *adjacent* to — that's where "exposed" findings come from
- Flag gaps where a category *should* exist in the system but doesn't

Stack markers: `[H]` frontend, `[P]` backend/API, `[Both]`. (Adapt to your repo's app boundaries.)

## Contents

1. API & interface design
2. Module boundaries & coupling
3. Data model & schema architecture
4. State management & UI architecture
5. Async / eventing / jobs
6. Error handling & observability
7. Configuration & environment
8. Extensibility vs simplicity (principle lens)
9. Cross-cutting concerns
10. File/folder organization
11. Dependency architecture
12. Documentation as architecture
13. Resilience / operational architecture
14. Naming & domain language
15. Testing architecture

---

## 1. API & interface design [P, cross-app contract]

*"Is this API a contract I'd want to live with for three years?"*

- REST endpoints resource-oriented, not RPC-bolted-onto-HTTP (`POST /users/:id/activate` ok; `POST /activate-user` smells)
- Request/response schemas defined once in a validation library and reused — not duplicated between handler and client
- Error shape consistent across endpoints; error codes are stable contracts, not leaked internals
- HTTP verbs correct — no GETs that mutate, no POSTs that read
- Paging / filtering / sorting — one convention, not three
- Idempotency — write endpoints handle replay (idempotency keys, upserts, deterministic IDs) where it matters
- Auth declared per endpoint in one consistent way — not middleware here, decorator there, inline check elsewhere
- Versioning strategy exists, or a deliberate "single version, never break" stance with guardrails
- **Websocket contracts**: message envelope shape, backward compatibility, handshake auth (browsers can't attach headers — documented pattern?)
- Cross-app contracts (frontend → backend): one source of truth for types, not two hand-maintained shapes

## 2. Module boundaries & coupling [Both]

*"If I need to change feature X, how many unrelated files do I have to touch?"*

- Domain logic (business rules) separated from infrastructure (http, db, auth)
- Route handlers stay thin — business logic lives one layer down
- No circular dependencies between modules
- Imports are leaf-pure — top-level import doesn't trigger side effects (db connect, env read, feature flag fetch)
- Shared types live in a shared package or equivalent — not duplicated across apps
- The frontend doesn't import backend internals — or does it, and is that the smell?
- Growing `switch` / `if-else` chains where a new feature forces a new case in existing code (extension smell)
- God modules with many unrelated exports

## 3. Data model & schema architecture [Both, ORM + access-control policies]

*"Will this schema bend or break under the next two features?"*

- DB ENUMs vs string literal tables — ENUMs require migrations to extend
- Access-control / authorization policies (`@@allow` / `@@deny`-style, or your ORM's equivalent) match the real auth intent — not a subset, not a superset
- Indices match actual query patterns — missing index on a common filter column is architecture, not perf
- Nullability is deliberate, not lazy — `nullable: true` because of a meaningful optional state, not because it was easier
- Soft delete vs hard delete — consistent strategy within a domain
- Tenancy model enforced at the schema layer, not just at the query layer where it's easy to forget
- PII / regulated-data fields typed or tagged distinctly so logging, exports, and audit can treat them specially
- Relations with explicit `onDelete` behavior
- Derived data is computed when cheap, stored when expensive — deliberate choice
- Migration safety — can this change roll back? Does it lock a hot table?
- Denormalization has a recorded reason, not accidental

## 4. State management & UI architecture [H]

*"Where does this piece of state live, and why there?"*

- Server state (React Query / SWR / equivalent) vs client state (local component state / a store) — not mixed in the same concept
- URL is used for shareable / deep-linkable state; not trapped in component memory
- Prop drilling past N levels — context candidate, or misplaced state
- Context used for state that's actually props (over-applied), or things that should be context but are drilled
- Derived state in component state when memoization or derivation would do (stale duplication risk)
- Form state — one library or pattern, not three
- Optimistic update strategy consistent, or deliberately absent

## 5. Async / eventing / jobs [P]

*"When something goes wrong asynchronously, can we recover?"*

- Fire-and-forget vs awaited — deliberate, not accidental
- Queue usage — where jobs go, retry policy, DLQ, visibility
- Cron / scheduled jobs registered in one place, observable
- Inbound webhooks — signature verification + idempotency
- Outbound webhooks — retry + backoff + backpressure
- Real-time (websockets) — reconnection, message ordering guarantees, backpressure when client is slow
- Long-running operations — request/response vs job pattern — consistent rule

## 6. Error handling & observability [Both]

*"Can I debug this at 3am?"*

- Typed errors, not stringly-typed; `Error.cause` preserved through layers
- Logging taxonomy — info / warn / error have consistent meanings; structured fields
- PII / regulated-data sanitization at the log boundary, not sprinkled through call sites
- Traces span module boundaries (handler → service → repo)
- Metrics emitted at the right layer, named consistently
- Health checks define what "healthy" means for the service
- Audit logs (regulatory / compliance disclosures) separate from operational logs — different retention, different consumer

## 7. Configuration & environment [Both]

*"If I move this to a new environment, what breaks silently?"*

- Env var contract — schema parsed/validated at boot, not ad-hoc `process.env.X` throughout code
- `.env.example` stays in sync with the schema
- Public-vs-private env var policy (e.g. framework-prefixed public vars) — what's safe to expose, documented; reviewer flags new ones without a decision
- Secrets — in secret manager or env, not code; rotation documented
- Feature flags — consistent pattern, rollout strategy (per-user / per-org / global), kill switches
- Config vs code — when a constant becomes an env var vs stays inline, deliberate

## 8. Extensibility vs simplicity (the principle lens) [Both]

*"Is this the simplest thing that serves today AND the likely next change?"*

The three principles — simple first, extensible first, optimize for change — live here.

- **Simple first violation**: wrapper layers that add nothing, premature interfaces with one impl, factories with one product, config for values that have one meaning
- **Missing abstraction**: three sibling modules copy-pasted with no extraction
- **Extensible first violation**: new-feature-requires-editing-existing-code patterns (switches, hardcoded maps) where extension is the foreseeable evolution
- **Optimize for change violation**: fast-changing domain shares a module with slow-changing stable core — changes keep rippling through stable code
- **Speculative extensibility**: options / config for a future no one asked for

## 9. Cross-cutting concerns [Both]

*"Does every feature handle these the same way, or does each one reinvent it?"*

- **Request / correlation / trace ID propagation** — threaded through handler → service → repo → logs
- **Auth context / user identity propagation** — one shape carried everywhere, not re-fetched at each layer
- **Tenant isolation** — enforced at schema + query layer, verified consistently
- **Authorization enforcement** — centralized (access-control policies) or scattered; defense in depth where it matters
- **Feature flag gating** — wrapped in one pattern (component / route / db-visibility), not `if (flag)` sprinkled ad hoc
- **Caching** — where policy lives, invalidation strategy, cache keys scoped right
- **Rate limiting / throttling** — where enforced, by what key (user / tenant / IP)
- **Audit trail emission** — regulatory events emitted via one consistent pattern
- **Domain events / internal eventing** — if used at all, one bus; not ad hoc pub-sub
- **Product telemetry / analytics** — consistent event naming, one SDK, PII-aware
- **React error boundaries** [H] — scope of boundaries, fallback UX, reporting
- **Input validation at the HTTP edge** — validation schemas at handler entry, one pattern
- **Output serialization / PII redaction** — consistent shape before leaving the process

(Date / timezone / i18n are covered by conventions, not architecture.)

## 10. File/folder organization [Both]

*"Can a new dev find where X lives in under 30 seconds?"*

- Colocation — tests, stories, styles next to source, or deliberately not
- Domain-oriented vs technical-layer-oriented structure — consistent within an app
- Barrel files (`index.ts`) — helping re-export surface, or hiding coupling?
- Import aliases consistent (`@/...` vs relative)
- Folder depth — inverted pyramid or flat?
- Feature folders vs type folders (all `hooks/` vs `features/X/hooks`) — one model per app

## 11. Dependency architecture [Both]

- Third-party SDKs wrapped behind project-owned interfaces (so swap is possible) vs used raw
- Runtime vs dev dependency placement correct
- Direct deps whose transitive blast radius is large — deliberate?
- Version pinning policy
- Workspace packages vs registry packages — boundary clear?

## 12. Documentation as architecture [Both]

*"Does the doc match the code? Does the code match the doc?"*

- Architecture docs — does reality match? Which doc is stale?
- ADRs (architecture decision records) written for non-obvious decisions (why websockets not SSE, why REST not tRPC, why this vendor not that)
- Onboarding — can the docs alone explain where to put a new feature?
- Contract docs (API shape, event shape, message shape) exist where they'd save a future integrator an hour

## 13. Resilience / operational architecture [P]

- Timeouts declared on external calls (DB, HTTP, third-party services)
- Retries with backoff, capped attempts
- Graceful degradation — what still works if auth is down, if the backend is down, if a third-party service is down
- Transactions where invariants demand them, or compensating actions where they can't
- Backpressure on inbound (rate limit, queue depth, 429s)
- Circuit breakers around flaky upstream services
- Shutdown semantics — in-flight work drained on redeploy?

## 14. Naming & domain language [Both]

*"If I showed this code to a product person, would they recognize the words?"*

- Names match domain vocabulary, not CS abstractions (`CustomerOrder` not `Record`)
- Same concept has the same name across frontend and backend
- Glossary maintained (even informally)
- Acronyms expanded somewhere, not presumed

## 15. Testing architecture [Both]

*"Does the test shape make the code safe to change?"*

- Test pyramid — unit / integration / e2e in reasonable proportion for this module
- Integration tests hit a real DB (mock/prod divergence is a common source of bugs)
- Risky boundaries — auth, money, migrations, schema access policies — covered
- Test data via factories, not sprawling fixtures
- Slow tests not silently accepted as the norm
- Contract tests where two apps share a contract (frontend ↔ backend)
