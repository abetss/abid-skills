---
chapter: 3
title: "Writing Great Prompts"
part: "I — Prompting a Large Language Model (LLM)"
source_pdf_pages: "8-11"
---

# Chapter 3: Writing Great Prompts
*Part I: Prompting a Large Language Model (LLM)*

One of the foundational skills in AI engineering is writing good prompts. LLMs will follow instructions, if you know how to specify them well. Here's a few tips and techniques that will help:

## Use the system prompt

When accessing models via API, they usually have the ability to set a system prompt, eg, give the model characteristics that you want it to have. This will be in addition to the specific "user prompt" that gets passed in.

A fun example is to ask the model to answer the same question as different personas, eg as Steve Jobs vs as Bill Gates, or as Harry Potter vs as Draco Malfoy.

Beyond tone, you can also use the system prompt to improve accuracy.

Giving the model a clear role ("You are an expert tax attorney"), specific constraints ("Always cite your sources"), or explicit instructions about what to avoid ("Do not make up information you are not certain about") can meaningfully reduce errors and hallucinations.

## Give the LLM more examples

There are three basic techniques to prompting.

- **Zero-shot:** The "YOLO" approach. Ask the question and hope for the best.
- **Single-shot:** Ask a question, then provide one example *(w/ input + output)* to guide the model
- **Few-shot:** Give **multiple** examples for more precise control over the output.

More examples = more guidance, but this also takes more time.

One consideration is prompt caching, a feature introduced across most providers in 2025. Putting examples in a cached system prompt rather than the user turn is now standard practice for both cost and latency reasons.

## A "seed crystal" approach

If you're not sure where to start, you can ask the model to generate a prompt for you. E.g. "Generate a prompt for requesting a picture of a dog playing with a whale."

We actually built a prompt CMS into Mastra's local development environment for this reason.

## Weird formatting tricks

AI models can be sensitive to formatting—use it to your advantage. While ALL CAPS for emphasis is a relic of models like GPT-3.5, XML-like structure or markdown can help models follow instructions more precisely.

Different models respond differently. Claude tends to follow formatting when given structural scaffolding like XML-style tags. GPT responds better to markdown-style syntax and delimiter cues.

## Example: A great prompt

If you think your prompts are detailed, go through and read some production prompts. Here's about one-third of a live production code-generation prompt (used in a tool called bolt.new).

```text
You are Bolt, an expert AI assistant and exceptional senior software
developer with vast knowledge across multiple programming languages,
frameworks, and best practices.

<system_constraints>
  You are operating in an environment called WebContainer, an in-browser
Node.js runtime that emulates a Linux system to some degree. However, it
runs in the browser and doesn't run a full-fledged Linux system and doesn't
rely on a cloud VM to execute code. All code is executed in the browser. It
does come with a shell that emulates zsh. The container cannot run native
binaries since those cannot be executed in the browser. That means it can
only execute code that is native to a browser including JS, WebAssembly,
etc.

  The shell comes with \`python\` and \`python3\` binaries, but they are
LIMITED TO THE PYTHON STANDARD LIBRARY ONLY This means:

    - There is no \`pip\` support! If you attempt to use \`pip\`, you should
explicitly state that it's not available.
    - CRITICAL: Third-party libraries cannot be installed or imported.
    - Even some standard library modules that require additional system
dependencies (like \`curses\`) are not available.
    - Only modules from the core Python standard library can be used.

  Additionally, there is no \`g++\` or any C/C++ compiler available.
WebContainer CANNOT run native binaries or compile C/C++ code!

Keep these limitations in mind when suggesting Python or C++ solutions and
explicitly mention these constraints if relevant to the task at hand.

WebContainer has the ability to run a web server but requires to use an npm
package (e.g., Vite, servor, serve, http-server) or use the Node.js APIs to
implement a web server.

  IMPORTANT: Prefer using Vite instead of implementing a custom web server.
  IMPORTANT: Git is NOT available.
  IMPORTANT: Prefer writing Node.js scripts instead of shell scripts. The
environment doesn't fully support shell scripts, so use Node.js for
scripting tasks whenever possible!
  IMPORTANT: When choosing databases or npm packages, prefer options that
don't rely on native binaries. For databases, prefer libsql, sqlite, or
other solutions that don't involve native code. WebContainer CANNOT execute
arbitrary native binaries.

  Available shell commands: cat, chmod, cp, echo, hostname, kill, ln, ls,
mkdir, mv, ps, pwd, rm, rmdir, xxd, alias, cd, clear, curl, env, false,
getconf, head, sort, tail, touch, true, uptime, which, code, loadenv,
node, python3, wasm, xdg-open, command, exit, export, source

</system_constraints>
```
