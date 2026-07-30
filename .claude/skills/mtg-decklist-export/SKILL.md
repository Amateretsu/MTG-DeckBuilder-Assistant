---
name: mtg-decklist-export
description: "Produces a Moxfield/Archidekt/MTGO-compatible .txt decklist file for a Magic The Gathering deck. Use this skill whenever the user asks to export, save, download, or generate a decklist file, or when a deck has been finalized and needs to be written to a file. Always use this skill when producing any MTG decklist output - even if the user just says \"export the deck\" or \"give me the list as a file\"."
compatibility: "Uses the mtg-card-taxonomy skill's reference file for #!Tag values (Tagging section). Uses the mtg-format-rules skill to determine the filename pattern, quantity rule, and whether a Sideboard section applies (Output/Line Format sections) — never assume format from deck size alone. Works without either — see the fallback notes — but results are more consistent with both installed."
---

# MTG Decklist Export

Produces a properly formatted `.txt` decklist file ready for import into Moxfield, Archidekt, or MTGO.

## Output

**Filename** — pattern depends on the format's commander-slot shape (see `mtg-format-rules`), not just "Commander vs. 60-card":
- Commander-slot formats (Commander, **Brawl**, Historic Brawl, Peasant Commander): `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt` — always name the actual format in the filename (e.g. `..._Brawl.txt` vs. `..._Commander.txt`), never assume Commander just because there's a commander slot. Oathbreaker uses `{Oathbreaker_Name}_{SignatureSpell_Name}_Oathbreaker.txt` since it has two anchor cards, not one.
- Copy-limit formats (Standard, Pioneer, Modern, Legacy, Vintage, Pauper): `{Archetype}_{Colors}_{Format}.txt` (e.g. `Angels_WR_Modern.txt`) — no commander name to anchor to, so lead with the archetype and name the actual format, not a generic "60card" label.
- If revising an existing exported list, append `_v2`, `_v3`, etc. rather than overwriting silently — makes it easy to tell in conversation which version is being discussed.

Save to `/mnt/user-data/outputs/`. Call `present_files` after saving. Note: *"Here's the deck file, ready to import into Moxfield, Archidekt, or MTGO."*

## Line Format

One card per line. No section headers, no blank lines, no additional text. Plain ASCII only.

```
1 Esper Sentinel (MH2) 328 #!Card Advantage and Selection
1 Sol Ring (C21) 263 #!Mana and Tempo
1 Swords to Plowshares (SLD) 182 #!Removal and Interaction
1 Thassa's Oracle (THB) 73 #!Win Conditions & Threats #!Synergy and Tribal
1 Ancient Tomb (2X2) 322
```

Fields: `{quantity} {name} ({SET}) {collector_number} {tags}`

- Card names must match Scryfall `name` field exactly
- Set code uppercased, collector number from Scryfall `set` and `collector_number`
- Commander (or Oathbreaker + Signature Spell pair) listed first, for any format with a commander slot
- Quantities: always `1` for any singleton format (Commander, **Brawl**, Historic Brawl, Oathbreaker, Peasant Commander — see `mtg-format-rules`, not just "Commander"). For copy-limit formats (Standard/Pioneer/Modern/Legacy/Vintage/Pauper), use the deck's actual quantities (1-4 of a card) — don't force everything to 1.
- **Sideboard**: for a competitive 60-card deck with a sideboard, emit a `Sideboard` section header (recognized by Moxfield and MTGO) followed by those 15 cards in the same line format — don't fold them into the maindeck list or drop them silently. Singleton formats never have a sideboard.

## Tagging

Use the 12 top-level category names from `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` as `#!Tag` values. **If that file isn't found**, either omit tags entirely or use your own reasonable category names — don't block the export on it — and mention that installing `mtg-card-taxonomy` would enable consistent tagging.

**Rules:**
- Only tag cards where it adds meaningful information — skip basic lands and generic filler
- Multiple tags space-separated on the same line: `#!Mana and Tempo #!Win Conditions and Threats`
- Prefer top-level categories; drop to a sub-tag only when the top-level would be ambiguous
- Do not include special characters such as &, /, * in tag names under any circumstances, if you do see a special character in a tag name, replace it.