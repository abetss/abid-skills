---
chapter: 14
title: "Suspend and Resume"
part: "IV — Graph-Based Workflows"
source_pdf_pages: "52-55"
---

# Chapter 14: Suspend and Resume
*Part IV: Graph-Based Workflows*

> Summary (paraphrased, not a verbatim transcription). Code/API examples and diagrams are transcribed exactly.

Workflows sometimes need to pause while waiting for something outside the agent's control — a human approval, a slow external API, or a long-running async process. Because the third party can take arbitrarily long to respond, you don't want to hold a running process open the whole time.

Instead, persist the workflow's state and provide a function you can call later to pick up where you left off. Mastra exposes this with `.suspend()` and `.resume()`.

To handle suspended workflows, you watch for status changes and resume execution when ready. The suspend/resume flow looks like this:

```
                                                    Suspend
              .step(step1)      .then(step2)      .suspend()
   ( In )--------->[ step 1 ]------>[ step 2 ]------------> < suspended >
                        |               |                                  \
                    output 1        output 2                               ( out )
                        v               v                                  /
                         \----> <  context  > <----                       /
                        ^               ^         \                      /
                    output 3        output 4       v                    /
       .after(stepOne) |  .then(step4) |                               /
            [ step 3 ]-+------------->[ step 4 ]-----------------------/
```

```
                                                    Resume
              .step(step1)      .then(step2)
   ( In )--------->[ step 1 ]------>[ step 2 ]--------------------------\
                        |               |                              ( out )
                    output 1        output 2                            /
                        v               v                              /
                         \----> <  context  > <----                   /
                        ^               ^                            /
                    output 3        output 4                        /
       .after(stepOne) |  .then(step4) |                           /
            [ step 3 ]-+------------->[ step 4 ]------------------/
```

A workflow with suspend and resume starts with steps — the building blocks of workflows. Create a step using `createStep`:

```ts
// Create a step with defined input/output schemas and execution logic
const inputSchema = z.object({
  inputValue: z.string(),
});

const myStep = createStep({
  id: "my-step",
  description: "Does something useful",
  inputSchema,
  outputSchema: z.object({
    outputValue: z.string(),
  }),
  // Optional: Define the resume schema for step resumption
  resumeSchema: z.object({
    resumeValue: z.string(),
  }),
  // Optional: Define the suspend schema for step suspension
  suspendSchema: z.object({
    suspendValue: z.string(),
  }),
  execute: async ({
    inputData,
    mastra,
    getStepResult,
    getInitData,
    runtimeContext,
  }) => {
    const otherStepOutput = getStepResult(step2);
    const initData = getInitData<typeof inputSchema>(); // typed as the input schema variable (zod schema)
    return {
      outputValue: `Processed: ${inputData.inputValue}, ${initData.startValue} (runtimeContextValue: ${runtimeContext.get("runtimeContextValue")})`,
    };
  },
});
```

Then create a workflow using `createWorkflow`:

```ts
// Create a workflow with defined steps and execution flow
const myWorkflow = createWorkflow({
  id: "my-workflow",
  // Define the expected input structure (should match the first step's inputSchema)
  inputSchema: z.object({
    startValue: z.string(),
  }),
  // Define the expected output structure (should match the last step's outputSchema)
  outputSchema: z.object({
    result: z.string(),
  }),
  steps: [step1, step2, step3], // Declare steps used in this workflow
})
  .then(step1)
  .then(step2)
  .then(step3)
  .commit();

// Register workflow with Mastra instance
const mastra = new Mastra({
  vnext_workflows: {
    myWorkflow,
  },
});

// Create a run instance of the workflow
const run = mastra.vnext_getWorkflow("myWorkflow").createRun();
```

Once you've defined a workflow, run it like so:

```ts
// Create a run instance
const run = myWorkflow.createRun();

// Start the workflow with input data
const result = await run.start({
  inputData: {
    startValue: "initial data",
  },
});

// Access the results
console.log(result.steps); // All step results
console.log(result.steps["step-id"].output); // Output from a specific step

if (result.status === "success") {
  console.log(result.result); // The final result of the workflow, result of the last step (or `.map()` output, if used as last step)
} else if (result.status === "suspended") {
  const resumeResult = await run.resume({
    step: result.suspended[0], // there is always at least one step id in the suspended array, in this case we resume the first suspended execution path
    resumeData: {
      /* user input */
    },
  });
} else if (result.status === "failed") {
  console.error(result.error); // only exists if status is failed, this is an instance of Error
}
```

That's a full AI agent workflow in Mastra — it branches, pauses execution, and then resumes — in a couple dozen lines of code.

In production, make sure workflow state is persisted to a durable store. A suspended workflow that lives only in memory won't survive a server restart.
