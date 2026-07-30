---
name: mtg-deckbuilding
description: Build, revise, or cut down a Magic The Gathering deck — including building a deck from a player's owned collection, trimming a card pool down to a legal deck size, choosing land counts, suggesting cuts/upgrades, or cross-referencing a wishlist against a ManaBox collection export. Use this whenever the user wants to construct or meaningfully edit a deck (not just analyze, export, or write a primer for one that's already finished) — including phrases like "build me a deck", "help me build a deck from my collection", "how many lands should I run", "what should I cut from this deck", "improve this deck using cards I own", or "trim this list down to 60/99 cards". Always use this before mtg-decklist-export, mtg-visualization, or mtg-primer when the deck itself isn't finalized yet — those skills assume a finished decklist as input.
compatibility: Uses the mtg-collection skill to fetch and read the user's owned-card data (section 3) — always consult it rather than assuming a stale upload. Also uses the mtg-card-taxonomy skill's reference file for functional-role categorization (section 4). Works without either — see fallback notes in each section — but results are more consistent with both installed.
---

# MTG Deckbuilding

Builds or revises a real, legal Magic deck — as opposed to `mtg-visualization` (analyzes a finished deck), `mtg-decklist-export` (formats a finished deck as a file), or `mtg-primer` (writes a guide for a finished deck). Those three skills all assume the decklist is already done; this one is for when it isn't yet.

## 1. Determine format first — it changes everything downstream

Ask yourself (infer from context where possible, ask the user if genuinely ambiguous):
- **Deck size:** 60-card constructed, or 100-card Commander/Brawl (singleton)?
- **Power level / setting:** casual kitchen-table, competitive constructed, cEDH, etc. — affects how aggressively to prioritize efficiency over synergy/fun.

This determines quantity limits (singleton vs up-to-4-of), land count targets, and which downstream skill conventions apply (`mtg-decklist-export`'s filename pattern and "all quantities 1" rule is Commander-specific — for a 60-card deck, quantities can be 1-4 and the filename should reflect the archetype, not a commander name).

## 2. Land count and curve

Don't guess a land count from intuition — use the actual math, then adjust for archetype.

**Baseline formula** (Frank Karsten's regression across tournament-winning decklists):

```
lands = 19.59 + (1.90 × average mana value of non-land cards) − 0.28 × (count of cheap cantrips/ramp)
```

This baseline is calibrated across a mixed population of decks. Real archetypes deviate from it in a consistent direction — apply the adjustment, don't just report the raw number:

| Archetype (60-card) | Typical range | Notes |
|---|---|---|
| Aggro (avg MV < 2.5, wants to end the game fast) | 20-23 | Sits at the low end of what the formula predicts — willing to trade some consistency for action density |
| Midrange (avg MV 2.5-3.2) | 22-24 | Close to the formula's raw output |
| Control (avg MV 3+, wants every land drop) | 24-26 | At or above the formula's output |

| Archetype (100-card Commander) | Typical range |
|---|---|
| Low curve / aggressive Commander | 33-35 lands + ~2-3 ramp/rocks |
| Average Commander deck | 36-38 lands + ~3-5 ramp/rocks |
| High curve / ramp-heavy Commander | 38-40 lands + 5+ ramp/rocks |

**When a number you produce disagrees with a generic "24 lands" rule of thumb the user has seen elsewhere:** that generic rule is usually either outdated beginner advice or is Commander's ~38% ratio applied incorrectly to a 60-card deck. Show your actual math (the formula, the archetype adjustment) rather than asserting a number — that's what lets the user (or you) catch it if it's wrong, and it's a much stronger answer than "trust me."

**Color sources**, once total land count is set: count colored mana symbols across the nonland cards (not just card count — a card with a WW cost pulls twice as hard on your white sources as a single-W card). Skew the basic/dual split toward whichever color has the higher pip demand, especially double-pip costs.

## 3. Building from a collection

If the deck is being built or trimmed from cards the user owns:

1. **Fetch first, via the `mtg-collection` skill** — don't assume an old upload or project file is current. That skill covers pulling the latest export from the user's Drive folder (and the fallback order if Drive isn't available) and gives you a local CSV path to work from.
2. Use that skill's `scripts/match_collection.py` — specifically `load_collection_with_binders` + `check_cards_binder_aware` (not the plain `load_collection`/`check_cards`) — to cross-reference candidates against ownership. The binder-aware pair distinguishes cards that are actually free to use from cards already sleeved into another one of the user's decks; the plain pair would silently treat both as "owned." Don't hand-roll this matching logic here, it's already written and tested there.
3. Match by **exact printing** (name + set + collector number), not just name — a deck can call for a printing the user doesn't actually have even if they own the card in some other set.
4. **Surface `needs_pull` results explicitly** rather than quietly including the card as if it were free — e.g. "Swords to Plowshares is owned, but your only copy is currently in Tribal Cat (2017)." Default to flagging, not excluding: the user may want to break the other deck down for parts. Only drop a needs_pull card from consideration if the user has said existing decks should stay intact.
5. If the user provides a starting wishlist/decklist that's larger than a legal deck size, treat it as a card pool to trim, not a finished list — cut down to the target size using the same reasoning as section 4.
6. If you want to search the *whole* collection for upgrades (not just a given wishlist), you don't have card colors/types in the raw CSV — cross-reference candidate card names you already know are relevant against the collection using `load_collection_by_name`, and verify anything you're not 100% certain about via web search (see section 5) before recommending it. Don't assume a card is on-color or does what you remember without checking if it's going into the final list.

## 4. Making cuts and additions — show your reasoning

When trimming a pool or proposing upgrades, state *why* each cut or addition happens, not just the final list. The user should be able to tell at a glance: what got removed, what replaced it, and what functional role changed. Group changes by reason (e.g. "redundant with X", "off-curve", "strictly upgraded by Y") rather than listing them as an undifferentiated wall — this is what actually lets the user sanity-check the work instead of just trusting it.

Use the categories in `/mnt/skills/user/mtg-card-taxonomy/references/MTG-Card-Function-Tags.md` to reason about *balance*, not just individual card quality — e.g. "this pool has 8 pieces of interaction and 1 combat trick" is a more useful diagnostic than evaluating each card in isolation. **If that file isn't found** (the `mtg-card-taxonomy` skill isn't installed), fall back to your own judgment on functional categories — the reasoning in this section still applies without the formal taxonomy — and mention to the user that installing `mtg-card-taxonomy` would give more consistent tagging across skills.

## 5. Verify every card that makes the final cut

Don't rely on memory for a card's exact mana cost, color, type, or effect once it's actually going into a decklist — memory is a fine first pass for brainstorming candidates, but confirm before it's in the final list you hand the user. **Check the `mtg-collection` skill's Scryfall data cache first** (section 5 there) — it's a fast path for exactly this: oracle text, mana cost, type, color identity, and commander/standard/modern legality for cards already in the user's collection. Only fall back to a fresh web search + fetch (Scryfall or a card database) for cards not found in the cache, or for anything price-sensitive (the cache deliberately excludes prices). This matters most for:
- **Color identity** — an off-color card silently breaks the mana base (a card that looks like it fits can turn out to need a color the deck doesn't run)
- **Whether it's actually removal/interaction** vs. something narrower (artifact/enchantment-only answers, conditional removal, etc.) that plays a different role than assumed
- **Exact cost**, when it affects curve analysis or color-source math

A quick way to sanity-check yourself: if you're about to write a card's rules text from memory and you're not fully certain, that uncertainty is the signal to search before including it — not a reason to hedge the wording and hope it's close enough.

## 6. Handoff to other skills

Once the deck is finalized:
- **`mtg-decklist-export`** to produce the downloadable `.txt`
- **`mtg-visualization`** for the analysis dashboard
- **`mtg-primer`** for a written guide
- **`mtg-budget-swaps`** if the user wants cheaper alternatives (distinct from collection-building — that's "what to buy," this skill is "what to play with what you have")

Mention these proactively once a deck is done rather than waiting to be asked — the user often wants at least the export.
