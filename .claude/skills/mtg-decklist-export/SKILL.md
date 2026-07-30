---
name: mtg-decklist-export
description: "Produces a Moxfield/Archidekt/MTGO-compatible .txt decklist file for a Magic The Gathering deck. Use this skill whenever the user asks to export, save, download, or generate a decklist file, or when a deck has been finalized and needs to be written to a file. Always use this skill when producing any MTG decklist output - even if the user just says \"export the deck\" or \"give me the list as a file\"."
compatibility: "Uses the mtg-card-taxonomy skill's reference file for #!Tag values (Tagging section). Works without it — see the fallback note there — but tags are more consistent with it installed."
---

# MTG Decklist Export

Produces a properly formatted `.txt` decklist file ready for import into Moxfield, Archidekt, or MTGO.

## Output

**Filename:**
- Commander: `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt`
- 60-card constructed: `{Archetype}_{Colors}_{Format}.txt` (e.g. `Angels_WR_60card.txt`) — no commander name to anchor to, so lead with the archetype
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
- Commander listed first (Commander format only)
- Quantities: always `1` for Commander (singleton). For 60-card constructed, use the deck's actual quantities (1-4 of a card, following the format's copy limit) — don't force everything to 1.

## Tagging

Use the 12 top-level category names from `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` as `#!Tag` values. **If that file isn't found**, either omit tags entirely or use your own reasonable category names — don't block the export on it — and mention that installing `mtg-card-taxonomy` would enable consistent tagging.

**Rules:**
- Only tag cards where it adds meaningful information — skip basic lands and generic filler
- Multiple tags space-separated on the same line: `#!Mana and Tempo #!Win Conditions and Threats`
- Prefer top-level categories; drop to a sub-tag only when the top-level would be ambiguous
- Do not include special characters such as &, /, * in tag names under any circumstances, if you do see a special character in a tag name, replace it.