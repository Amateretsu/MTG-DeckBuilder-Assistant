# MTG DeckBuilder Assistant

A Claude Code project for building, revising, analyzing, and exporting Magic: The Gathering decks — both 100-card Commander/EDH and 60-card constructed. It combines live Scryfall verification, the user's own ManaBox card collection, and a consistent card-tagging taxonomy to produce verified, format-legal decklists with professional-quality output.

---

## How It Works

You interact with the assistant in natural language inside Claude Code. The assistant routes your request to the appropriate skill, verifies every card via Scryfall, and produces a formatted output.

| What you want | Skill invoked |
|---|---|
| Build, revise, or trim a deck (including from cards you own) | `mtg-deckbuilding` |
| Fetch/read your card collection or cached Scryfall card facts | `mtg-collection` |
| Export a finalized decklist to a `.txt` file | `mtg-decklist-export` |
| Write a deck primer/guide | `mtg-primer` |
| Analyze a deck with an interactive dashboard | `mtg-visualization` |
| Find budget replacements for expensive cards | `mtg-budget-swaps` |
| Look up how a card is categorized by function | `mtg-card-taxonomy` |

`mtg-deckbuilding` is the entry point whenever the deck itself isn't finalized yet — the other skills all assume a finished decklist as input.

---

## Skills

### Deckbuilding (`mtg-deckbuilding`)

Builds or revises a real, legal deck — from scratch, from a wishlist, or from cards the user already owns. Determines format (60-card vs. Commander) and power level, calculates land count and curve using Frank Karsten's regression formula (with archetype-specific adjustments), balances color sources, and cross-references candidates against the user's collection via `mtg-collection` (binder-aware, so cards already sleeved into another deck aren't silently treated as free). Shows its reasoning for every cut or addition rather than just handing over a final list.

**Example prompts:**
- "Build me a deck from my collection."
- "How many lands should I run in this list?"
- "Trim this pool down to 99 cards."

### Collection Data (`mtg-collection`)

Single source of truth for "what cards does the user own" and a fast-path cache of static Scryfall card facts (oracle text, cost, type, legality). Pulls the latest ManaBox export from the user's Google Drive "ManaBox Exports" folder (falling back to an uploaded CSV or static project file), and exposes exact-printing and binder-aware ownership lookups. Other skills call into this one rather than re-implementing collection or card-fact lookups.

### Decklist Export (`mtg-decklist-export`)

Produces a `.txt` decklist compatible with Moxfield, Archidekt, and MTGO — one card per line, `{quantity} {name} ({SET}) {collector_number} {tags}`, with functional-role tags drawn from `mtg-card-taxonomy`.

**Example prompts:**
- "Export my Meren of Clan Nel Toth reanimator deck."
- "Give me the list as a file."

### Deck Primer (`mtg-primer`)

Writes a Moxfield-compatible Markdown primer (`.md`) that teaches someone else to pilot the deck — overview, win conditions, mulligan guide, mana base, problem cards, flex slots, and a revision log — using Moxfield's panel/accordion structure rather than plain markdown headings.

**Example prompts:**
- "Write a primer for this deck."
- "Create a guide explaining how to pilot this list."

### Deck Analysis Dashboard (`mtg-visualization`)

Renders an interactive HTML dashboard (Chart.js) showing summary stats, a mana curve bar chart, a card type breakdown, a functional-role distribution chart, a format-specific archetype panel (Commander mechanics or 60-card key synergies), and a land base breakdown.

**Example prompts:**
- "Visualize this deck."
- "Show me a mana curve analysis."

### Budget Swap Guide (`mtg-budget-swaps`)

Identifies the most expensive cards in a deck (live Scryfall pricing) and suggests verified, same-role replacements, with a total savings summary.

**Example prompts:**
- "Make this deck cheaper."
- "Suggest swaps under $5."

### Card Function Taxonomy (`mtg-card-taxonomy`)

Shared reference defining 12 top-level functional categories (Card Advantage, Removal, Mana and Tempo, Win Conditions, Synergy, Protection, Board Wipes, Combat Tricks, Recursion, Stax, Equipment and Auras, Utility). A dependency of the other skills so tagging stays consistent across the toolset rather than each skill drifting on its own definitions.

**Example prompts:**
- "What category would you put Swords to Plowshares in?"
- "What's the standard taxonomy for tagging a decklist?"

---

## General Guidelines

**Always verify cards.** The assistant checks every card against Scryfall before including it in output — never assumed or memorized set codes or collector numbers.

**Format rules are enforced.** 60-card constructed and 100-card Commander (99 + commander, singleton, strict color identity) are both validated before output.

**Collection-aware by default.** When a deck is being built or trimmed from owned cards, `mtg-deckbuilding` and `mtg-collection` distinguish cards that are actually free to use from copies already committed to another one of the user's decks.

**Card tagging is functional, not decorative.** Tags describe what a card *does* mechanically and why it belongs in the deck, using the shared taxonomy in `mtg-card-taxonomy`.

---

## Project Structure

```
MTG-DeckBuilder-Assistant/
├── .claude/
│   ├── CLAUDE.md                  # Core project instructions
│   ├── settings.json               # Permissions and skill configuration
│   └── skills/
│       ├── mtg-deckbuilding/       # Build/revise/trim a deck
│       ├── mtg-collection/         # Collection ownership + Scryfall cache
│       ├── mtg-decklist-export/    # .txt decklist export
│       ├── mtg-primer/             # Markdown deck primer
│       ├── mtg-visualization/      # Dashboard analysis
│       ├── mtg-budget-swaps/       # Budget replacement guide
│       └── mtg-card-taxonomy/      # Shared functional-role taxonomy
└── data/
    ├── scryfall_cache.csv          # Weekly-refreshed static card facts
    └── scryfall_seen_ids.json      # Cache bookkeeping
```

---

## External Integrations

- **Scryfall** — Card legality, set data, collector numbers, and pricing (via web search)
- **Google Drive** — Source for the user's live ManaBox collection export
- **Moxfield / Archidekt / MTGO** — Export targets for the `.txt` decklist format and Moxfield-flavored primer markdown
- **Chart.js** — Powers the interactive visualization dashboard
