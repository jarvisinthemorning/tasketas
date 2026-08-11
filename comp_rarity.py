"""Simple, auditable Battlegrounds card-offer rarity estimates."""

from __future__ import annotations

import itertools
import math

STANDARD_TRIBES = (
    "beast",
    "demon",
    "dragon",
    "elemental",
    "mech",
    "murloc",
    "naga",
    "pirate",
    "quilboar",
    "undead",
)
POOL_COPIES = {1: 15, 2: 15, 3: 13, 4: 11, 5: 9, 6: 7, 7: 5}
SHOP_SLOTS = {1: 3, 2: 4, 3: 4, 4: 5, 5: 5, 6: 6, 7: 6}


class RarityUnavailable(ValueError):
    """Raised when the catalog cannot support an honest offer percentage."""


def _solo_pool_card(card: dict) -> bool:
    modes = {str(mode).lower() for mode in card.get("modes", [])}
    return card.get("pool") is True and (not modes or "solo" in modes)


def _tavern_card(card: dict, card_type: str) -> bool:
    categories = {str(category).lower() for category in card.get("categories", [])}
    return (
        _solo_pool_card(card)
        and card.get("type") == card_type
        and (not categories or "tavern" in categories)
    )


def _tribes(card: dict) -> set[str]:
    return {
        str(tribe).strip().lower()
        for tribe in card.get("tribes", [])
        if str(tribe).strip().lower() in STANDARD_TRIBES
    }


def _legal_in_lobby(card: dict, active_tribes: frozenset[str]) -> bool:
    required = _tribes(card)
    return not required or not required.isdisjoint(active_tribes)


def _at_least_one(total: int, target: int, slots: int) -> float:
    if total <= 0 or target <= 0 or slots <= 0:
        return 0.0
    draw = min(total, slots)
    misses = total - target
    if misses < draw:
        return 1.0
    return 1 - math.comb(misses, draw) / math.comb(total, draw)


def _minion_rarity(cards: list[dict], target: dict) -> dict:
    if not _tavern_card(target, "minion"):
        raise RarityUnavailable(
            f"{target.get('name', target.get('id'))} is not a Tavern-pool minion"
        )
    tier = target.get("tier")
    if not isinstance(tier, int) or tier not in POOL_COPIES:
        raise ValueError(f"Minion {target.get('name', target.get('id'))} has no supported Tavern Tier")
    required_tribes = _tribes(target)
    lobbies = [
        frozenset(combo)
        for combo in itertools.combinations(STANDARD_TRIBES, 5)
        if not required_tribes or not required_tribes.isdisjoint(combo)
    ]
    probabilities: list[float] = []
    for lobby in lobbies:
        total = 0
        target_copies = 0
        for card in cards:
            card_tier = card.get("tier")
            if (
                not _tavern_card(card, "minion")
                or not isinstance(card_tier, int)
                or card_tier > tier
                or card_tier not in POOL_COPIES
                or not _legal_in_lobby(card, lobby)
            ):
                continue
            copies = POOL_COPIES[card_tier]
            total += copies
            if int(card.get("id", -1)) == int(target["id"]):
                target_copies += copies
        probabilities.append(_at_least_one(total, target_copies, SHOP_SLOTS[tier]))
    probability = sum(probabilities) / len(probabilities) if probabilities else 0.0
    tribe_note = ", ".join(sorted(required_tribes))
    return {
        "probability": probability,
        "percent": round(probability * 100, 1),
        "basis": f"per refresh at Tavern Tier {tier}",
        "conditional_tribes": sorted(required_tribes),
        "assumption": (
            f"needed tribe active ({tribe_note}), uncontested full pool"
            if required_tribes
            else "uncontested full pool"
        ),
    }


def _single_offer_rarity(cards: list[dict], target: dict) -> dict:
    tier = target.get("tier")
    if not isinstance(tier, int):
        categories = {
            str(category).strip().lower()
            for category in target.get("categories", [])
            if str(category).strip() and str(category).strip().lower() != "tavern"
        }
        if not categories:
            raise RarityUnavailable(
                f"Spell {target.get('name', target.get('id'))} has no rarity pool"
            )
        category = sorted(categories)[0]
        eligible = [
            card
            for card in cards
            if _solo_pool_card(card)
            and card.get("type") == "spell"
            and category in {str(value).strip().lower() for value in card.get("categories", [])}
        ]
        probability = 1 / len(eligible) if eligible else 0.0
        return {
            "probability": probability,
            "percent": round(probability * 100, 1),
            "basis": f"per random {category} roll",
            "conditional_tribes": [],
            "assumption": f"current Solo {category} spells are equally likely",
        }
    eligible = [
        card
        for card in cards
        if _tavern_card(card, "spell")
        and isinstance(card.get("tier"), int)
        and card["tier"] <= tier
    ]
    probability = 1 / len(eligible) if eligible else 0.0
    return {
        "probability": probability,
        "percent": round(probability * 100, 1),
        "basis": f"per Tavern-spell offer at Tier {tier}",
        "conditional_tribes": [],
        "assumption": "eligible Tavern spells are equally likely",
    }


def _four_choice_rarity(cards: list[dict], target: dict) -> dict:
    card_type = target["type"]
    pool_type = "trinket" if card_type == "trinket" else "hero"
    eligible = [card for card in cards if _solo_pool_card(card) and card.get("type") == pool_type]
    probability = min(4, len(eligible)) / len(eligible) if eligible else 0.0
    label = "Trinket offer" if card_type == "trinket" else "Hero selection"
    is_baseline = card_type == "trinket"
    return {
        "probability": probability,
        "percent": round(probability * 100, 1),
        "basis": (
            f"catalog baseline per four-choice {label}"
            if is_baseline
            else f"per four-choice {label}"
        ),
        "conditional_tribes": [],
        "assumption": (
            "four equally likely choices from the current Solo trinket catalog; eligibility modifiers ignored"
            if is_baseline
            else "four hero choices from the current selectable Solo hero catalog"
        ),
        "estimate": is_baseline,
    }


def calculate_card_rarity(cards_payload: dict, card_id: int) -> dict:
    """Estimate one card's chance in its relevant offer, conditional and uncontested."""
    cards_by_id = cards_payload.get("cards", {})
    target = cards_by_id.get(str(card_id)) or cards_by_id.get(card_id)
    if not isinstance(target, dict):
        raise ValueError(f"Unknown card ID: {card_id}")
    cards = [card for card in cards_by_id.values() if isinstance(card, dict)]
    card_type = target.get("type")
    if card_type == "minion":
        result = _minion_rarity(cards, target)
    elif card_type == "spell":
        result = _single_offer_rarity(cards, target)
    elif card_type in {"trinket", "hero_power"}:
        result = _four_choice_rarity(cards, target)
    else:
        raise RarityUnavailable(
            f"Unsupported rarity type for {target.get('name', card_id)}: {card_type}"
        )
    return {"card_id": int(target["id"]), "type": card_type, **result}
