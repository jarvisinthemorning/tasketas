import gzip
import json
import random
import tempfile
import unittest
from pathlib import Path

from comp_power import (
    _simulate_hogrider,
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
            demon_entry(False), CARDS, simulations=200, seed=77, checkpoint_turn=10
        )
        expanded = demon_entry(True)
        expanded["minions"][-1]["count"] = 2
        harder, _ = evaluate_comp(
            expanded, CARDS, simulations=200, seed=77, checkpoint_turn=10
        )
        self.assertGreater(baseline["probability"], harder["probability"])

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
