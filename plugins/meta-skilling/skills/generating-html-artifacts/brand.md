# Saved brand / theme

Read this every run and apply it. Update it when the user gives brand feedback ("use blue", "I prefer a serif", "make it denser"). This is the persisted theme — distinct from `memory.md`, which holds how-to-build lessons.

## Accent

Tokens use **semantic** names (see `references/design-rules.md`), not color names.

- `--primary` (brand action color): `#1c6b46` light / `#5bbd8a` dark · `--primary-foreground`: `#ffffff` light / `#06210f` dark
- `--accent` (soft tinted surface): `#e6f1ec` light / `#16352a` dark · `--accent-foreground`: `#10472d` light / `#9fe3c0` dark

## Code & inverse surfaces

Code blocks **follow the theme** (not fixed-dark). See `references/design-rules.md` for the full rule.

- `--code-bg`: `#edece4` light / `#16191d` dark · `--code-fg`: `#1a1d21` light / `#f2f3f4` dark
- syntax: `--code-comment` `#5b6168`/`#9aa0a8` · `--code-keyword` `#9c3a2c`/`#7fd0a3` · `--code-string` `#155e3b`/`#c9d99a` · `--code-number` `#7a4f00`/`#e0b083` · `--code-fn` `#6f42c1`/`#c9b98a`
- `--inverse`: `#16191d` · `--inverse-foreground`: `#f2f3f4` — fixed dark in both themes, for dark buttons / inverted slides only.

## Fonts

- Stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Helvetica, Arial, sans-serif`
- No external/CDN fonts (artifacts must be self-contained and offline-capable).

## Shape & density

- Corner radius: `14px`
- Density: spacious (generous section gaps, ~65–75ch measure)

## Notes

- Default brand established 2026-06-22 from the existing `subjects.html` aesthetic (system-font, deep-green accent, 14px radius).
