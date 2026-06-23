# Design Workflow

For UI components and pages, from rough requirements to handoff.

Entry point: `design-discovery` (full process) **or** `design-iterate` (skip
discovery, go straight to variants).

## Happy Path — full design discovery first

```
┌─────────────────────────┐
│    design-discovery     │
└────────────┬────────────┘
             │   (Round 3: Design → invokes design-iterate)
             ▼
┌─────────────────────────┐
│     design-iterate      │
└────────────┬────────────┘
             │
             ├──► ┌─────────────────────────┐
             │    │     design-in-asci      │
             │    └─────────────────────────┘
             │
             └──► ┌─────────────────────────┐
                  │   design-in-storybook   │
                  └─────────────────────────┘
                              │
                              ▼
                   (return to design-iterate;
                    loop until user approves)
                              │
                              ▼
                  (return to design-discovery
                    Round 4: Specify)
                              │
                              ▼
┌─────────────────────────┐
│    view-model-props     │
└─────────────────────────┘
```

## Happy Path — straight to iteration (skip discovery)

```
┌─────────────────────────┐
│     design-iterate      │
└────────────┬────────────┘
             │
             ├──► ┌─────────────────────────┐
             │    │     design-in-asci      │
             │    └─────────────────────────┘
             │
             └──► ┌─────────────────────────┐
                  │   design-in-storybook   │
                  └─────────────────────────┘
```

## Choosing the medium

```
  design-in-asci         →  fast wireframes; structure & layout
                            still being debated; cheap to throw away
  design-in-storybook    →  real components in the browser with
                            theme, tokens, states; closer to production
```

## Inside `design-iterate` (the iteration loop)

```
┌─────────────────────────┐
│     design-iterate      │
└────────────┬────────────┘
             │
             ├──► plan variants
             ├──► dispatch rendering layer (asci or storybook)
             ├──► team internal review (Product + Designer)
             ├──► hand off to user
             ├──► capture user feedback
             │
             │   feedback?
             │     │
             │     ├── yes ──► next iteration ─── (loop back to plan)
             │     │
             │     └── no  ──► finalize
             │
             └──► write design-result.md
```

## Alternate Paths

### Quick architecture sketch (not a UI variant)

```
┌─────────────────────────┐
│   excalidraw-diagram    │
└─────────────────────────┘
```

### Component prop interfaces only (post-design handoff)

```
┌─────────────────────────┐
│    view-model-props     │
└─────────────────────────┘
```
