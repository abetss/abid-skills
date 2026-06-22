---
chapter: 6
title: "Tool Calling"
part: "II — Building an Agent"
source_pdf_pages: "20-23"
---

# Chapter 6: Tool Calling
*Part II: Building an Agent*

Tools are functions that agents can call to perform specific tasks — whether that's fetching weather data, querying a database, or processing calculations.

The key to effective tool use is clear communication with the model about what each tool does and when to use it.

Here's an example of creating and using a tool:

```ts
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

const getWeatherInfo = async (city: string) => {
  // Replace with an actual API call to a weather service
  console.log(`Fetching weather for ${city}...`);
  // Example data structure
  return { temperature: 20, conditions: "Sunny" };
};

export const weatherTool = createTool({
  id: "Get Weather Information",
  description: `Fetches the current weather information for a given city`,
  inputSchema: z.object({
    city: z.string().describe("City name"),
  }),
  outputSchema: z.object({
    temperature: z.number(),
    conditions: z.string(),
  }),
  execute: async ({ context: { city } }) => {
    console.log("Using tool to fetch weather information for", city);
    return await getWeatherInfo(city);
  },
});
```

Best practices:

- Provide detailed descriptions in the tool definition and system prompt
- Use specific input/output schemas
- Use semantic naming that matches the tool's function (eg `multiplyNumbers` instead of `doStuff`)

**Remember:** The more clearly you communicate a tool's purpose and usage to the model, the more likely it is to use it correctly. You should describe both what it does and when to call it.

**Designing your tools: The most important step**

When you're creating an AI application, the most important thing you should do is think carefully about your tool design:

- **What the tools will you need?**
- **What will each of them do?**

It is genuinely important that you *write this list out clearly before you start coding*, even if it's just jotted down on a napkin left over from lunch at your desk.

**Real-world example: Alana's book recommendation agent**

Alana Goyal, a Mastra investor, wanted to build an agent that could analyze, and give intelligent recommendations about, her library of investor books.

**First attempt:**

She tried dropping all the books into the agent's knowledge window. This didn't work well — the agent couldn't reason about the data in a structured way.

**Better approach:**

She broke the problem down into a set of specific tools, each handling a different aspect of the data:

- A tool for accessing the corpus of investors
- A tool for book recommendations
- A tool for books tagged by genre

Then, she added more tools for common operations:

- Get all books by genre
- Get book recommendations by investor
- Sort people writing recommendations by type (founders, investors, etc.)

If a human analyst were doing this project, they'd follow a specific set of operations or queries.

The trick is to take those operations and write them as tools or queries that your agent can use.

**Result:**

With these tools in place, the agent could now intelligently analyze the corpus of books, answer nuanced questions, and provide useful recommendations — just like a skilled human analyst.

**Takeaway:**

Think like an analyst. Break your problem into clear, reusable operations. Write each as a tool.

If you do this, your agent will be much more capable, reliable, and useful.
