#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comp_pipeline import normalize_api_cards, validate_patch_name

API = "https://hsbg.cards/api/v1/cards"
PATCH_NOTES = "https://hsbg.cards/patch-notes/{patch}"
ROOT = Path(__file__).resolve().parents[1]


def active_output_path(root: Path = ROOT) -> Path:
    site = json.loads((root / "data/site.json").read_text(encoding="utf-8"))
    patch = validate_patch_name(site["latest_patch"])
    return root / "data/patches" / patch / "cards.json"


def active_patch(root: Path = ROOT) -> str:
    site = json.loads((root / "data/site.json").read_text(encoding="utf-8"))
    return validate_patch_name(site["latest_patch"])


def reconcile_patch_pool(cards: list[dict], patch_html: str, fetch_card) -> list[dict]:
    changes = {
        int(card_id): change
        for card_id, change in re.findall(
            r'data-card-id="(\d+)"(?:(?!data-card-id).)*?diff-badge-(returning|removed)',
            patch_html,
            flags=re.DOTALL,
        )
    }
    reconciled = [card for card in cards if changes.get(int(card["id"])) != "removed"]
    by_id = {int(card["id"]): index for index, card in enumerate(reconciled)}
    for card_id, change in changes.items():
        if change != "returning":
            continue
        card = dict(fetch_card(card_id))
        card["pool"] = True
        if card_id in by_id:
            reconciled[by_id[card_id]] = card
        else:
            by_id[card_id] = len(reconciled)
            reconciled.append(card)
    return reconciled


def fetch_patch_html(patch: str) -> str:
    request = urllib.request.Request(
        PATCH_NOTES.format(patch=urllib.parse.quote(patch)),
        headers={"User-Agent": "battlegrounds-comp-guides/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def fetch_card(card_id: int) -> dict:
    request = urllib.request.Request(
        f"{API}/{card_id}",
        headers={"User-Agent": "battlegrounds-comp-guides/0.1"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["data"]


def fetch_all_cards(patch: str | None = None) -> list[dict]:
    cards: list[dict] = []
    offset = 0
    while True:
        query = urllib.parse.urlencode({"pool": "current", "limit": 100, "offset": offset})
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
    if patch is not None:
        cards = reconcile_patch_pool(cards, fetch_patch_html(patch), fetch_card)
    return cards


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the deterministic Battlegrounds card catalog")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or active_output_path()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    normalized = normalize_api_cards(fetch_all_cards(active_patch()), generated_at=generated_at)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    current = sum(1 for card in normalized["cards"].values() if card["pool"])
    print(f"Wrote {len(normalized['cards'])} cards ({current} current) to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
