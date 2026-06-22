# Understanding the Current Landscape

> Load the relevant codebase context into this conversation so that all subsequent work is informed by actual code.

## Memory

Read `landscape-memory.md` in this skill directory before starting. It contains learnings about what to trace, hidden connections, and commonly missed files.

## Need

Read the code that needs to be in context for the rest of the planning to go well. The value is not a report — it's having the actual code in the conversation context so that flow design, architecture decisions, and task breakdown are grounded in reality.

## Methods

- **Chase the code from starting points** — Identify entry points relevant to the work, then trace through the code following references, imports, and calls until you've loaded all the relevant context
- **Read files directly** — Do NOT use agents. Agents run in separate context. The whole point is to have the code in THIS conversation's context
- Ask the user only if you had specific question you couldn't find a satisfying answer too
- **Read existing documentation** — Architecture docs, conventions, table-of-content.md in the project often found in a-docs, a-kb. See their table of contents
- **Surface architecture opportunities** — For every technical decision you encounter while exploring, ask: is there more than one decent way to achieve this? If yes, does it warrant an architectural discussion? If so, add it to a running list of architecture discussions to bring up to the user

## How to Chase the Code

Based on the context given to you so far, identify the starting points for what you're building. Then trace through the code, following each reference until you've loaded everything relevant.

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

### Step 1: Identify starting points

Based on the context given to you so far, determine where to start reading. Present to user:

```
Based on the requirements, here are the starting points I'll trace from:

1. [Starting point] — [why this is relevant]
2. [Starting point] — [why]
3. [Starting point] — [why]

Any other areas I should look at?
```

Unless you have specific questions for the user, start reading. Otherwise ask first.

### Step 2: Chase the code

From each starting point, read files by following references, imports, and calls. Read each file directly — do not summarize or paraphrase what you find. The goal is to have the code in context.

### Step 3: Document what was read

After reading, write the reference list to `plan-prep.md`. This list serves two purposes:
1. Shows what context was loaded and why
2. Allows future components or sessions to decide which files to re-read if needed

### Step 4: Write to memory

If the user pointed you to files you wouldn't have found on your own, write to `landscape-memory.md`. Record the pattern, not the path — "when working on X, also read Y because..." The specific file may change; the connection pattern persists.

## Output

Document in `plan-prep.md` (append after previous component):

```markdown
## Current Landscape — Related Files reference

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
