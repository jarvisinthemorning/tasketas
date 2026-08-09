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

MODEL_VERSION = "power-v4"
DEFAULT_SIMULATIONS = 5_000
DEFAULT_SEED = 14_014
ROLL_START_TURN = 10
ROLL_TURNS = 4
CHECKPOINT_TURN = 14
CONTENTION_HOLD_CHANCE = 0.35

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

ENGINE_PROFILES = (
    ("hogrider", frozenset({HOGRIDER, GEM_RAT})),
    ("demon-shop-consume", frozenset({DISTRACTOR, FELBOAR})),
    ("plaguerunner-butchering", frozenset({PLAGUERUNNER, DRUSTFALLEN_BUTCHER})),
    (
        "vindicator-poet-warpwing",
        frozenset({FIRE_FORGED_EVOKER, CRIMSON_VINDICATOR, PERSISTENT_POET, WARPWING}),
    ),
)


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
    minion_ids = frozenset(_entry_card_ids(entry, "minions"))
    spell_ids = frozenset(_entry_card_ids(entry, "spells"))
    for name, requirements in ENGINE_PROFILES:
        if requirements <= minion_ids:
            if name == "hogrider" and GEM_DAY not in spell_ids:
                raise ValueError("Hogrider simulations require Gem Day in spells")
            if name == "demon-shop-consume" and METHODICAL_MADNESS not in spell_ids:
                raise ValueError("Demon shop-consume simulations require Methodical Madness in spells")
            if name == "plaguerunner-butchering" and BUTCHERING not in spell_ids:
                raise ValueError("Plaguerunner simulations require Butchering in spells")
            if name == "vindicator-poet-warpwing" and MIGHTY_DRAGONBREATH not in spell_ids:
                raise ValueError("Warpwing simulations require Mighty Dragonbreath in spells")
            return name
    raise ValueError("No deterministic power profile supports this composition yet")


def _minion_requirements(entry: dict) -> Counter[int]:
    requirements: Counter[int] = Counter()
    for item in entry.get("minions", []):
        item = {"card_id": item} if isinstance(item, int) and not isinstance(item, bool) else item
        if not isinstance(item, dict):
            raise TypeError("minions entries must be card IDs or mappings")
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
    pool = _pool_for_lobby(cards_payload, active_tribes, 6)
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
    return {
        "turn": turn,
        "raw_stats": sum(unit["attack"] + unit["health"] for unit in board),
        "power": effective_board_power(board),
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
    protected_warpwings: list[tuple[dict, int]] = []
    for index, unit in enumerate(board):
        if unit["card_id"] != WARPWING:
            continue
        adjacent_poets = [
            board[neighbor]
            for neighbor in (index - 1, index + 1)
            if 0 <= neighbor < len(board) and board[neighbor]["card_id"] == PERSISTENT_POET
        ]
        if adjacent_poets:
            multiplier = max(2 if poet["golden"] else 1 for poet in adjacent_poets)
            protected_warpwings.append((unit, multiplier))
    evoker_attack = sum(4 if unit["golden"] else 2 for unit in evokers)
    evoker_health = sum(2 if unit["golden"] else 1 for unit in evokers)

    for turn in range(online_turn, checkpoint_turn + 1):
        dragonbreaths = sum(2 if unit["golden"] else 1 for unit in vindicators)
        dragonbreath_attack = dragonbreaths * 2
        dragonbreath_health = dragonbreaths * 2
        retained_attack = evoker_attack + dragonbreath_attack
        retained_health = evoker_health + dragonbreath_health
        for unit, poet_multiplier in protected_warpwings:
            unit["attack"] += retained_attack * poet_multiplier
            unit["health"] += retained_health * poet_multiplier
        # Each combat-cast Dragonbreath doubles the Evoker's current buff for
        # later fights; it cannot enlarge the Start-of-Combat effect already
        # resolved this combat.
        evoker_attack *= 2**dragonbreaths
        evoker_health *= 2**dragonbreaths
        events = [
            (
                f"Retained +{retained_attack}/+{retained_health} on "
                f"{len(protected_warpwings)} Poet-protected Warpwings after "
                f"{dragonbreaths} Mighty Dragonbreath casts"
            )
        ]
        traces.append(_snapshot(turn, board, events))
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
    board_template = _expanded_board(entry, cards_payload)
    required_tribes = {str(tribe).strip().lower() for tribe in entry.get("tribes", [])}
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
            else:
                trace = _simulate_demons(
                    entry,
                    cards_payload,
                    board,
                    online_turn,
                    checkpoint_turn,
                    active_tribes,
                    power_rng,
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
        minion_ids = frozenset(_entry_card_ids(entry, "minions"))
        if not any(requirements <= minion_ids for _, requirements in ENGINE_PROFILES):
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
