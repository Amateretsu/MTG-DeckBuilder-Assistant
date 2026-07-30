#!/usr/bin/env python3
"""
Exact hypergeometric draw-probability math for a Magic The Gathering deck.

Usage as a library (preferred — import and call from a one-off script so you
can print exactly what's relevant to the current question):

    from hypergeometric import probability_at_least, opening_hand_probability, by_turn_probability

    # Odds of at least 3 lands in a 7-card opening hand, 99-card deck, 37 lands
    p = opening_hand_probability(deck_size=99, successes_in_deck=37, hand_size=7, at_least=3)

    # Odds of at least 1 black source by turn 3, on the play, 60-card deck, 9 black sources
    p = by_turn_probability(deck_size=60, successes_in_deck=9, turn=3, on_play=True, at_least=1)

Also runnable directly for a quick gut-check:

    python3 hypergeometric.py <deck_size> <successes_in_deck> <sample_size> <at_least>

Notes:
- This models drawing without replacement, which is how a deck actually works
  (unlike a binomial approximation, which assumes replacement and is subtly
  wrong for small deck sizes like a 60 or 99-card deck).
- "successes_in_deck" depends on the question — total lands for a land check,
  every source of a specific color for a color check, every card matching a
  taxonomy category for an effect check. See the mtg-consistency SKILL.md for
  how to pick the right count.
- on_play=True means no draw step on turn 1 (7 cards seen by turn 1, 7 + (N-1)
  by turn N); on_play=False means a draw step every turn (7 + N by turn N).
"""

import sys
from math import comb


def probability_exactly(deck_size, successes_in_deck, sample_size, exactly):
    """P(exactly `exactly` successes) drawing `sample_size` cards from a deck of `deck_size`."""
    if exactly > successes_in_deck or exactly > sample_size:
        return 0.0
    failures_in_deck = deck_size - successes_in_deck
    failures_drawn = sample_size - exactly
    if failures_drawn > failures_in_deck or failures_drawn < 0:
        return 0.0
    return (
        comb(successes_in_deck, exactly)
        * comb(failures_in_deck, failures_drawn)
        / comb(deck_size, sample_size)
    )


def probability_at_least(deck_size, successes_in_deck, sample_size, at_least):
    """P(at least `at_least` successes) drawing `sample_size` cards from a deck of `deck_size`."""
    upper = min(successes_in_deck, sample_size)
    return sum(
        probability_exactly(deck_size, successes_in_deck, sample_size, k)
        for k in range(at_least, upper + 1)
    )


def opening_hand_probability(deck_size, successes_in_deck, hand_size=7, at_least=1):
    """P(at least `at_least` successes) in an opening hand of `hand_size` cards."""
    return probability_at_least(deck_size, successes_in_deck, hand_size, at_least)


def by_turn_probability(deck_size, successes_in_deck, turn, on_play=True, hand_size=7, at_least=1):
    """
    P(at least `at_least` successes) seen by a given turn.

    on_play=True: no draw step turn 1, so cards seen by turn N = hand_size + (N - 1).
    on_play=False (on the draw): a draw step every turn, cards seen by turn N = hand_size + N.
    """
    cards_seen = hand_size + (turn - 1 if on_play else turn)
    cards_seen = min(cards_seen, deck_size)
    return probability_at_least(deck_size, successes_in_deck, cards_seen, at_least)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <deck_size> <successes_in_deck> <sample_size> <at_least>")
        sys.exit(1)
    deck_size, successes_in_deck, sample_size, at_least = (int(a) for a in sys.argv[1:])
    p = probability_at_least(deck_size, successes_in_deck, sample_size, at_least)
    print(f"P(at least {at_least} in {sample_size} drawn from {deck_size}, {successes_in_deck} successes) = {p:.4f}")
