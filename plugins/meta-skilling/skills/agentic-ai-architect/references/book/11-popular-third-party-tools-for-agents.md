---
chapter: 11
title: "Popular Third-Party Tools for Agents"
part: "III — Tools & MCP"
source_pdf_pages: "42-44"
---

# Chapter 11: Popular Third-Party Tools for Agents
*Part III: Tools & MCP*

Agents are only as powerful as the tools you give them. As a result, an ecosystem has sprung up around popular types of tools.

## Web scraping & computer use

One of the core tool use cases for agents is browser search.

This includes web scraping, automating browser tasks, and extracting information. You can use built-in tools, connect to MCP servers, or integrate with higher-level automation platforms.

There are a few different tools you could take to add search to your agents:

- **Cloud-based web search APIs.** There are a few web search APIs that have become popular for LLMs to use, including Exa, Browserbase, and Tavily.
- **Agentic web search.** Tools like Stagehand (in JavaScript) and Browser Use (in Python, with MCP servers for JS users) have plain English language APIs that you can use to describe web scraping tasks.
- **Low-level open-source search tools.** Microsoft's Playwright project remains widely used as the underlying engine that many agentic browser tools are built on.

When you provide browser tools to agents, you often encounter similar challenges to traditional browser automation.

- **Anti-bot detection.** From browser fingerprinting to WAFs to captchas, many websites protect against automated traffic.
- **Fragile setups.** Browser use setups sometimes break if target websites change their layout or modify some CSS.

These challenges are solvable — just budget a bit of time for some munging and glue work!

## Third-party integrations

Agents need to connect with the systems where user data lives — and they need the ability to both read and write from those systems.

Most agents (like most SaaS apps) need access to a core set of *general* integrations like email, calendar, or documents.

Your personal assistant agent will need access to Gmail, Google Calendar, or Microsoft Outlook.

Your sales agent will need to integrate with Salesforce or Hubspot. Your HR agent will need to integrate with Rippling or Workday.

It's possible the services you need already ship in an MCP server before you reach for an iPaaS. The ecosystem has grown significantly and many popular tools now offer native MCP support.

Most people building agents want to avoid spending months building bog-standard integrations and choose an "agentic iPaas" (integration-platform-as-a-service). We've seen folks be happy with Arcade and Composio, which are general services, but there are specialized services in various domains as well.
