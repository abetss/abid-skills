# Discover Existing Capabilities and Solutions

> Establish what the named platforms already support and what nearby implementations already exist before designing something new.

## Need

A plan can be technically sound and still waste effort when it overlooks a native capability, package, plugin, product, service, or internal implementation that already solves much of the requested problem. This component makes adopt-versus-extend-versus-build evidence explicit.

Use it when work:

- builds on or integrates with a named platform, framework, product, protocol, API, or service;
- creates a new extension, package, tool, service, or system for behavior that may already exist; or
- requires a material adopt-versus-extend-versus-build decision.

This component is not repository tracing. Select **Understand the Current Repo Landscape** when an existing codebase also needs inspection. **Research Solution Precedents** is separate: use it for broader architectural lessons after nearby capabilities and solutions are understood.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Return material adopt/extend/build decisions and unresolved capability questions to the plan-prep owner; do not edit the architecture index.

## Required Inputs

- Requirements or equivalent work description
- Named technologies and known environment constraints

## Optional Inputs

- Current repo landscape findings
- Existing architecture points
- User-supplied sources or candidate solutions

## Procedure

### Step 1: Build the question set

Turn the requirements into decision-critical questions. Answer each question below when applicable; mark it not applicable with a reason rather than silently omitting it.

1. What existing environment or system must the work fit?
2. What do the named platforms support natively?
3. Does the requested user behavior already exist in the same ecosystem as a package, plugin, product, service, example, or internal implementation?
4. Which nearby solutions can be adopted unchanged, extended, combined, or used as source precedents?
5. What compatibility, maintenance, licensing, security, lifecycle, and operational constraints affect reuse?
6. What requirements remain unmet by the closest solution?
7. Which unanswered questions could materially change the design?

Add work-specific questions as needed. Record every material question with why it matters and its completion condition.

### Step 2: Map evidence surfaces

For each question, identify the relevant surfaces before deep research:

- official documentation index and relevant capability/API/lifecycle guides;
- official examples, schemas, release notes, and source where needed;
- ecosystem package or plugin directory;
- relevant registries and repository search;
- installed/local packages and internal solution catalogs when available;
- user-supplied candidates, preserved as explicit candidates.

Use technology names combined with requested behaviors in discovery queries. An inaccessible URL establishes only that URL's failure. Try ordinary official navigation or another official source within the lane budget, then report the remaining gap precisely.

### Step 3: Run bounded discovery first

Run a short candidate-discovery pass before selecting deep-research targets. Familiar general frameworks and previously known candidates do not replace this pass unless a sufficiently current discovery artifact already covers the same technologies and behaviors, or the user explicitly restricts the candidate set.

Record a **candidate-discovery handoff** containing:

- question coverage;
- surfaces searched;
- exact search terms or navigation starting points;
- candidates found;
- open questions; and
- unsearched or inaccessible surfaces.

This handoff is sufficient to select broader precedent lanes; it is not approval to make a decision that depends on unfinished candidate verification.

Rank candidates in this order:

1. Same requested behavior in the same ecosystem
2. Same behavior in another ecosystem
3. General architectural patterns

This component normally investigates the first two. Route the third to **Research Solution Precedents** when deeper comparison is useful.

### Step 4: Fan out shortlist verification

Choose the smallest shortlist that covers the credible nearby alternatives. Assign one bounded lane per independent candidate or source cluster and run ready lanes concurrently.

Each lane receives an evidence cap, deadline, sufficient-evidence stopping condition, and result contract. Verify against primary sources and distinguish:

- documented capability from inference;
- current version behavior from living or mismatched documentation;
- adoption unchanged from extension or fork requirements;
- product fit from merely similar terminology;
- established facts from unanswered questions.

### Step 5: Compare adopt, extend, and build

For the closest candidates, compare:

- requirements covered and unmet;
- integration and migration cost;
- extension points and coupling;
- maintenance, compatibility, licensing, and security implications;
- operational and lifecycle gaps;
- evidence needed before relying on uncertain claims.

A recommendation to build a custom subsystem must either compare the closest credible candidate or provide a bounded **no credible candidate found** record with searched surfaces, queries, limitations, and residual uncertainty. It must name the unmet requirements that justify building instead of adopting or extending. A bounded negative result is not proof that no solution exists.

### Step 6: Verify coverage and synthesize

One owner writes `existing-solutions.md`. Before accepting the component, verify that:

- every material question has an answer, explicit unresolved status, or justified not-applicable disposition;
- named-platform official capabilities and same-ecosystem implementations were investigated when applicable;
- searched surfaces and queries are recorded;
- each applicable solution space has either source-backed closest-candidate comparisons or a bounded no-credible-candidate record;
- unresolved evidence that could change adopt/extend/build blocks that decision and its dependent design/tasks under the shared architecture protocol;
- a nonblocking follow-up includes a rationale showing why its answer cannot change the decision.

An agent exit, source count, or populated report does not satisfy this gate by itself.

## Output

Write `{work-folder}/existing-solutions.md` with:

- Question and coverage matrix
- Named-platform native capabilities
- Discovery surfaces and queries
- Candidate inventory and shortlist rationale
- Closest-solution comparisons
- Adopt/extend/build assessment
- Version and evidence caveats
- Unanswered questions and architecture contributions

Present the findings and get user approval before architecture or design depends on them.
