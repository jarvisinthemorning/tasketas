#!/usr/bin/env python3
"""Print simple offer rarity for one or more current Battlegrounds cards."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from comp_rarity import RarityUnavailable, calculate_card_rarity


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate conditional, uncontested card-offer rarity")
    parser.add_argument("card_ids", nargs="+", type=int)
    parser.add_argument("--cards", type=Path, default=ROOT / "data/cards.json")
    args = parser.parse_args()

    payload = json.loads(args.cards.read_text(encoding="utf-8"))
    results = []
    for card_id in args.card_ids:
        try:
            results.append(calculate_card_rarity(payload, card_id))
        except RarityUnavailable as error:
            results.append(
                {
                    "card_id": card_id,
                    "status": "unavailable",
                    "display": "Generated",
                    "reason": str(error),
                }
            )
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
