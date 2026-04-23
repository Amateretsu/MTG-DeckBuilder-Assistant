---
name: mtg-budget-swaps
description: MTG budget swap guide — identifies expensive cards and suggests cheaper replacements. Use for budget alternatives, cheaper options, cost reduction, "budget version", "swap expensive cards", "make this deck cheaper".
---

# MTG Budget Swap Guide

Identifies the most expensive cards in a deck and suggests verified budget replacements.

---

## Execution Phases

### Phase 0 — Read Context Files

Use the Read tool to load both context files before doing anything else:

- `.claude/skills/mtg-export/DECK_RULES.md` — color identity gate (all replacements must pass it)
- `.claude/skills/mtg-export/SCRYFALL.md` — card lookup strategy (WebSearch, not WebFetch)

### Phase 1 — Deck Rules Gate

Complete `DECK_RULES.md` Steps 1–3 and write the output explicitly:

```
Commander: [Name]
Legal colors: [list]
Banned colors: [list]
Tribal type(s): [from oracle text]
Core mechanic: [one sentence]
```

Every replacement candidate must pass the color identity filter before being named.

### Phase 2 — Identify Expensive Cards

Search for current prices using WebSearch: `"[Card Name]" MTG price USD 2025 2026`

Do not use memorized or assumed prices. Identify the 9–12 most expensive cards, sorted descending by USD price.

### Phase 3 — Find Replacements

For each expensive card, find a budget replacement that:
- Costs ≤ $5 USD (note if no sub-$5 option exists)
- **Passes the color identity filter from Phase 1** — verify before naming
- Shares the same functional tag(s) from MTG-Card-Function-Tags.md
- Serves a meaningfully similar role in the deck

Verify each replacement candidate via the SCRYFALL.md strategy before including it.

---

## Presentation

Render as an HTML widget via `visualize:show_widget` if available.

**Header:** Two stat cards — estimated total deck cost and total savings from all swaps (green).

**Per swap panel:**
- Card name (bold) + current price (red) + savings badge (green, right-aligned)
- Swap line in blue: "**Swap:** [Replacement] (~$X)"
- 2–3 sentences on what the replacement does, what's gained, and what's lost
- 1–2 additional alternatives where relevant

**Keep These:** After all swaps, list affordable cards that are core to the strategy and worth keeping at any budget.

**Summary line:** *"Total savings: ~$X,XXX — deck drops from ~$X,XXX to ~$XXX while keeping [strategy] intact."*

**Action button** via `sendPrompt()`: `"Generate the updated budget decklist with all swaps applied"`
