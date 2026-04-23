---
name: mtg-visualization
description: Interactive MTG deck analysis dashboard using Chart.js. Use for deck analysis, visualization, mana curve, or breakdown requests. Also use when a completed deck is presented unless the user only wants the export.
---

# MTG Deck Analysis Visualization

Produces an interactive HTML dashboard via `visualize:show_widget` using Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).

## Common Settings

- Dark mode: detect via `matchMedia`; derive `textColor` and `gridColor`
- All charts: `responsive: true`, `maintainAspectRatio: false`, no built-in legend
- Bars: `borderRadius: 4`, `borderSkipped: false`
- CSS vars: `--color-background-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-border-tertiary`, `--border-radius-md`, `--border-radius-lg`
- Accessibility: `<h2 class="sr-only">` + `role="img"` and `aria-label` on every `<canvas>`

**Color palette:** Creatures `#534AB7` · Artifacts `#1D9E75` · Sorceries `#D85A30` · Instants `#378ADD` · Planeswalkers `#D4537E` · Enchantments `#888780`

## 1. Summary Stat Cards

4-column CSS grid, `--color-background-secondary` background, 24px number / 13px label:
**Cards** (total) · **Avg mana value** (non-land, 1 decimal) · **Lands** · **Ramp sources** (non-land acceleration)

## 2. Mana Curve Bar Chart

Vertical bar, `barPercentage: 0.7`. X-axis MV 0–13+. Bars MV 7+ in `#534AB7`, below in `#1D9E75`. If the commander has a mechanic with a relevant MV threshold (e.g. cascade), add an `afterLabel` tooltip noting it. Title: "Mana curve (N non-land cards)".

## 3. Card Types Doughnut

`cutout: '55%'`, no built-in legend. Custom flex-wrapped legend with color swatches. Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments, Battles/Other if present.

## 4. Functional Roles Horizontal Bar

`indexAxis: 'y'`, `barPercentage: 0.6`, categories in descending count order drawn from the deck's actual tags. Use these 12 top-level tag names exactly:

`Card Advantage` · `Removal` · `Countermagic` · `Mana` · `Recursion` · `Tutors` · `Win Conditions` · `Creatures` · `Synergy` · `Enchantments` · `Resource Denial` · `Utility`

## 5. Commander Mechanic Panel

Rounded panel. Format: commander name as heading, core engine in 2–3 sentences, enablers as an inline list, each of 3 notable synergy targets with a one-sentence note. Adapt entirely to the actual commander — no generic text.

## 6. Land Base Breakdown

4-column grid (same styling as stat cards): **Ramp lands** · **Utility lands** · **Interaction lands** · **Basic lands**.

## 7. Action Buttons

3 buttons via `sendPrompt()`:
- `"Export this [Commander] deck as a .txt file and write the Moxfield primer"`
- `"Suggest budget alternatives for the most expensive cards in this deck"`
- `"What are the best opening hands and mulligan strategy for this deck?"`
