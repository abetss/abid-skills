# Research Solution Precedents

> Research broader architectural precedents after native capabilities and nearby existing solutions are understood.

## Problem

Nearby solutions may not resolve a consequential or unfamiliar decision. Broader systems and practitioners can supply proven architectural patterns, operational lessons, and trade-offs.

This component does not own named-platform capability or same-ecosystem package/plugin discovery. Select **Discover Existing Capabilities and Solutions** for that work. General precedents cannot establish that no closer implementation exists.

## Intended Outcome

A cited set of credible comparable approaches, with enough context to judge what is transferable to this project.

This capability is optional and independently selectable. It may support any decision requiring external evidence and is not a fixed predecessor to another component or concern.

## Shared Architecture-Decision Protocol

Read and follow `../architecture-decision-protocol.md`. Contribute and return the architecture points encountered while evaluating precedents; report evidence without selecting the project's architecture.

## Required Inputs

- A specific problem or research question
- Known constraints relevant to comparing solutions
- The candidate-discovery handoff from Discover Existing Capabilities and Solutions when both components are selected

## Optional Inputs

- Architecture decision inventory
- Current-landscape findings
- Requirements and desired-flow findings from Design the Solution
- Existing technical direction
- Scale, reliability, security, or cost targets
- Preferred sources or time range

Optional inputs focus the research but do not require another component to have run.

## Procedure

### Step 1: Bound the research

Define the exact research question, comparison criteria, required evidence, source or evidence cap, lane deadline, and sufficient-evidence stopping condition. Do not begin open-ended browsing. If the user supplied preferred precedents, preserve them as separate candidates.

### Step 2: Discover broader precedent candidates briefly

When the relevant broader precedents are unknown, run one short discovery pass that returns a bounded candidate list. Discovery identifies lanes; it does not perform the full research. Prefer precedents that illuminate unresolved questions or gaps from `existing-solutions.md`. Skip this pass only when the user restricts the scope to named precedents or a current discovery record covers the same question. Familiarity with several frameworks is not such a record.

### Step 3: Fan out independent lanes

Create one bounded lane per independent precedent, research question, or source cluster. Run the largest dependency-ready set concurrently up to available capacity. One lane must not investigate several independent precedents sequentially.

Each lane receives:

- One precedent or research question
- The comparison criteria and project constraints
- Required evidence and source-quality expectations
- Its source or evidence cap
- Its stopping condition and deadline
- A result contract covering context, approach, strengths, limitations, failures, transferable lessons, mismatches, citations, and evidence gaps

When independent source retrieval inside one lane would otherwise dominate elapsed time, fan those source clusters out as well and consolidate them within that lane.

### Step 4: Stop predictably

A lane stops when its evidence condition is met, its cap is reached, or its deadline expires. On cap or deadline, return the evidence collected and name the remaining gap instead of continuing indefinitely. A stalled lane must terminate as an explicit gap or blocker; it must not hold the workflow open without a terminal policy.

### Step 5: Synthesize once

After the lanes finish, one owner compares and deduplicates their results, identifies cross-precedent patterns, and writes `solution-research.md`. Research lanes return results and never write the shared artifact directly.

## Completion gate

Before accepting this component, verify that each selected precedent answers a stated broader comparison question, independent lanes respected their caps/deadlines, and the synthesis distinguishes architectural lessons from direct product fit. If nearby-solution discovery was applicable but not completed, return that coverage gap rather than treating general research as complete solution discovery.

## Outputs

`solution-research.md`, containing:

- Research question and scope
- Comparable companies, projects, or practitioners
- Approach used in each precedent
- Original context, constraints, and scale
- Reported strengths, limitations, and failures
- Transferable lessons and mismatches for this project
- Patterns across precedents
- Source links and publication dates
- Evidence gaps and uncertainty

This component reports precedents; it does not choose the project’s architecture.
