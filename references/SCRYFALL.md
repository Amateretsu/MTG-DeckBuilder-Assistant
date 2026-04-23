# Scryfall Card Lookup Strategy

---

## Why the API Returns 403

The Scryfall REST API (`api.scryfall.com`) is **not fundamentally blocked** — it returns 403 because WebFetch sends a missing or generic `User-Agent` header, which Scryfall's bot-detection flags as suspicious traffic. Their documentation explicitly states: "default library values are flagged as suspicious."

The fix would be sending a descriptive header like `User-Agent: MTG-DeckBuilder/1.0`. WebFetch does not support custom headers, so this cannot be resolved at the tool level. **Use WebSearch as the primary strategy.** If a future MCP tool supports custom request headers, the API endpoint `https://api.scryfall.com/cards/named?exact={URL-encoded name}` would work correctly with proper headers.

**Error codes to know:**
| Code | Cause |
|---|---|
| 403 | Blocked as suspicious — missing/generic User-Agent |
| 429 | Rate limited — exceeded 10 requests/second |

For large-scale card data (full set lists, bulk oracle text), use Scryfall's bulk data downloads at `https://scryfall.com/docs/api/bulk-data` rather than individual API calls.

---

## Primary Strategy — WebSearch

### Single Card Lookup

```
"[Exact Card Name]" MTG scryfall oracle text set collector number
```

For **well-known cards** (released before 2025):
- Add `allowed_domains: ["scryfall.com"]`

For **unfamiliar set codes or post-cutoff cards**:
- Remove domain restriction
- Add year context: `"[Card Name]" MTG 2025 2026 oracle text scryfall`

### Batch Lookups

Fire up to 8 WebSearch calls **in parallel in a single message**. Never chain them one-at-a-time.

Prioritize these in every session:
1. The commander — always verify oracle text, never rely on memory
2. All cards with post-2024 or unrecognized set codes
3. Every new card being proposed as an addition

---

## What to Record from Each Result

| Field | Why |
|---|---|
| Exact card name | Must match Scryfall `name` field exactly for the `.txt` line |
| Set code | Uppercased in the `.txt` line |
| Collector number | Exact string in the `.txt` line |
| Oracle text | Color identity check + mechanical fit check |
| Type line | Tribal compatibility check |

---

## Known Post-Cutoff Set Codes (2025–2026)

| Code | Set Name |
|---|---|
| FCA | Final Fantasy: Through the Ages |
| FIN | Magic: The Gathering — FINAL FANTASY |
| FIC | Final Fantasy Commander |
| ECL | Lorwyn Eclipsed |
| ECC | Lorwyn Eclipsed Commander |
| TLE | Avatar: The Last Airbender Eternal |
| EOE | Edge of Eternities |
| TDC | Tarkir: Dragonstorm Commander |

When encountering any unknown set code, search `MTG "[set code]" set name 2025 2026` before treating the card as suspicious or invalid.
