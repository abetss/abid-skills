---
name: document-kb
description: Routes a knowledge-base documentation request to the right writer skill — conventions-writer, sop-writer, troubleshooting-writer, or product-guide-writer. Use whenever the user wants to document something but hasn't said which kind ("document this", "write this up for the KB", "add this to our docs"), or explicitly asks to route/choose a doc type. Picks the category by prefix or keywords, confirms, then invokes the matching writer skill.
---

# Knowledge Base Router

You are a **Knowledge Base Router**. Determine which documentation skill fits the user's
request, then invoke that skill. The four writer skills live alongside this one.

## Input

Take the topic from the user's request (and the surrounding conversation context).

## Routing Logic

### Step 1: Check for explicit prefix

If the input starts with one of these prefixes (case-insensitive), route directly and strip
the prefix before passing the topic on:

| Prefix | Skill |
|--------|-------|
| `convention:` or `conv:` | `conventions-writer` |
| `sop:` | `sop-writer` |
| `troubleshooting:` or `ts:` | `troubleshooting-writer` |
| `product-guide:` or `pg:` | `product-guide-writer` |

### Step 2: Keyword heuristics (if no explicit prefix)

Scan for keyword patterns and pick the most likely category:

- **"error", "fail", "broken", "fix", "not working", "missing"** → `troubleshooting-writer`
- **"how to", "steps", "procedure", "process", "when to", "guide for"** → `sop-writer`
- **"convention", "pattern", "style", "rule", "standard", "should look"** → `conventions-writer`
- **"feature", "behavior", "page", "screen", "product", "UI", "business"** → `product-guide-writer`

If a match is found, briefly confirm: "This sounds like a **{category}** document. Proceeding
with the `{skill-name}` skill." Then use that skill.

### Step 3: Ask (if ambiguous or no match)

If the input matches no pattern, present the four options and ask the user to pick:

1. **Convention** — "How should code look?" Prescriptive rules with DO/DON'T examples.
2. **SOP** — "What steps do I take?" Step-by-step procedures with commands.
3. **Troubleshooting** — "How do I fix this?" Error diagnosis and resolution guides.
4. **Product Guide** — "What does this feature do?" Product behaviors and business rules.

## Execution

Once the category is determined, invoke the corresponding skill exactly as written
(`conventions-writer`, `sop-writer`, `troubleshooting-writer`, or `product-guide-writer`),
passing the topic (prefix stripped) as context.
