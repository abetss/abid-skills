# Template routing table

The decision layer for picking a layout. The skill ships a **library of purpose-built
templates** under `assets/templates/`; this table routes the content to the one whose
**presentation model** fits. These templates are a *seed* — you can use one directly, adapt
the closest match, or generate your own layout when nothing fits (see "Growing the library"
in `SKILL.md`).

The job is matching *the shape of the information* to *the shape of the page*. Markdown
flattens everything into one scrollable column. Each template trades that column for a spatial
layout that makes a specific kind of information legible: diffs become annotated side-by-sides,
processes become flowcharts, options become things you can point at. Pick by asking **"what
does the reader need to DO with this — compare, scan, navigate, feel, or edit?"** — not by
keyword-matching the topic.

> **Templates are blueprints, not finished output.** Every artifact you ship must still pass
> the skill's contract. After you pick and adapt a template, run the **"Bring a library
> template up to our rules"** checklist at the bottom and then `scripts/validate_artifact.py`.
> The seed templates use small, dense type and a placeholder palette; the contract (largish
> text, brand palette, auto dark/light, source mirror) wins.

## How to read the strengths/tradeoffs

- **Presentation strengths** = what this layout makes effortless that prose can't.
- **Tradeoffs / avoid when** = where the format fights the content, or costs more
  effort than it returns. If your content hits an "avoid when," pick a different row.

---

## Quick-scan routing table

| # | Template | One-line: it is… | Reach for it when… | Avoid when… |
|---|----------|------------------|--------------------|-------------|
| 01 | [Three code approaches](#01--three-code-approaches) | Side-by-side comparison of N solution directions, tradeoffs inline | The reader must **choose between options** and you want them compared, not sequential | There's only one real option, or options aren't comparable on shared axes |
| 02 | [Visual design directions](#02--visual-design-directions) | A handful of live-rendered layout/palette options | Showing **look-and-feel choices** the reader should react to, not imagine | The thing isn't visual; differences are behavioral not aesthetic |
| 03 | [Annotated pull request](#03--annotated-pull-request) | A diff with margin notes, severity tags, jump links | **Reviewing a concrete code change** line-by-line with commentary | No diff exists yet; you're explaining structure not changes (use 04) |
| 04 | [Module map](#04--module-map) | An unfamiliar package as boxes-and-arrows, hot path highlighted | Making **code architecture / call-graph** visible at a glance | The reader needs the literal code, not its shape |
| 05 | [Living design system](#05--living-design-system) | Tokens (color/type/spacing) rendered as copyable swatches | Documenting or reviewing a **design system / token set** | You have components to show, not tokens (use 06) |
| 06 | [Component variants](#06--component-variants) | Every size/state/intent of one component on a contact sheet | Reviewing **all variations of a single component** together | Showing many different components, or system-level tokens (use 05) |
| 07 | [Animation sandbox](#07--animation-sandbox) | One transition in isolation with duration/easing sliders | **Tuning motion** — the reader needs to *feel* and adjust timing | Static layout; nothing moves |
| 08 | [Clickable flow](#08--clickable-flow) | A few linked screens you can click through | Conveying a **multi-screen interaction / user journey** end-to-end | A single screen, or you only need to discuss one state |
| 09 | [Arrow-key slide deck](#09--arrow-key-slide-deck) | A short presentation, one section per slide, keyboard nav | **Presenting sequentially** in a meeting — a narrative with a pace | Reference material people scan non-linearly (a deck hides everything but one slide) |
| 10 | [SVG figure sheet](#10--svg-figure-sheet) | Inline vector diagrams for a post, tweakable/copyable | Producing **illustrations / figures** to lift into a document | The figure is a process with logic (use 13) or live data (use a chart) |
| 11 | [Weekly status report](#11--weekly-status-report) | Shipped/slipped + a small chart, built for a Monday skim | A **recurring status update** people should actually read | A one-off deep narrative; an incident (use 12) |
| 12 | [Incident timeline](#12--incident-timeline) | Post-mortem: minute-by-minute timeline, logs, follow-ups | Writing a **post-mortem / incident review** with a clear sequence | Routine status (use 11); no temporal sequence to show |
| 13 | [Annotated flowchart](#13--annotated-flowchart) | A process as a real flowchart, click a step for detail | Explaining a **pipeline / decision process / state machine** | Static structure with no flow (use 04); pure prose explanation |
| 14 | [Feature explainer](#14--feature-explainer) | TL;DR + collapsible steps + tabbed snippets + FAQ | Teaching **how a specific feature/system works** in this codebase | A general concept untethered to one codebase (use 15) |
| 15 | [Concept explainer](#15--concept-explainer) | A concept taught with a live interactive demo + glossary | Teaching an **abstract concept** where playing with it builds intuition | The concept has no interactive model; a feature walkthrough (use 14) |
| 16 | [Implementation plan](#16--implementation-plan) | Milestones on a timeline + data-flow + mockups + risk table | Handing off a **plan an implementer will execute** | Early exploration before a direction is chosen (use 01) |
| 17 | [PR write-up for reviewers](#17--pr-write-up-for-reviewers) | Author's case: motivation, before/after, file-by-file tour | Explaining the **"why" of a change** to orient reviewers | Line-level review annotations (use 03); the change isn't built yet |
| 18 | [Ticket triage board](#18--ticket-triage-board) | Drag tickets across Now/Next/Later/Cut, export markdown | **Prioritizing a backlog** interactively, then exporting the result | A fixed list to display read-only; nothing to sort |
| 19 | [Feature flag editor](#19--feature-flag-editor) | Grouped toggles + dependency warnings + copy-diff | **Configuring a set of flags/settings** with interdependencies | A flat list with no logic between options |
| 20 | [Prompt tuner](#20--prompt-tuner) | Editable template + live-rerendering sample outputs | **Iterating on a prompt/template** with instant feedback | One-shot text with no variables to vary |

---

## Detailed cards

Open the matching file under `assets/templates/`. Each is a complete, working,
zero-dependency `.html` page — treat it as a scaffold: keep the structure and interaction
code, swap in the user's real content, then bring it up to the contract (checklist below).

### 01 — Three code approaches
**File:** `assets/templates/01-exploration-code-approaches.html`
**It is:** Three (or N) candidate solutions laid out in parallel columns, each with its
code sketch and tradeoffs called out inline on the same row.
**When to use:** The reader is deciding *which way to build something* and you want them
to compare directions at a glance instead of holding three sequential explanations in
their head. The canonical "fan out, then point at one" exploration artifact.
**Presentation strengths:** Side-by-side forces honest comparison on shared axes; tradeoffs
sit next to the thing they describe; the reader can scan one dimension across all options.
**Tradeoffs / avoid when:** Only works when options are genuinely comparable. One dominant
option makes the columns feel like padding. Too many options (>4) breaks side-by-side — fall
back to a ranked list. Once a direction is *picked*, switch to 16 (implementation plan).

### 02 — Visual design directions
**File:** `assets/templates/02-exploration-visual-designs.html`
**It is:** A small set of layout/palette/style directions rendered live so the reader
reacts to the actual pixels.
**When to use:** Presenting **aesthetic / look-and-feel** options — landing page styles,
color directions, layout treatments — where "describe it" loses to "show it."
**Presentation strengths:** Real rendering beats description for anything visual; placing
options adjacent makes differences pop; the reader judges with their eyes, not imagination.
**Tradeoffs / avoid when:** Only pays off when the difference is *visual*. If the options
differ behaviorally or structurally, this format hides the real distinction. Each direction
costs real layout work — don't generate ten throwaways.

### 03 — Annotated pull request
**File:** `assets/templates/03-code-review-pr.html`
**It is:** A diff rendered with margin notes, severity tags (blocker/nit/question), and
jump links — the reviewer's view.
**When to use:** **Reviewing a concrete code change** and attaching commentary to specific
lines. The diff already exists; you're marking it up.
**Presentation strengths:** Comments anchor to exact lines instead of "in function X near
the top"; severity tags let the author triage; jump links beat scrolling a terminal diff.
**Tradeoffs / avoid when:** Needs a real diff. For explaining *why* a change was made at a
narrative level, use 17. For unfamiliar code with no change yet, use 04.

### 04 — Module map
**File:** `assets/templates/04-code-understanding.html`
**It is:** A package or subsystem drawn as boxes and arrows, with the hot path highlighted
and entry points listed.
**When to use:** Making the **architecture/shape** of unfamiliar code legible — what calls
what, where the important path runs, where to start reading.
**Presentation strengths:** Call graphs are inherently spatial; markdown flattens them, this
restores the 2-D structure; highlighting the hot path tells the reader where to look first.
**Tradeoffs / avoid when:** Conveys structure, not the literal code — if the reader needs the
actual lines, pair with 03. Very large graphs get hairy; scope to one subsystem.

### 05 — Living design system
**File:** `assets/templates/05-design-system.html`
**It is:** Color, type-scale, and spacing **tokens** pulled from a repo and rendered as
swatches/specimens the reader can copy from.
**When to use:** Documenting or reviewing a **design system** at the token level — the
primitives, not the components built from them.
**Presentation strengths:** A `#3B82F6` swatch communicates instantly where a hex string
doesn't; type scales shown at real size are judgeable; copy-to-clipboard closes the loop.
**Tradeoffs / avoid when:** It's about tokens. To show assembled components in their states,
use 06. Not a substitute for the actual stylesheet/Figma source of truth.

### 06 — Component variants
**File:** `assets/templates/06-component-variants.html`
**It is:** Every size, state, and intent of **one** component laid out on a single contact
sheet (default/hover/disabled × sm/md/lg × primary/secondary…).
**When to use:** Reviewing **all the variations of a single component** at once — catching
the inconsistent disabled state, the missing size.
**Presentation strengths:** The full matrix is visible together, so gaps and inconsistencies
jump out; reviewers compare states without clicking through a Storybook.
**Tradeoffs / avoid when:** One component at a time — many different components belong in a
gallery, and raw tokens belong in 05.

### 07 — Animation sandbox
**File:** `assets/templates/07-prototype-animation.html`
**It is:** A single transition/animation isolated on the page with live sliders for duration
and easing.
**When to use:** **Tuning motion.** Motion can't be described, only felt — give the reader the
real curve and let them dial it in.
**Presentation strengths:** Five seconds of the real easing beats a paragraph about it;
sliders turn "a bit snappier?" into a value you can read off and ship.
**Tradeoffs / avoid when:** Only for things that move. Static layout decisions gain nothing.
It's a tuning toy, not a place to show final polished UI.

### 08 — Clickable flow
**File:** `assets/templates/08-prototype-interaction.html`
**It is:** A handful of screens linked together with enough fidelity to click through the
whole interaction.
**When to use:** Conveying a **multi-step interaction or user journey** — onboarding, a
checkout, a wizard — where the *sequence* and *transitions* are the point.
**Presentation strengths:** Lets the reader *feel* whether the flow is right; surfaces dead
ends and awkward steps that a screenshot list hides.
**Tradeoffs / avoid when:** Overkill for a single screen or one state. Higher build cost than
static mockups — use only when the interaction itself is in question.

### 09 — Arrow-key slide deck
**File:** `assets/templates/09-slide-deck.html`
**It is:** A short presentation as one HTML file, one `<section>` per slide, left/right arrow
navigation, no build step.
**When to use:** **Presenting sequentially** — a narrative you'll walk someone through in a
meeting, one idea per slide, with deliberate pacing.
**Presentation strengths:** Enforces one-idea-per-slide discipline; arrow-key pacing controls
attention; portable and projectable with zero tooling.
**Tradeoffs / avoid when:** A deck *hides* everything but the current slide — terrible for
reference material people need to scan or search. If readers will jump around or skim, use a
scrolling report (11/14/16) instead. Don't pour dense detail onto slides.

### 10 — SVG figure sheet
**File:** `assets/templates/10-svg-illustrations.html`
**It is:** The diagrams/figures for a post drawn as inline SVG, each tweakable and copyable
on its own.
**When to use:** Producing **illustrations** to lift into a blog post, doc, or deck — vector
art the reader can hand-edit or paste out individually.
**Presentation strengths:** Inline SVG is real vector output, not a screenshot; each figure is
independently copyable; hand-editable after the fact.
**Tradeoffs / avoid when:** For a *process* with logic and clickable steps, use 13. For
data-driven charts that update, this isn't a charting tool. Bespoke art takes effort per figure.

### 11 — Weekly status report
**File:** `assets/templates/11-status-report.html`
**It is:** What shipped, what slipped, blockers, and a small chart — formatted for a fast skim.
**When to use:** A **recurring status update** (weekly/sprint) that you want people to actually
read instead of skip.
**Presentation strengths:** Structure + a little color turns a wall of bullets into something
scannable in 30 seconds; the chart carries the trend the prose would bury.
**Tradeoffs / avoid when:** Built for routine cadence and skimming, not deep narrative. For an
outage retrospective use 12; for a one-time strategy doc a deck or explainer fits better.

### 12 — Incident timeline
**File:** `assets/templates/12-incident-report.html`
**It is:** A post-mortem with a minute-by-minute timeline, log excerpts at each step, and a
follow-up checklist.
**When to use:** Writing an **incident review / post-mortem** where the *sequence of events* and
the response are central.
**Presentation strengths:** A vertical timeline makes "what happened when" unambiguous; inline
log excerpts ground each step in evidence; the checklist makes follow-ups trackable.
**Tradeoffs / avoid when:** Wants a real temporal sequence — don't force routine status into it
(use 11). Heavier structure than a quick update deserves.

### 13 — Annotated flowchart
**File:** `assets/templates/13-flowchart-diagram.html`
**It is:** A process (deploy pipeline, decision tree, state machine) drawn as a real flowchart;
clicking a step reveals what runs, timings, and failure paths.
**When to use:** Explaining a **process with branches and flow** — anything with "if this then
that," stages, or failure paths.
**Presentation strengths:** Flow and branching are spatial — boxes-and-arrows beat numbered
prose; click-to-expand keeps the overview clean while detail stays one click away.
**Tradeoffs / avoid when:** For *static* structure (who-calls-whom) use 04. A purely linear
process with no branches may not need a chart at all. (For diagrams driven from markdown
```mermaid``` blocks, see `references/depth-and-diagrams.md` + `scripts/render_diagrams.py`.)

### 14 — Feature explainer
**File:** `assets/templates/14-research-feature-explainer.html`
**It is:** A "how does X work here" explainer: TL;DR box, collapsible request-path steps,
tabbed config/code snippets, and an FAQ.
**When to use:** Teaching **how a specific feature or system works in this codebase** — rate
limiting, auth, the job queue — to someone ramping up.
**Presentation strengths:** TL;DR serves skimmers; collapsible steps let depth be opt-in; tabs
keep parallel snippets compact; the FAQ pre-answers the obvious questions.
**Tradeoffs / avoid when:** Tied to a concrete system. For a *general* concept with an
interactive model, use 15. Collapsible structure adds nothing to short content.

### 15 — Concept explainer
**File:** `assets/templates/15-research-concept-explainer.html`
**It is:** An abstract concept taught with a **live interactive demo** (e.g. a consistent-hash
ring you add/remove nodes from), a comparison table, and a hover-linked glossary.
**When to use:** Teaching an **abstract / theoretical concept** where *manipulating* it builds
intuition that prose can't.
**Presentation strengths:** Interactive models turn passive reading into "oh, I see"; the
glossary disambiguates jargon in place; comparison tables anchor the concept against neighbors.
**Tradeoffs / avoid when:** Pays off only when there's a model worth manipulating — building the
interactive demo is real work. For a codebase feature walkthrough use 14.

### 16 — Implementation plan
**File:** `assets/templates/16-implementation-plan.html`
**It is:** The plan you hand off: milestones on a timeline, a data-flow diagram, inline mockups,
the risky code called out, and a risk table.
**When to use:** A direction is **chosen** and you're handing an implementer a plan they can
actually execute — sequencing, interfaces, risks.
**Presentation strengths:** Timeline makes sequence and dependencies visible; mockups + data-flow
sit next to the milestones they belong to; the risk table forces unknowns into the open.
**Tradeoffs / avoid when:** This is post-decision. While still *exploring* directions, use 01.
Don't build the full plan artifact for a trivial one-step change.

### 17 — PR write-up for reviewers
**File:** `assets/templates/17-pr-writeup.html`
**It is:** The author's case for a change: motivation, before/after, a file-by-file tour with
the *why*, and where to focus review.
**When to use:** Orienting **reviewers (or future readers) on why a change exists** and how to
approach reviewing it — the narrative companion to the diff.
**Presentation strengths:** Before/after makes the delta concrete; the file-by-file tour routes
the reviewer's attention; "where to focus" respects their time.
**Tradeoffs / avoid when:** Explains the *why*, not line-level nits — pair with 03 for those.
The change should already exist; for a forward-looking plan use 16.

### 18 — Ticket triage board
**File:** `assets/templates/18-editor-triage-board.html`
**It is:** A throwaway editor: drag tickets across Now / Next / Later / Cut columns, then copy
the final ordering out as markdown.
**When to use:** **Prioritizing a backlog interactively** — when dragging things into buckets is
easier than describing the order in a text box — and you need the result back as text.
**Presentation strengths:** Direct manipulation beats prose for ordering; the export button
turns UI work back into committable text, keeping you in the loop.
**Tradeoffs / avoid when:** It's an *editor*, not a display — pointless for a fixed read-only
list. Always keep the export step; an editor with no way out is a dead end.

### 19 — Feature flag editor
**File:** `assets/templates/19-editor-feature-flags.html`
**It is:** Toggles grouped by area, dependency warnings when a prerequisite is off, and a
"copy diff" button for just the changed keys.
**When to use:** **Configuring a set of flags/settings with interdependencies** — where toggling
one thing should warn about another — and exporting only what changed.
**Presentation strengths:** Grouping + dependency warnings prevent invalid combinations a flat
list would allow; copy-diff exports a minimal, reviewable change.
**Tradeoffs / avoid when:** Earns its complexity only when options *interact*. A flat,
independent settings list doesn't need this; a static config is just text.

### 20 — Prompt tuner
**File:** `assets/templates/20-editor-prompt-tuner.html`
**It is:** An editable template on the left with variable slots highlighted; sample inputs on the
right that re-render live as you type.
**When to use:** **Iterating on a prompt or any variable-driven template** where you want to see
how edits play out across several real inputs at once.
**Presentation strengths:** Live re-render tightens the edit→see-result loop; multiple sample
inputs catch a change that helps one case and breaks another; highlighted slots make structure clear.
**Tradeoffs / avoid when:** Needs variables and sample inputs to be worth it. One-shot static
text with nothing to parameterize gains nothing from the machinery.

---

## Bring a library template up to our rules

The seed templates are blueprints, not finished output. After you copy one and swap in real
content, apply these before validating (full detail in `references/design-rules.md`):

- [ ] **Reskin to the brand palette.** Replace the template's `:root` (and the dark
      `@media (prefers-color-scheme: dark)` `:root`) token *values* with the brand palette
      from `brand.md` — keep the token *names* and every `var()` reference. The seed accents
      are already swapped to brand green; verify nothing reads as the old placeholder palette,
      and that any chart/swatch colors stay high-contrast in both themes.
- [ ] **Keep the surface model: the page is never pure white.** Body/page background is
      off-white (`#f7f7f5` light / `#14171a` dark); cards/panels are white (`#ffffff` /
      `#1d2126`) with a visible border (`#d9d8d4` / `#2c323a`) so they lift off the page.
      Never set the body and cards to the same color — see "The surface model" in
      `references/design-rules.md`.
- [ ] **Largish text.** Raise content fonts to the type scale: body ≥ 18px, secondary ≥ 16px,
      UI chrome (badges/labels) ≥ 14px. The seed templates run dense (10–15px) — bump them.
- [ ] **No gray text.** Swap any mid-gray text for a darker ink that meets contrast.
- [ ] **Auto dark/light only.** Templates already use `@media (prefers-color-scheme: dark)`
      and no toggle — keep it that way. Do not add a toggle or `[data-theme]`.
- [ ] **Add the source mirror.** Inject `<script type="text/markdown" id="artifact-source">`
      with the artifact's content as markdown (the seed templates lack it).
- [ ] **Validate.** `python scripts/validate_artifact.py <file.html>` → fix every ERROR.
      Accessibility items (skip link, landmarks) are warnings — add them if cheap, but they
      don't block.

---

## When nothing fits — go bespoke

These templates cover common shapes, not every shape. If the content genuinely doesn't match a row:

- **Combine.** Many real artifacts borrow from two — e.g. an implementation plan (16) that
  embeds a flowchart (13), or a feature explainer (14) with a concept demo (15). Start from the
  closest template and graft the second pattern in.
- **Generalize the closest match.** A "vendor comparison" isn't listed, but it's structurally
  template 01 (options side-by-side). A "roadmap" is template 16's timeline without the code.
- **Build bespoke.** When the content is long-form/linear or no spatial layout adds anything,
  generate from `assets/template.html` (the generic sidebar-TOC document scaffold) following
  `references/design-rules.md` and `references/navigation-patterns.md`. This is the original
  generating-html-artifacts path and is the right default for captured findings / reports.
- **Grow the library.** If you invent a layout worth reusing, save it as a candidate template —
  see "Growing the library" in `SKILL.md`.

Name the choice and the runner-up in one line before building, so the user can redirect early
if you guessed wrong.

---

*Seed templates adapted from the MIT-licensed `anthropics/html-effectiveness` template set;
palette and type re-themed to this skill's brand and design rules.*
