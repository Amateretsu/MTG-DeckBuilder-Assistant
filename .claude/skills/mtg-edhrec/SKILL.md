---
name: mtg-edhrec
description: Grounds Commander-format synergy suggestions in real community data — commander popularity/rank, commonly-run synergy cards, and known combo lines — via targeted WebSearch queries against EDHREC and Commander Spellbook. Use whenever a Commander-format synergy suggestion, a "what goes well with this commander" question, a "how popular/played is this commander" question, or a combo-finishing question needs real community signal instead of pure judgment. Used internally by mtg-deckbuilding (grounding synergy suggestions) and mtg-primer ("Why This Build vs. Similar Decks" section and combo-line write-ups). Commander-format only — EDHREC has no meaningful 60-card constructed equivalent, don't invoke this for non-Commander decks.
compatibility: Uses WebSearch only (already allowlisted in .claude/settings.json) — no new WebFetch domain, no external package, no pip install. This supersedes an earlier pyedhrec-package-based design for this skill, dropped because pip installs from PyPI aren't reachable in this project's execution environment; WebSearch has no such dependency.
---

# MTG EDHREC / Commander Synergy Data

Pulls three kinds of real community signal for a Commander deck via WebSearch, instead of relying on pure LLM judgment for "what goes with this commander":

1. **Commander popularity/rank** — how widely-played a commander is, and roughly how many decks are registered for it on EDHREC.
2. **Common synergy cards** — cards that show up disproportionately often in decks built around this commander, beyond generic goodstuff.
3. **Known combos** — verified combo lines involving this commander or a card in the deck.

## Why WebSearch, not a package or direct fetch

No package install and no new WebFetch domain needed — `WebSearch` is already allowlisted in `.claude/settings.json`, so this works today with zero permission changes. Search snippets are lower-precision than a structured API would be (no exact synergy percentages, no guaranteed up-to-date deck counts), so treat everything here as a **directional community signal to cite**, not an exact statistic to quote as if it were verified data — say "commonly paired with" or "frequently included," not a fabricated precise percentage that the search results didn't actually give you.

## 1. Commander popularity/rank

```
"<Commander Name>" edhrec rank number of decks
```

Add `site:edhrec.com` to prioritize EDHREC's own page for well-known commanders; drop the site restriction for a very recent or obscure commander where EDHREC's own page might not be well-indexed yet. Report what you actually find (approximate rank, deck count if stated) — if search results don't surface a number, say popularity data wasn't found rather than guessing one.

## 2. Common synergy cards

```
"<Commander Name>" edhrec high synergy cards
"<Commander Name>" edhrec top cards
```

Fire these in parallel with any other lookups you're already doing for the same commander — don't chain them one at a time. Cross-reference anything you pull back against the user's actual card pool/collection and format legality exactly as `mtg-deckbuilding` already does — this only adds a data-backed shortlist, it doesn't replace ownership or legality checks, and every card still needs Scryfall verification before it goes in a final decklist.

## 3. Known combos

```
"<Commander Name>" combo commanderspellbook
"<Card Name>" combo commanderspellbook
```

Commander Spellbook (commanderspellbook.com) documents verified, step-by-step combo lines and is generally more precise for this than EDHREC's own synergy data. When citing a combo, spell out the actual steps and what it produces (e.g. "Kinnan + Basalt Monolith + Staff of Domination is infinite mana — untap Monolith with Kinnan's trigger, spend through Staff for infinite colorless") — a card-name list alone isn't useful to someone who doesn't already know why. This mirrors `mtg-primer`'s existing Win Conditions section rule; when this skill's combo lookup is feeding that section, keep it consistent with that rule rather than restating combos more loosely here.

## What this data is and isn't

- **Is:** a real community-inclusion and combo signal to cite when it's genuinely available from search results.
- **Isn't:** a legality or oracle-text source (still verify every card via Scryfall before including it in output) and isn't pricing (use `mtg-budget-swaps`'s live Scryfall pricing for cost). Also isn't a guaranteed-current statistic — a search snippet can be stale; say so if a result looks dated rather than presenting it as this week's numbers.
- **Commander-only.** Don't call this for a 60-card constructed deck — EDHREC's and Commander Spellbook's data models are both commander-centric.

## Consumption notes for dependent skills

- **mtg-deckbuilding**: when suggesting synergy pieces for a Commander build, cross-check candidates against section 2's lookup — cite the actual signal ("commonly run alongside this commander" / "EDHREC lists this among top synergy cards") rather than presenting a suggestion as pure judgment when a real search result backs it. Still filter every candidate through the user's actual card pool/collection and format legality exactly as before.
- **mtg-primer**: the "Why This Build vs. Similar Decks" section (conditional — only when there's a genuinely comparable deck) can cite section 1/2 results as one concrete comparison point rather than an invented comparison; the Win Conditions section can use section 3's combo lookups for a verified step-by-step line instead of reconstructing one from memory. Still skip either section entirely if there's nothing informative to say, per that skill's existing rules.
