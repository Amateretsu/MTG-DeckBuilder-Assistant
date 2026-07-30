---
name: mtg-budget-swaps
description: Produces a budget swap guide for a Magic The Gathering deck, identifying expensive cards and suggesting cheaper replacements. Use this skill whenever the user asks about budget alternatives, cheaper options, reducing deck cost, or making a deck more affordable. Trigger on phrases like "budget version", "cheaper alternatives", "swap expensive cards", "what can I cut for budget", "budget swaps", or "make this deck cheaper".
compatibility: Uses the mtg-card-taxonomy skill's reference file to match replacements by functional role (Process section). Uses the mtg-format-rules skill to confirm a replacement is legal in the *same* format as the card it replaces (Process section), not just legal somewhere. Uses the mtg-dashboard-template skill for stat-card/badge styling and the semantic color palette (Presentation section). Works without any of them — see the fallback notes — but output is more consistent with all installed.
---

# MTG Budget Swap Guide

Identifies the most expensive cards in a deck and suggests verified budget replacements.

## Process

1. Identify the 9–12 most expensive cards by `prices.usd` from Scryfall, sorted descending
2. For each, find a budget replacement that:
   - Is verified via Scryfall (legal in the *same format as the original card* — check via `mtg-format-rules`'s live legality lookup rather than assuming "legal somewhere" is good enough; correct color identity)
   - Shares the same functional tag(s) from `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` — **if that file isn't found**, judge "meaningfully similar role" yourself and mention that installing `mtg-card-taxonomy` would make role-matching more consistent
   - Serves a meaningfully similar role in the deck

## Presentation

Render as an HTML widget via `visualize:show_widget` if available. Use `mtg-dashboard-template`'s stat-card grid, badge component, and semantic palette (cost = red-orange, savings = green, info/action = blue) for consistency with `mtg-visualization`'s dashboards. **If `mtg-dashboard-template` isn't installed**, fall back to the same red/green/blue scheme described inline below.

**Header:** Two stat cards — estimated total deck cost and total savings from all swaps (green).

**Per swap panel:**
- Card name (bold) + current price (red) + savings badge (green, right-aligned)
- Swap line in blue: "**Swap:** [Replacement] (~$X)"
- 2–3 sentences on what the replacement does, what's gained, and what's lost
- 1–2 additional alternatives where relevant

**Keep These:** After all swaps, list affordable cards that are core to the strategy and worth keeping at any budget.

**Summary line:** *"Total savings: ~$X,XXX — deck drops from ~$X,XXX to ~$XXX while keeping [strategy] intact."*

**Action button** via `sendPrompt()`: `"Generate the updated budget decklist with all swaps applied"`
