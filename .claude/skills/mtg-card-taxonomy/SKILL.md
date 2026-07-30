---
name: mtg-card-taxonomy
description: Shared taxonomy for categorizing Magic The Gathering cards by their functional role in a deck (Card Advantage, Removal, Ramp, Win Conditions, Synergy, etc). Used internally by mtg-deckbuilding, mtg-visualization, mtg-decklist-export, and mtg-budget-swaps for tagging, categorizing, and reasoning about deck composition — read references/MTG-Card-Function-Tags.md whenever one of those skills needs to tag a card or reason about a deck's role balance. Also trigger this directly if the user asks a categorization question on its own, e.g. "how do you classify Magic cards by function", "what category would you put Swords to Plowshares in", or "what's the standard taxonomy for tagging a decklist".
---

# MTG Card Function Taxonomy

A single shared reference — `references/MTG-Card-Function-Tags.md` — defining 12 top-level functional categories for Magic cards (Card Advantage and Selection, Removal and Interaction, Mana and Tempo, Win Conditions and Threats, Synergy and Tribal, Protection and Resilience, Board Wipes and Sweepers, Combat Tricks and Pump, Recursion and Graveyard, Stax and Disruption, Equipment and Auras, Utility and Value), plus tagging guidance and a calibration table of example cards per category.

This skill exists to be a **dependency of other skills**, not a workflow of its own. `mtg-deckbuilding`, `mtg-visualization`, `mtg-decklist-export`, and `mtg-budget-swaps` all read the reference file here rather than each maintaining their own copy of the taxonomy — that way there's one definition of "what counts as removal" across the whole toolset instead of four skills quietly drifting apart.

**If you're one of those four skills and need the taxonomy:** read `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` directly. Don't inline a shortened version of the categories into your own skill file — if the taxonomy changes, it should only need to change in one place.

**If a user asks a standalone categorization question** (not in service of building/exporting/analyzing a specific deck), just read the reference file and answer from it directly — no need to route into one of the workflow skills first.
