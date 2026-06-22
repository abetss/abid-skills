---
chapter: 23
title: "Workflows as Tools"
part: "VI — Multi-Agent Systems"
source_pdf_pages: "79"
---

# Chapter 23: Workflows as Tools
*Part VI: Multi-Agent Systems*

Hopefully, by now, you're starting to see that all multi-agent architecture comes down to which primitives you're using and how you're arranging them.

It's particularly important to remember this framing when trying to build more complex tasks into agents.

Let's say you want your agent(s) to always run 3 separate tasks sequentially. You may want to turn each of those tasks into individual workflows, so you can stipulate a workflow's order of steps and provide more structure.

Each of these workflows can then be passed along as *tools* to the agent(s).
