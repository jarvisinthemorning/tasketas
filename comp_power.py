"""Deterministic Battlegrounds composition power simulations.

Registry entries contain only composition cards and materialized result values.
All model constants, mechanic handling, and checkpoint choices live here. Full
runs are written to a separate compressed artifact per composition.
"""

from __future__ import annotations

import gzip
import json
import math
import random
from collections import Counter
from copy import deepcopy
from pathlib import Path

from comp_evaluation import SHOP_SLOTS, STANDARD_TRIBES, _pool_for_lobby

MODEL_VERSION = "power-v6"
DEFAULT_SIMULATIONS = 5_000
DEFAULT_SEED = 14_014
ROLL_START_TURN = 10
ROLL_TURNS = 4
CHECKPOINT_TURN = 14
CONTENTION_HOLD_CHANCE = 0.20
POOL_COPIES_BY_TIER = {1: 15, 2: 15, 3: 13, 4: 11, 5: 9, 6: 7, 7: 5}

HOGRIDER = 116195
GEM_RAT = 116434
GEM_DAY = 116596
BRAMBLE_TUNNELER = 132632
JAILBIRD_JUGGERNAUT = 132636
GATEKEEPER_AMALGAM = 133329
DISTRACTOR = 132901
FELBOAR = 110664
BALINDA = 130298
METHODICAL_MADNESS = 132903
METHODICAL_GOLD_COST = 3
BRANN = 96786
SHELL_COLLECTOR = 80740
BARRIER_BANSHEE = 133081
PLAGUERUNNER = 126451
DRUSTFALLEN_BUTCHER = 120104
BUTCHERING = 110412
CATACLYSMIC_HARBINGER = 130884
FRIENDLY_GEIST = 120219
FIRE_FORGED_EVOKER = 120301
CRIMSON_VINDICATOR = 132953
PERSISTENT_POET = 108463
WARPWING = 92413
MIGHTY_DRAGONBREATH = 132995
TASTY_LOBSTER = 132796
DEATHSTRIDER = 132808
HEADHUNTER_GRYPHON = 132800
KALECGOS = 60630
BRONZE_TIMEWALKER = 132955
SKY_HATCH_RUNAWAY = 132957
MOAT_CUSTODIAN = 132981
MANA_SURGE = 120674
GLAMBOT = 132893
FAUNA_WHISPERER = 120905
UTILITY_DRONE = 98588
DRAKKARI_ENCHANTER = 101314
NATURAL_BLESSING = 104472
TRANQUIL_MEDITATIVE = 119942
GROUNDBREAKER = 114816
ENTERPRISING_ESCAPEE = 132762
HOOKTUSK = 132925
CLEVER_CASTAWAY = 132921
LOCKBOX = 132766
SNAZZY_PHANTOM = 133083
HANDLESS_FORSAKEN = 95265
SHAMANIC_TIDECALLER = 133026
TWILIGHT_TIDEHUNTER = 132989
CHORAL_MRGLR = 98948
FLIGHTY_SCOUT = 120677
EXPERT_AVIATOR = 126637
BREAM_COUNTER = 98509
AMALGAMATION = 132790
MALDRAXXUS_DAGGER = 133713
TIMEWARPED_EMBALMER = 127446
LEEROY = 90425
POWER_OF_THE_LICH_KING = 126271
VIGILANT_BRISTLEMANE = 132320
TRENCH_FIGHTER = 126671
GEM_CONFISCATION = 110642
UNBOUND_TEMPEST = 132983
AIR_REVENANT = 126173
SPIRIT_SWAP = 71464

# name, required board minions, required spells/generated contracts,
# required hand minions, and conditional prerequisites.
ENGINE_PROFILES = (
    ("hogrider", Counter({HOGRIDER: 1, GEM_RAT: 1}), Counter({GEM_DAY: 1}), Counter(), Counter()),
    (
        "demon-shop-consume",
        Counter({DISTRACTOR: 1, FELBOAR: 1}),
        Counter({METHODICAL_MADNESS: 1}),
        Counter(),
        Counter(),
    ),
    (
        "plaguerunner-butchering",
        Counter({PLAGUERUNNER: 1, DRUSTFALLEN_BUTCHER: 1}),
        Counter({BUTCHERING: 1}),
        Counter(),
        Counter(),
    ),
    (
        "vindicator-poet-warpwing",
        Counter({FIRE_FORGED_EVOKER: 1, CRIMSON_VINDICATOR: 1, PERSISTENT_POET: 1, WARPWING: 1}),
        Counter({MIGHTY_DRAGONBREATH: 1}),
        Counter(),
        Counter(),
    ),
    (
        "lobster-deathstrider",
        Counter({TASTY_LOBSTER: 1, DEATHSTRIDER: 1, HEADHUNTER_GRYPHON: 1}),
        Counter(),
        Counter(),
        Counter(),
    ),
    (
        "kalecgos-battlecry",
        Counter({KALECGOS: 1, BRANN: 1, BRONZE_TIMEWALKER: 2, SKY_HATCH_RUNAWAY: 1}),
        Counter(),
        Counter(),
        Counter(),
    ),
    ("moat-mana-surge", Counter({MOAT_CUSTODIAN: 1, MANA_SURGE: 1}), Counter(), Counter(), Counter()),
    (
        "tempest-revenant",
        Counter({UNBOUND_TEMPEST: 1, AIR_REVENANT: 1}),
        Counter(),
        Counter(),
        Counter({SPIRIT_SWAP: 1}),
    ),
    (
        "utility-drone-magnetics",
        Counter({GLAMBOT: 1, FAUNA_WHISPERER: 1, UTILITY_DRONE: 1, BALINDA: 1, DRAKKARI_ENCHANTER: 1}),
        Counter({NATURAL_BLESSING: 1}),
        Counter(),
        Counter(),
    ),
    (
        "fauna-spellcraft",
        Counter({TRANQUIL_MEDITATIVE: 1, FAUNA_WHISPERER: 1, BALINDA: 1}),
        Counter({NATURAL_BLESSING: 1}),
        Counter(),
        Counter(),
    ),
    (
        "escapee-hooktusk",
        Counter({ENTERPRISING_ESCAPEE: 1, HOOKTUSK: 1, CLEVER_CASTAWAY: 1}),
        Counter({LOCKBOX: 1}),
        Counter(),
        Counter(),
    ),
    (
        "snazzy-reborn",
        Counter({SNAZZY_PHANTOM: 1, BARRIER_BANSHEE: 1, HANDLESS_FORSAKEN: 1}),
        Counter(),
        Counter(),
        Counter(),
    ),
    (
        "tidecaller-handbuff",
        Counter({SHAMANIC_TIDECALLER: 1, TWILIGHT_TIDEHUNTER: 1, CHORAL_MRGLR: 1, EXPERT_AVIATOR: 1}),
        Counter(),
        Counter({BREAM_COUNTER: 1}),
        Counter(),
    ),
    (
        "dagger-amalgamation",
        Counter({GATEKEEPER_AMALGAM: 1, BALINDA: 1}),
        Counter({AMALGAMATION: 1}),
        Counter(),
        Counter({MALDRAXXUS_DAGGER: 1}),
    ),
    (
        "embalmer-scam",
        Counter({TIMEWARPED_EMBALMER: 2, LEEROY: 2}),
        Counter({POWER_OF_THE_LICH_KING: 1}),
        Counter(),
        Counter(),
    ),
    (
        "bristlemane-juggernaut",
        Counter({VIGILANT_BRISTLEMANE: 1, JAILBIRD_JUGGERNAUT: 1, TRENCH_FIGHTER: 1}),
        Counter({GEM_CONFISCATION: 1}),
        Counter(),
        Counter(),
    ),
)

PROFILE_ASSUMPTIONS = {
    "hogrider": ["One Gem Day and deterministic end-of-turn placement budget."],
    "demon-shop-consume": ["Four Tavern-6 recruit phases and deterministic spell/consume actions."],
    "plaguerunner-butchering": ["Conditional on Plaguerunner Portrait; portrait odds are excluded."],
    "vindicator-poet-warpwing": ["Only Dragons immediately adjacent to Persistent Poet retain combat gains."],
    "lobster-deathstrider": ["One source-verified Headhunter Gryphon Rally attack per combat; Lobster's hidden future improvement is unmodeled."],
    "kalecgos-battlecry": ["One immediate Sky-hatch Battlecry on assembly; two combat-generated Timewalker Battlecries become playable next turn."],
    "moat-mana-surge": ["Two Elemental plays per recruit turn and one Custodian Rally per combat."],
    "tempest-revenant": [
        "Conditional on Spirit Swap; hero-selection odds and random Dark Gifts are excluded.",
        "One Air Revenant activation and three Elemental plays resolve each recruit turn; each active Easterly Winds contributes one bounded +6/+6 hit to the selected Tavern anchor.",
    ],
    "utility-drone-magnetics": ["Natural Blessing is generated by Fauna and end-of-turn effects resolve in board order."],
    "fauna-spellcraft": ["Natural Blessing is generated by Fauna; one Meditative spell increment resolves first."],
    "escapee-hooktusk": ["Ten Gold creates two ordered Escapee triggers; only Clever Castaway Activates count as Discovers and Hooktusk's hidden improvement is excluded."],
    "snazzy-reborn": ["One Handless Forsaken Reborn event per combat; combat buffs do not persist."],
    "tidecaller-handbuff": ["One targetable Tavern spell and one Murloc cycle per recruit turn."],
    "dagger-amalgamation": ["Conditional on owning Maldraxxus Dagger; generated copies begin next recruit turn."],
    "embalmer-scam": ["Conditional on the Timewarped setup and Power of the Lich King; removal capacity is bounded."],
    "bristlemane-juggernaut": ["One generated Gem Confiscation is usable on each recruit turn after assembly."],
}


def _card(cards_payload: dict, card_id: int) -> dict:
    card = cards_payload.get("cards", {}).get(str(card_id))
    if not card:
        raise ValueError(f"Unknown card ID: {card_id}")
    return card


def _entry_card_ids(entry: dict, field: str) -> list[int]:
    result: list[int] = []
    for item in entry.get(field, []):
        if isinstance(item, int) and not isinstance(item, bool):
            result.append(item)
            continue
        if not isinstance(item, dict):
            raise TypeError(f"{field} entries must be card IDs or mappings")
        card_id = item.get("card_id")
        count = item.get("count", 1)
        if not isinstance(card_id, int) or isinstance(card_id, bool):
            raise TypeError(f"{field}.card_id must be an integer")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise ValueError(f"{field}.count must be a positive integer")
        result.extend([card_id] * count)
    return result


def _profile_for(entry: dict) -> str:
    minion_counts = Counter(_entry_card_ids(entry, "minions"))
    spell_counts = Counter(_entry_card_ids(entry, "spells"))
    hand_counts = Counter(_entry_card_ids(entry, "hand_minions"))
    prerequisite_counts = Counter(_entry_card_ids(entry, "prerequisites"))
    resource_errors = {
        "hogrider": "Hogrider simulations require Gem Day in spells",
        "demon-shop-consume": "Demon shop-consume simulations require Methodical Madness in spells",
        "plaguerunner-butchering": "Plaguerunner simulations require Butchering in spells",
        "vindicator-poet-warpwing": "Warpwing simulations require Mighty Dragonbreath in spells",
        "utility-drone-magnetics": "utility-drone-magnetics simulations require Natural Blessing in spells",
        "fauna-spellcraft": "fauna-spellcraft simulations require Natural Blessing in spells",
        "escapee-hooktusk": "Escapee simulations require Lockbox in spells",
        "tidecaller-handbuff": "Tidecaller simulations require Bream Counter in hand_minions",
        "dagger-amalgamation": "Dagger simulations require Amalgamation and Maldraxxus Dagger",
        "embalmer-scam": "Embalmer simulations require Power of the Lich King",
        "bristlemane-juggernaut": "Bristlemane simulations require Gem Confiscation in spells",
        "tempest-revenant": "Tempest-Revenant simulations require Spirit Swap in prerequisites",
    }
    for name, minions, spells, hand_minions, prerequisites in ENGINE_PROFILES:
        if minions <= minion_counts:
            if not spells <= spell_counts or not hand_minions <= hand_counts or not prerequisites <= prerequisite_counts:
                raise ValueError(resource_errors[name])
            return name
    raise ValueError("No deterministic power profile supports this composition yet")


def _minion_requirements(entry: dict, field: str = "minions") -> Counter[int]:
    requirements: Counter[int] = Counter()
    for item in entry.get(field, []):
        item = {"card_id": item} if isinstance(item, int) and not isinstance(item, bool) else item
        if not isinstance(item, dict):
            raise TypeError(f"{field} entries must be card IDs or mappings")
        card_id = item.get("card_id")
        count = item.get("count", 1)
        golden_count = item.get("golden_count", 0)
        if not all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (card_id, count, golden_count)
        ):
            raise TypeError("minion card_id, count, and golden_count must be integers")
        if count < 1 or golden_count < 0 or golden_count > count:
            raise ValueError("minion counts must satisfy 0 <= golden_count <= count")
        assert isinstance(card_id, int)
        card_id = int(card_id)
        # Each Golden board body consumes three shop copies instead of one.
        requirements[card_id] += count + 2 * golden_count
    return requirements


def _expanded_board(entry: dict, cards_payload: dict) -> list[dict]:
    board: list[dict] = []
    for item in entry.get("minions", []):
        item = {"card_id": item} if isinstance(item, int) and not isinstance(item, bool) else item
        if not isinstance(item, dict):
            raise TypeError("minions entries must be card IDs or mappings")
        card_id = item.get("card_id")
        count = item.get("count", 1)
        golden_count = item.get("golden_count", 0)
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in (card_id, count, golden_count)):
            raise ValueError("minion card_id, count, and golden_count must be integers")
        if count < 1 or golden_count < 0 or golden_count > count:
            raise ValueError("minion counts must satisfy 0 <= golden_count <= count")
        card = _card(cards_payload, card_id)
        if card.get("type") != "minion":
            raise ValueError(f"{card.get('name', card_id)} is not a minion")
        for index in range(count):
            golden = index < golden_count
            attack_key = "attack_gold" if golden else "attack"
            health_key = "health_gold" if golden else "health"
            attack = card.get(attack_key)
            health = card.get(health_key)
            if not isinstance(attack, int) or not isinstance(health, int):
                raise TypeError(f"{card.get('name', card_id)} is missing normalized base stats")
            board.append(
                {
                    "card_id": card_id,
                    "name": card.get("name", str(card_id)),
                    "attack": attack,
                    "health": health,
                    "golden": golden,
                    "keywords": list(card.get("keywords", [])),
                    "tribes": [str(tribe).lower() for tribe in card.get("tribes", [])],
                    "blood_gem_attack": 0,
                    "blood_gem_health": 0,
                }
            )
    if not 1 <= len(board) <= 7:
        raise ValueError("a simulated composition must contain 1 to 7 minions")
    return board


def effective_board_power(board: list[dict]) -> int:
    """Convert a board into a mechanics-aware deterministic strength score.

    This is a ranking heuristic, not combat simulation or win probability.
    Raw permanent stats form the base. Keyword bonuses are explicit utility
    credits so later model versions can change them without touching the
    registry: Divine Shield adds one health-bar equivalent, Reborn adds another
    attack plus one health, Venomous/Poisonous adds a 500-stat removal credit,
    and Cleave adds one extra attack target.
    """
    power = 0.0
    reborn_count = sum(
        "reborn" in {str(value).strip().lower() for value in unit.get("keywords", [])}
        for unit in board
    )
    for original in board:
        unit = dict(original)
        attack = max(0, int(unit.get("attack", 0)))
        health = max(0, int(unit.get("health", 0)))
        keywords = {str(value).strip().lower() for value in unit.get("keywords", [])}
        if unit.get("card_id") == BARRIER_BANSHEE and reborn_count:
            # Credit one expected Reborn trigger. Full trigger counts require
            # opponent, attack-order, death, and board-space simulation.
            gain = 14 if unit.get("golden") else 7
            attack += gain
            health += gain
            keywords.add("divine shield")
        unit_power = attack + health
        if "divine shield" in keywords:
            unit_power += health
        if "reborn" in keywords:
            unit_power += attack + 1
        if keywords.intersection({"venomous", "poisonous"}):
            unit_power += 500
        if unit.get("card_id") == LEEROY:
            removal_uses = int(unit.get("removal_uses", 2 if "reborn" in keywords else 1))
            unit_power += 500 * removal_uses
        if "cleave" in keywords:
            unit_power += attack
        if unit.get("card_id") == JAILBIRD_JUGGERNAUT:
            summon_stats = int(unit.get("blood_gem_attack", 0)) + int(
                unit.get("blood_gem_health", 0)
            )
            unit_power += summon_stats * (2 if unit.get("golden") else 1)
        power += unit_power
    return round(power)


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(percentile * len(ordered)) - 1))
    return ordered[index]


def _active_tribes(rng: random.Random) -> frozenset[str]:
    return frozenset(rng.sample(STANDARD_TRIBES, 5))


def _simulate_acquisition(
    cards_payload: dict,
    requirements: Counter[int],
    required_tribes: set[str],
    rng: random.Random,
    roll_turns: int,
) -> tuple[int | None, frozenset[str], list[int]]:
    active_tribes = _active_tribes(rng)
    if not required_tribes <= active_tribes:
        return None, active_tribes, []
    unique_pool = _pool_for_lobby(cards_payload, active_tribes, 6)
    pool = [
        card_id
        for card_id in unique_pool
        for _ in range(
            POOL_COPIES_BY_TIER.get(int(_card(cards_payload, card_id).get("tier") or 0), 1)
        )
    ]
    held_by_rival: list[int] = []
    for card_id in sorted(requirements):
        if card_id in pool and rng.random() < CONTENTION_HOLD_CHANCE:
            pool.remove(card_id)
            held_by_rival.append(card_id)
    acquired: Counter[int] = Counter()
    for turn_offset in range(roll_turns):
        gold = 10
        while pool:
            shop = rng.sample(pool, k=min(SHOP_SLOTS[6], len(pool)))
            for card_id in sorted(requirements):
                while (
                    acquired[card_id] < requirements[card_id]
                    and card_id in shop
                    and gold >= 3
                ):
                    acquired[card_id] += 1
                    pool.remove(card_id)
                    shop.remove(card_id)
                    gold -= 3
            if all(acquired[card_id] >= count for card_id, count in requirements.items()):
                return ROLL_START_TURN + turn_offset, active_tribes, held_by_rival
            if gold < 1:
                break
            gold -= 1
    return None, active_tribes, held_by_rival


def _sample_shop_body(cards_payload: dict, active_tribes: frozenset[str], rng: random.Random) -> dict:
    pool = _pool_for_lobby(cards_payload, active_tribes, 6)
    for _ in range(50):
        card = _card(cards_payload, rng.choice(pool))
        if isinstance(card.get("attack"), int) and isinstance(card.get("health"), int):
            return card
    raise ValueError("Unable to sample a Tavern minion with normalized stats")


def _sample_shop_bodies(
    cards_payload: dict, active_tribes: frozenset[str], rng: random.Random
) -> list[dict]:
    pool = _pool_for_lobby(cards_payload, active_tribes, 6)
    shop_ids = rng.sample(pool, k=min(SHOP_SLOTS[6], len(pool)))
    bodies = [
        _card(cards_payload, card_id)
        for card_id in shop_ids
        if isinstance(_card(cards_payload, card_id).get("attack"), int)
        and isinstance(_card(cards_payload, card_id).get("health"), int)
    ]
    rng.shuffle(bodies)
    return bodies


def _snapshot(turn: int, board: list[dict], events: list[str]) -> dict:
    raw_stats = sum(unit["attack"] + unit["health"] for unit in board)
    power = effective_board_power(board)
    return {
        "turn": turn,
        "raw_stats": raw_stats,
        "power": power,
        "score_components": {
            "raw_stats": raw_stats,
            "mechanics_utility": power - raw_stats,
        },
        "events": events,
    }


def _simulate_hogrider(
    entry: dict,
    cards_payload: dict,
    board: list[dict],
    online_turn: int,
    checkpoint_turn: int,
    rng: random.Random,
) -> list[dict]:
    gem_attack = 1
    gem_health = 1
    pending_gem_days = 0
    pending_rally_cards = 0
    traces: list[dict] = []

    def cast_tea_set(repeats: int) -> None:
        for _ in range(repeats):
            for tribe in STANDARD_TRIBES:
                candidates = [
                    unit
                    for unit in board
                    if tribe in unit["tribes"] or "all" in unit["tribes"]
                ]
                if candidates:
                    target = rng.choice(candidates)
                    target["attack"] += 2
                    target["health"] += 2

    for turn in range(online_turn, checkpoint_turn + 1):
        events: list[str] = []
        rats = [unit for unit in board if unit["card_id"] == GEM_RAT]
        hogriders = [unit for unit in board if unit["card_id"] == HOGRIDER]

        def play_choose_one(*, upgrades_gems: bool, active_hogriders: list[dict] = hogriders) -> None:
            nonlocal gem_attack, gem_health
            if upgrades_gems:
                if rng.random() < 0.5:
                    gem_attack += 1
                else:
                    gem_health += 1
            for hogrider in active_hogriders:
                repeats = 2 if hogrider["golden"] else 1
                for unit in board:
                    if unit is hogrider:
                        continue
                    if "quilboar" in unit["tribes"] or "all" in unit["tribes"]:
                        unit["attack"] += gem_attack * repeats
                        unit["health"] += gem_health * repeats
                        unit["blood_gem_attack"] += gem_attack * repeats
                        unit["blood_gem_health"] += gem_health * repeats
                        if unit["card_id"] == GATEKEEPER_AMALGAM:
                            cast_tea_set((2 if unit["golden"] else 1) * repeats)

        for _ in range(pending_gem_days):
            play_choose_one(upgrades_gems=True)
        for _ in range(pending_rally_cards):
            # The random Choose One pool contains both Gem upgrades and other
            # effects. Every card triggers Hogrider; one quarter upgrades Gems.
            play_choose_one(upgrades_gems=rng.random() < 0.25)

        next_gem_days = sum(2 if unit["golden"] else 1 for unit in rats)
        brambles = [unit for unit in board if unit["card_id"] == BRAMBLE_TUNNELER]
        next_rally_cards = sum(
            sum(rng.random() < 0.8 for _ in range(2 if unit["golden"] else 1))
            for unit in brambles
        )
        events.append(
            f"Played {pending_gem_days} banked Gem Days and {pending_rally_cards} banked Rally cards; "
            f"banked {next_gem_days + next_rally_cards} for next recruit phase; "
            f"Blood Gems reached +{gem_attack}/+{gem_health}"
        )
        pending_gem_days = next_gem_days
        pending_rally_cards = next_rally_cards
        traces.append(_snapshot(turn, board, events))
    return traces


def _spell_multiplier(board: list[dict]) -> int:
    balindas = [unit for unit in board if unit["card_id"] == BALINDA]
    if not balindas:
        return 1
    return max(3 if unit["golden"] else 2 for unit in balindas)


def _consume_into(unit: dict, shop_card: dict, shop_buff: int, multiplier: int = 1) -> None:
    unit["attack"] += (int(shop_card["attack"]) + shop_buff) * multiplier
    unit["health"] += (int(shop_card["health"]) + shop_buff) * multiplier
    for keyword in shop_card.get("keywords", []):
        keyword = str(keyword).strip().lower()
        if keyword and keyword not in unit["keywords"]:
            unit["keywords"].append(keyword)


def _simulate_demons(
    entry: dict,
    cards_payload: dict,
    board: list[dict],
    online_turn: int,
    checkpoint_turn: int,
    active_tribes: frozenset[str],
    rng: random.Random,
) -> list[dict]:
    traces: list[dict] = []
    shop_buff = 0
    casts_since_felboar = 0
    spell_multiplier = _spell_multiplier(board)
    one_time_brann_economy = any(unit["card_id"] == BRANN for unit in board) and any(
        unit["card_id"] == SHELL_COLLECTOR for unit in board
    )
    distractors = [unit for unit in board if unit["card_id"] == DISTRACTOR]
    felboars = [unit for unit in board if unit["card_id"] == FELBOAR]
    target = distractors[0]
    for turn in range(online_turn, checkpoint_turn + 1):
        events: list[str] = []
        # Methodical Madness is repeatable fuel; the global model controls how
        # many copies are found rather than storing an evaluation knob per comp.
        # At 3 Gold each plus Refreshes, the normal 10-Gold turn can support
        # at most two found copies. Brann + Shell Collector contributes its
        # one-time coin Battlecry only on the assembly turn.
        spell_actions = rng.choices((1, 2), weights=(35, 65), k=1)[0]
        if one_time_brann_economy and turn == online_turn:
            spell_actions += 1
        casts = 0
        consumed = 0
        for _ in range(spell_actions):
            shop = _sample_shop_bodies(cards_payload, active_tribes, rng)
            for _ in range(spell_multiplier):
                if len(shop) < 2:
                    break
                casts += 1
                shop_buff += 4 if target["golden"] else 2
                for _ in range(2):
                    _consume_into(target, shop.pop(), shop_buff)
                    consumed += 1
                casts_since_felboar += 1
                if casts_since_felboar == 3:
                    for felboar in felboars:
                        if not shop:
                            break
                        _consume_into(
                            felboar,
                            shop.pop(),
                            shop_buff,
                            2 if felboar["golden"] else 1,
                        )
                        consumed += 1
                    casts_since_felboar = 0
        events.append(
            f"Spent up to {spell_actions * METHODICAL_GOLD_COST} Gold on {spell_actions} "
            f"Methodical Madness actions; {casts} casts consumed {consumed} shop bodies; "
            f"Tavern buff reached +{shop_buff}/+{shop_buff}"
        )
        traces.append(_snapshot(turn, board, events))
    return traces


def _simulate_plaguerunner(
    entry: dict,
    cards_payload: dict,
    board: list[dict],
    online_turn: int,
    checkpoint_turn: int,
    rng: random.Random,
) -> list[dict]:
    """Model the source-shown Portrait, Butchering, and spell-copy loop."""
    del entry, cards_payload, rng
    traces: list[dict] = []
    pending_butcherings = 1
    tavern_spell_attack_bonus = 0
    plague = next(unit for unit in board if unit["card_id"] == PLAGUERUNNER)
    plague_is_golden = bool(plague["golden"])

    for turn in range(online_turn, checkpoint_turn + 1):
        actions = pending_butcherings
        total_attack_gain = 0
        for _ in range(actions):
            deathrattle_gain = 8 if plague_is_golden else 4
            gain = 5 + tavern_spell_attack_bonus + deathrattle_gain
            for unit in board:
                if "undead" in unit["tribes"] or "all" in unit["tribes"]:
                    unit["attack"] += gain
            total_attack_gain += gain
            # Plaguerunner Portrait explicitly returns a plain copy.
            plague_is_golden = False

        geists = [unit for unit in board if unit["card_id"] == FRIENDLY_GEIST]
        tavern_spell_attack_bonus += sum(2 if unit["golden"] else 1 for unit in geists)
        butchers = [unit for unit in board if unit["card_id"] == DRUSTFALLEN_BUTCHER]
        butcher_refills = sum(2 if unit["golden"] else 1 for unit in butchers)
        harbingers = [unit for unit in board if unit["card_id"] == CATACLYSMIC_HARBINGER]
        harbinger_refills = sum(2 if unit["golden"] else 1 for unit in harbingers)
        # Plaguerunner Portrait returns the destroyed Plaguerunner. Optional
        # spell-copy trinkets are not modeled or assigned invented odds.
        pending_butcherings = butcher_refills + harbinger_refills
        events = [
            (
                f"Spent {actions} Butchering actions for +{total_attack_gain} Attack per Undead; "
                f"Friendly Geist raised future Tavern-spell Attack by +{tavern_spell_attack_bonus}; "
                f"banked {pending_butcherings} Butcherings"
            )
        ]
        traces.append(_snapshot(turn, board, events))
    return traces


def _simulate_warpwing(
    entry: dict,
    cards_payload: dict,
    board: list[dict],
    online_turn: int,
    checkpoint_turn: int,
    rng: random.Random,
) -> list[dict]:
    """Model Evoker/Vindicator combat buffs retained by Poet on Warpwings."""
    del entry, cards_payload, rng
    traces: list[dict] = []
    evokers = [unit for unit in board if unit["card_id"] == FIRE_FORGED_EVOKER]
    vindicators = [unit for unit in board if unit["card_id"] == CRIMSON_VINDICATOR]
    protected_dragons: list[tuple[dict, int]] = []
    for index, unit in enumerate(board):
        if "dragon" not in unit["tribes"] and "all" not in unit["tribes"]:
            continue
        adjacent_poets = [
            board[neighbor]
            for neighbor in (index - 1, index + 1)
            if 0 <= neighbor < len(board) and board[neighbor]["card_id"] == PERSISTENT_POET
        ]
        if adjacent_poets:
            multiplier = max(2 if poet["golden"] else 1 for poet in adjacent_poets)
            protected_dragons.append((unit, multiplier))
    evoker_attack = sum(4 if unit["golden"] else 2 for unit in evokers)
    evoker_health = sum(2 if unit["golden"] else 1 for unit in evokers)

    for turn in range(online_turn, checkpoint_turn + 1):
        dragonbreaths = sum(2 if unit["golden"] else 1 for unit in vindicators)
        for unit, poet_multiplier in protected_dragons:
            # Mighty Dragonbreath buffs all minions, repeats for Dragons, and
            # repeats once more for Divine Shield minions.
            repeats = 2 + (1 if "divine shield" in unit["keywords"] else 0)
            retained_attack = evoker_attack + dragonbreaths * repeats
            retained_health = evoker_health + dragonbreaths * repeats
            unit["attack"] += retained_attack * poet_multiplier
            unit["health"] += retained_health * poet_multiplier
        # Each combat-cast Dragonbreath doubles the Evoker's current buff for
        # later fights; it cannot enlarge the Start-of-Combat effect already
        # resolved this combat.
        evoker_attack *= 2**dragonbreaths
        evoker_health *= 2**dragonbreaths
        events = [
            (
                f"Retained Evoker and Dragonbreath combat gains on "
                f"{len(protected_dragons)} Poet-adjacent Dragons after "
                f"{dragonbreaths} Mighty Dragonbreath casts"
            )
        ]
        traces.append(_snapshot(turn, board, events))
    return traces


def _simulate_legacy(
    profile: str,
    entry: dict,
    cards_payload: dict,
    board: list[dict],
    online_turn: int,
    checkpoint_turn: int,
    rng: random.Random,
) -> list[dict]:
    """Simulate one of the source-grounded legacy composition engines."""
    if profile == "bristlemane-juggernaut":
        traces: list[dict] = []
        bristlemane = next(unit for unit in board if unit["card_id"] == VIGILANT_BRISTLEMANE)
        juggernaut = next(unit for unit in board if unit["card_id"] == JAILBIRD_JUGGERNAUT)

        def add_gems(unit: dict, count: int) -> None:
            unit["attack"] += count
            unit["health"] += count
            unit["blood_gem_attack"] += count
            unit["blood_gem_health"] += count

        for turn in range(online_turn, checkpoint_turn + 1):
            target = None
            if turn > online_turn:
                target = juggernaut if turn == checkpoint_turn else bristlemane
                add_gems(target, 2)
                index = board.index(target)
                adjacent = [
                    board[position]
                    for position in (index - 1, index + 1)
                    if 0 <= position < len(board)
                ]
                for neighbor in adjacent:
                    target["attack"] += neighbor["blood_gem_attack"]
                    target["health"] += neighbor["blood_gem_health"]
                    target["blood_gem_attack"] += neighbor["blood_gem_attack"]
                    target["blood_gem_health"] += neighbor["blood_gem_health"]
                    neighbor["attack"] -= neighbor["blood_gem_attack"]
                    neighbor["health"] -= neighbor["blood_gem_health"]
                    neighbor["blood_gem_attack"] = 0
                    neighbor["blood_gem_health"] = 0
                if target is bristlemane:
                    for neighbor in adjacent:
                        add_gems(neighbor, 2 if bristlemane["golden"] else 1)
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (
                            "No generated Confiscation is usable on the assembly turn"
                            if target is None
                            else f"Gem Confiscation targeted {target['name']}; Juggernaut bank is "
                            f"+{juggernaut['blood_gem_attack']}/+{juggernaut['blood_gem_health']}"
                        )
                    ],
                )
            )
        return traces
    if profile == "embalmer-scam":
        leeroys = [unit for unit in board if unit["card_id"] == LEEROY]
        # Two Embalmers plus the initial Reborn Rites grant a bounded five
        # available Leeroy deaths: 3 on the first body and 2 on the second.
        leeroys[0]["removal_uses"] = 3
        leeroys[1]["removal_uses"] = 2
        leeroys[0]["keywords"].append("reborn")
        return [
            _snapshot(
                turn,
                board,
                [
                    ("Credited five bounded Leeroy removal uses from two Embalmers and Reborn Rites; "
                    "this is removal capacity, not guaranteed kills")
                ],
            )
            for turn in range(online_turn, checkpoint_turn + 1)
        ]
    if profile == "dagger-amalgamation":
        traces: list[dict] = []
        gatekeepers = [unit for unit in board if unit["card_id"] == GATEKEEPER_AMALGAM]
        gifts = sum(
            item.get("count", 1)
            for item in entry.get("spells", [])
            if item.get("card_id") == AMALGAMATION
        )
        spell_multiplier = _spell_multiplier(board)
        for turn in range(online_turn, checkpoint_turn + 1):
            copied = 0
            if turn > online_turn and len(board) < 7:
                copied_unit = deepcopy(gatekeepers[0])
                board.append(copied_unit)
                gatekeepers.append(copied_unit)
                copied = 1
            casts = gifts * spell_multiplier if turn == online_turn else 0
            tea_sets = casts * sum(2 if unit["golden"] else 1 for unit in gatekeepers)
            for _ in range(tea_sets):
                for tribe in STANDARD_TRIBES:
                    candidates = [
                        unit
                        for unit in board
                        if tribe in unit["tribes"] or "all" in unit["tribes"]
                    ]
                    if candidates:
                        target = rng.choice(candidates)
                        target["attack"] += 2
                        target["health"] += 2
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (f"Resolved {casts} Amalgamation casts through Balinda and "
                        f"{tea_sets} Gatekeeper Tea Sets; Dagger added {copied} delayed copy")
                    ],
                )
            )
        return traces
    if profile == "tidecaller-handbuff":
        traces: list[dict] = []
        hand = _expanded_board({"minions": entry.get("hand_minions", [])}, cards_payload)
        hand_unit = next(unit for unit in hand if unit["card_id"] == BREAM_COUNTER)
        hand_attack = hand_unit["attack"]
        hand_health = hand_unit["health"]
        tidecallers = [unit for unit in board if unit["card_id"] == SHAMANIC_TIDECALLER]
        tidehunters = [unit for unit in board if unit["card_id"] == TWILIGHT_TIDEHUNTER]
        aviators = [unit for unit in board if unit["card_id"] == EXPERT_AVIATOR]
        for turn in range(online_turn, checkpoint_turn + 1):
            tidecaller_gain = sum(6 if unit["golden"] else 3 for unit in tidecallers)
            tidehunter_gain = sum(12 if unit["golden"] else 6 for unit in tidehunters)
            for unit in board:
                if "murloc" in unit["tribes"] or "all" in unit["tribes"]:
                    unit["attack"] += tidecaller_gain
                    unit["health"] += tidecaller_gain
            # One declared Murloc cycle grows Bream Counter by +6/+6.
            hand_attack += tidecaller_gain + tidehunter_gain + 6
            hand_health += tidecaller_gain + tidehunter_gain + 6
            combat_board = deepcopy(board)
            for unit in combat_board:
                if unit["card_id"] == CHORAL_MRGLR:
                    multiplier = 2 if unit["golden"] else 1
                    unit["attack"] += hand_attack * multiplier
                    unit["health"] += hand_health * multiplier
            if aviators and len(combat_board) < 7:
                summoned = deepcopy(hand_unit)
                summoned["attack"] = hand_attack
                summoned["health"] = hand_health
                combat_board.append(summoned)
            traces.append(
                _snapshot(
                    turn,
                    combat_board,
                    [
                        (f"One targeted spell and one Murloc cycle made Bream Counter reach "
                        f"{hand_attack}/{hand_health}; Choral and Expert Aviator converted it in combat")
                    ],
                )
            )
        return traces
    if profile == "snazzy-reborn":
        traces: list[dict] = []
        for turn in range(online_turn, checkpoint_turn + 1):
            combat_board = deepcopy(board)
            undead = [
                unit
                for unit in combat_board
                if "undead" in unit["tribes"] or "all" in unit["tribes"]
            ]
            recipient = undead[-1]
            reborn_events = sum(
                2 if unit["golden"] else 1
                for unit in combat_board
                if unit["card_id"] == HANDLESS_FORSAKEN
            )
            snazzy_gain = 2 * sum(
                2 if unit["golden"] else 1
                for unit in combat_board
                if unit["card_id"] == SNAZZY_PHANTOM
            )
            banshee_gain = sum(
                14 if unit["golden"] else 7
                for unit in combat_board
                if unit["card_id"] == BARRIER_BANSHEE
            )
            recipient["attack"] += reborn_events * snazzy_gain
            recipient["health"] += reborn_events * snazzy_gain
            for banshee in (
                unit for unit in combat_board if unit["card_id"] == BARRIER_BANSHEE
            ):
                gain = 14 if banshee["golden"] else 7
                banshee["attack"] += reborn_events * gain
                banshee["health"] += reborn_events * gain
                if "divine shield" not in banshee["keywords"]:
                    banshee["keywords"].append("divine shield")
            traces.append(
                _snapshot(
                    turn,
                    combat_board,
                    [
                        (f"Credited {reborn_events} Handless Forsaken Reborn event(s): "
                        f"Banshee itself gains +{banshee_gain}/+{banshee_gain} and Divine Shield; "
                        f"Snazzy gives +{snazzy_gain}/+{snazzy_gain} to the right-most Undead")
                    ],
                )
            )
        return traces
    if profile == "escapee-hooktusk":
        traces: list[dict] = []
        lockbox_timer: int | None = None
        golden_minions_played = 0
        escapees = [unit for unit in board if unit["card_id"] == ENTERPRISING_ESCAPEE]
        hooktusks = [unit for unit in board if unit["card_id"] == HOOKTUSK]
        castaways = [unit for unit in board if unit["card_id"] == CLEVER_CASTAWAY]
        for turn in range(online_turn, checkpoint_turn + 1):
            opened = 0
            if lockbox_timer is not None:
                lockbox_timer -= 1
                if lockbox_timer <= 0:
                    golden_minions_played += 1
                    opened += 1
                    lockbox_timer = None
            # Ten Gold creates two ordered Escapee triggers per recruit turn.
            for escapee in escapees:
                for _ in range(2):
                    if lockbox_timer is None:
                        lockbox_timer = 5
                    else:
                        lockbox_timer -= 2 if escapee["golden"] else 1
                        if lockbox_timer <= 0:
                            golden_minions_played += 1
                            opened += 1
                            lockbox_timer = None
            discovers = (
                sum(2 if unit["golden"] else 1 for unit in castaways)
                if (turn - online_turn) % 2 == 0
                else 0
            )
            for hooktusk in hooktusks:
                base_gain = 2 if hooktusk["golden"] else 1
                for unit in board:
                    if unit is not hooktusk and ("pirate" in unit["tribes"] or "all" in unit["tribes"]):
                        unit["attack"] += base_gain * discovers
                        unit["health"] += base_gain * discovers
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (f"Opened {opened} Lockbox reward(s) and resolved {discovers} Castaway Discover action(s); "
                        f"timer {lockbox_timer}, Golden rewards {golden_minions_played}; Lockboxes never count as Discovers")
                    ],
                )
            )
        return traces
    if profile == "fauna-spellcraft":
        traces: list[dict] = []
        spell_bonus = 0
        meditatives = [unit for unit in board if unit["card_id"] == TRANQUIL_MEDITATIVE]
        faunas = [unit for unit in board if unit["card_id"] == FAUNA_WHISPERER]
        end_multiplier = max(
            (3 if unit["golden"] else 2 for unit in board if unit["card_id"] == DRAKKARI_ENCHANTER),
            default=1,
        )
        spell_multiplier = _spell_multiplier(board)
        for turn in range(online_turn, checkpoint_turn + 1):
            for unit in meditatives:
                spell_bonus += 2 if unit["golden"] else 1
            casts = 0
            for fauna in faunas:
                index = board.index(fauna)
                adjacent = [
                    board[target]
                    for target in (index - 1, index + 1)
                    if 0 <= target < len(board)
                ]
                for target in adjacent:
                    for _ in range(
                        (2 if fauna["golden"] else 1) * end_multiplier * spell_multiplier
                    ):
                        casts += 1
                        target_tribes = set(target["tribes"])
                        for unit in board:
                            if target_tribes.intersection(unit["tribes"]) or "all" in unit["tribes"]:
                                unit["attack"] += 3 + spell_bonus
                                unit["health"] += 3 + spell_bonus
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (f"Meditative spell bonus reached +{spell_bonus}/+{spell_bonus}; "
                        f"Fauna resolved {casts} Natural Blessing casts")
                    ],
                )
            )
        return traces
    if profile == "utility-drone-magnetics":
        traces: list[dict] = []
        magnetizations = {id(unit): 0 for unit in board}
        faunas = [unit for unit in board if unit["card_id"] == FAUNA_WHISPERER]
        glambots = [unit for unit in board if unit["card_id"] == GLAMBOT]
        drones = [unit for unit in board if unit["card_id"] == UTILITY_DRONE]
        end_multiplier = max(
            (3 if unit["golden"] else 2 for unit in board if unit["card_id"] == DRAKKARI_ENCHANTER),
            default=1,
        )
        spell_multiplier = _spell_multiplier(board)
        for turn in range(online_turn, checkpoint_turn + 1):
            casts = 0
            for fauna in faunas:
                fauna_index = board.index(fauna)
                adjacent = [
                    board[index]
                    for index in (fauna_index - 1, fauna_index + 1)
                    if 0 <= index < len(board)
                ]
                for target in adjacent:
                    for _ in range(
                        (2 if fauna["golden"] else 1) * end_multiplier * spell_multiplier
                    ):
                        casts += 1
                        target_tribes = set(target["tribes"])
                        for unit in board:
                            if target_tribes.intersection(unit["tribes"]) or "all" in unit["tribes"]:
                                unit["attack"] += 3
                                unit["health"] += 3
                        if "mech" in target["tribes"] or "all" in target["tribes"]:
                            satellites = sum(2 if unit["golden"] else 1 for unit in glambots)
                            target["attack"] += 6 * satellites
                            target["health"] += 6 * satellites
                            magnetizations[id(target)] += satellites
            for drone in drones:
                drone_gain = (8 if drone["golden"] else 4) * end_multiplier
                for unit in board:
                    gain = drone_gain * magnetizations[id(unit)]
                    unit["attack"] += gain
                    unit["health"] += gain
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (f"Resolved {casts} Natural Blessing casts before Utility Drone; "
                        f"tracked {sum(magnetizations.values())} Magnetizations")
                    ],
                )
            )
        return traces
    if profile == "moat-mana-surge":
        traces: list[dict] = []
        extra_attack = 0
        extra_health = 0
        elemental_plays = 2
        surges = [unit for unit in board if unit["card_id"] == MANA_SURGE]
        custodians = [unit for unit in board if unit["card_id"] == MOAT_CUSTODIAN]
        for turn in range(online_turn, checkpoint_turn + 1):
            base_attack = sum(8 if unit["golden"] else 4 for unit in surges)
            base_health = base_attack
            for _ in range(elemental_plays):
                for unit in board:
                    if "elemental" in unit["tribes"] or "all" in unit["tribes"]:
                        unit["attack"] += base_attack + extra_attack
                        unit["health"] += base_health + extra_health
            extra_attack += sum(2 if unit["golden"] else 1 for unit in custodians)
            extra_health += sum(4 if unit["golden"] else 2 for unit in custodians)
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (f"Played {elemental_plays} Elementals through Mana Surge; "
                        f"Moat amplifier reached +{extra_attack}/+{extra_health}")
                    ],
                )
            )
        return traces
    if profile == "tempest-revenant":
        traces: list[dict] = []
        active_winds = 0
        revenants = [unit for unit in board if unit["card_id"] == AIR_REVENANT]
        tempests = [unit for unit in board if unit["card_id"] == UNBOUND_TEMPEST]
        for turn in range(online_turn, checkpoint_turn + 1):
            active_winds += sum(2 if unit["golden"] else 1 for unit in revenants)
            # Spirit Swap lends the Tavern anchor the strongest friendly Attack
            # until next turn. The temporary swap never mutates the warband;
            # Tempest's later stat gain is permanent.
            swapped_attack = max(unit["attack"] for unit in board)
            anchor_health = 6 * active_winds
            for tempest in tempests:
                multiplier = 2 if tempest["golden"] else 1
                tempest["attack"] += swapped_attack * multiplier
                tempest["health"] += anchor_health * multiplier
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (
                            f"Resolved {active_winds} active Easterly Winds on the bounded Tavern anchor; "
                            f"Spirit Swap copied {swapped_attack} Attack before three Elemental plays triggered Tempest"
                        )
                    ],
                )
            )
        return traces
    if profile == "kalecgos-battlecry":
        traces: list[dict] = []
        brann_multiplier = max(
            (3 if unit["golden"] else 2 for unit in board if unit["card_id"] == BRANN),
            default=1,
        )
        kalecgos_gain = sum(
            4 if unit["golden"] else 2 for unit in board if unit["card_id"] == KALECGOS
        )
        for turn in range(online_turn, checkpoint_turn + 1):
            battlecry_actions = 1 if turn == online_turn else 3
            gain = battlecry_actions * brann_multiplier * kalecgos_gain
            for unit in board:
                if "dragon" in unit["tribes"] or "all" in unit["tribes"]:
                    unit["attack"] += gain
                    unit["health"] += gain
            traces.append(
                _snapshot(
                    turn,
                    board,
                    [
                        (
                            f"Resolved {battlecry_actions} "
                            f"{'immediate Battlecry' if turn == online_turn else 'Battlecry actions'} with "
                            f"{brann_multiplier}x Brann triggers for +{gain}/+{gain} on Dragons"
                        )
                    ],
                )
            )
        return traces
    if profile != "lobster-deathstrider":
        raise ValueError(f"Legacy profile handler is not implemented: {profile}")

    traces: list[dict] = []
    lobsters = [unit for unit in board if unit["card_id"] == TASTY_LOBSTER]
    deathstriders = [unit for unit in board if unit["card_id"] == DEATHSTRIDER]
    for turn in range(online_turn, checkpoint_turn + 1):
        combat_board = deepcopy(board)
        targets = [
            unit
            for unit in combat_board
            if unit["card_id"] != TASTY_LOBSTER
            and ("beast" in unit["tribes"] or "all" in unit["tribes"])
        ][:2]
        triggers = sum(2 if unit["golden"] else 1 for unit in deathstriders)
        for _ in range(triggers):
            for lobster in lobsters:
                amount = 2 if lobster["golden"] else 1
                for target in targets:
                    target["attack"] += amount
                    target["health"] += amount
        traces.append(
            _snapshot(
                turn,
                combat_board,
                [
                    (f"A source-verified Rally attack triggered the Lobster Deathrattle {triggers} time(s); "
                    "the hidden future-Lobster improvement is deliberately unmodeled")
                ],
            )
        )
    return traces


def _representative_trace(successes: list[dict], target_power: int) -> dict:
    return min(successes, key=lambda run: (abs(run["power"] - target_power), run["run"]))


def evaluate_comp(
    entry: dict,
    cards_payload: dict,
    *,
    simulations: int = DEFAULT_SIMULATIONS,
    seed: int = DEFAULT_SEED,
    checkpoint_turn: int = CHECKPOINT_TURN,
) -> tuple[dict, dict]:
    """Evaluate one supported registry entry and return summary plus full runs."""
    if isinstance(simulations, bool) or not isinstance(simulations, int) or simulations < 1:
        raise ValueError("simulations must be a positive integer")
    if checkpoint_turn < ROLL_START_TURN:
        raise ValueError("checkpoint_turn cannot precede the roll start")
    profile = _profile_for(entry)
    requirements = _minion_requirements(entry)
    requirements.update(_minion_requirements(entry, "hand_minions"))
    if profile == "embalmer-scam":
        requirements.pop(TIMEWARPED_EMBALMER, None)
    board_template = _expanded_board(entry, cards_payload)
    required_tribes = {
        str(tribe).strip().lower()
        for tribe in entry.get("tribes", [])
        if str(tribe).strip().lower() in STANDARD_TRIBES
    }
    runs: list[dict] = []
    successes: list[dict] = []
    for run_number in range(simulations):
        run_seed = seed * 1_000_003 + run_number * 2
        acquisition_rng = random.Random(run_seed)
        power_rng = random.Random(run_seed + 1)
        online_turn, active_tribes, held_by_rival = _simulate_acquisition(
            cards_payload,
            requirements,
            required_tribes,
            acquisition_rng,
            min(ROLL_TURNS, checkpoint_turn - ROLL_START_TURN + 1),
        )
        run = {
            "run": run_number,
            "eligible": required_tribes <= active_tribes,
            "active_tribes": sorted(active_tribes),
            "held_by_rival": held_by_rival,
            "online_turn": online_turn,
            "power": 0,
            "turns": [],
        }
        if online_turn is not None:
            board = [
                {**unit, "keywords": list(unit["keywords"]), "tribes": list(unit["tribes"])}
                for unit in board_template
            ]
            if profile == "hogrider":
                trace = _simulate_hogrider(
                    entry, cards_payload, board, online_turn, checkpoint_turn, power_rng
                )
            elif profile == "plaguerunner-butchering":
                trace = _simulate_plaguerunner(
                    entry, cards_payload, board, online_turn, checkpoint_turn, power_rng
                )
            elif profile == "vindicator-poet-warpwing":
                trace = _simulate_warpwing(
                    entry, cards_payload, board, online_turn, checkpoint_turn, power_rng
                )
            elif profile == "demon-shop-consume":
                trace = _simulate_demons(
                    entry,
                    cards_payload,
                    board,
                    online_turn,
                    checkpoint_turn,
                    active_tribes,
                    power_rng,
                )
            else:
                trace = _simulate_legacy(
                    profile, entry, cards_payload, board, online_turn, checkpoint_turn, power_rng
                )
            run["turns"] = trace
            run["power"] = trace[-1]["power"]
            successes.append(run)
        runs.append(run)

    powers = [run["power"] for run in successes]
    online_turns = [run["online_turn"] for run in successes]
    p20 = _percentile(powers, 0.20)
    p50 = _percentile(powers, 0.50)
    p80 = _percentile(powers, 0.80)
    summary = {
        "probability": round(len(successes) / simulations, 6),
        "turns_to_online": _percentile(online_turns, 0.50),
        "p20_power": p20,
        "p50_power": p50,
        "p80_power": p80,
    }
    representative = (
        {
            "p20": _representative_trace(successes, p20),
            "p50": _representative_trace(successes, p50),
            "p80": _representative_trace(successes, p80),
        }
        if successes
        else {"p20": None, "p50": None, "p80": None}
    )
    artifact = {
        "slug": entry.get("slug"),
        "model_version": MODEL_VERSION,
        "profile": profile,
        "conditional_prerequisites": {
            "spells": _entry_card_ids(entry, "spells"),
            "cards": _entry_card_ids(entry, "prerequisites"),
        },
        "assumptions": PROFILE_ASSUMPTIONS.get(profile, []),
        "acquisition_assumptions": {
            "pool_copies_by_tier": {str(tier): copies for tier, copies in POOL_COPIES_BY_TIER.items()},
            "rival_hold_chance_per_required_card": CONTENTION_HOLD_CHANCE,
            "roll_start_turn": ROLL_START_TURN,
            "roll_turns": ROLL_TURNS,
        },
        "seed": seed,
        "checkpoint_turn": checkpoint_turn,
        "simulation_count": simulations,
        "summary": summary,
        "representative_traces": representative,
        "simulations": runs,
    }
    return summary, artifact


def write_simulation_artifact(path: Path, artifact: dict) -> None:
    """Write reproducible gzip JSON (fixed mtime and canonical key order)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(artifact, sort_keys=True, separators=(",", ":")) + "\n").encode()
    with path.open("wb") as raw, gzip.GzipFile(
        filename="", mode="wb", fileobj=raw, mtime=0
    ) as compressed:
        compressed.write(payload)


def recalculate_registry(
    registry: dict,
    cards_payload: dict,
    *,
    simulation_dir: Path,
    simulations: int = DEFAULT_SIMULATIONS,
    seed: int = DEFAULT_SEED,
    checkpoint_turn: int = CHECKPOINT_TURN,
) -> dict:
    """Recalculate every supported entry without storing model config in it."""
    updated = deepcopy(registry)
    updated["schema_version"] = 2
    result_fields = (
        "probability",
        "turns_to_online",
        "p20_power",
        "p50_power",
        "p80_power",
    )
    for entry in updated.get("pages", []):
        # Legacy guide sections describe options and mentions, not a legal
        # seven-slot board. Never infer a simulated composition from them.
        entry.setdefault("minions", [])
        entry.setdefault("spells", [])
        for obsolete in (
            "core",
            "addons",
            "cycle",
            "cards",
            "evaluation",
            "power_p20",
            "power_p50",
            "power_p80",
        ):
            entry.pop(obsolete, None)
        for field in result_fields:
            entry.pop(field, None)
        minion_counts = Counter(_entry_card_ids(entry, "minions"))
        if not any(requirements <= minion_counts for _, requirements, _, _, _ in ENGINE_PROFILES):
            continue
        summary, artifact = evaluate_comp(
            entry,
            cards_payload,
            simulations=simulations,
            seed=seed,
            checkpoint_turn=checkpoint_turn,
        )
        entry.update(summary)
        write_simulation_artifact(simulation_dir / f"{entry['slug']}.json.gz", artifact)
    return updated
