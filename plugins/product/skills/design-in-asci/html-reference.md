# HTML Mockup Reference

## Tailwind CDN + oklch — The Gotcha

**Tailwind CDN v3 CANNOT resolve oklch/var() colors with opacity modifiers.**

These will NOT work when configured via `tailwindcss.config`:
- `bg-primary/30` — opacity modifier on oklch value
- `text-muted-foreground` — var() color
- `bg-card` — var() color

### Solution: Define CSS utility classes manually in `<style>`

Tailwind CDN is only used for **layout utilities** (flex, gap, p-3, font-bold, w-[180px], etc.). All theme colors, border-colors, and border-radii must be defined as plain CSS classes.

```html
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {
    /* Copy ALL variables from apps/home/core/style/globals.css :root block */
    --radius: 0.625rem;
    --primary: oklch(0.85 0.12 145);
    --primary-foreground: oklch(0.15 0 0);
    --secondary: oklch(0.88 0.08 65);
    --secondary-foreground: oklch(0.15 0 0);
    --background: oklch(0.985 0.008 85);
    --card: oklch(0.99 0.005 85);
    --foreground: oklch(0.15 0 0);
    --card-foreground: oklch(0.15 0 0);
    --muted: oklch(0.92 0.04 65);
    --muted-foreground: oklch(0.35 0 0);
    --accent: oklch(0.9 0.06 145);
    --accent-foreground: oklch(0.15 0 0);
    --border: oklch(0.88 0.03 145);
    --success: oklch(0.72 0.15 145);
    --success-foreground: oklch(0.15 0 0);
    --destructive: oklch(0.65 0.25 27);
    /* Add feature-specific vars as needed */
  }

  /* Theme utility classes — one per bg/text/border you use */
  .bg-background { background-color: var(--background); }
  .bg-card { background-color: var(--card); }
  .bg-muted { background-color: var(--muted); }
  .text-foreground { color: var(--foreground); }
  .text-card-foreground { color: var(--card-foreground); }
  .text-muted-foreground { color: var(--muted-foreground); }
  .text-success { color: var(--success); }
  .border-border { border-color: var(--border); }

  /* Custom radii (project uses --radius, not Tailwind defaults) */
  .rounded-lg { border-radius: var(--radius); }
  .rounded-md { border-radius: calc(var(--radius) - 2px); }
  .rounded-sm { border-radius: calc(var(--radius) - 4px); }

  /* Opacity variants — use raw oklch with alpha, NOT var() */
  .bg-muted\/30 { background-color: oklch(0.92 0.04 65 / 0.3); }
  .bg-success\/20 { background-color: oklch(0.72 0.15 145 / 0.2); }
</style>
```

### Rules

1. **Extract ALL** CSS variables from `apps/home/core/style/globals.css` `:root` block
2. **Define a CSS class** for every `bg-*`, `text-*`, `border-*` color you use in HTML
3. **Opacity variants** (`color/30`): use raw oklch with alpha — `oklch(L C H / alpha)` — NOT `var()` with Tailwind's `/opacity` modifier
4. **Standard Tailwind utilities** work fine from CDN: flex, gap, p-3, font-bold, w-[180px], text-sm, etc.
5. **`rounded-lg/md/sm`** must be overridden — project uses custom `--radius`
6. **DO NOT use `tailwindcss.config`** for colors — it won't work with oklch/var()

## HTML Template

Each file shows all 3 viewports stacked: **desktop → mobile → tablet**.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[TICKET] — [Screen Name]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root { /* ... extracted vars ... */ }
    /* ... utility class overrides ... */
    .viewport-label {
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted-foreground);
      margin-bottom: 0.5rem;
    }
    .viewport-frame {
      border: 1px dashed var(--border);
      border-radius: var(--radius);
      padding: 1rem;
      margin-bottom: 3rem;
    }
  </style>
</head>
<body class="bg-background text-foreground p-8 font-sans">

  <h1 class="text-xl font-bold mb-1">[TICKET] — [Screen Name]</h1>
  <p class="text-muted-foreground mb-8">[Brief description]</p>

  <!-- ===== DESKTOP (880px) ===== -->
  <div class="viewport-label">Desktop (880px)</div>
  <div class="viewport-frame" style="max-width: 880px;">

    <!-- CURRENT STATE -->
    <section class="mb-8">
      <h2 class="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">
        Current
      </h2>
      <!-- component at desktop width -->
    </section>

    <hr class="border-border mb-8">

    <!-- PROPOSED -->
    <section class="mb-8">
      <h2 class="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-1">
        [Scenario Name]
      </h2>
      <p class="text-sm text-muted-foreground mb-6">[What changed]</p>
      <!-- component mockup -->
    </section>

  </div>

  <!-- ===== MOBILE (343px) ===== -->
  <div class="viewport-label">Mobile (343px)</div>
  <div class="viewport-frame" style="max-width: 343px;">
    <!-- Same sections, adapted for mobile width -->
  </div>

  <!-- ===== TABLET (624px) ===== -->
  <div class="viewport-label">Tablet (624px)</div>
  <div class="viewport-frame" style="max-width: 624px;">
    <!-- Same sections, adapted for tablet width -->
  </div>

</body>
</html>
```

## Process (HTML-specific)

1. Read `apps/home/core/style/globals.css` — extract `:root` CSS variables
2. Read existing component code — understand current markup structure
3. Identify feature-specific colors — add to `:root` and create utility classes
4. Build "Current State" section first — baseline for comparison
5. Build proposed variations with labeled scenarios
6. Group related states (e.g., "Holiday split", "Period split", "Both splits")
