# EDHREC Card Discovery

EDHREC aggregates Commander deck data from Moxfield, Archidekt, and Scryfall. Use it in Phase 3 to surface high-synergy candidates before finalizing cuts and additions, and to pressure-test proposed changes against community consensus.

EDHREC pages are accessible via **WebFetch** (no 403 issues unlike Scryfall API).

---

## URL Construction

**Pattern:** `https://edhrec.com/commanders/[slug]`

**Slug rules:** Lowercase the commander name → replace spaces with hyphens → strip all punctuation (commas, apostrophes, periods, colons).

| Commander | Slug |
|---|---|
| Kibo, Uktabi Prince | `kibo-uktabi-prince` |
| Atraxa, Praetors' Voice | `atraxa-praetors-voice` |
| Tymna the Weaver | `tymna-the-weaver` |
| K'rrik, Son of Yawgmoth | `krik-son-of-yawgmoth` |

---

## Two Pages to Fetch

Fetch both in parallel at the start of Phase 3:

| URL | What it shows |
|---|---|
| `edhrec.com/commanders/[slug]` | All recommended cards, sorted by synergy |
| `edhrec.com/commanders/[slug]/commander-matters` | Filtered to cards that directly interact with the commander's mechanics |

---

## Reading the Data

EDHREC returns two metrics per card. They mean different things:

**Inclusion %** — What percentage of tracked decks with this commander include this card.
- High inclusion (>70%) = community consensus; likely correct for this deck
- Low inclusion with high synergy = niche but specifically powerful with this commander

**Synergy %** — How much MORE often this card appears with this commander compared to general decks of the same color identity.
- High synergy (>50%) = commander-specific fit; not just a good Gruul card, a good *Kibo* card
- Negative synergy = card is actually less popular with this commander than in the color in general

**Prioritize high-synergy cards for additions.** They represent what the community has discovered is uniquely good with this commander. High-inclusion, low-synergy cards are often mana rocks and staples that belong in any deck of the color — useful but not informative about this commander's identity.

---

## How to Use in Phase 3

1. **Before listing any candidates**, fetch both EDHREC pages and record the top 10–15 High Synergy cards
2. **When evaluating additions**: cross-reference each candidate against the High Synergy list — a card the community rates highly that is missing from the current list is a strong addition
3. **When evaluating cuts**: if a card you're considering cutting has >60% inclusion and >40% synergy, note that in the cut reasoning — it may be a mistake
4. **Do not override the color identity gate**: EDHREC can suggest cards outside the commander's color identity in error. All candidates still must pass `DECK_RULES.md` Step 4 before being named

---

## Sample Size Caveat

EDHREC's data quality scales with deck count. Note the tracked deck count shown on the page:
- **<50 decks**: directionally useful, not authoritative — treat as hints, not verdicts
- **50–500 decks**: reliable community signal for most card decisions
- **500+ decks**: high confidence; inclusion and synergy percentages are statistically meaningful
