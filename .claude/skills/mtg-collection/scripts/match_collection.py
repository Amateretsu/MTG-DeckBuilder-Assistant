#!/usr/bin/env python3
"""
Cross-reference a candidate card list against a ManaBox collection export.

Usage as a library (preferred — import and call from a one-off script so you
can print exactly what's relevant to the current task):

    from match_collection import load_collection, check_cards

    # csv_path should point at whatever the mtg-collection skill's fetch step
    # produced (e.g. /tmp/manabox_collection.csv from the Drive "ManaBox
    # Exports" folder) — see the mtg-collection skill for how to get it.
    owned = load_collection("/tmp/manabox_collection.csv")
    result = check_cards(owned, [
        {"name": "Swords to Plowshares", "set": "AFC", "cn": "75", "qty": 1},
        {"name": "Prison Realm",         "set": "WAR", "cn": "26", "qty": 3},
    ])
    print(result["total_qty"])       # sum of all requested quantities
    print(result["missing"])         # entries with 0 owned at that exact printing
    print(result["short"])           # entries where owned < requested
    print(result["ok"])              # bool — True if nothing missing or short

Also runnable directly for a quick gut-check:

    python3 match_collection.py <collection.csv> <candidates.json>

where candidates.json is a JSON array of {"name", "set", "cn", "qty"} objects.

Notes:
- Matching is by exact printing (name + set code + collector number), not just
  card name — a deck built from "any copy" of a card the user owns can name a
  printing they don't actually have if you match on name alone.
- Set code is uppercased for comparison; collector number is compared as the
  raw string from the CSV (ManaBox sometimes zero-pads, sometimes doesn't —
  don't coerce to int).
- If you need to check whether a card is owned *at all* regardless of
  printing (e.g. "do they own a copy of Lightning Strike anywhere"), use
  load_collection_by_name() instead — see below.
- If you need to know whether owned copies are actually free to use, or
  currently sleeved into another deck, use load_collection_with_binders() +
  check_cards_binder_aware() instead of load_collection()/check_cards() — see
  below. A card can show as "owned" while every copy is committed to another
  deck; the plain functions above don't distinguish that.
"""

import csv
import json
import sys
from collections import defaultdict


def load_collection(csv_path):
    """Load a ManaBox export into {(name, SET, collector_number): total_qty}."""
    owned = defaultdict(int)
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                row["Name"].strip(),
                row["Set code"].strip().upper(),
                row["Collector number"].strip(),
            )
            owned[key] += int(row["Quantity"])
    return owned


def load_collection_by_name(csv_path):
    """Load a ManaBox export into {name: total_qty_across_all_printings}.

    Use this when the deck doesn't care which printing, just whether the
    card is owned at all and how many copies exist across the whole collection.
    """
    owned = defaultdict(int)
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owned[row["Name"].strip()] += int(row["Quantity"])
    return owned


def load_collection_with_binders(csv_path):
    """Load a ManaBox export into a per-printing free-vs-committed breakdown.

    ManaBox's "Binder Type" column is "binder" for general storage (loose
    copies, not tied to any deck) or "deck" for a copy currently sleeved into
    a named deck (given by "Binder Name", e.g. "Tribal Cat (2017)"). Summing
    Quantity across all rows (what load_collection() does) treats both the
    same — a card entirely sleeved into an existing deck reads as "owned"
    even though there isn't actually a free copy to put in a new one.

    Returns:
        {(name, SET, collector_number): {
            "free": int,                          # loose copies, binder-type rows
            "committed": [{"deck": str, "qty": int}, ...],  # per-deck breakdown
            "total": int,                         # free + sum(committed qty)
        }}
    """
    owned = defaultdict(lambda: {"free": 0, "committed": [], "total": 0})
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                row["Name"].strip(),
                row["Set code"].strip().upper(),
                row["Collector number"].strip(),
            )
            qty = int(row["Quantity"])
            binder_type = row["Binder Type"].strip().lower()
            binder_name = row["Binder Name"].strip()

            entry = owned[key]
            entry["total"] += qty
            if binder_type == "deck":
                entry["committed"].append({"deck": binder_name, "qty": qty})
            else:
                entry["free"] += qty
    return dict(owned)


def check_cards(owned, candidates):
    """
    candidates: list of {"name": str, "set": str, "cn": str, "qty": int}
    Returns dict with total_qty, missing (list), short (list of (candidate, have)), ok (bool).

    Note: this treats a card sleeved into another deck the same as a loose
    copy — it only tells you whether it's owned at all, not whether it's
    actually free to use. Use check_cards_binder_aware() when that distinction
    matters (e.g. building a new deck and wanting to know what needs pulling
    from an existing one).
    """
    total_qty = 0
    missing = []
    short = []
    for c in candidates:
        key = (c["name"].strip(), c["set"].strip().upper(), str(c["cn"]).strip())
        have = owned.get(key, 0)
        total_qty += c["qty"]
        if have == 0:
            missing.append(c)
        elif have < c["qty"]:
            short.append((c, have))
    return {
        "total_qty": total_qty,
        "missing": missing,
        "short": short,
        "ok": not missing and not short,
    }


def check_cards_binder_aware(owned, candidates):
    """
    Binder-aware version of check_cards() — distinguishes "owned and free"
    from "owned but currently sleeved into another deck."

    owned: output of load_collection_with_binders()
    candidates: list of {"name": str, "set": str, "cn": str, "qty": int}

    Returns dict with:
        total_qty:   sum of all requested quantities
        missing:     candidates with 0 owned at all (free + committed == 0)
        short:       candidates where total owned (free + committed) < requested —
                     genuinely don't own enough copies regardless of source
        needs_pull:  candidates where free alone isn't enough but free + committed
                     covers it — i.e. owned, but some copies need to be pulled out
                     of another deck. Each entry is
                     (candidate, free_have, total_have, committed_list) where
                     committed_list is [{"deck": str, "qty": int}, ...] for that
                     printing, so you can tell the user exactly which deck(s)
                     to pull from.
        ok:          True only if free copies alone cover every candidate —
                     nothing missing, short, or needing a pull from another deck.

    Default behavior when presenting needs_pull to the user: flag it, don't
    silently exclude the card — the user may well want to break down an old
    deck to build a new one, and hiding that tradeoff isn't helpful. Only
    treat needs_pull entries as unavailable if the user has said they want
    existing decks left intact.
    """
    total_qty = 0
    missing = []
    short = []
    needs_pull = []
    for c in candidates:
        key = (c["name"].strip(), c["set"].strip().upper(), str(c["cn"]).strip())
        entry = owned.get(key)
        total_qty += c["qty"]

        if entry is None or entry["total"] == 0:
            missing.append(c)
            continue

        free_have = entry["free"]
        total_have = entry["total"]

        if total_have < c["qty"]:
            short.append((c, total_have))
        elif free_have < c["qty"]:
            needs_pull.append((c, free_have, total_have, entry["committed"]))
        # else: fully covered by free copies, no flag needed

    return {
        "total_qty": total_qty,
        "missing": missing,
        "short": short,
        "needs_pull": needs_pull,
        "ok": not missing and not short and not needs_pull,
    }


def _main():
    if len(sys.argv) != 3:
        print("Usage: python3 match_collection.py <collection.csv> <candidates.json>")
        sys.exit(1)

    owned = load_collection_with_binders(sys.argv[1])
    with open(sys.argv[2]) as f:
        candidates = json.load(f)

    result = check_cards_binder_aware(owned, candidates)

    print(f"Total requested quantity: {result['total_qty']}")
    if result["missing"]:
        print("\n--- MISSING (0 owned at this exact printing) ---")
        for m in result["missing"]:
            print(f"  {m['qty']}x {m['name']} ({m['set']}) {m['cn']}")
    if result["short"]:
        print("\n--- SHORT (own fewer total copies than requested) ---")
        for c, have in result["short"]:
            print(f"  want {c['qty']}x {c['name']} ({c['set']}) {c['cn']} — have {have} total")
    if result["needs_pull"]:
        print("\n--- OWNED BUT COMMITTED (need to pull from another deck) ---")
        for c, free_have, total_have, committed in result["needs_pull"]:
            print(f"  want {c['qty']}x {c['name']} ({c['set']}) {c['cn']} — {free_have} free, {total_have} total")
            for entry in committed:
                print(f"      {entry['qty']}x currently in \"{entry['deck']}\"")
    if result["ok"]:
        print("\nAll quantities OK, fully covered by free copies.")


if __name__ == "__main__":
    _main()
