---
name: mtg-primer
description: Produces a Moxfield-compatible Markdown deck primer (.md file) for a Magic The Gathering deck. Use this skill whenever the user asks to write, generate, or create a deck primer, deck guide, or deck description. Also use it automatically alongside the mtg-decklist-export skill whenever a completed deck is being exported — a primer should always accompany a new decklist. Trigger on phrases like "write a primer", "create a guide for my deck", "explain the deck", or "generate the primer file".
compatibility: Uses the mtg-format-rules skill for the filename pattern (Output section). Uses the mtg-consistency skill to cite real draw-probability numbers in the Gameplan & Mulligan Guide section. Uses the mtg-edhrec skill (Commander formats only) for the Why This Build vs. Similar Decks and Win Conditions sections. Works without any of them — see the fallback notes — but output is more consistent with all installed.
---

# MTG Deck Primer

Produces a Moxfield-compatible Markdown primer file for a completed deck. Structure and conventions below are adapted from an experienced primer author's guide (cEDH-focused originally, generalized here for any format) — the underlying principle is that a primer teaches someone else to pilot the deck, not just describes what's in it.

## Output

**Filename:** `{Commander_Name}_{Tribe_or_Archetype}_{Format}_Primer.md` for any commander-slot format (Commander, **Brawl**, Historic Brawl, Peasant Commander — name the actual format, don't default to "Commander" just because there's a commander slot); `{Oathbreaker_Name}_{SignatureSpell_Name}_Oathbreaker_Primer.md` for Oathbreaker; `{Archetype}_{Colors}_{Format}_Primer.md` for copy-limit formats (no commander to anchor to). See `mtg-format-rules` for the format catalog if the commander-slot-vs-copy-limit distinction is unclear.
Save to `/mnt/user-data/outputs/`. Call `present_files` after saving. Note: *"Here's the primer, ready to paste into Moxfield's primer editor."*

## Moxfield Markdown Rules

- Supported: `#` headings, `**bold**`, `*italic*`, `~~strikethrough~~`, ordered/unordered lists, tables, `---`, inline links, inline images
- Card image links: `[[Card Name]]` or `[[Card Name|SET]]` — highlight a card's name at least the first mention per panel so readers (especially newer players) can hover for the card image. Not necessary on every repeat mention within the same panel — that gets tedious for no added value.
- Collapsible sections: `===accordion` / `===panel: Title` / `===endpanel` / `===endaccordion`
- **Panels are the real hierarchy, not markdown headers.** Moxfield builds its primer table-of-contents/navigation from `===panel:` entries, not from `#`/`##`/`###` headings. A section that should be independently navigable — reachable without scrolling past everything before it — needs to be its own top-level panel, full stop. Markdown headings inside a panel's body are just formatting within that panel's text, not a substitute for panel structure.
- **Panels nest, but a nested `===panel:` needs its own `===accordion`/`===endaccordion` wrapper around it** — a bare `===panel:` dropped directly inside another panel's body, with no accordion wrapper, doesn't get parsed as a panel at all; Moxfield renders the literal `===panel: Title` text inline with the following paragraph instead of a collapsible header. Confirmed by observed rendering failure, not just spec-reading — don't skip the wrapper to save two lines. Use this pattern for one-entry-per-item breakdowns inside a broader section — e.g. one sub-panel per key card inside "Single-Card Discussion," or one sub-panel per dated revision inside "Card Log":
  ```
  ===panel: Single-Card Discussion

  ===accordion

  ===panel: Card Name

  Body text.
  ===endpanel

  ===endaccordion

  ===endpanel
  ```
  Closing the parent panel collapses all its children with it, which is exactly what keeps a long primer manageable. Also: put a blank line between every `===panel: Title` line and its body text — without it, some renders run the title into the first sentence.
- **Not supported:** code blocks, blockquotes, TeX, header anchor links
- Inline HTML allowed — no `<style>` or `<script>`

## Should this deck get a primer at all?

Ask before writing one, or at least flag it if the user hasn't considered it: a primer earns its keep when the deck's win path, sequencing, or card choices aren't obvious from the list alone (combo decks, decks with several build-around synergies, anything competitive where matchup knowledge matters). A deck that's genuinely simple to pilot — vanilla aggro, a stock precon with no changes — doesn't need one; writing an in-depth primer for it mostly restates what a reader gets from just looking at the list. Don't block on this if the user has clearly already asked for one, but it's worth a one-line note if the deck is trivially simple.

## Primer Structure

Adapt all content to the specific deck — no placeholder text. Everything after the title/tagline/intro hook lives inside **one top-level accordion**, with each numbered section below as its own top-level panel (per the hierarchy rule above). Include a section only if it adds real information for *this* deck — an empty or restated section is worse than no section.

1. **Title, tagline, and intro hook** — `# [Deck Name] — [Theme]`, a one-line italic description, then a short prose hook *outside* any panel (2-4 sentences). Default to a direct, repeatable pattern: a short burst of "Do you like X? Do you like Y?" questions naming the deck's actual mechanical hooks (not generic flavor), so a skeptical reader can self-select in or out within one sentence. Keep the questions specific to what the deck does — "Do you like drawing extra cards? Do you like countering your opponent's win attempt on the spot?" not "Do you like having fun?"
2. **Overview** *(panel)* — what the deck's core plan is and who it suits. For Commander, cover what the commander does. Keep this to the plan itself — comparisons to other decks belong in the next section, not folded in here.
3. **Why This Build vs. Similar Decks** *(panel, conditional)* — only include when there's a genuinely comparable deck to measure against (another commander in the same colors/strategy, or another archetype in the same format/metagame). Name 2-3 concrete comparison points and what's actually different, not just "this one's better." For a Commander-format deck, pull a real comparison point from `mtg-edhrec` (e.g. how this build's card choices diverge from EDHREC's average decklist for the commander) rather than inventing one — but still skip the section entirely if nothing informative turns up, don't force a comparison to fill the slot.
4. **Win Conditions** *(panel, conditional)* — only include if the deck has more than one genuine path to closing a game. Short bulleted list, one line per win con naming the enabling card(s) and the practical trigger — this should be scannable at a glance mid-game, not another nested accordion. For combo formats, include the exact step-by-step line for each combo, not just the card names — "Kinnan + Basalt Monolith + Staff of Domination is infinite mana" means nothing to a reader who doesn't already know why. Spell out the loop and what finishes the game off it. For a Commander-format deck, check `mtg-edhrec`'s combo lookup for a verified line involving the deck's cards before writing one from memory. Skip this section for decks with a single obvious win condition (most creature-based 60-card decks) — forcing a list out of one plan just restates the Overview; use Single-Card Discussion for those instead. End with a one-line note on what to do when the active win con gets answered.
5. **Single-Card Discussion** *(panel, nested sub-panels)* — the 60-card-format equivalent of a win-conditions breakdown when there isn't a discrete combo to list. One nested panel per key card or tight synergy cluster (3-6 typical), each covering the card's role, what it enables, and any non-obvious interaction. This is where a reader learns *why* a card is in the 75/60, not just that it is.
6. **Gameplan & Mulligan Guide** *(panel)* — combine these; they're one continuous topic. Lead with 2-3 example hands to assess (a genuinely good keep, a marginal/mediocre keep, and a clear ship) with reasoning for each — "lands and castables" alone isn't sufficient reasoning, explain why the hand does or doesn't advance the plan. Use `mtg-consistency` to cite an actual draw-probability number backing the land/color-source part of that reasoning (e.g. "62% to have 3+ lands in your opening 7") rather than a purely narrative call — this doesn't replace the sequencing/matchup judgment below, it just grounds the one part of the assessment that's genuinely computable. Then cover the turn-by-turn arc (early/mid/late, or by phase if that fits the deck better) — what to develop first, when to hold up interaction vs. deploy threats, and any tutor/search priority (which tutor gets which target and why, not a flat list of every tutor in the deck).
7. **Mana Base** *(panel)* — land count rationale, key utility lands, mana-fixing notes.
8. **Problem Cards** *(panel, conditional)* — cards or effects that specifically counter this deck's plan (a hate piece, a sweeper that punishes the deck's board state, an artifact-hate card that strips key equipment). Include this whenever such cards are identifiable; it's genuinely useful and rarely a stretch. Group similar effects into one paragraph rather than a card-by-card list when there are several doing the same thing (e.g. "cards that shut off extra card draw" as one entry, not five).
9. **Matchups** *(panel, conditional)* — only include when there's a real, identifiable local or format metagame to discuss (known competitive archetypes, a known playgroup's decks). Don't fabricate a metagame for a casual or freshly-built deck with no play history — say so and skip the section instead of inventing matchup advice with no basis. Cover 2-4 matchups: top meta decks/archetypes, or the mirror if relevant, with how the gameplan shifts against each.
10. **Considering Cards / Flex Slots** *(panel)* — cards that could reasonably be in the deck but aren't (owned-but-cut, or not-yet-owned upgrades), and why they didn't make it — distinct from a sideboard, this is "close calls," not "answers to bring in." Table format if more than 4 entries.
11. **Card Log** *(panel, nested sub-panels)* — one nested sub-panel per revision, dated, naming exactly what came in and what went out with brief reasoning for each swap. Start this the first time a deck changes after its initial build — don't retroactively construct a fake history, but do log the current build as an entry if this primer already reflects changes from an earlier version discussed with the user. This is the section that will get touched most often going forward; say so to the user so they know to come back to it after future changes rather than treating the primer as a one-time artifact.

**Not included by default** (mention as optional if the user is building a long-lived, actively-piloted deck, but don't generate placeholder content for them): **Game Log** — a running log of notable in-game moments, which only makes sense once the deck has actually been played and requires the user's own play history, not something to fabricate.

## An honesty caveat this skill can't get around

The guide this structure is based on assumes the primer author has piloted the deck extensively — real games, real losses, real refinements. Claude hasn't played the deck; everything here comes from deck-construction reasoning (card text, curve math, collection data), not table experience. That's a real gap, and it matters most for three sections: **Gameplan & Mulligan Guide** (`mtg-consistency` grounds the land/color-count part of the hand assessment in real math, but the sequencing, tutor-priority, and turn-by-turn calls are still informed guesses, not tested ones), **Problem Cards** (identified from card text/mechanics, not from actually losing to them), and **Card Log** (only reflects changes made in conversation, not iterative playtesting). Say so plainly to the user when handing off a primer — frame these three sections as a strong first draft to refine once they've actually piloted the deck, not settled fact.
