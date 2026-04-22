---
name: mtg-primer
description: Produces a Moxfield-compatible Markdown deck primer (.md file) for a Magic The Gathering deck. Use this skill whenever the user asks to write, generate, or create a deck primer, deck guide, or deck description. Also use it automatically alongside the mtg-decklist-export skill whenever a completed deck is being exported — a primer should always accompany a new decklist. Trigger on phrases like "write a primer", "create a guide for my deck", "explain the deck", or "generate the primer file".
---

# MTG Deck Primer

Produces a Moxfield-compatible Markdown primer file for a completed deck.

## Output

**Filename:** `{Commander_Name}_{Tribe_or_Archetype}_{Format}_Primer.md`
Save to `/mnt/user-data/outputs/`. Call `present_files` after saving. Note: *"Here's the primer, ready to paste into Moxfield's primer editor."*

## Moxfield Markdown Rules

- Supported: `#` headings, `**bold**`, `*italic*`, `~~strikethrough~~`, ordered/unordered lists, tables, `---`, inline links, inline images
- Card image links: `[[Card Name]]` or `[[Card Name|SET]]`
- Collapsible sections: `===accordion` / `===panel: Title` / `===endpanel` / `===endaccordion`
- **Not supported:** code blocks, blockquotes, TeX, header anchor links
- Inline HTML allowed — no `<style>` or `<script>`

## Primer Structure

Adapt all content to the specific commander and deck — no placeholder text.

1. **Title & tagline** — `# [Commander] — [Theme]` and a one-line italic description
2. **Overview** — 2–3 paragraphs: what the commander does, the deck's identity, who it suits
3. **Game Plan** — accordion with three panels: Early (turns 1–3), Mid (turns 4–6), Late (turn 7+)
4. **Key Cards & Synergies** — accordion with 3–5 panels, one per synergy cluster, using `[[Card Name]]` links
5. **Mana Base** — brief prose: land count rationale, key utility lands, mana-fixing notes
6. **Mulligan Guide** — what to keep/ship, 2–3 example keep hands with reasoning
7. **Flex Slots & Upgrades** — swap suggestions by budget or meta; use a table if more than 4 swaps
8. **Card Choices & Exclusions** — accordion with panels for non-obvious inclusions or common cuts
