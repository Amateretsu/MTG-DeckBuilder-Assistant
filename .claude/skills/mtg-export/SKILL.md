---
name: mtg-export
description: Exports a Moxfield/Archidekt/MTGO-compatible .txt decklist and writes a Moxfield-compatible Markdown primer. Use whenever a deck is finalized or the user asks to export, save, or generate a decklist file. Always produces both files together.
---

# MTG Decklist Export + Primer

Produces two files for every export: a `.txt` decklist and a `.md` primer.

**Filenames:**
- `{Commander_Name}_{Tribe_or_Archetype}_{Format}.txt`
- `{Commander_Name}_{Tribe_or_Archetype}_{Format}_Primer.md`

Note after saving: *"Here's the deck file and primer — the .txt is ready to import into Moxfield, Archidekt, or MTGO; paste the .md into Moxfield's primer editor."*

---

## Execution Phases

Follow these phases in strict order. Do not skip ahead. Do not begin card evaluation until Phase 1 is written out in full.

---

### Phase 0 — Read Context Files

Use the Read tool to load all three context files before doing anything else:

- `references/DECK_RULES.md` — color identity gate and format rules
- `references/SCRYFALL.md` — card lookup strategy (WebSearch, not WebFetch)
- `.claude/skills/mtg-export/EDHREC.md` — card discovery and synergy validation

---

### Phase 1 — Deck Rules Gate

Complete every step in `references/DECK_RULES.md` and write the output explicitly:

```
Commander: [Name]
Legal colors: [list]
Banned colors: [list]
Format: Commander (100 cards, singleton)
Tribal type(s): [from oracle text]
Core mechanic: [one sentence]
```

Do not proceed to Phase 2 until this block is written.

---

### Phase 2 — Card Verification

Using the strategy from `SCRYFALL.md`:

1. **Always verify the commander first** — never rely on memorized oracle text
2. **Identify all unfamiliar set codes** in the existing list — look them up in the Known Post-Cutoff Set Codes table before treating them as suspicious
3. **Batch lookups** — fire all WebSearch calls in parallel (up to 8 per message)
4. **Record for each card:** exact name, set code, collector number, oracle text, type line

For an existing Moxfield import, only verify:
- The commander
- All cards with post-2024 or unrecognized set codes
- All new additions being proposed

---

### Phase 3 — Card Selection (optimization mode only)

Skip this phase if the user is exporting an existing final list with no changes.

**Step 3a — Fetch EDHREC data first**

Using the rules in `EDHREC.md`, fetch both pages in parallel:
- `edhrec.com/commanders/[slug]`
- `edhrec.com/commanders/[slug]/commander-matters`

Record the top High Synergy cards and their scores. Note the tracked deck count to calibrate confidence.

**Step 3b — Identify cuts**

- Identify weak performers: cards with no triggered abilities, ETBs, or synergy with the commander's core mechanic
- Identify off-theme cards: cards that don't interact with the commander's tribal type or mechanic
- Cross-check each cut against EDHREC: if a card has >60% inclusion and >40% synergy, flag it before cutting
- State each cut with one-line reasoning

**Step 3c — Select additions**

- Start from the EDHREC High Synergy list — any card there that is missing from the current list is a candidate
- Every candidate must pass the Phase 1 color identity filter before being named
- Verify each candidate via Phase 2 (Scryfall) before confirming it as an addition
- Match cuts count exactly — additions must equal cuts to maintain 100 cards
- For each addition: state the synergy rationale and EDHREC score if available

**Do not loop.** Fetch EDHREC → list candidates → filter by color identity → verify survivors → finalize. Move on.

---

### Phase 4 — Assemble Decklist

Count cards before writing the file:
- Non-land cards + non-basic lands + basic lands = 99
- Confirm total = 99 before writing

**Format:**

```
Commander
1 {Commander} ({SET}) {collector_number} {tags}

Deck
1 {card} ({SET}) {collector_number} {tags}
...
```

Plain ASCII only. No blank lines within each section. Cards in alphabetical order within the Deck section. Basic lands use multi-quantity lines (e.g., `20 Forest (J25) 95`).

**Tagging rules:**
- Only tag where it adds meaningful information — skip basic lands and pure dual lands
- Two tag types must be applied correctly:
  - **Global Tags (`#!`)** — The card's universal mechanical function; roles that apply to this card in any deck. Use for broad, format-agnostic categories.
  - **Deck Tags (`#`)** — The card's strategic role in *this specific deck*. Use when the value is tied to the commander's mechanic, a deck-specific combo line, or a tribal/theme role that wouldn't generalize elsewhere.
- Tags are space-separated; a card can carry both types: `#!Mana #!Synergy #Win Conditions`

| Tag | Covers |
|---|---|
| `Card Advantage` | Draw, selection, impulse draw, looting, graveyard value |
| `Removal` | Targeted removal, board wipes, bounce, exile, fight |
| `Countermagic` | Hard counters, soft counters, stax, protection, redirect |
| `Mana` | Ramp, rocks, dorks, cost reduction, rituals, treasure |
| `Recursion` | Graveyard recursion, reanimation, flashback, self-mill |
| `Tutors` | Library search of any kind |
| `Win Conditions` | Finishers, combo pieces, alternative wins |
| `Creatures` | Evasion, utility, beaters, blockers, tokens, anthems |
| `Synergy` | Tribal payoffs, aristocrats, ETB/LTB payoffs, sacrifice |
| `Enchantments` | Auras, equipment, sagas, enchantress, artifact payoffs, voltron |
| `Resource Denial` | Land destruction, hand disruption, lockpieces, taxation, pillow fort |
| `Utility` | Haste enablers, copy effects, flicker, political, catch-all, hate bears |

**When to use each type:**
- `#!` if the tag applies to this card in most deck contexts (e.g., Sol Ring is always `#!Mana`)
- `#` if the tag only applies because of this deck's commander, theme, or combo (e.g., a creature that's a `#Win Conditions` piece only because of a specific loop this deck runs)
- When uncertain, ask: *would I tag this card the same way in a completely different deck?* If yes → `#!`. If no → `#`.

---

### Phase 5 — Write Primer

Moxfield-compatible Markdown. Adapt all content to the specific commander and deck — no placeholder text.

**Moxfield Markdown rules:**
- Supported: `#` headings, `**bold**`, `*italic*`, `~~strikethrough~~`, ordered/unordered lists, tables, `---`, inline links, inline images
- Card links: `[[Card Name]]` or `[[Card Name|SET]]`
- Collapsible: `===accordion` / `===panel: Title` / `===endpanel` / `===endaccordion`
- Not supported: code blocks, blockquotes, TeX, header anchor links
- Inline HTML allowed — no `<style>` or `<script>`

**Structure:**

1. **Title & tagline** — `# [Commander] — [Theme]` and a one-line italic description
2. **Overview** — 2–3 paragraphs: what the commander does, the deck's identity, who it suits. Reference card counts by role (e.g., "12 pieces of ramp, 8 draw spells").
3. **Game Plan** — accordion with three panels: Early (turns 1–3), Mid (turns 4–6), Late (turn 7+)
4. **Key Cards & Synergies** — accordion with 3–5 panels, one per synergy cluster; 2–4 cards per panel with `[[Card Name]]` links; lead each card in bold
5. **Mana Base** — brief prose: land count rationale, key utility lands, mana-fixing notes
6. **Mulligan Guide** — what to keep/ship, 2–3 example keep hands with reasoning
7. **Flex Slots & Upgrades** — swap suggestions by budget or meta; use a table if more than 4 swaps
8. **Card Choices & Exclusions** — accordion with panels for non-obvious inclusions and deliberate cuts
