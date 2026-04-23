---
name: mtg-deck-analysis
description: Comprehensive MTG deck analysis with interactive visualization. Evaluates consistency, synergy density, role balance, strengths, and weaknesses. Use for "analyze this deck", "how good is this deck", detailed feedback requests, or any time the user wants in-depth analysis without exporting.
---

# MTG Deck Analysis

Produces a comprehensive interactive HTML dashboard via `visualize:show_widget` using Chart.js (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`).

No files are saved. All output is rendered as an interactive widget.

---

## Common Widget Settings

- Dark mode: detect via `matchMedia`; derive `textColor` and `gridColor`
- All charts: `responsive: true`, `maintainAspectRatio: false`, no built-in legend
- Bars: `borderRadius: 4`, `borderSkipped: false`
- CSS vars: `--color-background-secondary`, `--color-text-primary`, `--color-text-secondary`, `--color-border-tertiary`, `--border-radius-md`, `--border-radius-lg`
- Accessibility: `<h2 class="sr-only">` + `role="img"` and `aria-label` on every `<canvas>`

**Color palette:** Creatures `#534AB7` · Artifacts `#1D9E75` · Sorceries `#D85A30` · Instants `#378ADD` · Planeswalkers `#D4537E` · Enchantments `#888780`

---

## Execution Phases

### Phase 0 — Load Reference Files

Read all three reference files before proceeding:

- `references/MTG-Card-Function-Tags.md` — canonical tag names and card categorization rules
- `references/DECK_RULES.md` — color identity gate and format constraints (use in Phase 1)
- `references/SCRYFALL.md` — card lookup strategy (use when verifying Critical Gap suggestions in Phase 4)

---

### Phase 1 — Commander & Deck Context

Identify and write out explicitly before proceeding:

```
Commander: [Name]
Colors: [W/U/B/R/G flags]
Format: [Commander / Brawl / etc.]
Core mechanic: [one sentence]
Tribal type(s): [from oracle text, or N/A]
Total cards: [N]
```

---

### Phase 2 — Categorize All Cards

Tag every non-land card with one or more tags from `MTG-Card-Function-Tags.md`. Record counts per tag. Then compute:

- **Total lands** (total, basics vs. non-basics)
- **Ramp sources** — non-land cards tagged `Mana`
- **Average mana value** — non-lands only, 1 decimal
- **Synergy cards** — cards that directly enable, trigger, or scale with the commander's core mechanic (record count and names)
- **Mana curve** — count of non-land cards at each MV: 0, 1, 2, 3, 4, 5, 6, 7+

Do not proceed to Phase 3 until all counts are written out.

---

### Phase 3 — Consistency Evaluation

Score each role category against the recommended ranges for Commander (100-card singleton):

| Role | Recommended Range | Weight |
|------|-------------------|--------|
| Card Advantage | 8–12 | High |
| Removal | 7–10 | High |
| Mana (ramp, non-land) | 10–14 | High |
| Lands | 35–38 | High |
| Win Conditions | 3–6 | Medium |
| Countermagic | 5–10 (blue decks) / 0–3 (others) | Medium |
| Recursion | 3–7 | Low |
| Tutors | 2–6 | Low |

**Scoring:** Within range = 2pts · One step outside = 1pt · Two+ steps outside = 0pts.
**Normalize** the weighted total to a 0–100 Consistency Score.

Labels: **85–100** Optimized · **70–84** Strong · **55–69** Solid · **40–54** Developing · **<40** Needs Work

**Synergy Density:** `(synergy card count / total non-land cards) × 100` → report as a percentage with label: ≥60% High · 40–59% Moderate · <40% Low

---

### Phase 4 — Strengths & Weaknesses

Based on role counts, synergy density, curve shape, and commander context, identify:

- **3 Strengths** — what the deck executes well (e.g., "14 ramp sources ensure early acceleration," "7 recursive threats make the deck resilient to removal")
- **3 Weaknesses** — gaps or vulnerabilities (e.g., "only 5 draw spells limits late-game gas," "no exile-based removal leaves the deck soft to indestructible threats")
- **1 Critical Gap** — the single most impactful missing role or underrepresented category; name 1–2 specific cards that would address it

Be specific to the actual cards and commander — no generic filler.

---

### Phase 5 — Render Dashboard

Render all analysis as a single `visualize:show_widget` HTML file with the following sections in order:

#### 1. Header

Commander name as `<h1>`, format and colors as a subtitle line, core mechanic as a one-line italic tagline.

#### 2. Summary Stat Cards

5-column CSS grid, `--color-background-secondary` background, 24px number / 13px label:

**Total Cards** · **Avg Mana Value** · **Lands** · **Ramp Sources** · **Consistency Score** (colored by label: green ≥70 · yellow 55–69 · red <55)

#### 3. Role Balance Panel

Horizontal list or grid showing each tracked role category. For each: role name, actual count, recommended range, and a color-coded status indicator:
- Green: within range
- Yellow: one step outside range
- Red: two+ steps outside range

#### 4. Mana Curve Bar Chart

Vertical bar, `barPercentage: 0.7`. X-axis MV 0–7+. Bars MV 6+ in `#534AB7`, below in `#1D9E75`. If the commander has a mechanic with a relevant MV threshold (e.g., cascade), add an `afterLabel` tooltip noting it. Title: "Mana curve (N non-land cards)".

#### 5. Card Types Doughnut

`cutout: '55%'`, no built-in legend. Custom flex-wrapped legend with color swatches. Categories: Creatures, Artifacts, Sorceries, Instants, Planeswalkers, Enchantments, Battles/Other if present.

#### 6. Functional Roles Horizontal Bar

`indexAxis: 'y'`, `barPercentage: 0.6`, categories in descending count order. Use these top-level tag names exactly (skip any with 0 count):

`Card Advantage` · `Removal` · `Countermagic` · `Mana` · `Recursion` · `Tutors` · `Win Conditions` · `Creatures` · `Synergy` · `Enchantments` · `Resource Denial` · `Utility`

#### 7. Synergy Density Indicator

Rounded panel showing synergy density percentage and label (High / Moderate / Low), with a list of up to 8 key synergy cards by name.

#### 8. Commander Mechanic Panel

Rounded panel. Format: commander name as heading, core engine in 2–3 sentences, enablers as an inline list, each of 3 notable synergy targets with a one-sentence note. Adapt entirely to the actual commander — no generic text.

#### 9. Strengths & Weaknesses Panel

Two-column layout:
- **Strengths** column (green accent): 3 bullet points from Phase 4
- **Weaknesses** column (red accent): 3 bullet points from Phase 4
- **Critical Gap** row spanning full width (amber accent): 1 sentence naming the gap and 1–2 suggested cards

#### 10. Land Base Breakdown

4-column grid (same styling as stat cards): **Ramp Lands** · **Utility Lands** · **Interaction Lands** · **Basic Lands**.

#### 11. Action Buttons

3 buttons via `sendPrompt()`:
- `"Export this [Commander] deck as a .txt file and write the Moxfield primer"`
- `"Suggest budget alternatives for the most expensive cards in this deck"`
- `"What upgrades would most improve this deck's consistency score?"`
