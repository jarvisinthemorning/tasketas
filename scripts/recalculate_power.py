#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from comp_pipeline import build_index, publish_comp
from comp_power import (
    CHECKPOINT_TURN,
    DEFAULT_SEED,
    DEFAULT_SIMULATIONS,
    recalculate_registry,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministically recalculate composition probability and power"
    )
    parser.add_argument("--simulations", type=int, default=DEFAULT_SIMULATIONS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--checkpoint-turn", type=int, default=CHECKPOINT_TURN)
    parser.add_argument(
        "--base-url",
        default="https://jarvisinthemorning.github.io/tasketas",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Update registry and artifacts without rebuilding static pages",
    )
    args = parser.parse_args()

    registry_path = ROOT / "data/registry.json"
    cards_path = ROOT / "data/cards.json"
    simulations_dir = ROOT / "data/simulations"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    cards = json.loads(cards_path.read_text(encoding="utf-8"))
    updated = recalculate_registry(
        registry,
        cards,
        simulation_dir=simulations_dir,
        simulations=args.simulations,
        seed=args.seed,
        checkpoint_turn=args.checkpoint_turn,
    )
    registry_path.write_text(
        json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    rendered = 0
    if not args.no_render:
        for entry in updated.get("pages", []):
            if "p80_power" not in entry:
                continue
            content_path = ROOT / "content" / f"{entry['slug']}.md"
            if not content_path.is_file():
                raise FileNotFoundError(f"Missing guide source for simulated comp: {content_path}")
            publish_comp(
                content_path=content_path,
                cards_path=cards_path,
                registry_path=registry_path,
                template_path=ROOT / "templates/comp.html",
                output_dir=ROOT / "dist",
                public_base_url=args.base_url,
                register=False,
            )
            rendered += 1
        build_index(
            registry_path=registry_path,
            cards_path=cards_path,
            template_path=ROOT / "templates/index.html",
            output_dir=ROOT / "dist",
        )

    evaluated = sum("p80_power" in page for page in updated.get("pages", []))
    print(
        f"Updated {evaluated} compositions at Turn {args.checkpoint_turn}; "
        f"rendered {rendered}; artifacts: {simulations_dir}/*.json.gz"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
