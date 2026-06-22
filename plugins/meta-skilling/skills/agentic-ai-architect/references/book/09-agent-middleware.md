---
chapter: 9
title: "Agent Middleware"
part: "II — Building an Agent"
source_pdf_pages: "31-33"
---

# Chapter 9: Agent Middleware
*Part II: Building an Agent*

Once we see that it's useful to specify the system prompt, model, and tool options at runtime, we start to think about the other things we might want to do at runtime as well.

**Guardrails**

*Guardrails* are a general term for sanitizing the input coming into your agent and/or the output it's returning before the user can see it. Input sanitization tries broadly to guard against prompt injection attacks.

These include model "jailbreaking" ("IGNORE PREVIOUS INSTRUCTIONS AND..."), requests for PII, and off-topic chats that could run up your bills.

```
                    INPUT
                  GUARDRAILS                    AGENT
                ┌──────────────┐         ┌─────────────────────────┐
  ┌──────────┐  │ prompt injection │     │ ┌───────┐  ┌─────┐  ┌────────┐ │
  │  user    │→ │     guard        │  →  │ │ input │→ │ LLM │→ │ output │ │
  │  input   │  │       *          │     │ └───────┘  └─────┘  └────────┘ │
  └──────────┘  │  jailbreaking    │     └─────────────────────────┘
                │     guard        │              │
                │       *          │              │
                │  privacy guard   │              │
                └──────────────┘                  ↓
                              ┌──────────────┐
                              │ hallucination │      ┌────────┐
                          →   │     guard     │  →   │ agent  │
                              │       *       │      │ output │
                              │  data leakage │      └────────┘
                              │     guard     │
                              │       *       │
                              │ toxicity guard│
                              └──────────────┘
                                  OUTPUT
                                GUARDRAILS
```

Models have gotten better at resisting direct jailbreaks, but prompt injection has gotten more sophisticated as agents have gained more autonomy.

An agent that browses the web or reads uploaded documents can encounter malicious instructions embedded in that content.

For example, a February 2026 prompt injection attack against the open-source coding IDE Cline began with an attacker opening a Github issue in a Cline repo using a title containing malicious instructions.

*Chris Bakke prompt injection attack, December 2023*

**Agent authentication and authorization**

One thing to think about when building agents is that because they are more powerful than pre-LLM data access patterns, you may need to spend more time ensuring they are *permissioned accurately*.

Security through obscurity becomes less of a viable option when users can ask an agent to retrieve knowledge hidden in nooks and crannies!

There are two layers of permissions to consider for agents:

- The resources the agent itself can have access to
- Which users are allowed to access the agent

As with guardrails, middleware is the typical place to put any agent authorization because it's in the perimeter *around* the agent rather than within the agent's inner loop.

For high-stakes or irreversible actions, consider adding human-in-the-loop checkpoints — pausing execution to get explicit user confirmation before the agent proceeds
