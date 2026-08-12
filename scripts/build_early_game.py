#!/usr/bin/env python3
"""Build the standalone Season 14 early-game guide from the current card catalogue."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PACKAGES = [
    (1, "Bodies that do more", "Standalone tempo", "Efficient first buys that leave combat value or future resources.", [110101, 104551, 132792]),
    (1, "Buff into a shield", "Mini-synergy", "Mini-Myrmidon pushes Scarlet Survivor toward 6 Attack; the Shield is tempo, not a Dragon commitment.", [129749, 80738]),
    (1, "Gems without forcing Quilboar", "Economy", "Razorfen Geomancer supplies two flexible buffs; Tusked Camper grows while attacking. Buy the stats, not a tribe promise.", [70143, 122568]),
    (1, "Flexible gold and stats", "Economy", "Southsea Busker smooths next turn. Suspicious Prisonguard is a solid body whose paid +3/+3 can rescue a weak combat.", [98501, 132915]),
    (2, "Beetle bridge", "Mini-synergy", "Forest Rover improves Beetles and leaves one behind; Flittering Bat supplies extra Beast bodies to exploit the buff.", [115577, 132792]),
    (2, "Recruit-phase Beast hit", "Mini-synergy", "Lionfish turns a Tavern card into Fishbait; your left-most Beast attacks it and keeps the +5/+5 reward for combat.", [132794, 132802]),
    (2, "Cheap Mech reinforcement", "Mini-synergy", "Interpreter adds immediate stats to played or Magnetized Mechs; Cord Puller is a sturdy early target and summon.", [115678, 110101]),
    (2, "Economy that still boards", "Economy", "These bodies preserve value for a later turn. Take them when their current stats do not leave you exposed.", [64038, 80740, 97604]),
    (2, "Blood Gem combat package", "Soft direction", "Roadboar generates Gems while attacking; Prodigious Tusker converts other attacks into immediate Gem buffs. Useful bridge, not yet Core.", [70157, 122098]),
    (2, "Dragon combat burst", "Mini-synergy", "Electric Synthesizer buffs your other Dragons now and again at combat start. One good Dragon partner is enough; do not force the tribe.", [100026, 129749]),
    (3, "Wide-board stabilizer", "Standalone tempo", "Wolf Pup turns a reasonably full board into immediate combat stats. It is a stabilizer, not a Beast endgame signal.", [132806]),
    (3, "Undead pressure", "Bridge", "Dustbone permanently raises Undead Attack through Rally; Caretaker and Handless add multiple combat bodies.", [122229, 113158, 95265]),
    (3, "Mech shield reset", "Bridge", "Deflect-o-Bot becomes much stronger when Cord Puller or another Mech summons in combat; Prosthetic Hand adds Reborn and can Magnetize.", [61930, 110101, 112364]),
    (3, "Dragon shield bridge", "Bridge", "Amber Guardian protects another Dragon at combat start. Pair it with your best existing Dragon; it need not dictate the final comp.", [95006, 129749]),
    (3, "Gold with a body", "Economy", "Private Investigator is a 5/6 now and can bank +1 net Gold for next turn through Activate. Fruit Vendor converts spare Gold into flexible buffs.", [132318, 132917]),
    (3, "Gem bridge to a real decision", "Soft direction", "Gem Rat creates recurring Gem Days. Keep scaling if a genuine payoff arrives; otherwise use the Gems and remain open.", [116434]),
]


def load_cards(path: Path) -> dict[str, dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cards = raw.get("cards")
    if not isinstance(cards, dict):
        raise ValueError("cards.json must contain a cards mapping")
    return cards


def validate_card(card_id: int, expected_tier: int, cards: dict[str, dict]) -> dict:
    card = cards.get(str(card_id))
    if not card:
        raise ValueError(f"Unknown card ID: {card_id}")
    if card.get("type") != "minion" or card.get("pool") is not True:
        raise ValueError(f"Card {card_id} must be a current Tavern minion")
    if "solo" not in (card.get("modes") or []):
        raise ValueError(f"Card {card_id} is not Solo legal")
    tier = card.get("tier")
    if tier not in (1, 2, 3) or tier > expected_tier:
        raise ValueError(f"Card {card_id} must be Tavern Tier 1-{expected_tier}")
    if not card.get("image") or not card.get("detail"):
        raise ValueError(f"Card {card_id} lacks image/detail URL")
    return card


def render_card(card: dict) -> str:
    name = html.escape(card["name"])
    return f'''<a class="card" href="{html.escape(card['detail'])}" target="_blank" rel="noopener noreferrer">
      <img src="{html.escape(card['image'])}" alt="{name}" loading="lazy" width="512" height="686">
      <span>{name}</span>
    </a>'''


def render_packages(cards: dict[str, dict]) -> str:
    chunks = []
    current_tier = None
    for tier, title, label, purpose, ids in PACKAGES:
        if tier != current_tier:
            if current_tier is not None:
                chunks.append("</div></section>")
            chunks.append(f'<section class="tier-section" id="tier-{tier}"><div class="section-heading"><p class="kicker">Tavern {tier}</p><h2>Tier {tier} packages</h2></div><div class="package-grid">')
            current_tier = tier
        resolved = [validate_card(card_id, tier, cards) for card_id in ids]
        chunks.append(f'''<article class="package">
          <div class="package-copy"><span class="badge">{html.escape(label)}</span><h3>{html.escape(title)}</h3><p>{html.escape(purpose)}</p></div>
          <div class="card-row">{''.join(render_card(card) for card in resolved)}</div>
        </article>''')
    if current_tier is not None:
        chunks.append("</div></section>")
    return "\n".join(chunks)


def build(cards_path: Path, template_path: Path, output_path: Path) -> Path:
    cards = load_cards(cards_path)
    template = template_path.read_text(encoding="utf-8")
    marker = "{{PACKAGES}}"
    if template.count(marker) != 1:
        raise ValueError("Early-game template must contain exactly one {{PACKAGES}} marker")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.replace(marker, render_packages(cards)), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cards", type=Path, default=ROOT / "data/cards.json")
    parser.add_argument("--template", type=Path, default=ROOT / "templates/early-game.html")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/early-game.html")
    args = parser.parse_args()
    print(build(args.cards, args.template, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
