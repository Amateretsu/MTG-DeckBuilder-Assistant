---
name: mtg-format-rules
description: Shared reference for Magic The Gathering format construction rules — deck size, copy limits, sideboard rules, commander-slot shape, and live banned/restricted-list lookups — across Standard, Pioneer, Modern, Legacy, Vintage, Pauper, Commander, Brawl, Historic Brawl, Oathbreaker, and Peasant Commander. Used internally by mtg-deckbuilding, mtg-decklist-export, and mtg-visualization whenever a format needs to be identified, a deck needs to be validated against its construction rules, or a card's legality/ban status needs checking. Also trigger this directly if the user asks a format-rules question on its own, e.g. "how big is a Brawl deck", "is this legal in Pauper", "what's banned in Modern right now", or "does Oathbreaker use a sideboard".
compatibility: Pure reference skill, no workflow of its own — mirrors mtg-card-taxonomy's role as a shared dependency. Banned/restricted-list checks use live Scryfall search syntax via the already-allowlisted api.scryfall.com/scryfall.com WebFetch domains; no new permissions needed.
---

# MTG Format Rules

A single shared reference — `references/MTG-Format-Rules.md` — defining construction rules per format, plus the live-lookup strategy for banned/restricted lists. Exists to be a **dependency of other skills**, not a workflow of its own: `mtg-deckbuilding`, `mtg-decklist-export`, and `mtg-visualization` all read from here rather than each keeping their own copy of format knowledge, the same way they already share `mtg-card-taxonomy` for functional-role tagging.

**If you're one of those three skills and need format rules:** read `references/MTG-Format-Rules.md` in this skill directly. Don't inline a shortened version of the catalog into your own skill file — if a format's rules change (or a new format gets added), it should only need to change here.

**If a user asks a standalone format-rules question** (not in service of building/exporting/analyzing a specific deck), read the reference file and answer from it directly — no need to route into one of the workflow skills first.

## Never conflate Brawl with Commander

The single most important thing this skill exists to fix: **"Brawl" and "Commander" are different formats with different deck sizes.** Real Brawl is 60-card singleton with a Standard-legal commander; Commander/EDH is 100-card singleton. If a user says "Brawl" without qualifying it, ask which they mean — "60-card Brawl (Standard-legal singleton), or 100-card Commander?" — rather than assuming either one. Never silently treat "Brawl" as shorthand for "Commander."

## Live banned/restricted-list lookups

Don't maintain or trust a hardcoded banned-list — Wizards' Banned & Restricted announcements change these on a schedule this file can't track. Instead, use Scryfall's search syntax live, via the same `api.scryfall.com`/`scryfall.com` WebFetch access already used for card verification:

```
https://api.scryfall.com/cards/search?q=banned%3Apauper
https://api.scryfall.com/cards/search?q=restricted%3Avintage
```

Substitute the format name (`standard`, `pioneer`, `modern`, `legacy`, `vintage`, `pauper`, `commander`, `brawl`, `historicbrawl`, `oathbreaker`) for the value after `banned:`/`restricted:`. For a single card's legality across formats, fetch it by exact name (`/cards/named?exact=...`) and read the `legalities` object directly rather than cross-referencing a separate list.

For a full check on every card in a decklist, prefer the `mtg-collection` skill's Scryfall data cache first (it carries `legalities_commander`/`legalities_standard`/`legalities_modern` columns already) and fall back to the live per-card lookup above only for formats the cache doesn't cover (Pioneer, Legacy, Vintage, Pauper, Brawl, Oathbreaker) or for anything the cache's truncation might have missed.

## Format catalog

See `references/MTG-Format-Rules.md` for the full table (deck size, copy limit, sideboard, commander-slot shape, land-math table to use per format). Summary of what needs disambiguation most:

| Format | Deck size | Copy limit | Sideboard | Commander slot |
|---|---|---|---|---|
| Standard / Pioneer / Modern / Legacy / Vintage | 60 min | 4-of | 15-card (Bo3) | None |
| Pauper | 60 min | 4-of (commons only) | 15-card (Bo3) | None |
| Commander / EDH | Exactly 100 | Singleton | None | 1 legendary creature (or card that says it can be a commander) |
| **Brawl** | Exactly 60 | Singleton | None | 1 legendary creature/planeswalker, Standard-legal |
| Historic Brawl | Exactly 100 | Singleton | None | Same shape as Commander, Historic-legal card pool (MTG Arena) |
| Oathbreaker | Exactly 60 nonland + land | Singleton | None | 1 Planeswalker ("Oathbreaker") + 1 Signature Spell (instant/sorcery) |
| Peasant Commander | 99 + 1 | Singleton | None | Same as Commander; the 99 must be common/uncommon rarity |

## Sideboard (Bo3) construction guidance

For competitive 60-card formats played best-of-three: a 15-card sideboard exists to answer specific matchups, not to be a second maindeck. When helping build or discuss one:
- Identify 3-5 likely matchup archetypes for the format's current metagame (skip this if there's no real identifiable metagame to reason about — don't invent one for a casual or brand-new deck)
- For each sideboard card, name what it answers and what maindeck card it typically replaces (the "boarding plan"), not just a flat list
- `mtg-decklist-export` should use a recognized `Sideboard` section header (both Moxfield and MTGO support one) when a deck being exported has one — don't fold sideboard cards into the maindeck list or drop them silently

## Land count / curve — format deltas

Most formats reuse `mtg-deckbuilding`'s existing tables as-is:
- Standard/Pioneer/Modern/Legacy/Vintage/Pauper/Peasant Commander → the existing 60-card archetype table (aggro/midrange/control)
- **Brawl** → the existing 60-card archetype table (it's genuinely a 60-card format, despite the "Commander-adjacent" framing many players use)
- Commander/Historic Brawl/Oathbreaker → the existing 100-card Commander archetype table

No format in this catalog needs new land-count math beyond what `mtg-deckbuilding` already computes — the fix here is entirely about routing each format to the *correct* existing table, not deriving new formulas.

## Consumption notes for dependent skills

- **mtg-deckbuilding** section 1: call into this skill's Brawl/Commander disambiguation instead of its own binary; use the catalog table above (not a hardcoded assumption) to determine deck size, copy limit, and land-math table.
- **mtg-decklist-export**: quantity rule ("always 1" vs. "1-4") and filename pattern become format-parameterized from the catalog instead of hardcoded to "Commander vs. 60-card"; add `Sideboard` section-header support for formats that have one.
- **mtg-visualization**: sections 5-6 (archetype panel, land base breakdown) generalize from a 2-way Commander/60-card branch to a format-family branch (singleton-style vs. copy-limit-style), using this catalog rather than re-deriving format logic.
- **mtg-budget-swaps**: when suggesting a swap, confirm the replacement is legal in the *same* format as the card it's replacing (via the live lookup above), not just "legal somewhere."
