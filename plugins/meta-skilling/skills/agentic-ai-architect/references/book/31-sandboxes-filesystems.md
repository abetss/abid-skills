---
chapter: 31
title: "Sandboxes & Filesystems"
part: "IX — Coding Agents"
source_pdf_pages: "109-110"
---

# Chapter 31: Sandboxes & Filesystems
*Part IX: Coding Agents*

Any agent that writes and executes code needs somewhere safe to run it.

You probably don't want to run agent-generated code directly on your servers — this creates both resource contention and security risks.

Sandboxes provide an isolated environment where code runs separately from your application via containers, micro-VMs, or intercepted system calls.

In 2026, there's a category of dedicated platforms like E2B, Daytona, and Modal. Cloud providers like Cloudflare and Vercel also offer sandbox primitives.

## Ephemeral vs. stateful sandboxes

For one-off tasks, you want an ephemeral sandbox — it can spin up, runs some code, and disappear.

For longer-horizon tasks, you may want a stateful sandbox that persists between calls — your agent can install dependencies, write files, and return to the same environment later.

## Filesystems

Most sandbox platforms expose a filesystem API so your agent can read and write files just like it would on a local machine. Whether that filesystem survives between sessions depends on the platform — ephemeral sandboxes wipe it on teardown, stateful ones persist it.

Some platforms also let you snapshot the filesystem and restore to it later. This is particularly useful for evals: run your agent against a known starting state, check what changed, roll back, and run again.

## Managing latency

Sandboxes add latency. A 150ms startup is fine for a coding agent that runs for minutes, but noticeable if you're spinning up a new sandbox on every tool call.

Some teams strike a balance: create one sandbox per agent session, reuse it across all tool calls, then tear it down when the session ends.
