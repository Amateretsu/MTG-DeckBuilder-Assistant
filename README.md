# MTG DeckBuilder Assistant

A Claude Code project for building, analyzing, and exporting Magic: The Gathering Commander (EDH) decks. It combines Scryfall card data, EDHREC community statistics, and a consistent card-tagging taxonomy to produce verified, format-legal decklists with professional-quality output.

---

## How It Works

You interact with the assistant in natural language inside Claude Code. The assistant routes your request to the appropriate skill, verifies every card via Scryfall, and produces a formatted output. Three skills cover the main deckbuilding workflows:

| What you want | Skill invoked |
|---|---|
| Export a finalized decklist + write a primer | `mtg-export` |
| Analyze a deck with an interactive dashboard | `mtg-visualization` |
| Find budget replacements for expensive cards | `mtg-budget-swaps` |

---

## Skills

### Export Decklist + Primer (`mtg-export`)

Produces two files for a finalized deck:
- A `.txt` decklist compatible with Moxfield, Archidekt, and MTGO
- A Markdown primer formatted for Moxfield, covering game plan, key synergies, mana base, mulligan guide, and flex slots

Each card is annotated with functional role tags (e.g., `#!Ramp`, `#!CardAdvantage`) drawn from the taxonomy in `references/MTG-Card-Function-Tags.md`.

**Example prompts:**
- "Export my Meren of Clan Nel Toth reanimator deck."
- "Finalize this list and write a primer."

### Deck Analysis Dashboard (`mtg-visualization`)

Renders an interactive HTML dashboard inside the conversation showing:
- Summary stats (card count, average mana value, land count, ramp sources)
- Mana curve bar chart
- Card type breakdown doughnut chart
- Functional role distribution across all 12 tag categories
- Commander mechanic summary with key synergy targets
- Land base breakdown

**Example prompts:**
- "Visualize this deck."
- "Show me a mana curve analysis."
- "Build an analysis dashboard for my list."

### Budget Swap Guide (`mtg-budget-swaps`)

Identifies the most expensive cards in a deck and suggests verified replacements at $5 or under, filtered by color identity. Each swap includes:
- Current price vs. replacement price
- Why the replacement works for the deck's strategy
- One or two alternative options
- Total savings summary

**Example prompts:**
- "Make this deck cheaper."
- "Find budget alternatives for the expensive cards."
- "Suggest swaps under $5."

---

## General Guidelines

**Always verify cards.** The assistant checks every card against Scryfall before including it in output. Do not assume memorized set codes or collector numbers are correct — the project enforces live lookups.

**Format rules are enforced.** All decks are validated against Commander format rules: 100 cards (99 + commander), singleton except basic lands, and strict color identity constraints. The assistant will flag violations before producing output.

**Provide the full decklist when possible.** The more complete your starting list, the better the optimization and analysis. You can paste a raw list in any common format (one card per line, with or without quantities).

**Card tagging is functional, not decorative.** Tags describe what a card *does* mechanically and *why* it belongs in the deck. A card can have multiple tags. The full tag reference is in [references/MTG-Card-Function-Tags.md](references/MTG-Card-Function-Tags.md).

---

## Project Structure

```
MTG-DeckBuilder-Assistant/
├── .claude/
│   ├── CLAUDE.md              # Core project instructions
│   ├── settings.json          # Permissions and skill configuration
│   └── skills/
│       ├── mtg-export/        # Decklist export + primer skill
│       ├── mtg-visualization/ # Dashboard analysis skill
│       └── mtg-budget-swaps/  # Budget replacement skill
└── references/
    └── MTG-Card-Function-Tags.md  # Canonical card role taxonomy
```

---

## External Integrations

- **Scryfall** — Card legality, set data, and collector numbers (via web search)
- **EDHREC** — Community synergy percentages and inclusion rates for card selection
- **Moxfield / Archidekt / MTGO** — Export targets for the `.txt` decklist format
- **Chart.js** — Powers the interactive visualization dashboard
