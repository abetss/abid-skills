---
chapter: 12
title: "Workflows 101"
part: "IV — Graph-Based Workflows"
source_pdf_pages: "47"
---

# Chapter 12: Workflows 101
*Part IV: Graph-Based Workflows*

> Summary (paraphrased, not a verbatim transcription). Code/API examples are transcribed exactly.

Individual agents are powerful because they can call any tool (function) at any step. That flexibility is sometimes more than a task needs.

Graph-based workflows have emerged as a more deterministic way to build with models. A workflow graph spells out the sequence of actions, the branching logic, and the conditions an agent follows to reach a goal — essentially describing the flow of execution and decision-making.

Workflows and agents are not mutually exclusive. In practice you often combine them: agents handle the open-ended reasoning steps, while workflows provide deterministic scaffolding around those agents.

Why reach for a workflow abstraction instead of just writing plain code? Workflow primitives make it easy to define branching logic, run steps in parallel, create checkpoints, and add tracing — plus you get a graph you can visualize.
