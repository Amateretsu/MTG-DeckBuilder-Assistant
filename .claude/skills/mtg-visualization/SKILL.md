---
name: mtg-visualization
description: Produces an interactive deck analysis dashboard for a Magic The Gathering deck (any format — 60-card constructed, Commander, Brawl, Oathbreaker, etc.) using Chart.js. Use this skill whenever the user asks to analyze, visualize, or see a breakdown of a deck — including requests like "analyze this deck", "show me the curve", "give me a deck breakdown", "visualize the mana base", or "show deck stats". Also use it when a completed deck is presented and the user hasn't explicitly said they only want the export.
compatibility: Uses mtg-dashboard-template for color palette, Chart.js defaults, stat-card CSS, and accessibility conventions (Common Settings) — don't re-inline a separate copy. Uses mtg-format-rules to pick the format-family branch in sections 5-6, instead of a hardcoded Commander-vs-60-card binary. Uses mtg-card-taxonomy for the Functional Roles chart (section 4). Works without any — see fallback notes — more consistent with all installed.
---

# MTG Deck Analysis Visualization

Produces an interactive dashboard using Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).

**Rendering:** prefer `visualize:show_widget` when that tool is available — it's the intended path for an inline, interactive dashboard and needs no file cleanup. Fall back to a saved HTML file (via `create_file`, presented with `present_files`) only if `visualize:show_widget` isn't in your toolset for this session, or the user specifically wants a file they can keep/reopen outside the conversation. Don't default to the file path just because it's the more familiar tool call — check what's actually available first.

**Format branches everything in sections 5 and 6 below** — determine the format family via `mtg-format-rules` (singleton/commander-slot formats — Commander, Brawl, Historic Brawl, Oathbreaker, Peasant Commander — vs. copy-limit formats — Standard, Pioneer, Modern, Legacy, Vintage, Pauper) before building those two sections. Never assume "Commander" just because a deck has a commander slot — **Brawl decks are 60-card**, which matters for land-base framing in section 6. See `mtg-deckbuilding` if the deck itself isn't finalized yet.

## Common Settings

Use `mtg-dashboard-template`'s style guide for dark-mode detection, CSS variables, Chart.js option defaults, the card-type color palette (including the Battles/Other slot), and accessibility conventions (`sr-only` headings, `role="img"`/`aria-label`) — don't re-inline a separate copy here. **If `mtg-dashboard-template` isn't installed**, fall back to: `matchMedia`-based dark-mode detection with `textColor`/`gridColor` derived from it; `responsive: true`, `maintainAspectRatio: false`, `legend: false`; bars with `borderRadius: 4`, `borderSkipped: false`; and a card-type palette of Creatures `#534AB7` · Artifacts `#1D9E75` · Sorceries `#D85A30` · Instants `#378ADD` · Planeswalkers `#D4537E` · Enchantments `#888780` · Battles/Other `#B08D57` — and mention that installing `mtg-dashboard-template` would keep this consistent with `mtg-budget-swaps`'s styling.

## 1. Summary Stat Cards

4-column CSS grid, `--color-background-secondary` background, 24px number / 13px label:
**Cards** (total) · **Avg mana value** (non-land, 1 decimal) · **Lands** · **Ramp sources** (non-land acceleration)

## 2. Mana Curve Bar Chart

Vertical bar, `barPercentage: 0.7`. X-axis MV 0–13+. Bars MV 7+ in `#534AB7`, below in `#1D9E75`. If the commander has a mechanic with a relevant MV threshold (e.g. cascade), add an `afterLabel` tooltip noting it. Title: "Mana curve (N non-land cards)".

## 3. Card Types Doughnut

`cutout: '55%'`, no built-in legend. Custom flex-wrapped legend with color swatches. Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments, Battles/Other if present.

## 4. Functional Roles Horizontal Bar

`indexAxis: 'y'`, `barPercentage: 0.6`, categories in descending count order. Pull the taxonomy from `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` — use whichever of the 12 top-level categories actually appear in this deck (most decks only touch 4-6 of them; don't force every category to show up). Every nonland card should land in exactly one bucket for this chart even if it could arguably tag two ways elsewhere — pick its primary role so the bars sum to the nonland card count. **If that file isn't found**, improvise reasonable functional categories yourself (the chart still works, just without the shared vocabulary) and note in your reply that installing `mtg-card-taxonomy` would keep categories consistent with your other MTG skills.

## 5. Archetype Panel — branches by format family

**Commander-slot formats (Commander, Historic Brawl, Peasant Commander — 100-card):** "Commander Mechanic Panel" — rounded panel summarizing the commander's core engine, key enablers, and 3 notable synergy targets. Adapt entirely to the actual commander — no generic text. Pull real synergy signal from `mtg-edhrec` when available rather than relying purely on judgment.

**Brawl and Oathbreaker (60-card, still commander/oathbreaker-anchored):** same "Commander Mechanic Panel" shape as above (there's still a single card, or card pair for Oathbreaker, to anchor it), but land-base framing in section 6 follows the 60-card branch, not the 100-card one — don't let the commander slot pull this into the wrong land-base bucket.

**Copy-limit formats (Standard, Pioneer, Modern, Legacy, Vintage, Pauper):** "Deck Identity & Key Synergies" panel instead — a short tag line naming the archetype (e.g. "Boros Aggro → Angels top-end → Equipment Voltron"), 2-3 sentences on the actual gameplan, then "Core enablers" and "Notable synergy targets" lists specific to this decklist. Same spirit as the commander panel — no generic filler — just without a single anchor card.

## 6. Land Base Breakdown — branches by format family

4-column grid (same styling as stat cards).

**100-card Commander-slot formats (Commander, Historic Brawl, Peasant Commander):** **Ramp lands** · **Utility lands** · **Interaction lands** · **Basic lands**

**60-card formats, including Brawl and Oathbreaker** (copy-limit or singleton, all share the same land-base framing at this size): **Basic lands** · **Fixing lands** (duals/gates/shocks — anything primarily there for color fixing) · **Utility/manlands** (creature lands, sac lands, cycling lands, anything with a nonbasic ability beyond fixing) · **Interaction lands** (0 is a normal answer for most decks at this size — don't force a nonzero number)

## 7. Action Buttons

3 buttons via `sendPrompt()`. Adapt to what's actually true of this deck rather than using the same three by default:
- Always include: `"Export this deck as a downloadable .txt file"` (name it after the commander for Commander decks, the archetype for constructed)
- `"Suggest budget alternatives for the most expensive cards in this deck"` — **only** if this deck is being priced for purchase. Skip it (swap in something else, e.g. mulligan guide or a sideboard/upgrade-from-collection prompt) if the deck was built from cards the user already owns — budget swaps don't make sense for "here's what I have."
- `"What are the best opening hands and mulligan strategy for this deck?"`
