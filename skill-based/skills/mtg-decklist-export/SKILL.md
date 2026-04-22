---
name: mtg-decklist-export
description: Produces a Moxfield/Archidekt/MTGO-compatible .txt decklist file for a Magic The Gathering deck. Use this skill whenever the user asks to export, save, download, or generate a decklist file, or when a deck has been finalized and needs to be written to a file. Always use this skill when producing any MTG decklist output - even if the user just says "export the deck" or "give me the list as a file".
---

# MTG Decklist Export

Produces a properly formatted `.txt` decklist file ready for import into Moxfield, Archidekt, or MTGO.

## Output

**Filename:** `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt`
Save to `/mnt/user-data/outputs/`. Call `present_files` after saving. Note: *"Here's the deck file, ready to import into Moxfield, Archidekt, or MTGO."*

## Line Format

One card per line. No section headers, no blank lines, no additional text. Plain ASCII only.

```
1 Esper Sentinel (MH2) 328 #!Card Advantage & Selection
1 Sol Ring (C21) 263 #!Mana & Tempo
1 Swords to Plowshares (SLD) 182 #!Removal & Interaction
1 Thassa's Oracle (THB) 73 #!Win Conditions & Threats #!Synergy & Tribal
1 Ancient Tomb (2X2) 322
```

Fields: `{quantity} {name} ({SET}) {collector_number} {tags}`

- Card names must match Scryfall `name` field exactly
- Set code uppercased, collector number from Scryfall `set` and `collector_number`
- Commander listed first
- All quantities `1` (Commander format)

## Tagging

Use the 12 top-level category names from MTG-Card-Function-Tags.md as `#!Tag` values.

**Rules:**
- Only tag cards where it adds meaningful information — skip basic lands and generic filler
- Multiple tags space-separated on the same line: `#!Mana & Tempo #!Win Conditions & Threats`
- Prefer top-level categories; drop to a sub-tag only when the top-level would be ambiguous
