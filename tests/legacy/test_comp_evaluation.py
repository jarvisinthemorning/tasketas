import unittest

from comp_evaluation import (
    calculate_baseline_gain,
    classify_frequency,
    eligible_lobby_probability,
    estimate_pivot_probability,
)


class CompEvaluationTests(unittest.TestCase):
    def test_hogrider_core_floor_uses_one_gem_day_and_five_targets(self):
        result = calculate_baseline_gain(
            "hogrider-core-v1",
            turns=4,
            parameters={
                "other_quilboars": 5,
                "choose_one_cards_per_turn": 1,
                "starting_gem_attack": 1,
                "starting_gem_health": 1,
            },
        )
        self.assertEqual(result["projected_stat_gain"], 90)

    def test_demon_core_floor_accumulates_persistent_shop_buffs(self):
        result = calculate_baseline_gain(
            "demon-shop-consume-v1",
            turns=2,
            parameters={
                "felboars": 1,
                "spell_casts_per_turn": 3,
                "average_base_shop_attack": 6,
                "average_base_shop_health": 6,
            },
        )
        self.assertEqual(result["projected_stat_gain"], 60)

    def test_eligible_lobby_probability_for_one_required_tribe(self):
        self.assertEqual(eligible_lobby_probability(1), 0.5)

    def test_frequency_labels_keep_the_numeric_probability_visible(self):
        self.assertEqual(classify_frequency(0.25), "Common")
        self.assertEqual(classify_frequency(0.06), "Regular")
        self.assertEqual(classify_frequency(0.02), "Rare")
        self.assertEqual(classify_frequency(0.005), "High-roll")
        self.assertEqual(classify_frequency(0.0005), "Lottery")

    def test_pivot_simulation_is_deterministic_and_completes_a_tiny_pool(self):
        cards = {
            "cards": {
                "1": {"id": 1, "type": "minion", "tier": 1, "tribes": ["Demon"], "pool": True},
            }
        }
        first = estimate_pivot_probability(
            cards,
            required_card_ids=[1],
            required_tribes=["demon"],
            tavern_tier=1,
            turns=1,
            simulations=100,
            seed=7,
        )
        second = estimate_pivot_probability(
            cards,
            required_card_ids=[1],
            required_tribes=["demon"],
            tavern_tier=1,
            turns=1,
            simulations=100,
            seed=7,
        )
        self.assertEqual(first, second)
        self.assertEqual(first["conditional_probability"], 1.0)
        self.assertEqual(first["random_lobby_adjusted_probability"], 0.5)
        self.assertEqual(first["conditional_ci95"], [1.0, 1.0])

    def test_pivot_simulation_rejects_unsupported_duplicate_targets_and_boolean_counts(self):
        cards = {
            "cards": {
                "1": {
                    "id": 1,
                    "name": "Target",
                    "type": "minion",
                    "tier": 1,
                    "tribes": ["Demon"],
                    "modes": ["solo"],
                    "pool": True,
                    "categories": ["tavern"],
                }
            }
        }
        with self.assertRaisesRegex(ValueError, "duplicate required"):
            estimate_pivot_probability(
                cards,
                required_card_ids=[1, 1],
                required_tribes=["demon"],
                tavern_tier=1,
                turns=1,
                simulations=10,
            )
        with self.assertRaisesRegex(ValueError, "must be integers"):
            estimate_pivot_probability(
                cards,
                required_card_ids=[1],
                required_tribes=["demon"],
                tavern_tier=1,
                turns=1,
                simulations=True,
            )
    def test_pivot_simulation_excludes_duos_only_cards(self):
        cards = {
            "cards": {
                "1": {
                    "id": 1,
                    "type": "minion",
                    "tier": 1,
                    "tribes": ["Demon"],
                    "modes": ["duos"],
                    "pool": True,
                }
            }
        }
        with self.assertRaisesRegex(ValueError, "required card is absent"):
            estimate_pivot_probability(
                cards,
                required_card_ids=[1],
                required_tribes=["demon"],
                tavern_tier=1,
                turns=1,
                simulations=10,
            )


if __name__ == "__main__":
    unittest.main()