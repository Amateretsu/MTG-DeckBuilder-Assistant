---
name: mtg-collection
description: Fetches and reads the user's current Magic The Gathering card collection (a ManaBox export) before any task that depends on what cards they own, AND provides a fast-path cache of static Scryfall card data (oracle text, cost, type, legality) to speed up card verification. This is the single source of truth for both collection ownership data and cached card facts — always use this skill instead of re-deriving fetch logic or assuming a stale file whenever a task involves "my collection," "cards I own," building or trimming a deck from owned cards, checking whether specific printings are owned, cross-referencing a wishlist/decklist against ownership, or verifying a card's oracle text/legality. Other MTG skills (mtg-deckbuilding, and any future skill needing ownership data or card facts) depend on this skill and should call into it rather than hardcoding a CSV path or always doing a fresh web search.
compatibility: Requires Google Drive tool access to search and download from the user's "ManaBox Exports" folder (collection data — section 1). Falls back to an uploaded CSV or a static project file if Drive is unavailable — see section 2. The Scryfall data cache (section 5) requires web_fetch access to a public GitHub raw URL — no additional setup needed.
---

# MTG Collection Data

Single source of truth for "what cards does the user own." Every other MTG skill that needs ownership data should call into this skill rather than re-implementing collection lookup, hardcoding a CSV path, or assuming an old upload is current.

## 1. Fetching the latest collection export

The user maintains a Google Drive folder named **"ManaBox Exports"** where fresh CSV exports from the ManaBox app get dropped. Always pull the most recent file from there before any collection-aware task — never assume a stale upload or the project's static CSV is current.

Steps:
1. `Google Drive:search_files` with query `title contains 'ManaBox Exports' and mimeType = 'application/vnd.google-apps.folder'` to get the folder ID. Don't hardcode the folder ID — the folder could be recreated with a new one, so look it up each time you don't already have it fresh in context.
2. `Google Drive:search_files` with query `parentId = '<folder_id>'` to list its contents.
3. Sort results by `modifiedTime` descending and take the first — that's the active export. If multiple files share the same latest timestamp, flag it to the user rather than guessing which is authoritative.
4. `Google Drive:download_file_content` on that file's `fileId` to get the CSV content (base64-encoded).
5. Decode and write it to a local scratch path, e.g. `/tmp/manabox_collection.csv`, for use by `scripts/match_collection.py` or direct analysis.
6. If older exports are sitting alongside the newest one, flag them to the user (filenames + dates) so they can clear them out themselves — don't delete Drive files even if asked to "clean up automatically," since no delete/trash tool is available here regardless.

## 2. Fallback order if Drive is unavailable

1. Google Drive folder "ManaBox Exports" (preferred — always current)
2. A CSV the user uploaded directly in this conversation (`/mnt/user-data/uploads/*.csv`)
3. A static collection file already in project knowledge (e.g. a `ManaBox_Collection-*.csv`) — tell the user this may be stale and offer to check Drive instead
4. If none of the above exist, ask the user to export their collection from the ManaBox app (Collection tab → top-right menu → Export CSV) and either upload it here or drop it in the Drive folder

Don't silently fall back past step 1 — if the Drive search fails or comes back empty, say so before reaching for an older source, so the user knows they might be looking at outdated ownership data.

## 3. Working with the data once fetched

Use `scripts/match_collection.py` rather than hand-rolling CSV parsing — it's already written and tested:

- `load_collection(csv_path)` → `{(name, SET, collector_number): qty}` — for exact-printing lookups (does the user own *this specific* printing of a card), summed across every row regardless of where the card currently is
- `load_collection_by_name(csv_path)` → `{name: total_qty}` — for "do they own this card at all, in any printing"
- `check_cards(owned, candidates)` — cross-references a wishlist/candidate list against `owned`, returns `total_qty`, `missing`, `short`, and `ok`

**When it matters whether owned copies are actually free to use** (e.g. building or trimming a deck, where a card already sleeved into another existing deck isn't really available), use the binder-aware pair instead:

- `load_collection_with_binders(csv_path)` → `{(name, SET, collector_number): {"free": int, "committed": [{"deck": str, "qty": int}, ...], "total": int}}`, split using the CSV's `Binder Type` column (`"binder"` = loose/free, `"deck"` = currently sleeved into that named deck)
- `check_cards_binder_aware(owned, candidates)` — same shape as `check_cards`, plus a `needs_pull` list for candidates that are owned in total but don't have enough *free* copies; each entry names exactly which deck(s) the missing copies are sitting in

Default when presenting `needs_pull` results to the user: **flag it, don't silently exclude the card.** They may genuinely want to break down an old deck to build a new one — hiding that option isn't helpful. Only treat committed copies as unavailable if the user has said they want existing decks left intact.

See the docstrings in the script for exact usage examples.

## 4. CSV schema reference

Columns present in a ManaBox export: `Binder Name, Binder Type, Name, Set code, Set name, Collector number, Foil, Rarity, Quantity, ManaBox ID, Scryfall ID, Purchase price, Misprint, Altered, Condition, Language, Purchase price currency, Added`.

Notes:
- **Collector number** is compared as a raw string — ManaBox sometimes zero-pads, sometimes doesn't. Don't coerce to int.
- **Set code** should be uppercased for comparison.
- **Quantity** is per-row, per-binder — the same card can appear in multiple rows if it's filed across different binders/decks (e.g. "Kyle's Collection" and "Personal Collection"). Sum across rows for total ownership of a printing; `load_collection` and `load_collection_by_name` already do this correctly.
- **Binder Type** is `"binder"` for loose/general storage or `"deck"` for a copy currently sleeved into a named deck (given by `Binder Name`). A card can show as "owned" while every copy is actually committed to another deck — plain `load_collection`/`check_cards` don't distinguish this; use the binder-aware functions above when it matters.

## 5. Scryfall data cache (static card facts — oracle text, cost, type, legality)

Separate from the ManaBox export above (which tells you what you *own*), a weekly-refreshed cache of static Scryfall data lives in a **public GitHub repo**, maintained by a scheduled Claude Code routine — not this skill. Use it as a fast path for card facts during deckbuilding/verification (mtg-deckbuilding section 5 and similar) instead of always doing a fresh web search + fetch.

**Fetching it:**
```
web_fetch: https://raw.githubusercontent.com/Amateretsu/MTG-DeckBuilder-Assistant/refs/heads/main/data/scryfall_cache.csv
```
Always pass an explicit, high `text_content_token_limit` on this fetch — the default truncates well before reaching the end of the file at current collection size (rows are roughly alphabetical by name, so truncation cuts off later letters first).

**Schema** (CSV columns): `oracle_id, name, mana_cost, cmc, type_line, oracle_text, colors, color_identity, legalities_commander, legalities_standard, legalities_modern, scryfall_id`

**Why oracle_id, not name:** Scryfall documents that name isn't a fully safe identity key — rare cases (tokens, Unstable/joke variants) can share a printed name while being different cards with different oracle text. The cache is keyed by `oracle_id` specifically to stay correct in that edge case, while still collapsing multiple owned printings of the same real card into one row.

**What it deliberately does NOT contain:** prices. Never treat this cache as a price source — always fetch current pricing live (Scryfall search+fetch) for anything price-sensitive (e.g. `mtg-budget-swaps`).

**Truncation is safe, not silently wrong — treat it that way:** if a card you're looking for isn't in the portion of the file you got back, that's not proof it's uncached — it may just be past the cutoff. In that case, fall back to live Scryfall search+fetch exactly as you would for a card that's genuinely missing from the cache. **Never skip verification because you assume a card is "probably in there."** This cache only ever saves redundant lookups; it should never be the reason a card's text/cost/legality goes unverified.
