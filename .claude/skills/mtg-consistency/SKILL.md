---
name: mtg-consistency
description: Computes real draw-probability numbers (hypergeometric distribution) for a Magic The Gathering deck — odds of hitting N lands, a given color source, or a named card type by a given turn or in an opening hand. Use whenever a mulligan/opening-hand assessment, a "how consistent is this manabase" question, or a land-count sanity check needs an actual number instead of narrative judgment. Used internally by mtg-primer (Gameplan & Mulligan Guide section) and mtg-deckbuilding (land-count/color-source sanity checks) — trigger directly if the user asks a standalone probability question, e.g. "what are the odds I have 3 lands in my opening hand" or "how likely am I to draw a black source by turn 3".
compatibility: Self-contained — scripts/hypergeometric.py uses only the Python standard library (math.comb), no external dependency and no network access needed.
---

# MTG Consistency / Draw-Probability Calculator

Computes exact hypergeometric probabilities for drawing cards from a Magic deck — the actual math behind "how likely am I to have X by turn Y," rather than a gut-feel estimate.

## Why this exists

`mtg-primer`'s Gameplan & Mulligan Guide section already caveats its own hand-assessment reasoning as "informed guesses, not tested" — Claude hasn't piloted the deck. That caveat can't go away, but the *land-count and color-source* part of a mulligan decision is genuinely computable from deck composition alone. Use this skill to cite a real number for that part, and keep the narrative-judgment caveat for everything else (sequencing, matchup knowledge, actual play experience).

## Usage

Import and call from a one-off script, same pattern as `mtg-collection`'s `match_collection.py`:

```python
from hypergeometric import probability_at_least, opening_hand_probability, by_turn_probability

# Odds of at least 3 lands in a 7-card opening hand, 99-card deck, 37 lands
p = opening_hand_probability(deck_size=99, successes_in_deck=37, hand_size=7, at_least=3)

# Odds of having drawn at least 1 black source by turn 3, on the play, 60-card deck
p = by_turn_probability(deck_size=60, successes_in_deck=9, turn=3, on_play=True, at_least=1)
```

`scripts/hypergeometric.py` is also runnable directly for a quick check:

```
python3 hypergeometric.py <deck_size> <successes_in_deck> <sample_size> <at_least>
```

## What counts as a "success"

Depends on the question being asked — pick the right count from the actual decklist, don't guess:
- **Land count check**: total lands in the deck (including any nonbasic that counts as a land).
- **Color source check**: every card that produces that specific color — basics of that color, duals/fetches/shocks that produce it, and any nonland mana rock/dork that taps for it. Don't count only basics.
- **Card-type/effect check** (e.g. "odds of a removal spell by turn 4"): every card tagged with the relevant `mtg-card-taxonomy` category, not just an intuitive subset.

## Sample size — opening hand vs. by-turn

- **Opening hand**: `hand_size` (7 for a fresh game; adjust for a scryed/mulliganed hand if the user specifies one).
- **By a given turn**: cards seen = hand size + cards drawn. On the play, you don't draw turn 1, so by turn *N* you've seen `hand_size + (N - 1)` cards; on the draw, `hand_size + N`. `by_turn_probability()` takes `on_play` as an explicit argument rather than assuming — always ask or infer which applies before computing.

## Presenting results

State the actual percentage and what it's conditional on ("62% to have 3+ lands in your opening 7, given 37 lands in 99") rather than just a bare number — that's what lets `mtg-primer`'s example-hand assessments read as reasoned rather than asserted. When a number is being used to justify a mulligan decision, name the threshold you're checking against (a commonly-used baseline is wanting roughly 60%+ for a "comfortable" keep on lands alone) rather than leaving the reader to infer whether the number is good or bad.
