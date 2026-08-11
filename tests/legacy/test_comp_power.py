import gzip
import json
import random
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import comp_power
from comp_power import (
    _profile_for,
    _simulate_hogrider,
    _simulate_legacy,
    _simulate_plaguerunner,
    _simulate_warpwing,
    effective_board_power,
    evaluate_comp,
    recalculate_registry,
    write_simulation_artifact,
)

CARDS = {
    "cards": {
        "132901": {
            "id": 132901,
            "name": "Devilish Distractor",
            "type": "minion",
            "tier": 4,
            "attack": 3,
            "health": 6,
            "attack_gold": 6,
            "health_gold": 12,
            "text": "Whenever you cast a spell on this, give minions in the Tavern +2/+2 this game.",
            "text_gold": "Whenever you cast a spell on this, give minions in the Tavern +4/+4 this game.",
            "keywords": [],
            "tribes": ["Demon"],
            "modes": ["solo"],
            "categories": ["tavern"],
            "pool": True,
        },
        "110664": {
            "id": 110664,
            "name": "Felboar",
            "type": "minion",
            "tier": 5,
            "attack": 2,
            "health": 6,
            "attack_gold": 4,
            "health_gold": 12,
            "text": "After you cast 3 spells, consume a minion in the Tavern to gain its stats.",
            "text_gold": "After you cast 3 spells, consume a minion in the Tavern to gain double its stats.",
            "keywords": [],
            "tribes": ["Demon", "Quilboar"],
            "modes": ["solo"],
            "categories": ["tavern"],
            "pool": True,
        },
        "130298": {
            "id": 130298,
            "name": "Balinda Stonehearth",
            "type": "minion",
            "tier": 6,
            "attack": 6,
            "health": 6,
            "attack_gold": 12,
            "health_gold": 12,
            "text": "Your spells that target friendly minions cast twice.",
            "text_gold": "Your spells that target friendly minions cast three times.",
            "keywords": ["aura"],
            "tribes": [],
            "modes": ["solo"],
            "categories": ["tavern"],
            "pool": True,
        },
        "132903": {
            "id": 132903,
            "name": "Methodical Madness",
            "type": "spell",
            "tier": 4,
            "attack": 0,
            "health": 0,
            "text": "Choose a friendly Demon. It consumes 2 random Tavern minions to gain their stats and Bonus Keywords.",
            "keywords": [],
            "tribes": [],
            "modes": ["solo"],
            "categories": ["tavern"],
            "pool": True,
        },
        "900": {
            "id": 900,
            "name": "Shielded Body",
            "type": "minion",
            "tier": 1,
            "attack": 10,
            "health": 10,
            "text": "Divine Shield",
            "keywords": ["divine shield"],
            "tribes": [],
            "modes": ["solo"],
            "categories": ["tavern"],
            "pool": True,
        },
    }
}

REAL_CARDS = json.loads((Path(__file__).parents[2] / "data" / "cards.json").read_text())


def demon_entry(with_balinda=True):
    minions = [
        {"card_id": 132901, "count": 1, "golden_count": 0},
        {"card_id": 110664, "count": 1, "golden_count": 0},
    ]
    if with_balinda:
        minions.append({"card_id": 130298, "count": 1, "golden_count": 0})
    return {
        "slug": "demon-test",
        "tribes": ["demon"],
        "minions": minions,
        "spells": [{"card_id": 132903, "count": 1}],
    }


class CompPowerTests(unittest.TestCase):
    def test_lobster_profile_scores_current_combat_without_persisting_combat_buffs(self):
        entry = {
            "minions": [
                {"card_id": 132796, "count": 1, "golden_count": 0},
                {"card_id": 132808, "count": 1, "golden_count": 0},
            ],
            "spells": [],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)
        base = comp_power.effective_board_power(board)

        trace = comp_power._simulate_legacy(
            "lobster-deathstrider", entry, REAL_CARDS, board, 13, 14, random.Random(1)
        )

        self.assertGreater(trace[-1]["power"], base)
        self.assertEqual((board[0]["attack"], board[0]["health"]), (1, 1))
        self.assertIn("Lobster Deathrattle", trace[-1]["events"][0])

    def test_kalecgos_profile_converts_battlecries_into_dragon_stats(self):
        entry = {
            "minions": [
                {"card_id": 60630, "count": 1, "golden_count": 0},
                {"card_id": 96786, "count": 1, "golden_count": 0},
                {"card_id": 132955, "count": 2, "golden_count": 0},
                {"card_id": 132957, "count": 1, "golden_count": 0},
            ],
            "spells": [],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "kalecgos-battlecry", entry, REAL_CARDS, board, 13, 14, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (20, 28))
        self.assertEqual((board[2]["attack"], board[2]["health"]), (18, 25))
        self.assertIn("1 immediate Battlecry", trace[0]["events"][0])
        self.assertIn("3 Battlecry actions", trace[-1]["events"][0])

    def test_moat_profile_amplifies_later_mana_surge_turns(self):
        entry = {
            "minions": [
                {"card_id": 132981, "count": 1, "golden_count": 0},
                {"card_id": 120674, "count": 1, "golden_count": 0},
            ],
            "spells": [],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "moat-mana-surge", entry, REAL_CARDS, board, 13, 14, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (22, 30))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (24, 25))
        self.assertIn("amplifier reached +2/+4", trace[-1]["events"][0])

    def test_utility_drone_profile_counts_fauna_casts_and_magnetizations(self):
        entry = {
            "minions": [
                {"card_id": 132893, "count": 1, "golden_count": 0},
                {"card_id": 120905, "count": 1, "golden_count": 0},
                {"card_id": 98588, "count": 1, "golden_count": 0},
            ],
            "spells": [{"card_id": 104472, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "utility-drone-magnetics", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (22, 22))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (4, 9))
        self.assertEqual((board[2]["attack"], board[2]["health"]), (20, 22))
        self.assertIn("2 Natural Blessing casts", trace[-1]["events"][0])

    def test_fauna_spellcraft_profile_applies_meditative_bonus_before_blessings(self):
        entry = {
            "minions": [
                {"card_id": 119942, "count": 1, "golden_count": 0},
                {"card_id": 120905, "count": 1, "golden_count": 0},
                {"card_id": 114816, "count": 1, "golden_count": 0},
            ],
            "spells": [{"card_id": 104472, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "fauna-spellcraft", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (11, 16))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (12, 17))
        self.assertEqual((board[2]["attack"], board[2]["health"]), (13, 12))
        self.assertIn("spell bonus reached +1/+1", trace[-1]["events"][0])

    def test_escapee_hooktusk_profile_separates_castaway_discovers_from_lockbox_rewards(self):
        entry = {
            "minions": [
                {"card_id": 132762, "count": 1, "golden_count": 0},
                {"card_id": 132925, "count": 1, "golden_count": 0},
                {"card_id": 132921, "count": 1, "golden_count": 0},
            ],
            "spells": [{"card_id": 132766, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "escapee-hooktusk", entry, REAL_CARDS, board, 13, 15, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (8, 8))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (4, 4))
        self.assertEqual((board[2]["attack"], board[2]["health"]), (4, 5))
        self.assertIn("1 Castaway Discover", trace[-1]["events"][0])
        self.assertNotIn("Lockbox Discover", trace[-1]["events"][0])

    def test_snazzy_profile_credits_one_conditional_reborn_trigger(self):
        entry = {
            "minions": [
                {"card_id": 133083, "count": 1, "golden_count": 0},
                {"card_id": 133081, "count": 1, "golden_count": 0},
                {"card_id": 95265, "count": 1, "golden_count": 0},
            ],
            "spells": [],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "snazzy-reborn", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        self.assertEqual((board[1]["attack"], board[1]["health"]), (7, 7))
        self.assertEqual(trace[-1]["raw_stats"], 49)
        self.assertEqual(trace[-1]["power"], 63)
        self.assertIn("Banshee itself", trace[-1]["events"][0])
        self.assertIn("right-most Undead", trace[-1]["events"][0])
        self.assertGreater(trace[-1]["power"], trace[-1]["raw_stats"])

    def test_tidecaller_profile_converts_targeted_spells_and_hand_stats_into_combat_power(self):
        entry = {
            "minions": [
                {"card_id": 133026, "count": 1, "golden_count": 0},
                {"card_id": 132989, "count": 1, "golden_count": 0},
                {"card_id": 98948, "count": 1, "golden_count": 0},
                {"card_id": 126637, "count": 1, "golden_count": 0},
            ],
            "hand_minions": [{"card_id": 98509, "count": 1, "golden_count": 0}],
            "spells": [],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "tidecaller-handbuff", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        self.assertEqual(trace[-1]["raw_stats"], 148)
        self.assertEqual((board[3]["attack"], board[3]["health"]), (6, 7))
        self.assertIn("Bream Counter reach 21/21", trace[-1]["events"][0])

    def test_dagger_profile_repeats_declared_gift_casts_through_balinda_and_gatekeeper(self):
        entry = {
            "minions": [
                {"card_id": 133329, "count": 1, "golden_count": 0},
                {"card_id": 130298, "count": 1, "golden_count": 0},
            ],
            "spells": [
                {"card_id": 132790, "count": 1},
                {"card_id": 132835, "count": 1},
                {"card_id": 132207, "count": 1},
            ],
            "prerequisites": [{"card_id": 133713, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "dagger-amalgamation", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        gain = 2 * len(comp_power.STANDARD_TRIBES) * 2
        self.assertEqual((board[0]["attack"], board[0]["health"]), (6 + gain, 6 + gain))
        self.assertIn("2 Amalgamation casts", trace[-1]["events"][0])

    def test_embalmer_profile_credits_reborn_leeroy_and_venomous_redundancy(self):
        entry = {
            "minions": [
                {"card_id": 127446, "count": 2, "golden_count": 0},
                {"card_id": 90425, "count": 2, "golden_count": 0},
            ],
            "spells": [{"card_id": 126271, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)

        trace = comp_power._simulate_legacy(
            "embalmer-scam", entry, REAL_CARDS, board, 13, 13, random.Random(1)
        )

        leeroys = [unit for unit in board if unit["card_id"] == 90425]
        self.assertEqual([unit["removal_uses"] for unit in leeroys], [3, 2])
        self.assertGreaterEqual(trace[-1]["power"], 2500)
        self.assertIn("five bounded Leeroy removal uses", trace[-1]["events"][0])

    def test_bristlemane_profile_tracks_gems_on_juggernaut_and_rally_golem(self):
        entry = {
            "minions": [
                {"card_id": 126671, "count": 1, "golden_count": 0},
                {"card_id": 132320, "count": 1, "golden_count": 0},
                {"card_id": 132636, "count": 1, "golden_count": 0},
            ],
            "spells": [{"card_id": 110642, "count": 1}],
        }
        board = comp_power._expanded_board(entry, REAL_CARDS)
        base = comp_power.effective_board_power(board)

        trace = comp_power._simulate_legacy(
            "bristlemane-juggernaut", entry, REAL_CARDS, board, 10, 14, random.Random(1)
        )

        self.assertEqual((board[1]["blood_gem_attack"], board[1]["blood_gem_health"]), (0, 0))
        self.assertEqual((board[2]["blood_gem_attack"], board[2]["blood_gem_health"]), (13, 13))
        self.assertGreater(trace[-1]["power"], base + 26)
        self.assertIn("Juggernaut bank is +13/+13", trace[-1]["events"][0])

    def test_lobster_evaluation_uses_legacy_trace(self):
        entry = {
            "slug": "beast-test",
            "tribes": ["beast"],
            "minions": [
                {"card_id": 132796, "count": 1, "golden_count": 0},
                {"card_id": 132808, "count": 1, "golden_count": 0},
                {"card_id": 132800, "count": 1, "golden_count": 0},
            ],
            "spells": [],
        }

        summary, artifact = evaluate_comp(entry, REAL_CARDS, simulations=200, seed=3)

        self.assertGreater(summary["probability"], 0)
        success = next(run for run in artifact["simulations"] if run["online_turn"] is not None)
        self.assertIn("Lobster Deathrattle", success["turns"][-1]["events"][0])

    def test_legacy_profiles_cover_every_missing_engine(self):
        cases = {
            "lobster-deathstrider": ([132796, 132808, 132800], [], [], []),
            "kalecgos-battlecry": ([60630, 96786, 132955, 132955, 132957], [], [], []),
            "moat-mana-surge": ([132981, 120674], [], [], []),
            "tempest-revenant": ([132983, 126173], [], [], [71464]),
            "utility-drone-magnetics": (
                [132893, 120905, 98588, 130298, 101314],
                [104472],
                [],
                [],
            ),
            "fauna-spellcraft": ([119942, 120905, 130298], [104472], [], []),
            "escapee-hooktusk": ([132762, 132925, 132921], [132766], [], []),
            "snazzy-reborn": ([133083, 133081, 95265], [], [], []),
            "tidecaller-handbuff": ([133026, 132989, 98948, 126637], [], [98509], []),
            "dagger-amalgamation": ([133329, 130298], [132790], [], [133713]),
            "embalmer-scam": (
                [127446, 127446, 90425, 90425],
                [126271],
                [],
                [],
            ),
            "bristlemane-juggernaut": ([132320, 132636, 126671], [110642], [], []),
        }
        for expected, (minions, spells, hand_minions, prerequisites) in cases.items():
            with self.subTest(profile=expected):
                entry = {
                    "minions": [
                        {"card_id": card_id, "count": count, "golden_count": 0}
                        for card_id, count in Counter(minions).items()
                    ],
                    "spells": [{"card_id": card_id, "count": 1} for card_id in spells],
                    "hand_minions": [
                        {"card_id": card_id, "count": 1, "golden_count": 0}
                        for card_id in hand_minions
                    ],
                    "prerequisites": [
                        {"card_id": card_id, "count": 1} for card_id in prerequisites
                    ],
                }
                self.assertEqual(_profile_for(entry), expected)

    def test_tempest_revenant_requires_spirit_swap_and_keeps_temporary_swap_out_of_board_state(self):
        entry = {
            "minions": [
                {"card_id": 132983, "count": 1},
                {"card_id": 126173, "count": 1},
            ],
            "spells": [],
            "prerequisites": [{"card_id": 71464, "count": 1}],
        }
        self.assertEqual(_profile_for(entry), "tempest-revenant")

        entry["prerequisites"] = []
        with self.assertRaisesRegex(ValueError, "Spirit Swap"):
            _profile_for(entry)

        def unit(card_id, attack, health):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": attack,
                "health": health,
                "golden": False,
                "keywords": [],
                "tribes": ["elemental"],
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [unit(126173, 3, 6), unit(132983, 3, 12)]
        trace = _simulate_legacy(
            "tempest-revenant", entry, REAL_CARDS, board, 12, 14, random.Random(1)
        )

        self.assertEqual((board[0]["attack"], board[0]["health"]), (3, 6))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (30, 24))
        self.assertIn("deferred", trace[0]["events"][0])
        self.assertIn("2 active Easterly Winds", trace[-1]["events"][0])
        self.assertIn("selected anchor received 1 hit", trace[-1]["events"][0])
        self.assertIn("Spirit Swap copied 12 Attack", trace[-1]["events"][0])

        registry = json.loads(
            (Path(__file__).resolve().parents[2] / "content" / "legacy" / "registry.json").read_text()
        )
        published = next(
            page for page in registry["pages"] if page["slug"] == "elemental-tempest-revenant-spirit-swap"
        )
        _, artifact = evaluate_comp(published, REAL_CARDS, simulations=500, seed=14_014)
        self.assertIn("base Tavern-minion stats", " ".join(artifact["assumptions"]))
        successful = next(run for run in artifact["simulations"] if run["online_turn"] is not None)
        self.assertIn("deferred", successful["turns"][0]["events"][0])
        self.assertTrue(
            any("random Tavern slots" in event for turn in successful["turns"] for event in turn["events"])
        )

        one_embalmer = {
            "minions": [
                {"card_id": 127446, "count": 1, "golden_count": 0},
                {"card_id": 90425, "count": 2, "golden_count": 0},
            ],
            "spells": [{"card_id": 126271, "count": 1}],
        }
        with self.assertRaisesRegex(ValueError, "No deterministic power profile"):
            _profile_for(one_embalmer)

    def test_warpwing_poet_does_not_retain_for_nonadjacent_warpwings(self):
        def unit(card_id, attack, health, tribes):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": attack,
                "health": health,
                "golden": False,
                "keywords": [],
                "tribes": tribes,
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [
            unit(92413, 12, 4, ["dragon"]),
            unit(120301, 8, 5, ["dragon"]),
            unit(132953, 8, 9, ["dragon"]),
            unit(108463, 2, 3, ["dragon"]),
            unit(92413, 12, 4, ["dragon"]),
        ]

        _simulate_warpwing({}, CARDS, board, 13, 13, random.Random(1))

        self.assertEqual((board[0]["attack"], board[0]["health"]), (12, 4))
        self.assertEqual((board[4]["attack"], board[4]["health"]), (16, 7))

    def test_poet_retains_combat_gains_on_every_adjacent_dragon(self):
        def unit(card_id, attack, health, keywords=()):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": attack,
                "health": health,
                "golden": False,
                "keywords": list(keywords),
                "tribes": ["dragon"],
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [
            unit(120301, 8, 5),
            unit(132953, 8, 9, ["divine shield"]),
            unit(108463, 2, 3),
            unit(92413, 12, 4),
        ]

        _simulate_warpwing({}, CARDS, board, 13, 13, random.Random(1))

        self.assertEqual((board[0]["attack"], board[0]["health"]), (8, 5))
        self.assertEqual((board[1]["attack"], board[1]["health"]), (13, 13))
        self.assertEqual((board[2]["attack"], board[2]["health"]), (2, 3))
        self.assertEqual((board[3]["attack"], board[3]["health"]), (16, 7))

    def test_warpwing_poet_retains_evoker_and_vindicator_combat_buffs(self):
        def unit(card_id, attack, health, tribes, keywords=()):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": attack,
                "health": health,
                "golden": False,
                "keywords": list(keywords),
                "tribes": tribes,
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [
            unit(120301, 8, 5, ["dragon"]),
            unit(132953, 8, 9, ["dragon"], ["divine shield"]),
            unit(92413, 12, 4, ["dragon"]),
            unit(108463, 2, 3, ["dragon"], ["divine shield"]),
            unit(92413, 12, 4, ["dragon"]),
        ]

        trace = _simulate_warpwing({}, CARDS, board, 13, 14, random.Random(1))

        self.assertEqual(len(trace), 2)
        self.assertEqual((board[2]["attack"], board[2]["health"]), (22, 11))
        self.assertEqual((board[4]["attack"], board[4]["health"]), (22, 11))
        self.assertIn("2 Poet-adjacent Dragons", trace[-1]["events"][0])

    def test_plaguerunner_converts_butchering_refills_into_permanent_attack(self):
        def unit(card_id, attack, health, tribes):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": attack,
                "health": health,
                "golden": False,
                "keywords": [],
                "tribes": tribes,
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [
            unit(126451, 4, 2, ["undead"]),
            unit(130884, 6, 10, []),
            unit(120219, 6, 3, ["undead"]),
            unit(120219, 6, 3, ["undead"]),
            unit(133081, 7, 7, ["undead"]),
            unit(120104, 2, 7, ["undead"]),
            unit(120104, 2, 7, ["undead"]),
        ]

        trace = _simulate_plaguerunner({}, CARDS, board, 13, 14, random.Random(1))

        self.assertEqual(len(trace), 2)
        self.assertEqual(board[0]["attack"], 46)
        self.assertEqual(board[1]["attack"], 6)
        self.assertIn("3 Butchering actions", trace[-1]["events"][0])

    def test_plaguerunner_evaluation_uses_its_engine_trace(self):
        cards = json.loads(json.dumps(CARDS))
        cards["cards"].update(
            {
                "126451": {
                    "id": 126451,
                    "name": "Plaguerunner",
                    "type": "minion",
                    "tier": 4,
                    "attack": 4,
                    "health": 2,
                    "attack_gold": 8,
                    "health_gold": 4,
                    "keywords": ["deathrattle"],
                    "tribes": ["Undead"],
                    "modes": ["solo"],
                    "categories": ["tavern"],
                    "pool": True,
                },
                "120104": {
                    "id": 120104,
                    "name": "Drustfallen Butcher",
                    "type": "minion",
                    "tier": 5,
                    "attack": 2,
                    "health": 7,
                    "attack_gold": 4,
                    "health_gold": 14,
                    "keywords": ["avenge"],
                    "tribes": ["Undead"],
                    "modes": ["solo"],
                    "categories": ["tavern"],
                    "pool": True,
                },
            }
        )
        entry = {
            "slug": "plaguerunner-test",
            "tribes": ["undead"],
            "minions": [
                {"card_id": 126451, "count": 1},
                {"card_id": 120104, "count": 1},
            ],
            "spells": [{"card_id": 110412, "count": 1}],
        }

        summary, artifact = evaluate_comp(entry, cards, simulations=200, seed=77)

        self.assertGreater(summary["probability"], 0)
        success = next(run for run in artifact["simulations"] if run["online_turn"] is not None)
        self.assertIn("Butchering actions", success["turns"][-1]["events"][0])

    def test_warpwing_evaluation_uses_its_engine_trace(self):
        catalog = json.loads((Path(__file__).parents[2] / "data/cards.json").read_text())
        required = (120301, 132953, 108463, 92413)
        cards = {"cards": {str(card_id): catalog["cards"][str(card_id)] for card_id in required}}
        entry = {
            "slug": "warpwing-test",
            "tribes": ["dragon"],
            "minions": [{"card_id": card_id, "count": 1} for card_id in required],
            "spells": [{"card_id": 132995, "count": 1}],
        }

        summary, artifact = evaluate_comp(entry, cards, simulations=200, seed=77)

        self.assertGreater(summary["probability"], 0)
        success = next(run for run in artifact["simulations"] if run["online_turn"] is not None)
        self.assertIn("Poet-adjacent Dragons", success["turns"][-1]["events"][0])

    def test_warpwing_profile_requires_the_full_retention_engine(self):
        entry = {
            "minions": [
                {"card_id": 120301, "count": 1},
                {"card_id": 132953, "count": 1},
                {"card_id": 108463, "count": 1},
                {"card_id": 92413, "count": 1},
            ],
            "spells": [{"card_id": 132995, "count": 1}],
        }
        self.assertEqual(_profile_for(entry), "vindicator-poet-warpwing")

        entry["spells"] = []
        with self.assertRaisesRegex(ValueError, "Mighty Dragonbreath"):
            _profile_for(entry)

        entry["spells"] = [{"card_id": 132995, "count": 1}]
        entry["minions"] = entry["minions"][:-1]
        with self.assertRaisesRegex(ValueError, "No deterministic power profile"):
            _profile_for(entry)

    def test_plaguerunner_profile_requires_butchering_fuel(self):
        entry = {
            "minions": [
                {"card_id": 126451, "count": 1},
                {"card_id": 120104, "count": 2},
            ],
            "spells": [{"card_id": 110412, "count": 1}],
        }
        self.assertEqual(_profile_for(entry), "plaguerunner-butchering")

        entry["spells"] = []
        with self.assertRaisesRegex(ValueError, "Butchering"):
            _profile_for(entry)

    def test_hogrider_delays_end_of_turn_fuel_and_resolves_gatekeeper_tea_set(self):
        def unit(card_id, tribes):
            return {
                "card_id": card_id,
                "name": str(card_id),
                "attack": 6,
                "health": 6,
                "golden": False,
                "keywords": [],
                "tribes": tribes,
                "blood_gem_attack": 0,
                "blood_gem_health": 0,
            }

        board = [
            unit(116195, ["quilboar"]),
            unit(116434, ["beast", "quilboar"]),
            unit(133329, ["all"]),
        ]
        first = _simulate_hogrider({}, CARDS, board, 10, 10, random.Random(1))
        self.assertEqual(first[-1]["raw_stats"], 36)

        board = [
            unit(116195, ["quilboar"]),
            unit(116434, ["beast", "quilboar"]),
            unit(133329, ["all"]),
        ]
        second = _simulate_hogrider({}, CARDS, board, 10, 11, random.Random(1))
        self.assertGreater(second[-1]["raw_stats"], 42)

    def test_evaluation_is_deterministic_and_keeps_percentiles_and_traces(self):
        first_summary, first_artifact = evaluate_comp(
            demon_entry(), CARDS, simulations=200, seed=77, checkpoint_turn=14
        )
        second_summary, second_artifact = evaluate_comp(
            demon_entry(), CARDS, simulations=200, seed=77, checkpoint_turn=14
        )

        self.assertEqual(first_summary, second_summary)
        self.assertEqual(first_artifact, second_artifact)
        self.assertEqual(
            set(first_summary),
            {"probability", "turns_to_online", "p20_power", "p50_power", "p80_power"},
        )
        self.assertLessEqual(first_summary["p20_power"], first_summary["p50_power"])
        self.assertLessEqual(first_summary["p50_power"], first_summary["p80_power"])
        self.assertEqual(len(first_artifact["simulations"]), 200)
        self.assertTrue(
            all("held_by_rival" in run for run in first_artifact["simulations"])
        )
        self.assertEqual(set(first_artifact["representative_traces"]), {"p20", "p50", "p80"})
        self.assertTrue(first_artifact["representative_traces"]["p80"]["turns"])

    def test_power_uses_card_keywords_and_balinda_multiplier(self):
        plain = effective_board_power(
            [{"card_id": 900, "attack": 10, "health": 10, "keywords": []}]
        )
        shielded = effective_board_power(
            [
                {
                    "card_id": 900,
                    "attack": 10,
                    "health": 10,
                    "keywords": ["divine shield"],
                }
            ]
        )
        self.assertGreater(shielded, plain)

        banshee_without_reborn = effective_board_power(
            [
                {
                    "card_id": 133081,
                    "attack": 7,
                    "health": 7,
                    "keywords": [],
                }
            ]
        )
        banshee_with_reborn = effective_board_power(
            [
                {
                    "card_id": 133081,
                    "attack": 7,
                    "health": 7,
                    "keywords": [],
                },
                {"card_id": 901, "attack": 5, "health": 5, "keywords": ["reborn"]},
            ]
        )
        reborn_body_alone = effective_board_power(
            [{"card_id": 901, "attack": 5, "health": 5, "keywords": ["reborn"]}]
        )
        self.assertGreater(
            banshee_with_reborn,
            banshee_without_reborn + reborn_body_alone,
        )

        without_balinda, _ = evaluate_comp(
            demon_entry(False), CARDS, simulations=200, seed=77, checkpoint_turn=14
        )
        with_balinda, _ = evaluate_comp(
            demon_entry(True), CARDS, simulations=200, seed=77, checkpoint_turn=14
        )
        self.assertGreater(with_balinda["p50_power"], without_balinda["p50_power"])

    def test_probability_requires_every_declared_minion_copy(self):
        baseline, _ = evaluate_comp(
            demon_entry(False), CARDS, simulations=200, seed=77, checkpoint_turn=11
        )
        expanded = demon_entry(True)
        expanded["minions"][-1]["count"] = 2
        expanded["minions"][-1]["golden_count"] = 0
        harder, _ = evaluate_comp(
            expanded, CARDS, simulations=200, seed=77, checkpoint_turn=11
        )
        self.assertGreater(baseline["probability"], harder["probability"])
        self.assertGreater(harder["probability"], 0)

    def test_embalmer_probability_is_conditional_on_timewarped_setup(self):
        entry = {
            "slug": "embalmer-test",
            "tribes": ["undead"],
            "minions": [
                {"card_id": 127446, "count": 2, "golden_count": 0},
                {"card_id": 90425, "count": 2, "golden_count": 0},
            ],
            "spells": [{"card_id": 126271, "count": 1}],
        }

        summary, artifact = evaluate_comp(entry, REAL_CARDS, simulations=500, seed=9)

        self.assertGreater(summary["probability"], 0)
        self.assertTrue(
            all(127446 not in run["held_by_rival"] for run in artifact["simulations"])
        )

    def test_menagerie_label_does_not_make_every_lobby_ineligible(self):
        entry = {
            "slug": "menagerie-test",
            "tribes": ["menagerie"],
            "minions": [
                {"card_id": 133329, "count": 1, "golden_count": 0},
                {"card_id": 130298, "count": 1, "golden_count": 0},
            ],
            "spells": [{"card_id": 132790, "count": 1}],
            "prerequisites": [{"card_id": 133713, "count": 1}],
        }

        summary, _ = evaluate_comp(entry, REAL_CARDS, simulations=200, seed=9)

        self.assertGreater(summary["probability"], 0)

    def test_checkpoint_before_second_roll_does_not_admit_later_online_runs(self):
        summary, artifact = evaluate_comp(
            demon_entry(False), CARDS, simulations=200, seed=77, checkpoint_turn=10
        )
        self.assertTrue(all(run["online_turn"] in (None, 10) for run in artifact["simulations"]))
        self.assertGreaterEqual(summary["probability"], 0)

    def test_simulation_artifact_is_written_as_deterministic_gzip(self):
        _, artifact = evaluate_comp(
            demon_entry(), CARDS, simulations=20, seed=77, checkpoint_turn=14
        )
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.json.gz"
            second = Path(tmp) / "second.json.gz"
            write_simulation_artifact(first, artifact)
            write_simulation_artifact(second, artifact)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with gzip.open(first, "rt", encoding="utf-8") as handle:
                restored = json.load(handle)
            self.assertEqual(restored, artifact)

    def test_registry_recalculation_materializes_results_and_separate_artifact(self):
        registry = {
            "schema_version": 1,
            "pages": [
                demon_entry(),
                {
                    "slug": "legacy-test",
                    "cards": [900],
                    "core": [900],
                    "addons": [],
                    "cycle": [],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            updated = recalculate_registry(
                registry,
                CARDS,
                simulation_dir=Path(tmp),
                simulations=50,
                seed=77,
                checkpoint_turn=14,
            )
            entry = updated["pages"][0]
            self.assertEqual(
                set(entry).intersection(
                    {
                        "probability",
                        "turns_to_online",
                        "p20_power",
                        "p50_power",
                        "p80_power",
                    }
                ),
                {
                    "probability",
                    "turns_to_online",
                    "p20_power",
                    "p50_power",
                    "p80_power",
                },
            )
            self.assertNotIn("evaluation", entry)
            self.assertTrue((Path(tmp) / "demon-test.json.gz").is_file())
            legacy = updated["pages"][1]
            self.assertEqual(legacy["minions"], [])
            self.assertEqual(legacy["spells"], [])
            for obsolete in ("core", "addons", "cycle", "cards", "evaluation"):
                self.assertNotIn(obsolete, legacy)


if __name__ == "__main__":
    unittest.main()
