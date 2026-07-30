# MTG Card Function Tags

Shared taxonomy for tagging and categorizing cards by the role they play in a deck. Used by `mtg-deckbuilding`, `mtg-decklist-export` (as `#!Tag` values), `mtg-visualization` (as Functional Roles bar chart categories), and `mtg-budget-swaps` (to find same-role replacements).

Every nonland card gets at least one top-level tag. Multicolor/modal cards can get more than one where genuinely ambiguous (e.g. a removal spell that also draws a card), but don't over-tag — pick the primary role first.

## The 12 top-level categories

1. **Card Advantage and Selection** — draws, tutors, impulse draw, scry/surveil, "rummaging" effects. The card nets you more resources or better resources than you started with.
2. **Removal and Interaction** — kills, exiles, bounces, counters, or otherwise neutralizes a specific opposing permanent or spell. Single-target by default; see Board Wipes for symmetric/mass effects.
3. **Mana and Tempo** — ramp, mana rocks/dorks, fixing lands, cost reducers. Anything whose job is getting you to your plays faster or more reliably, not the plays themselves.
4. **Win Conditions and Threats** — the cards actually meant to close the game: finishers, big beaters, combo pieces, alt-win cards.
5. **Synergy and Tribal** — cards that only make sense because of what else is in the deck (tribal lords, "matters" payoffs, anthem effects tied to a subtheme).
6. **Protection and Resilience** — hexproof/indestructible grantors, fog effects, damage prevention, counterspell-proofing.
7. **Board Wipes and Sweepers** — symmetric or near-symmetric mass removal. Distinct from single-target Removal because of the deckbuilding tension it creates in a proactive/aggro shell.
8. **Combat Tricks and Pump** — instant-speed or one-shot power/toughness boosts, keyword grants for a single combat.
9. **Recursion and Graveyard** — reanimation, graveyard recursion, self-mill enablers, graveyard hate.
10. **Stax and Disruption** — taxing effects, discard, land destruction, effects that slow the opponent down rather than advance your own board.
11. **Equipment and Auras (Voltron)** — equipment, auras, and the creatures/effects built specifically to support them (cost reducers, tutors for them, recursion for them).
12. **Utility and Value** — everything else that doesn't fit cleanly above: scry lands, cantrip lands, minor incidental value that isn't the card's main job.

## Tagging guidance

- **Skip basic lands and generic filler.** A vanilla 2/2 for {1}{W} with no text doesn't need a tag — it's just a body. Tag it only if it's doing something (e.g., it's a Human for tribal purposes → Synergy and Tribal).
- **Prefer the top-level category.** Only drop to a more specific note in prose (not a sub-tag) when the top-level would be genuinely ambiguous or misleading.
- **A card's tag is about its deckbuilding role, not its full text.** Skullclamp is "Card Advantage and Selection" even though it's an Equipment (Equipment and Auras) — pick whichever role the card is actually doing in *this* deck. In a Voltron shell it might tag as Equipment and Auras instead. Context matters more than the card's templating.
- **No special characters** (`&`, `/`, `*`) in tag values — spell them out (`and` not `&`).

## Quick reference: common cards by category

Not exhaustive — use as a calibration anchor, not a lookup table. Always verify a card's actual function via Scryfall before tagging it; don't assume from the name.

| Category | Example |
|---|---|
| Card Advantage and Selection | Skullclamp, Militia Bugler, Esper Sentinel |
| Removal and Interaction | Swords to Plowshares, Prison Realm, Lightning Strike |
| Mana and Tempo | Sol Ring, Boros Guildgate, Weapons Trainer (cost reduction) |
| Win Conditions and Threats | Aegis Angel, Victory's Herald |
| Synergy and Tribal | Thalia's Lieutenant, Benalish Commander |
| Protection and Resilience | Mask of Avacyn, Valorous Stance (indestructible mode) |
| Board Wipes and Sweepers | Deafening Clarion, Winds of Rath |
| Combat Tricks and Pump | War Flare, Run Amok, Triumph of Gerrard |
| Recursion and Graveyard | Tiana, Ship's Caretaker |
| Stax and Disruption | (situational — most aggro/midrange decks run few to none) |
| Equipment and Auras (Voltron) | Loxodon Warhammer, Hammer of Nazahn, Angelic Gift |
| Utility and Value | Seraph Sanctuary, cycling lands |
