#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comp_pipeline import normalize_api_cards

API = "https://hsbg.cards/api/v1/cards"


def fetch_all_cards() -> list[dict]:
    cards: list[dict] = []
    offset = 0
    while True:
        query = urllib.parse.urlencode({"limit": 100, "offset": offset})
        request = urllib.request.Request(
            f"{API}?{query}",
            headers={"User-Agent": "battlegrounds-comp-guides/0.1"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        batch = payload.get("data", [])
        cards.extend(batch)
        next_offset = payload.get("pagination", {}).get("nextOffset")
        if next_offset is None or not batch:
            break
        offset = int(next_offset)
    return cards


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the deterministic Battlegrounds card catalog")
    parser.add_argument("--output", type=Path, default=Path("data/cards.json"))
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    normalized = normalize_api_cards(fetch_all_cards(), generated_at=generated_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    current = sum(1 for card in normalized["cards"].values() if card["pool"])
    print(f"Wrote {len(normalized['cards'])} cards ({current} current) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
