# Infra notes — July

**Status:** fixture for the generating-html-artifacts evals · deliberately borderline blocks

Short notes from July. Each block below sits near the boundary between two
components — pick the one that fits the block's shape, not its topic.

## How the migration actually went

First we shipped the schema migration behind a flag. Then we enabled dual-write
at 10% and watched error rates for a day. After that we backfilled historical
rows in batches. Finally we cut reads over and dropped the old store a week
later. No timestamps worth showing — it's the sequence that matters.

## Three hosting options, judged on their own terms

- **Fly.io** — great if you want managed anycast and don't want to think about
  regions; the draw is operational simplicity, full stop.
- **Hetzner + Caddy** — the appeal is price: an order of magnitude cheaper, and
  we keep full control. The cost is that we own every failure.
- **Render** — the reason to pick it is team familiarity; two of us have run
  production there before. Nothing else distinguishes it.

There are no shared axes here — each option wins for a different reason.

## This week's numbers

PRs merged 14 · deploys 6 · incidents 1 · pass rate 99.1% · p95 235 ms ·
p99 410 ms · cache hit rate 94% · error budget remaining 61%.

## One thing you must not miss

A full cache flush during peak traffic can stampede the database for 30–60 s.
Use the per-key invalidation endpoint during business hours. This needs to be
visible on first read, not hidden behind a click.
