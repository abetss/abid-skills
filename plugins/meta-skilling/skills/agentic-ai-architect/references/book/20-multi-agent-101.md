---
chapter: 20
title: "Multi-Agent 101"
part: "VI — Multi-Agent Systems"
source_pdf_pages: "75-76"
---

# Chapter 20: Multi-Agent 101
*Part VI: Multi-Agent Systems*

Think about a multi-agent systems like a specialized team, like marketing or engineering. Different agents work together with their own specialized role to accomplish more complex tasks.

If you've used an agentic coding tools like Claude Code or Replit Agent, you've actually already been using a multi-agent system.

One agent works with you to plan / architect your code. After you've mapped it all out, you next work with a 'code manager' agent that passes instructions to a code writer, executes the resulting code in a sandbox, and passes any errors back to the code writer.

Each of these agents has different memories, different system prompts, and access to different tools.

We often joke that designing a multi-agent system involves a lot of skills used in designing an organization. You group related tasks into a job description. You might give creative tasks to one person and analytical tasks to another.

You want to think about network dynamics. Is it better for three specialized agents to gossip among themselves? Or feed their output back to a manager agent who can make a decision?

Multi-agent systems with subagents let you break down complex tasks into manageable pieces. And designs are fractal. A hierarchy is just a supervisor of supervisors.

But when you're building, start with the simplest version first.

Let's break down some of the patterns.
