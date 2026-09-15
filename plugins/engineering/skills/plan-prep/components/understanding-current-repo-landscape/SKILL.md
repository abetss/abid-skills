# Understand the Current Repo Landscape

> Load the relevant codebase context into this conversation so that all subsequent work is informed by actual code.

## Memory

Read `memory.md` in this component directory before starting. It contains learnings about what to trace, hidden connections, and commonly missed files.

## Need

When work modifies or integrates with an existing repository, read the code that must be in context for planning to go well. The value is not a report — it is having the authoritative implementation, tests, conventions, and local documentation in context so Design the Solution and task breakdown are grounded in reality.

This component does not discover native capabilities of an external platform or existing packages/products. Select **Discover Existing Capabilities and Solutions** for that work; both components may run when a repository integrates with a platform.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute and return the architecture points encountered while tracing the existing system; leave their lifecycle to the shared protocol.

## Methods

- **Partition independent starting points** — Separate unrelated repository entry points, subsystems, and local documentation areas into bounded scouting lanes
- **Fan out locator scouts** — Run read-only discovery lanes concurrently. Each scout returns exact paths, relationships, and reasons; scouts do not write shared artifacts or substitute summaries for authoritative code
- **Load authoritative code into the main context** — After scouting, the plan-prep owner validates the candidates and reads the relevant source files directly, batching independent reads concurrently when supported
- **Chase the code from starting points** — Follow references, imports, and calls in additional dependency-ready rounds until the relevant paths are grounded
- Ask the user only if you have a specific question you cannot answer from the available evidence
- **Read existing documentation** — Architecture docs, conventions, and project knowledge-base indexes often reveal required context
- **Surface architecture points** — For every technical decision you encounter while exploring, ask whether more than one credible approach exists and contribute material points through the shared architecture-decision protocol

## How to Chase the Code

Based on the context given to you so far, identify the starting points for what you're building. Group independent starting points into non-overlapping scouting lanes, then trace through the code, following each reference until you've loaded everything relevant.

**These are examples of tracing paths, not an exhaustive list:**

### Example 1: Display Flow (read-path)

```
START: What does the UI need to display?
    │
    ▼
UI Props Object ◀── Find the component, read its props interface
(transformer       What data does it expect?
 return type)
    │
    ▼
Transformer ◀── Find the transformer that produces those props
Input & Logic    What input does it need? What logic does it apply?
    │
    ▼
API Route ◀── Find the endpoint the transformer calls
Handler         What does the handler do? What does it return?
    │
    ▼
Database ◀── Find the models/tables the handler queries
Schema         What fields exist? What relationships?
```

### Example 2: Form Submission Flow (write-path)

```
START: User submits a form
    │
    ▼
Form Component ◀── What fields? What validation on the client?
    │
    ▼
Zod Schema / ◀── What validation schema does the form use?
Validation        What are the constraints?
    │
    ▼
Server Action ◀── What does the action do? Auth? Headers?
                   What API does it call?
    │
    ▼
API Route ◀── What does the endpoint validate?
Handler         What records does it create/update?
    │
    ▼
Database ◀── What tables are written to?
Schema         What constraints, relationships, triggers?
```

### Example 3: Side Effects and Background Work

```
START: An action triggers side effects
    │
    ├──▶ Notification ◀── How are notifications created?
    │    Service           What templates? What channels?
    │
    ├──▶ Workflow ◀── How are workflow records created?
    │    Audit Trail       What actions are tracked?
    │
    ├──▶ Queue / Job ◀── Is there a job queue?
    │                      What jobs get enqueued? How are they processed?
    │
    └──▶ Cron Job ◀── Are there scheduled tasks related to this area?
                       What do they do? When do they run?
```

These are starting patterns. The actual tracing depends on what you encounter — follow the code wherever it leads.

## Process

### Step 1: Identify repository starting points

Based on the context given to you so far, determine where to start reading in the repository or local codebase. Present to user:

```
Based on the requirements, here are the starting points I'll trace from:

1. [Starting point] — [why this is relevant] — lane: [bounded subsystem]
2. [Starting point] — [why] — lane: [bounded subsystem]
3. [Starting point] — [why] — lane: [bounded subsystem]

Any other areas I should look at?
```

Unless you have specific questions for the user, start reading. Otherwise ask first.

### Step 2: Scout and chase the code

Launch one read-only locator scout per independent lane and run all dependency-ready lanes concurrently up to available capacity. Each scout returns candidate files, relationships, unresolved branches, and why each item matters. It does not write `plan-prep.md`.

The plan-prep owner validates the returned candidates and reads the authoritative files directly into the main context. Read independent files in concurrent batches when supported. Follow newly discovered references in additional ready-set rounds rather than assigning all starting points to one sequential scout.

Complete this step only when every starting point and returned branch has been read, excluded with rationale, or recorded as an owned gap with blocking status.

### Step 3: Document what was read

One plan-prep owner writes the consolidated reference list to `plan-prep.md`. This list serves two purposes:
1. Shows what context was loaded and why
2. Allows future components or sessions to decide which files to re-read if needed

### Step 4: Write to memory

If the user pointed you to files you wouldn't have found on your own, write to `memory.md`. Record the pattern, not the path — "when working on X, also read Y because..." The specific file may change; the connection pattern persists.

## Output

Document in the `## Current Repo Landscape — Related Files reference` section of `plan-prep.md`:

```markdown
## Current Repo Landscape — Related Files reference

### [Area: e.g., Scheduling UI]
- `path/to/page.tsx` — [why: parent route for new feature]
- `path/to/component.tsx` — [why: similar list pattern to follow]

### [Area: e.g., Team Members (similar pattern)]
- `path/to/team_members/page.tsx` — [why: same CRUD pattern we'll follow]
- `lib/transformers/team_members_transformer.ts` — [why: transformer pattern to follow]
- `lib/actions/team_member_actions.ts` — [why: server action pattern]
- `tests/transformers/team_members_transformer.test.ts` — [why: test pattern]

### [Area: e.g., API Layer]
- `api/routes/team_members.ts` — [why: CRUD endpoint pattern with Zod validation]
- `tests/routes/team_members.test.ts` — [why: API test pattern]

### [Area: e.g., Database]
- `schema.zmodel` (relevant sections) — [why: existing models, relationships, access policies]
- `prisma/migrations/20260301_add_team_members.sql` — [why: migration pattern]

### [Area: e.g., Side Effects]
- `lib/notifications/notification_service.ts` — [why: how notifications are dispatched]
- `lib/workflows/workflow_service.ts` — [why: audit trail pattern]
```
