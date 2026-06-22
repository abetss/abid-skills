# Tradeoff Format

This is the heart of the skill. Get this wrong and the whole `tradeoffs.md` is just a difference table that doesn't help anyone decide.

## The three-way distinction

When you describe two options, the result is one of three things:

| What it is | What it looks like | When it's right |
|---|---|---|
| **Tradeoff** | "To get X you give up Y. Both options have real gains and real losses on each axis." | When the choice is non-obvious. Two responsible engineers could pick different sides. |
| **Difference** | "These two differ on Z." | When you're describing the *shape* of options, not the *choice* between them. |
| **Absolute-better** | "X is just better than Y." | When the rejected option dominates the chosen one. Rare. If you find yourself here, you probably haven't characterized the rejected option fairly. |

A `tradeoffs.md` section that reads as **difference** or **absolute-better** is failing. The reader can't *decide* from a difference table — they can only *describe*. They can't *learn* from an absolute-better claim — they can only *agree*.

**The diagnostic question** — if both options appear to gain on every dimension you mention, you've hidden the tradeoff. Push on the one option until you find what it costs.

## Tradeoff vs difference — three concrete pairs

**Bad (difference):**
> "Polling is simple. SSE is real-time."

You can't decide from this. Both sound like wins for their option.

**Good (tradeoff):**
> "**Real-timeness ↔ deploy-blast-radius.** Polling: **+** the next 15-second tick lands on the new replica after a deploy, users don't notice. **−** up to 15s lag on every badge update. SSE: **+** sub-second push. **−** every deploy reconnects every user simultaneously — a thundering-herd storm distributed only by the client's randomized backoff."

Now the choice is visible. To get real-time you accept deploy fragility. To get deploy invisibility you accept lag.

---

**Bad (difference):**
> "Event bus decouples producers and consumers. Direct calls couple them."

Decoupling-as-virtue isn't a tradeoff — it's just one side of one.

**Good (tradeoff):**
> "**Traceability ↔ pluggability.** Direct call: **+** one grep + one worker; 'I didn't get notified' is a 1-step trace. **−** adding a 2nd consumer requires producer-side change. Bus: **+** consumers plug in via subscription, zero producer change. **−** debugging requires multi-hop trace — was the event published, which subs matched, did the handler map it."

Two real things gained, two real things lost. Reader can weigh based on their context.

---

**Bad (absolute-better):**
> "We use Postgres because it's the right database for our workload."

If true, there's no story. Probably a hidden tradeoff.

**Good (tradeoff):**
> "**Consistency model ↔ horizontal write scalability.** Postgres: **+** strong consistency, transactions, mature ecosystem. **−** harder to scale writes past one master without sharding. Cassandra: **+** linear write scaling. **−** eventual consistency forces application-layer reconciliation logic for read-after-write."

## How to build a tradeoff table

```
| Axis | Option A (chosen) | Option B |
|---|---|---|
| **Some name ↔ other name** | **+** gain on this axis. **−** loss on this axis. | **+** what B gains. **−** what B loses. |
```

Three rules.

### 1. Each row is an AXIS

An axis is a dimension where the two options pull in opposite directions. Not "what each option has" — that's a feature list.

Concrete axis names beat abstract ones:
- *bad*: "Architecture"
- *good*: "Traceability ↔ pluggability"
- *bad*: "Performance"
- *good*: "Read-path latency ↔ write-path simplicity"

The `↔` arrow signals that this row is a tradeoff. If you can't name an arrow between two competing properties, you don't have an axis.

### 2. Every cell starts with **+** AND **−**

```
**+** what this option GAINS on this axis. **−** what this option LOSES on this axis.
```

If a cell has only **+** or only **−**, you're back to listing features or weaknesses, not showing a tradeoff. Force yourself to find the cost of every gain and the upside of every cost.

If you genuinely can't find a **−** for an option on some axis, that axis is not a tradeoff — it's shared ground. Move it to the next section.

### 3. Shared ground is NOT a tradeoff — call it out separately

Add a "**What they share (not tradeoffs)**" subsection right after the table:

> "Both deliver at-least-once with retries. Neither guarantees exactly-once on its own — both need to be combined with idempotency or a transactional outbox to approach it. Both can be made async and decoupled from the request path; that's not what distinguishes them."

This protects against the common interview trap where a candidate claims an advantage that isn't actually distinguishing.

## The full decision-doc structure

Each major decision in `tradeoffs.md` follows this skeleton. Sections in *italics* are optional — include them when they earn their keep.

```
## N. <Chosen option> vs <Alternative(s)>

*<Naming-trap callout>* — if there's a common naming overlap or framing trap (e.g. "we call it `.emit()` but it isn't EDA"), name it FIRST. Disarms the line of questioning.

### Context

The requirements that forced the choice. 3-6 enumerated bullets, concrete to the system.

### What the patterns actually are

Definition + code example + 3-line characterization for each option. For each:
- How the call site looks
- Who knows what (dependency direction)
- What the payload represents (command vs event vs other)

The reader should be able to recognize each pattern in any codebase after reading this.

### Side-by-side tradeoffs

The table. 8-14 rows. Each row an axis. Each cell **+** AND **−**.

**What they share (not tradeoffs):** 1-3 lines. Things both options give you. Explicitly NOT in the tradeoff table because they don't distinguish.

### Why <chosen> won — N reasons in priority order

Numbered list, 1-4 reasons. Each is a paragraph (2-5 sentences) that names ONE force and explains WHY that force tipped this decision in this codebase. Order by priority — what would still be true if the others changed.

### What would change our mind

When does the rejected option become the right one? 3-5 conditions. Concrete — "when a second consumer needs the same business signals," not "when we have more complexity."

*This is the staff-level signal.* It shows you understand the rejected option's value proposition, not just its costs.

*### The defense (scripts)*

For interview-facing docs. 2-3 likely pushbacks and the 1-paragraph rebuttal for each. Verbatim wording the reader can practice.

### What we accept

3-5 explicit costs. The bill. The reader leaves knowing what hurts about the choice and why we're paying it.

*### Adjacent alternatives we also considered*

For options that aren't on the main tradeoff axis (e.g. transactional outbox is about delivery guarantees, not command-vs-event — different concern). Lighter treatment: 1 paragraph definition + bullet list of why-rejected + migration-path note.

### One-line summary

Capable of standing alone as the elevator answer. Names the choice, names the dominant force, names the migration path.
```

## A worked snippet (taken from the canonical example)

The full example is at `a-docs/architecture/notification/tradeoffs.md` §1 in the source codebase where this skill was developed. If your project has it, read that. The structure below shows the skeleton with one row of the table filled in.

```markdown
## 1. Async command (task queue) vs Event-Driven Architecture

**This is the question to be ready for.** It cleanly separates "I read about microservices" answers from "I've actually shipped this" answers.

The pattern we use is often *miscalled* "event-driven" because the call site reads
`notification_service.emit(...)`. It is not EDA. It is an **asynchronous command pattern**
(also called a "task queue" or "queue-based RPC"). The naming overlap is the trap, and
a sharp interviewer will probe it — so be the one to name the trap first.

### Context

A timesheet line is edited. Two people should be notified. The edit happens in a route
handler that just committed a transaction. We now need:

1. To notify the right people.
2. Without slowing the user's response.
3. Without coupling timesheet to email.
4. Without coupling notification to timesheet's domain.
5. With the business operation succeeding even if notifications are down.

### What the patterns actually are

#### Async command (task queue) — what we have
```ts
notification_service.emit({ action, stakeholder_user_ids, body_context, ... })
```
- Producer calls a named function. Function is the destination.
- One consumer drains the queue.
- Payload is a command: "notify these recipients about this thing."
- Dependency points feature → notification system.

#### Event-Driven Architecture — what we did not build
```ts
event_bus.publish('timesheet.line.edited', { line_id, old, new })
// elsewhere, INDEPENDENTLY, subscribers map the event
```
- Producer publishes a domain fact.
- N consumers subscribe. Producer ignorant of them.
- Dependency points consumers → bus → event schema.

### Side-by-side tradeoffs

| Axis | Async command (chosen) | EDA |
|---|---|---|
| **Traceability ↔ pluggability** | **+** one grep + one worker; "I didn't get notified" is a 1-step trace. **−** adding a 2nd consumer requires producer-side change. | **+** consumers plug in via subscription, zero producer change. **−** debugging requires multi-hop trace — was the event published, which subs matched, did the handler map it. |
| ... 12 more rows ...                       | ...                               | ... |

**What they share (not tradeoffs):** Both deliver at-least-once with retries. Neither
guarantees exactly-once alone. Both decouple from the request path. That's not what
distinguishes them.

### Why async command won — four reasons in priority order

**1. One consumer.** EDA's value is decoupling producer from MANY consumers. We have many
producers (timesheet, scheduling, ...) but one consumer (the notification system). No
analytics, no search indexer, no second service. ...

**2. Debuggability.** When a manager says "I didn't get notified," ...

**3. The payload is genuinely command-shaped.** What we emit carries
`stakeholder_user_ids`, `body_context`, `actor_user_id` — notification-system concepts. ...

**4. EDA's migration cost in is small; out is large.** ...

### What would change our mind

EDA stops being over-engineering and starts being load-bearing when:

- A second consumer needs the same business signals (analytics + search + audit).
- Multi-team independence matters (notification team ≠ timesheet team).
- Replay becomes a product feature.
- Producer and consumer live in different services.

### The defense (scripts)

Lead with this — say it before they ask, disarms the line of questioning:

> "We use 'emit' for the call, but this isn't EDA. It's async command via a task queue. ..."

If they push: *"But it's async and decoupled — isn't that event-driven?"*

> "Async and decoupled are properties of many patterns. EDA is a specific commitment: events
> as domain facts, multiple subscribers, producer-ignorance. We have async-and-decoupled
> without producer-ignorance ..."

### What we accept

- A second consumer of the same signal requires a refactor.
- The producer carries some notification-shaped knowledge in the payload.
- No event log to replay against — per-module workflow tables serve that role.

### Adjacent alternatives we also considered

#### Transactional outbox

Orthogonal to "task queue vs EDA" — about *delivery guarantees*, not command-vs-event. ...
Rejected because the infra cost is the whole reason it exists, and our requirement is
best-effort. Migration path open.

#### Database triggers

Rejected because triggers fire on every CRUD ...

### One-line summary

We chose async command over EDA because we have one consumer, debuggability matters more
than decoupling at our team size, the payload is genuinely command-shaped, and the
migration path to EDA is open if and when our world changes. The naming (`emit`) is the
only event-driven thing about it.
```

## Anti-patterns to detect in your own draft

Before you ship `tradeoffs.md`, audit every section for these:

### 1. The "all wins" table

Every cell in your row is **+ +**. You named a difference, not a tradeoff. Push harder on each option until you find what it costs.

### 2. The "all losses" table

Every cell is **− −**. You're listing problems, not tradeoffs. Find what each option *does win* on this axis.

### 3. Vague axes

"Architecture" or "Performance" or "Quality" as row labels. Replace with concrete axes that name the X/Y tension: "Read-path latency ↔ write-path simplicity," "Operational surface ↔ per-consumer isolation."

### 4. Missing "what they share"

If both options give you the same property on some dimension, that property is NOT in your tradeoff table — it's a shared property and belongs in its own subsection. Failing to call this out hides where the choice actually is.

### 5. Missing "what would change our mind"

Without this, the doc sounds like "X is just better." Add the conditions under which Y becomes right. This is the staff-level signal.

### 6. Bullet lists masquerading as tradeoffs

```
- Pro: fast
- Pro: simple
- Con: doesn't scale
```

Pro/con lists collapse the axes. Two pros and one con doesn't say *which axis the con sits on* or *what the pros cost*. Always reach for the table.

### 7. The "we picked the best option" framing

If the rejected option sounds like an obvious mistake, you haven't characterized it fairly. Real engineers picked it for real reasons elsewhere. Steelman before you reject.

## How to test if you got it right

After writing a decision section, ask yourself:

1. **Can a reader who disagrees with the choice still get value from the doc?** A tradeoff doc serves the reader who might pick the other option in their context. A difference doc serves only the writer's worldview.

2. **Does every row of the table have a + AND a − for both options?** If not, what's missing?

3. **Could a senior engineer in a different context (different team size, different scale, different team-shape) read this and conclude "for us, the other option"?** If yes, you've captured a real tradeoff. If they can only nod, you've described a difference.

4. **Have I named what the chosen option costs?** "What we accept" should make the reader wince a little. If it doesn't, you're underselling the cost.

5. **Can I name the conditions under which I'd switch?** "What would change our mind" tests whether you understand the rejected option's value, not just its weakness.

If you can answer yes to all five, ship it.
