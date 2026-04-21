# MTG Deckbuilder — Output Instructions

This document specifies the exact output format and process for building, analyzing, and optimizing Magic: The Gathering Commander decks. It covers three deliverables: the **Deck Analysis Visualization**, the **Budget Swap Guide**, and the **Decklist Export**.

---

## 1. Deck Analysis Visualization

After assembling a full decklist, produce an interactive dashboard using the `visualize:show_widget` tool (HTML + Chart.js). The widget must include all of the following sections, in order.

### 1.1 Summary Stat Cards

Display a row of 4 stat cards in a CSS grid (`grid-template-columns: repeat(4, 1fr)`), each with a label and large number:

| Card           | Value Description                                      |
| -------------- | ------------------------------------------------------ |
| **Cards**      | Total cards in the deck (always 100 for Commander)      |
| **Avg mana value** | Mean mana value of all non-land cards, 1 decimal place |
| **Lands**      | Total land count                                        |
| **Ramp sources** | Total non-land mana acceleration cards                 |

Use `var(--color-background-secondary)` for card backgrounds. Font size: 24px for the number, 13px for the label.

### 1.2 Mana Curve Bar Chart

- Chart type: **vertical bar** (`type: 'bar'`), rendered on a `<canvas>` element using Chart.js (loaded from `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).
- X-axis: Mana value labels from `0` through `13` (or the deck's maximum), labeled "Mana value".
- Y-axis: Count of non-land cards at each mana value, labeled "Count".
- **Color coding**: Bars at MV 7+ use a distinct accent color (e.g., `#534AB7`) to indicate cascade-eligible spells with Zhulodok. Bars below MV 7 use a second color (e.g., `#1D9E75`).
- Tooltip: Show "Mana value X" as title, "N cards" as label, and for MV 7+ add `afterLabel`: "Triggers double cascade".
- Include a section title above the chart: **"Mana curve (N non-land cards)"** at 15px font-weight 500.
- Chart height: 300px, responsive, `maintainAspectRatio: false`.
- Bar styling: `borderRadius: 4`, `borderSkipped: false`, `barPercentage: 0.7`.

### 1.3 Card Types Doughnut Chart

- Chart type: **doughnut** (`type: 'doughnut'`), placed in a 2-column grid alongside the Functional Roles chart.
- Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments (and Battles / Other if present).
- `cutout: '55%'`, no built-in legend (`legend: { display: false }`).
- Below the chart, render a **custom legend** using flex-wrapped `<span>` elements, each with a 10×10px color swatch (`border-radius: 2px`) and the category name + count.
- Color palette (consistent across all charts):
  - Creatures: `#534AB7`
  - Artifacts: `#1D9E75`
  - Sorceries: `#D85A30`
  - Instants: `#378ADD`
  - Planeswalkers: `#D4537E`
  - Enchantments: `#888780`

### 1.4 Functional Roles Horizontal Bar Chart

- Chart type: **horizontal bar** (`type: 'bar'`, `indexAxis: 'y'`).
- Categories (in descending order by count): Threats / finishers, Ramp, Removal, Card draw, Utility, Protection.
- Each bar gets a unique color from the palette above.
- `barPercentage: 0.6`, `borderRadius: 4`.
- No legend.

### 1.5 Cascade Analysis Panel (Commander-specific)

- A text block inside a rounded panel (`var(--color-background-secondary)` background, `var(--border-radius-lg)` corners, `1rem 1.25rem` padding).
- Content should state:
  - How many spells at MV 7+ trigger double cascade.
  - How many non-land cards below MV 7 exist as cascade targets.
  - Name 3 key cascade targets with brief reasoning for each.
- Use `font-size: 13px`, `line-height: 1.7` for the body, and highlight key numbers with `font-weight: 500; color: var(--color-text-primary)`.

### 1.6 Land Base Breakdown

- A 4-column grid of stat cards (same styling as section 1.1), categorizing lands:
  - **Ramp lands** (lands that produce 2+ mana or cost-reduce: Ancient Tomb, Eldrazi Temple, Tron pieces, etc.)
  - **Utility lands** (Urza's Saga, Sanctum of Ugin, Reliquary Tower, etc.)
  - **Interaction lands** (Wasteland, Ghost Quarter, Demolition Field, etc.)
  - **Basic wastes** (count of Wastes)

### 1.7 Action Buttons

At the bottom, render 3 `<button>` elements using `sendPrompt()` to trigger follow-up actions:
- `"Export this [Commander] deck as a downloadable .txt file"` → generates the export file
- `"Suggest budget alternatives for the most expensive cards in this deck"` → triggers swap analysis
- `"What are the best opening hands and mulligan strategy for this deck?"` → triggers play guide

### 1.8 Theming and Accessibility

- Detect dark mode: `var isDark = matchMedia('(prefers-color-scheme: dark)').matches;`
- Set `textColor` and `gridColor` dynamically for chart axes/gridlines.
- Include `<h2 class="sr-only">` at the top describing the dashboard for screen readers.
- Every `<canvas>` must have `role="img"` and an `aria-label` with a text summary of the chart data.
- Use CSS variables throughout: `var(--color-background-secondary)`, `var(--color-text-primary)`, `var(--color-text-secondary)`, `var(--color-border-tertiary)`, `var(--border-radius-md)`, `var(--border-radius-lg)`.

---

## 2. Budget Swap Guide

When the user asks for budget alternatives, produce the following output. If the visualization tool is available, render as an HTML widget. If not, fall back to formatted text (as shown below).

### 2.1 Price Research Process

1. Search for current USD prices of every card in the deck using web search against sources like MTGStocks, MTG Decks, TCGPlayer, and Scryfall.
2. Identify the **9–12 most expensive cards**, sorted by price descending.
3. For each, find a functionally similar budget replacement and verify it via Scryfall (legal in format, correct color identity, similar role).

### 2.2 Summary Stat Cards (if visualization)

Two stat cards at the top:
- **Est. total (full list):** approximate total deck cost.
- **Savings from all swaps:** total savings if every swap is applied (use green/success color).

### 2.3 Swap Cards Format

Each swap is a card-style panel with:
- **Header row:** Card name (bold, 14px) + price in danger/red color + savings badge (green background, right-aligned).
- **Body:** "**Swap:** [Replacement Name] (~$X)" in info/blue color, followed by a plain-text explanation of why the swap works and what you lose. Offer 1–2 alternatives where relevant.

Example text format (for fallback when visualization times out):

```
**[Expensive Card]** (~$XXX) → **[Budget Card]** (~$X)
[Explanation of what the budget card does, how it compares, and what's lost in the swap. Mention if the expensive card is Reserved List or on the Game Changers list.]
```

### 2.4 "Keep These" Section

After all swaps, include a panel listing **cards worth keeping at any budget** — affordable cards that are core to the strategy. List each with its approximate price.

### 2.5 Summary Line

End with a one-line summary: "**Total savings: ~$X,XXX** if you make all swaps. The resulting deck drops from roughly $X,XXX to about $XXX while keeping [core strategy description] intact."

### 2.6 Action Button

A button using `sendPrompt()` to generate the updated budget decklist with all swaps applied.

---

## 3. Decklist Export

When exporting a completed decklist, produce a `.txt` file saved to `/mnt/user-data/outputs/` and presented via `present_files`.

### 3.1 File Naming

Use a descriptive filename with underscores: `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt`

Examples: `Zhulodok_Eldrazi_Commander.txt`, `Atraxa_Superfriends_Commander.txt`

### 3.2 File Format

```
// Commander
1 Commander Name

// Category Name (group cards by function)
1 Card Name
1 Another Card

// Next Category
1 Card Name
...
```

### 3.3 Category Groupings (Commander)

Organize cards into the following comment-delimited sections, in this order:

1. `// Commander` — The commander card(s)
2. `// Eldrazi Titans & Finishers` (or format-appropriate top-end name) — The biggest threats / win conditions
3. `// Eldrazi Midrange` (or equivalent) — Mid-curve tribal creatures
4. `// Eldrazi Utility Creatures` (or equivalent) — Smaller tribal creatures with utility effects
5. `// Planeswalkers` — If any
6. `// Enchantments` — If any
7. `// Mana Rocks & Ramp` — All non-land mana acceleration
8. `// Utility Artifacts` — Card selection, protection, synergy pieces
9. `// Removal Artifacts` — Artifact-based removal
10. `// Instants` — Instant-speed interaction
11. `// Sorceries` — Sorcery-speed spells
12. `// Lands - [Subcategory]` — Lands broken into sub-groups:
    - Acceleration (Eldrazi Temple, Ancient Tomb, etc.)
    - Tron Package (if applicable)
    - Urza Utility (Urza's Saga, Workshop, etc.)
    - Conditional Ramp (Temple of the False God, Shrine, etc.)
    - Tutors & Advantage (Sanctum of Ugin, War Room, etc.)
    - Utility (Darksteel Citadel, Reliquary Tower, etc.)
    - Interaction (Wasteland, Ghost Quarter, etc.)
    - Basics (list each basic on its own line: `1 Wastes`)

### 3.4 Formatting Rules

- One card per line: `{quantity} {exact Scryfall card name}`
- Use plain ASCII only
- Blank line between each category section
- Every card name must match its Scryfall `name` field exactly
- For Commander: all quantities are `1` (except basics which are also `1` each but listed individually)

### 3.5 Delivery

After creating the file:
1. Save to `/mnt/user-data/outputs/{filename}.txt`
2. Call `present_files` with the filepath
3. Add a brief note: "Here's the deck file, ready to import into Moxfield, Archidekt, or MTGO."

---

## 4. Post-Decklist Commentary

After presenting the visualization and/or export, provide a brief strategic summary covering:

1. **How the deck plays** — A 2-3 sentence description of the core game plan and ideal sequencing (e.g., "Ramp aggressively in turns 1-3, deploy commander turn 3-4, chain cascade spells").
2. **Key synergies** (3-4 highlighted combos) — Each as a bolded card name followed by 2-3 sentences explaining the interaction. Focus on non-obvious synergies the user might miss.
3. **Mana curve justification** — If the average MV is unusually high or low for the strategy, explain why it's intentional and how the deck compensates.

---

## 5. Chart.js Configuration Reference

All charts share these common options:

```javascript
// Dark mode detection
var isDark = matchMedia('(prefers-color-scheme: dark)').matches;
var textColor = isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.65)';
var gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';

// Common axis styling
ticks: { color: textColor, font: { size: 11 } }
grid: { color: gridColor }  // or { display: false } for category axes

// Common bar styling
borderRadius: 4
borderSkipped: false

// All charts
responsive: true
maintainAspectRatio: false
plugins: { legend: { display: false } }
```

Load Chart.js from CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
```

---

## 6. Fallback Behavior

If the `visualize:show_widget` tool times out or errors:
- Present all statistics as formatted text in the chat response.
- Use the text-based histogram format for the mana curve:
  ```
  CMC 0: ██ (2)
  CMC 1: ██████ (6)
  ...
  ```
- Present card type and functional role breakdowns as inline lists.
- Budget swaps render as the markdown format shown in section 2.3.
- The decklist export file is always produced regardless of visualization status.
