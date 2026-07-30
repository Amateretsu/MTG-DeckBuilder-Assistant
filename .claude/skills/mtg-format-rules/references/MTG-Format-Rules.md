# MTG Format Construction Rules

Canonical reference for format-specific deck construction rules. Read by `mtg-deckbuilding`, `mtg-decklist-export`, and `mtg-visualization` — don't copy this table into another skill file; point back here instead.

## Format catalog

| Format | Deck size | Copy limit | Sideboard | Commander slot | Land-math table to use |
|---|---|---|---|---|---|
| Standard | 60 min | 4-of | 15-card (Bo3) | None | 60-card archetype table |
| Pioneer | 60 min | 4-of | 15-card (Bo3) | None | 60-card archetype table |
| Modern | 60 min | 4-of | 15-card (Bo3) | None | 60-card archetype table |
| Legacy | 60 min | 4-of | 15-card (Bo3) | None | 60-card archetype table |
| Vintage | 60 min | 4-of (Power Nine typically restricted to 1) | 15-card (Bo3) | None | 60-card archetype table |
| Pauper | 60 min | 4-of, commons only (rarity is the legality gate, not the copy count) | 15-card (Bo3) | None | 60-card archetype table |
| Commander / EDH | Exactly 100 (99 + commander) | Singleton (basic lands exempt) | None | 1 legendary creature (or a card with "can be your commander" text) | 100-card Commander archetype table |
| **Brawl** | Exactly 60 (59 + commander) | Singleton (basic lands exempt) | None | 1 legendary creature or planeswalker, Standard-legal | 60-card archetype table — **this is a 60-card format, not 100-card** |
| Historic Brawl | Exactly 100 (99 + commander) | Singleton (basic lands exempt) | None | Same shape as Commander; card pool restricted to MTG Arena's Historic legality | 100-card Commander archetype table |
| Oathbreaker | Exactly 60 nonland/land total (58 + Oathbreaker + Signature Spell) | Singleton (basic lands exempt) | None | 1 Planeswalker ("Oathbreaker") + 1 instant/sorcery ("Signature Spell") | 60-card archetype table |
| Peasant Commander | 99 + 1 commander | Singleton (basic lands exempt) | None | Same shape as Commander; the 99 must be common/uncommon rarity | 100-card Commander archetype table |
| Limited (Draft/Sealed) | 40 min | Unlimited (pool-constrained, not copy-constrained) | N/A (no fixed sideboard concept the same way) | None | Not covered — different land math (~17-in-40), out of scope until requested |

## Color identity (Commander-family formats)

For any format with a commander slot (Commander, Brawl, Historic Brawl, Oathbreaker, Peasant Commander), every card in the deck must be a subset of the commander's/oathbreaker-pair's color identity — every colored mana symbol in the mana cost AND in all rules text (activated abilities, triggered abilities, static abilities, token-creation text, reminder text). A card whose text produces a token with a colored ability outside the commander's identity is illegal even if the card itself is on-color.

## Live banned/restricted-list lookups

Query Scryfall directly rather than hardcoding a list here — B&R lists change on Wizards' announcement schedule, not this repo's:

```
GET https://api.scryfall.com/cards/search?q=banned%3A{format}
GET https://api.scryfall.com/cards/search?q=restricted%3A{format}
```

Valid `{format}` values match the lowercase format names Scryfall recognizes: `standard`, `pioneer`, `modern`, `legacy`, `vintage`, `pauper`, `commander`, `brawl`, `historicbrawl`, `oathbreaker`, `paupercommander`.

For a single card, fetch it by exact name and read the `legalities` object on the result rather than cross-referencing a separate list:

```
GET https://api.scryfall.com/cards/named?exact={URL-encoded card name}
```

## Sideboard (Bo3) construction — 60-card competitive formats

A 15-card sideboard answers specific matchups; it isn't a second maindeck. When helping build or discuss one:
1. Identify 3-5 likely matchup archetypes for the format's current, real metagame — skip this step (don't invent a metagame) for a casual or freshly-built deck with no established meta context.
2. For each sideboard card, name what it answers and what maindeck card it typically swaps out for — the "boarding plan" — rather than presenting an undifferentiated list.
3. `mtg-decklist-export` should emit a `Sideboard` section header (recognized by Moxfield and MTGO) for any deck that has one, rather than merging sideboard cards into the maindeck list.

## Land count / curve — routing table

Every format above reuses one of `mtg-deckbuilding`'s two existing archetype tables — no new formula is needed for any format currently in scope:

- **60-card table** (aggro/midrange/control adjustments on Karsten's regression): Standard, Pioneer, Modern, Legacy, Vintage, Pauper, Brawl, Oathbreaker.
- **100-card Commander table** (low/average/high-curve ranges): Commander, Historic Brawl, Peasant Commander.

The historical bug this reference exists to prevent: routing Brawl to the 100-card table because "Brawl" sounds Commander-adjacent. It is not — verify deck size from this table before picking a land-math table, don't infer it from the format's name or reputation.

Limited/Draft/Sealed land math (~17 lands in a 40-card deck, driven by curve and color count rather than Karsten's constructed-metagame regression) is intentionally not covered here — Limited deckbuilding is out of scope for this suite until a user requests it (the suite's ownership/collection model is built around constructed/Commander, not a draft pool).
