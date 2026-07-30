#!/usr/bin/env python3
"""
Cross-reference a candidate card list against a ManaBox collection export.

Usage as a library (preferred — import and call from a one-off script so you
can print exactly what's relevant to the current task):

    from match_collection import load_collection, check_cards

    owned = load_collection("/mnt/user-data/uploads/ManaBox_Collection.csv")
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


def check_cards(owned, candidates):
    """
    candidates: list of {"name": str, "set": str, "cn": str, "qty": int}
    Returns dict with total_qty, missing (list), short (list of (candidate, have)), ok (bool).
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


def _main():
    if len(sys.argv) != 3:
        print("Usage: python3 match_collection.py <collection.csv> <candidates.json>")
        sys.exit(1)

    owned = load_collection(sys.argv[1])
    with open(sys.argv[2]) as f:
        candidates = json.load(f)

    result = check_cards(owned, candidates)

    print(f"Total requested quantity: {result['total_qty']}")
    if result["missing"]:
        print("\n--- MISSING (0 owned at this exact printing) ---")
        for m in result["missing"]:
            print(f"  {m['qty']}x {m['name']} ({m['set']}) {m['cn']}")
    if result["short"]:
        print("\n--- SHORT (own fewer copies than requested) ---")
        for c, have in result["short"]:
            print(f"  want {c['qty']}x {c['name']} ({c['set']}) {c['cn']} — have {have}")
    if result["ok"]:
        print("\nAll quantities OK, fully owned.")


if __name__ == "__main__":
    _main()
