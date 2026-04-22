# MTG Deckbuilder — Output Instructions

Always produce two files: the **Decklist Export** (`.txt`) and the **Deck Primer** (`.md`). Save all output files to `/mnt/user-data/outputs/`. Call `present_files` after saving each file.

The **Deck Analysis Visualization** and **Budget Swap Guide** are optional extras.

---

## 1. Deck Analysis Visualization

Produce an interactive dashboard via `visualize:show_widget` (HTML + Chart.js `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).

Detect dark mode via `matchMedia`; derive `textColor` and `gridColor` accordingly. All charts: `responsive: true`, `maintainAspectRatio: false`, `legend: false`, bars with `borderRadius: 4`, `borderSkipped: false`. Use CSS variables (`--color-background-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-border-tertiary`, `--border-radius-md`, `--border-radius-lg`) throughout. Include `<h2 class="sr-only">` and `role="img"` + `aria-label` on every `<canvas>`.

Color palette: Creatures `#534AB7` · Artifacts `#1D9E75` · Sorceries `#D85A30` · Instants `#378ADD` · Planeswalkers `#D4537E` · Enchantments `#888780`

### 1.1 Summary Stat Cards

4-column CSS grid, `--color-background-secondary` background: **Cards** (total) · **Avg mana value** (non-land, 1 decimal) · **Lands** · **Ramp sources** (non-land acceleration).

### 1.2 Mana Curve Bar Chart

Vertical bar, `barPercentage: 0.7`. X-axis MV 0–13+. Bars MV 7+ in `#534AB7`, below in `#1D9E75`. If the commander has a mechanic with a relevant MV threshold (e.g. cascade), add an `afterLabel` tooltip noting it. Title: "Mana curve (N non-land cards)".

### 1.3 Card Types Doughnut

`cutout: '55%'`, no built-in legend. Custom flex-wrapped legend with color swatches. Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments, Battles/Other if present.

### 1.4 Functional Roles Horizontal Bar

`indexAxis: 'y'`, `barPercentage: 0.6`, categories in descending count order drawn from the deck's actual MTG-Card-Function-Tags.md top-level categories.

### 1.5 Commander Mechanic Panel

Rounded panel summarizing the commander's core engine, key enablers, and 3 notable synergy targets. Adapt entirely to the actual commander — no generic text.

### 1.6 Land Base Breakdown

4-column grid (same styling as 1.1): **Ramp lands** · **Utility lands** · **Interaction lands** · **Basic lands**.

### 1.7 Action Buttons

3 buttons via `sendPrompt()`:
- `"Export this [Commander] deck as a downloadable .txt file"`
- `"Suggest budget alternatives for the most expensive cards in this deck"`
- `"What are the best opening hands and mulligan strategy for this deck?"`

---

## 2. Budget Swap Guide

Identify the 9–12 most expensive cards by `prices.usd`. For each, find a verified budget replacement with matching functional tag(s) and legal color identity.

Present as card-style panels: **name** + price (red) + savings badge (green). Swap line in blue: "**Swap:** [Name] (~$X)" + brief explanation of tradeoffs.

End with a **"Keep These"** list of affordable core cards and a summary line: *"Total savings: ~$X,XXX — deck drops from ~$X,XXX to ~$XXX while keeping [strategy] intact."*

Include a `sendPrompt()` button to generate the updated budget decklist.

---

## 3. Decklist Export

**Filename:** `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt`

**Line format** (one card per line, no headers, no blank lines):
```
1 Esper Sentinel (MH2) 328 #!Card Advantage & Selection
1 Sol Ring (C21) 263 #!Mana & Tempo
1 Swords to Plowshares (SLD) 182 #!Removal & Interaction
1 Thassa's Oracle (THB) 73 #!Win Conditions & Threats #!Synergy & Tribal
1 Ancient Tomb (2X2) 322
```

**Tagging:** Use the 12 top-level category names from MTG-Card-Function-Tags.md as `#!Tag` values. Only tag cards where it adds meaningful information — skip basic lands and generic filler. Multiple tags are space-separated. Drop to a sub-tag only when the top-level category would be ambiguous.

**Rules:** Plain ASCII. Card names must match Scryfall `name` exactly. Set code (uppercased) and collector number from Scryfall `set` and `collector_number`. Commander listed first. All quantities `1`.

---

## 4. Deck Primer

**Filename:** `{Commander_Name}_{Tribe_or_Archetype}_{Format}_Primer.md`

Moxfield primers use standard Markdown. Supported: headings, `**bold**`, `*italic*`, `~~strikethrough~~`, lists, tables, `---`, inline links, inline images. Card image links: `[[Card Name]]` or `[[Card Name|SET]]`. Collapsible sections: `===accordion` / `===panel: Title` / `===endpanel` / `===endaccordion`. Not supported: code blocks, blockquotes, TeX, header anchors. Inline HTML allowed; no `<style>` or `<script>`.

Adapt all content to the specific commander and deck — no placeholder text. Structure:

1. **Title & tagline** — `# [Commander] — [Theme]` and a one-line italic description.
2. **Overview** — 2–3 paragraphs: what the commander does, the deck's identity, who it suits.
3. **Game Plan** — accordion with three panels: Early (turns 1–3), Mid (turns 4–6), Late (turn 7+).
4. **Key Cards & Synergies** — accordion with 3–5 panels, one per synergy cluster, using `[[Card Name]]` links.
5. **Mana Base** — brief prose: land count rationale, key utility lands, mana-fixing notes.
6. **Mulligan Guide** — what to keep/ship, 2–3 example keep hands with reasoning.
7. **Flex Slots & Upgrades** — swap suggestions by budget or meta; use a table if more than 4 swaps.
8. **Card Choices & Exclusions** — accordion with panels for non-obvious inclusions or common cuts.
