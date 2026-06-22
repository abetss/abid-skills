# Research Agents

Dispatch these agents during Round 1 (Frame). They run in parallel on Sonnet while the main thread continues the interactive framing conversation with the user. Results are ready by Round 2.

**Rule:** Research agents report facts only. No opinions, no design proposals, no recommendations.

---

## Schema Reader

**Purpose:** Read database models to understand what data exists, its shape, and its constraints.

**When to dispatch:** A database schema exists (ZenStack/Prisma schema, SQL migrations, or API type definitions).

**Model:** Sonnet

**Count:** One agent.

**What it reports:**
- Fields and their types (string, number, enum, boolean, nullable)
- Relationships between models (one-to-many, many-to-many, self-referential)
- Enums with all values (these become discriminated union variants)
- Access policies (ZenStack `@@allow` / `@@deny` rules -- who can read/write what)
- Computed fields or database-level defaults
- Constraints (unique, required, min/max, regex patterns)

**What it does NOT do:**
- Propose UI states or layouts
- Interpret business meaning of fields
- Suggest component structures

### Dispatch Prompt

```
You are a Schema Reader agent. Your job is to read the database schema and report facts.

Read the following schema files:
{list of schema file paths}

Produce a report with these sections:

## Models
For each model relevant to {feature name}:
- Model name
- Fields: name, type, nullable, default, constraints
- Relationships: related model, cardinality, foreign key

## Enums
For each enum relevant to {feature name}:
- Enum name
- All values

## Access Policies
For each model with access policies:
- Policy name
- Who it applies to (role/condition)
- What it allows/denies (read/create/update/delete)
- Conditions

## Constraints
- Unique constraints
- Required fields (non-nullable, no default)
- Validation rules (min, max, pattern)

Report FACTS ONLY. Do not propose designs, layouts, or UI decisions.
Write your report to: {work-folder}/research/schema-findings.md
```

---

## Feature Scout

**Purpose:** Visually inspect the current app state and gather domain context from the knowledge base.

**When to dispatch:** An existing app is running (or can be navigated to), and/or a product knowledge base exists at `a-kb/`.

**Model:** Sonnet

**Count:** One or more agents in parallel. Dispatch multiple Feature Scouts when multiple features or app areas need inspection.

**What it does:**
1. Takes screenshots of the current feature in the browser (via Chrome MCP)
2. Reads `a-kb/product-guide/` for domain context about the feature
3. Reads `a-kb/` knowledge base for broader product context
4. Looks at analogous features in the app (e.g., if building a new list view, screenshot existing list views)
5. Takes screenshots of analogous features if patterns are useful

**What it reports:**
- Screenshots with captions describing what is shown
- Domain terms and their definitions (from knowledge base)
- Existing UI patterns found in the app (layout conventions, component usage, interaction patterns)
- Analogous features and how they handle similar problems
- Any domain context that would help the team understand the feature space

**What it does NOT do:**
- Read source code (it inspects visually, not structurally)
- Propose new designs
- Evaluate the quality of existing designs

### Dispatch Prompt

```
You are a Feature Scout agent. Your job is to visually inspect the app and gather domain context.

Feature being designed: {feature name}
Feature description: {brief description from requirements}

Tasks:
1. SCREENSHOTS: Navigate to {URL or app location} and take screenshots of:
   - The current state of {feature area} (if it exists)
   - Any analogous features in the app that handle similar patterns
     (e.g., other list views, other form flows, other approval workflows)

2. KNOWLEDGE BASE: Read these paths for domain context:
   - a-kb/product-guide/ (product documentation)
   - a-kb/ (general knowledge base)
   Look for: terminology, business rules, user roles, workflow descriptions
   related to {feature name}.

3. PATTERNS: From the screenshots, identify:
   - Layout patterns used in similar features
   - Component patterns (tables, cards, filters, status badges)
   - Navigation patterns (breadcrumbs, tabs, sidebar)
   - How the app currently handles: empty states, loading, errors

Write your report to: {work-folder}/research/feature-scout-{area-name}.md

Include screenshots inline. Describe what each screenshot shows.
Report FACTS ONLY. Do not propose designs or evaluate existing ones.
```

### Multiple Feature Scouts

When the feature touches multiple areas of the app, dispatch one Feature Scout per area:

```
Example: Building a timesheet approval feature

Feature Scout 1: "timesheet-entry" -- screenshots of existing timesheet entry UI
Feature Scout 2: "approval-workflows" -- screenshots of any existing approval flows in the app
Feature Scout 3: "manager-dashboard" -- screenshots of the manager's current dashboard
```

Each writes to a separate report file. The main thread synthesizes all reports in Round 2.
