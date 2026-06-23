# Document Knowledge Base Workflow

`document-kb` is a router. It picks one of four writer skills based on
the prefix or keywords in your input.

## Happy Path

```
┌────────────────────────┐
│      document-kb       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│         router         │
└───────────┬────────────┘
            │
            ├──► ┌────────────────────────┐
            │    │   conventions-writer   │
            │    └────────────────────────┘
            │
            ├──► ┌────────────────────────┐
            │    │       sop-writer       │
            │    └────────────────────────┘
            │
            ├──► ┌────────────────────────┐
            │    │ troubleshooting-writer │
            │    └────────────────────────┘
            │
            └──► ┌────────────────────────┐
                 │  product-guide-writer  │
                 └────────────────────────┘
```

## What each writer is for

```
┌────────────────────────┐
│   conventions-writer   │  →  "How should code look?"
└────────────────────────┘
┌────────────────────────┐
│       sop-writer       │  →  "What steps do I take?"
└────────────────────────┘
┌────────────────────────┐
│ troubleshooting-writer │  →  "How do I fix this error?"
└────────────────────────┘
┌────────────────────────┐
│  product-guide-writer  │  →  "What does this feature do?"
└────────────────────────┘
```

## Prefix shortcuts (forces the route)

```
  conv:    →  conventions-writer
  sop:     →  sop-writer
  ts:      →  troubleshooting-writer
  pg:      →  product-guide-writer
```

## Keyword heuristics (when no prefix given)

```
  "convention"  "pattern"  "style"  "rule"      →  conventions-writer
  "how to"      "steps"    "procedure"          →  sop-writer
  "error"       "fail"     "broken"  "fix"      →  troubleshooting-writer
  "feature"     "behavior" "page"    "UI"       →  product-guide-writer
```

## Direct skill access (skip the router)

```
┌────────────────────────┐
│   conventions-writer   │   ← invoke directly
└────────────────────────┘
┌────────────────────────┐
│       sop-writer       │   ← invoke directly
└────────────────────────┘
┌────────────────────────┐
│ troubleshooting-writer │   ← invoke directly
└────────────────────────┘
┌────────────────────────┐
│  product-guide-writer  │   ← invoke directly
└────────────────────────┘
```
