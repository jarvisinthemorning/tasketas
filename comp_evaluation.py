"""Experimental, auditable Battlegrounds composition evaluation helpers.

The shop model intentionally answers a narrow question: if a player reaches a
specified Tavern Tier and hard-rolls for the missing functional core over a
fixed number of 10-gold turns, how often is that core purchased? It is not an
attempt-level telemetry substitute and does not model Discovers, triples,
heroes, trinkets, selling economy, or survival.

Pool copies follow the Hearthstone Wiki Battlegrounds table captured on
2026-08-09: https://hearthstone.wiki.gg/wiki/Battlegrounds
"""

from __future__ import annotations

import itertools
import math
import random
from collections.abc import Iterable

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


def eligible_lobby_probability(
    required_tribe_count: int, *, total_tribes: int = 10, active_tribes: int = 5
) -> float:
    """Probability that every required tribe appears in a uniformly drawn lobby."""
    if required_tribe_count < 0 or required_tribe_count > active_tribes:
        return 0.0
    if total_tribes < active_tribes or required_tribe_count > total_tribes:
        return 0.0
    return math.comb(
        total_tribes - required_tribe_count, active_tribes - required_tribe_count
    ) / math.comb(total_tribes, active_tribes)


def classify_frequency(probability: float) -> str:
    """Readable label; callers should always display the probability too."""
    if probability >= 0.20:
        return "Common"
    if probability >= 0.05:
        return "Regular"
    if probability >= 0.01:
        return "Rare"
    if probability >= 0.001:
        return "High-roll"
    return "Lottery"


def calculate_baseline_gain(model: str, *, turns: int, parameters: dict) -> dict:
    """Calculate the transparent core-only scaling floor for a pilot comp."""
    if turns < 1:
        raise ValueError("turns must be positive")

    if model == "hogrider-core-v1":
        targets = int(parameters.get("other_quilboars", 5))
        cards_per_turn = int(parameters.get("choose_one_cards_per_turn", 1))
        hogriders = int(parameters.get("hogriders", 1))
        gem_attack = int(parameters.get("starting_gem_attack", 1))
        gem_health = int(parameters.get("starting_gem_health", 1))
        if min(targets, cards_per_turn, hogriders, gem_attack, gem_health) < 1:
            raise ValueError("Hogrider baseline parameters must be positive")
        gain = 0
        choices_played = 0
        for _ in range(turns):
            for _ in range(cards_per_turn):
                # Baseline fuel is Gem Day: alternate its +1 Attack / +1 Health
                # choices to avoid quietly optimizing one defensive matchup.
                if choices_played % 2 == 0:
                    gem_attack += 1
                else:
                    gem_health += 1
                choices_played += 1
                gain += hogriders * targets * (gem_attack + gem_health)
        return {
            "model": model,
            "projected_stat_gain": gain,
            "equation": "Gem Day upgrades one Blood Gem stat, then each Hogrider plays that Gem on every other Quilboar.",
        }

    if model == "demon-shop-consume-v1":
        felboars = int(parameters.get("felboars", 1))
        casts_per_turn = int(parameters.get("spell_casts_per_turn", 3))
        base_attack = int(parameters.get("average_base_shop_attack", 6))
        base_health = int(parameters.get("average_base_shop_health", 6))
        if min(felboars, casts_per_turn, base_attack, base_health) < 1:
            raise ValueError("Demon baseline parameters must be positive")
        shop_attack_buff = 0
        shop_health_buff = 0
        gain = 0
        casts_since_consume = 0
        for _ in range(turns):
            for _ in range(casts_per_turn):
                shop_attack_buff += 2
                shop_health_buff += 2
                casts_since_consume += 1
                if casts_since_consume == 3:
                    gain += felboars * (
                        base_attack + shop_attack_buff + base_health + shop_health_buff
                    )
                    casts_since_consume = 0
        return {
            "model": model,
            "projected_stat_gain": gain,
            "equation": "Each targeted spell gives the Tavern +2/+2; every third cast makes each Felboar consume one average shop body.",
        }

    raise ValueError(f"Unknown baseline model: {model}")


def _eligible_tribe_sets(required_tribes: set[str]) -> list[frozenset[str]]:
    unknown = required_tribes - set(STANDARD_TRIBES)
    if unknown:
        raise ValueError(f"Unknown required tribes: {', '.join(sorted(unknown))}")
    remaining = [tribe for tribe in STANDARD_TRIBES if tribe not in required_tribes]
    needed = 5 - len(required_tribes)
    if needed < 0:
        return []
    return [
        frozenset(required_tribes | set(extra))
        for extra in itertools.combinations(remaining, needed)
    ]


def _pool_for_lobby(
    cards_payload: dict, active_tribes: frozenset[str], tavern_tier: int
) -> list[int]:
    pool: list[int] = []
    for card in cards_payload.get("cards", {}).values():
        tier = card.get("tier")
        if card.get("type") != "minion" or card.get("pool") is not True:
            continue
        modes = {str(mode).lower() for mode in card.get("modes", [])}
        if modes and "solo" not in modes:
            continue
        categories = {str(category).lower() for category in card.get("categories", [])}
        if categories and "tavern" not in categories:
            continue
        if not isinstance(tier, int) or tier > tavern_tier or tier not in POOL_COPIES:
            continue
        tribes = {str(tribe).lower() for tribe in card.get("tribes", [])}
        if tribes and "all" not in tribes and tribes.isdisjoint(active_tribes):
            continue
        pool.extend([int(card["id"])] * POOL_COPIES[tier])
    return pool


def _remove_copies(pool: list[int], card_ids: Iterable[int], copies_each: int) -> None:
    for card_id in card_ids:
        for _ in range(copies_each):
            try:
                pool.remove(card_id)
            except ValueError:
                break


def _run_pivot_attempt(
    base_pool: list[int],
    required_card_ids: set[int],
    owned_card_ids: set[int],
    *,
    tavern_tier: int,
    turns: int,
    held_by_rivals: int,
    rng: random.Random,
) -> bool:
    pool = list(base_pool)
    acquired = set(owned_card_ids)
    _remove_copies(pool, acquired, 1)
    _remove_copies(pool, required_card_ids - acquired, held_by_rivals)
    slots = SHOP_SLOTS[tavern_tier]
    frozen_shop: list[int] | None = None

    for _ in range(turns):
        gold = 10
        while pool:
            shop = (
                frozen_shop
                if frozen_shop is not None
                else rng.sample(pool, k=min(slots, len(pool)))
            )
            frozen_shop = None
            missing = required_card_ids - acquired
            for card_id in sorted(missing):
                if card_id in shop and gold >= 3:
                    acquired.add(card_id)
                    gold -= 3
                    pool.remove(card_id)
            if required_card_ids <= acquired:
                return True
            missing_in_shop = (required_card_ids - acquired).intersection(shop)
            if missing_in_shop and gold < 3:
                frozen_shop = shop
                break
            if gold < 1:
                break
            gold -= 1
    return required_card_ids <= acquired


def estimate_pivot_probability(
    cards_payload: dict,
    *,
    required_card_ids: list[int],
    required_tribes: list[str],
    tavern_tier: int = 6,
    turns: int = 2,
    owned_card_ids: list[int] | None = None,
    held_by_rivals: int = 0,
    simulations: int = 50_000,
    seed: int = 14,
) -> dict:
    """Monte Carlo estimate for buying a functional core while hard-rolling.

    Results are averaged across all five-tribe lobby combinations containing
    the required tribes. Every simulated turn refills to 10 Gold. Required
    cards are bought immediately, rational freezes are carried to the next
    turn, and remaining Gold is spent on refreshes. Apart from explicit owned
    and rival-held target copies, the shared pool is pristine. This deliberately
    excludes generated cards, Discover odds, survival, and path-to-position.
    """
    integer_inputs = (tavern_tier, turns, simulations, held_by_rivals, seed)
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in integer_inputs
    ):
        raise ValueError(
            "tavern_tier, turns, simulations, held_by_rivals, and seed must be integers"
        )
    if tavern_tier not in SHOP_SLOTS:
        raise ValueError(f"Unsupported Tavern Tier: {tavern_tier}")
    if turns < 1 or simulations < 1 or held_by_rivals < 0:
        raise ValueError(
            "turns and simulations must be positive; held_by_rivals cannot be negative"
        )

    required_list = [int(card_id) for card_id in required_card_ids]
    owned_list = [int(card_id) for card_id in (owned_card_ids or [])]
    required = set(required_list)
    owned = set(owned_list)
    if not required:
        raise ValueError("required_card_ids cannot be empty")
    if len(required_list) != len(required):
        raise ValueError("duplicate required card IDs are not supported")
    if len(owned_list) != len(owned):
        raise ValueError("duplicate owned card IDs are not supported")
    if not owned <= required:
        raise ValueError("owned_card_ids must be part of required_card_ids")

    required_tribes = list(required_tribes)
    if not required_tribes or not all(
        isinstance(tribe, str) and tribe.strip() for tribe in required_tribes
    ):
        raise ValueError("required_tribes must contain non-empty tribe names")
    normalized_tribes = {tribe.strip().lower() for tribe in required_tribes}
    tribe_sets = _eligible_tribe_sets(normalized_tribes)
    if not tribe_sets:
        raise ValueError("No valid five-tribe lobbies satisfy required_tribes")
    pools = [
        _pool_for_lobby(cards_payload, tribes, tavern_tier) for tribes in tribe_sets
    ]
    if any(not all(card_id in pool for card_id in required - owned) for pool in pools):
        raise ValueError(
            "A required card is absent from at least one modeled eligible lobby pool"
        )

    rng = random.Random(seed)
    successes = 0
    for _ in range(simulations):
        pool = pools[rng.randrange(len(pools))]
        successes += _run_pivot_attempt(
            pool,
            required,
            owned,
            tavern_tier=tavern_tier,
            turns=turns,
            held_by_rivals=held_by_rivals,
            rng=rng,
        )

    conditional = successes / simulations
    eligible = eligible_lobby_probability(len(normalized_tribes))
    random_lobby_adjusted = conditional * eligible
    standard_error = math.sqrt(conditional * (1 - conditional) / simulations)
    ci_low = max(0.0, conditional - 1.96 * standard_error)
    ci_high = min(1.0, conditional + 1.96 * standard_error)

    def once_every(probability: float) -> float | None:
        return round(1 / probability, 1) if probability > 0 else None

    return {
        "conditional_probability": round(conditional, 6),
        "random_lobby_adjusted_probability": round(random_lobby_adjusted, 6),
        "eligible_lobby_probability": round(eligible, 6),
        "conditional_once_every": once_every(conditional),
        "random_lobby_adjusted_once_every": once_every(random_lobby_adjusted),
        "conditional_label": classify_frequency(conditional),
        "random_lobby_adjusted_label": classify_frequency(random_lobby_adjusted),
        "standard_error": round(standard_error, 6),
        "conditional_ci95": [round(ci_low, 6), round(ci_high, 6)],
        "simulations": simulations,
        "seed": seed,
        "tavern_tier": tavern_tier,
        "turns": turns,
        "held_by_rivals": held_by_rivals,
        "required_card_ids": sorted(required),
        "owned_card_ids": sorted(owned),
        "model": "hard-roll-v1",
    }
