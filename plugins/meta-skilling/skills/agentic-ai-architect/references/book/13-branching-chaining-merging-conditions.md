---
chapter: 13
title: "Branching, Chaining, Merging, Conditions"
part: "IV — Graph-Based Workflows"
source_pdf_pages: "48-51"
---

# Chapter 13: Branching, Chaining, Merging, Conditions
*Part IV: Graph-Based Workflows*

> Summary (paraphrased, not a verbatim transcription). Code/API examples and diagrams are transcribed exactly.

Several frameworks offer workflow-graph abstractions. The examples here use Mastra, but the primitives are similar across tools. The chapter walks through the basic operations first, then best practices.

## Branching

Branching is useful when you want to fan one input out to multiple LLM calls. Example: you have a long medical record and need to check for 12 different symptoms (drowsiness, nausea, etc.). You could run a single LLM call that checks all 12 symptoms at once, or — often more accurate — run 12 parallel LLM calls, each checking for one symptom.

In Mastra you create branches with the `.step()` command. The branching graph looks like this:

```
                .step(step0)          .then(step2)
   ( In ) ----------------> [ step 1 ] ---------> [ step 2 ] -------------------\
                                  |                    |                          \
                              output 1             output 2                      ( out )
                                  v                    v                          /
                                <------ <  context  > <------                    /
                                  ^                    ^                        /
                              output 3             output 4                   /
                .after(stepOne)   |                    |                     /
                  [ step 3 ] -----+    .then(step4)    [ step 4 ] ----------/
```

## Chaining

Chaining is the simplest operation. Use it when you need to fetch data from a remote source before passing it to an LLM, or to feed the output of one LLM call into the next.

In Mastra you chain with the `.then()` command. Each step waits for the previous step to finish and has access to the previous step's results.

```
       .step(step0)       .then(step2)        .then(step3)
( In )----->[ step 1 ]------->[ step 2 ]------->[ step 3 ]----->( out )
                |                  ^                ^
            output 1          output 2         output 3
                v                  |                |
                 \----------> <  context  > <------/
```

## Merging

After branching paths diverge to handle different aspects of a task, they often need to converge again to combine their results.

```
              .step(step0)         .then(step2)
              [ step 1 ]----------->[ step 2 ]
             /     |                    |        \
       .step(   output 1           output 2      \
       step0)      v                    v          \
( In )--+        <------ <  context  > <------       --->( out )
       \           ^                    ^           /
        \      output 3            output 4        /
         \         |     .then(step4)   |         /
          \------>[ step 3 ]--------->[ step 4 ]--/
                .step(step3)
```

## Conditions

Sometimes a workflow needs to make decisions based on intermediate results.

In workflow graphs, because multiple paths can execute in parallel, Mastra defines the conditional path execution on the *child* step rather than on the parent step.

In the example below, a `processData` step executes only when the `fetchData` step has succeeded:

```ts
myWorkflow.step(
  new Step({
    id: "processData",
    execute: async ({ context }) => {
      // Action logic
    },
  }),
  {
    when: {
      "fetchData.status": "success",
    },
  },
);
```

**Best practices:**

- Compose steps so the input/output at each step is meaningful — you'll see those values in your tracing. (Tracing is covered later in the book.)
- Decompose steps so the model only has to do one thing at a time. In practice this usually means no more than one model call per step.

Many special-case workflow graphs — loops, retries, and so on — can be built by combining these primitives.
