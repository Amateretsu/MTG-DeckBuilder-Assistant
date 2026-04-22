---
name: mtg-visualization
description: Produces an interactive deck analysis dashboard for a Magic The Gathering deck using Chart.js. Use this skill whenever the user asks to analyze, visualize, or see a breakdown of a deck — including requests like "analyze this deck", "show me the curve", "give me a deck breakdown", "visualize the mana base", or "show deck stats". Also use it when a completed deck is presented and the user hasn't explicitly said they only want the export.
---

# MTG Deck Analysis Visualization

Produces an interactive HTML dashboard via `visualize:show_widget` using Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).

## Common Settings

Detect dark mode via `matchMedia`; derive `textColor` and `gridColor` accordingly. All charts: `responsive: true`, `maintainAspectRatio: false`, `legend: false`, bars with `borderRadius: 4`, `borderSkipped: false`. Use CSS variables (`--color-background-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-border-tertiary`, `--border-radius-md`, `--border-radius-lg`) throughout. Include `<h2 class="sr-only">` and `role="img"` + `aria-label` on every `<canvas>`.

**Color palette:** Creatures `#534AB7` · Artifacts `#1D9E75` · Sorceries `#D85A30` · Instants `#378ADD` · Planeswalkers `#D4537E` · Enchantments `#888780`

## 1. Summary Stat Cards

4-column CSS grid, `--color-background-secondary` background, 24px number / 13px label:
**Cards** (total) · **Avg mana value** (non-land, 1 decimal) · **Lands** · **Ramp sources** (non-land acceleration)

## 2. Mana Curve Bar Chart

Vertical bar, `barPercentage: 0.7`. X-axis MV 0–13+. Bars MV 7+ in `#534AB7`, below in `#1D9E75`. If the commander has a mechanic with a relevant MV threshold (e.g. cascade), add an `afterLabel` tooltip noting it. Title: "Mana curve (N non-land cards)".

## 3. Card Types Doughnut

`cutout: '55%'`, no built-in legend. Custom flex-wrapped legend with color swatches. Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments, Battles/Other if present.

## 4. Functional Roles Horizontal Bar

`indexAxis: 'y'`, `barPercentage: 0.6`, categories in descending count order drawn from the deck's actual MTG-Card-Function-Tags.md top-level categories.

## 5. Commander Mechanic Panel

Rounded panel summarizing the commander's core engine, key enablers, and 3 notable synergy targets. Adapt entirely to the actual commander — no generic text.

## 6. Land Base Breakdown

4-column grid (same styling as stat cards): **Ramp lands** · **Utility lands** · **Interaction lands** · **Basic lands**.

## 7. Action Buttons

3 buttons via `sendPrompt()`:
- `"Export this [Commander] deck as a downloadable .txt file"`
- `"Suggest budget alternatives for the most expensive cards in this deck"`
- `"What are the best opening hands and mulligan strategy for this deck?"`
