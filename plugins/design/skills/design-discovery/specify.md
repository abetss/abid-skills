# Round 4: Specify

> Document component props per state for each component, then write the final design-discovery handoff manifest.
> This round runs by default. The user can opt out -- they will tell you. Do not ask.

## Goal

Two outputs:

1. **Per-component prop specs.** For each component designed in Round 3, produce a `view-model-props.md` next to the component's `final/` folder.
2. **Top-level manifest.** Produce `design-discovery-result.md` at the work folder root -- the single entry point for downstream skills (plan-prep, etc.).

Concerns like coverage matrices, transform function specs, testability maps, and implementation pointers are **out of scope** for design-discovery. Those belong to downstream skills.

## Step 1: Per-component view-model-props

For each component that has a `final/` folder from Round 3:

Read and follow the `view-model-props` skill, with the output target set to:

```
{component-variations-folder}/view-model-props.md
```

(Not the work folder. Co-locate with the component.)

The skill produces a document listing the component's current props, new/modified props required, and prop values per state.

Repeat for every component in scope.

## Step 2: Write the design-discovery manifest

Write `{work-folder}/design-discovery-result.md` with this exact format (~10-20 lines):

```markdown
# Design Discovery Result

**Feature:** {feature name from requirements}
**Date completed:** {date}

## Components designed
- {ComponentA} -- {absolute path to ComponentA-variations/}
- {ComponentB} -- {absolute path to ComponentB-variations/}
- {ComponentC} -- {absolute path to ComponentC-variations/}

Each component folder contains:
- `final/` -- the approved variant code
- `design-result.md` -- iteration summary, chosen variant, design decisions
- `view-model-props.md` -- component prop interfaces and prop values per state

## References
- Discovery: {absolute path to discovery.md}
- Requirements: {absolute path to requirements.md}
```

That's it. No prose, no recap. Just a tight manifest pointing at where the work lives.

## Gate

Round 4 is complete when:

1. Every component has `view-model-props.md` next to its `final/` folder
2. `design-discovery-result.md` exists at the work folder root
3. Every state discovered in Round 2 has a corresponding prop value example in some component's view-model-props.md
4. Product Manager confirms coverage
5. User signs off

After sign-off, design-discovery is complete. Downstream skills (plan-prep, etc.) read `design-discovery-result.md` as the single entry point and walk to whichever component artifacts they need.
