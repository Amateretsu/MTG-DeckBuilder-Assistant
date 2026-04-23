# Deck Rules Gate

Complete every step in order. Do not evaluate, select, or name any card until this gate is fully written out.

---

## Step 1 — Commander Color Identity

Look up the commander using the strategy in `references/SCRYFALL.md`. From the oracle text result, list every colored mana symbol found in:
- The mana cost
- ALL rules text: activated abilities, triggered abilities, static abilities, token creation text, reminder text

That complete set of colors is the deck's **legal color identity**.

Write it out explicitly before continuing:

```
Commander: [Name]
Legal colors: [e.g., Red, Green]
Banned colors: [e.g., White, Blue, Black]
```

---

## Step 2 — Format Constraints

| Constraint | Rule |
|---|---|
| Deck size | Exactly 100 cards including commander |
| Singletons | Max 1 copy per card (basic lands exempt) |
| Color identity | Every card must be a subset of the commander's identity |
| Commander zone | Commander listed in `Commander` section; 99 others in `Deck` section |

---

## Step 3 — Tribal / Mechanical Theme

From the commander's oracle text, extract:
- **Tribal types**: creature types explicitly named in the text (e.g., "Ape or Monkey")
- **Core mechanic**: what the commander rewards or enables
- **Tokens**: any tokens created — check the token's own text for additional color symbols

Write these out. They drive card selection in Phase 3.

---

## Step 4 — Color Identity Filter (hard gate)

Before placing any card on a candidate list, run this check:

1. Does its mana cost contain a symbol outside the legal colors? → **Cut it.**
2. Does its rules text contain a colored mana symbol outside legal colors? → **Cut it.**
3. Is it a land that produces only colors outside the legal identity? → **Cut it.**

Do not note rejects as "close calls." Do not include them provisionally. Drop and move on.
