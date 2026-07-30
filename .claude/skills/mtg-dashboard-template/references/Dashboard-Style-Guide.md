# MTG Dashboard Style Guide

Canonical visual system for `mtg-visualization` and `mtg-budget-swaps`. Read this instead of hardcoding colors/CSS in either skill.

## Card-type color palette

Used for card-type breakdowns (doughnut charts, curve bars, legends):

| Type | Color |
|---|---|
| Creatures | `#534AB7` |
| Artifacts | `#1D9E75` |
| Sorceries | `#D85A30` |
| Instants | `#378ADD` |
| Planeswalkers | `#D4537E` |
| Enchantments | `#888780` |
| Battles / Other | `#B08D57` |

The 7th slot (Battles/Other) exists because `mtg-visualization`'s card-type doughnut references this category when present in a deck but previously had no assigned color — always include it in any legend/chart that enumerates card types, even if it's rare in a given decklist.

## Semantic palette (status/value colors)

Used for anything communicating "good/bad/neutral" rather than a card type — e.g. `mtg-budget-swaps`'s cost/savings display:

| Meaning | Color | Typical use |
|---|---|---|
| Cost / negative | `#D85A30` (red-orange) | Current price of an expensive card being swapped out |
| Savings / positive | `#1D9E75` (green) | Savings badge, total-savings summary line |
| Info / action | `#378ADD` (blue) | "Swap:" line, action-button accents |

Reuses colors already present in the card-type palette (Sorceries' red-orange, Artifacts' green, Instants' blue) rather than inventing a second unrelated set — keeps the whole dashboard visually coherent even when a card-type chart and a cost/savings badge appear side by side.

## Dark-mode detection

```js
const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
```

Derive `textColor` and `gridColor` from this before building any chart. Use these CSS variables throughout rather than hardcoded hex values for anything that isn't one of the two palettes above:

- `--color-background-secondary`
- `--color-text-primary`
- `--color-text-secondary`
- `--color-border-tertiary`
- `--border-radius-md`
- `--border-radius-lg`

## Chart.js option defaults

Apply to every chart unless a specific chart type has a documented reason to deviate:

```js
{
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }, // build a custom flex-wrapped legend instead
}
```

Bar charts additionally: `borderRadius: 4`, `borderSkipped: false`, `barPercentage: 0.6–0.7` (0.7 for a single-series curve chart, 0.6 for a denser horizontal breakdown).

## Stat-card grid

The 4-column stat-card pattern used by `mtg-visualization`'s Summary Stat Cards and Land Base Breakdown, and by `mtg-budget-swaps`'s header (total cost / total savings):

```css
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 12px;
/* each cell: */
background: var(--color-background-secondary);
border-radius: var(--border-radius-md);
padding: 16px;
/* number: 24px, label: 13px, var(--color-text-secondary) */
```

Use fewer than 4 columns only when there are genuinely fewer than 4 stats to show (don't pad with filler cards) — collapse the grid's column count to match, don't leave empty cells.

## Badge component

For a right-aligned value badge (e.g. `mtg-budget-swaps`'s per-swap savings badge):

```css
display: inline-block;
padding: 2px 8px;
border-radius: 999px; /* pill shape */
font-size: 13px;
font-weight: 600;
/* background: semantic color at ~15% opacity, text: full-opacity semantic color */
```

Use the semantic palette above for the badge's color — green for savings, red-orange for cost, blue for neutral/info badges.

## Accessibility conventions

- Every `<canvas>`: `role="img"` + `aria-label` describing what the chart shows (not just "chart").
- Precede each chart section with an `<h2 class="sr-only">` naming the section, even when a visible title already exists nearby — screen readers need the heading in the accessibility tree.
- Action buttons (`sendPrompt()` triggers): must have a visible focus state (outline or ring) — don't rely on `:hover` alone since keyboard navigation doesn't trigger it.
- Badge and stat-card text must meet standard contrast minimums against their background at both the ~15%-opacity badge background and the full-opacity semantic color used for badge text — check this when picking opacity, don't assume 15% is always safe against every background token.
