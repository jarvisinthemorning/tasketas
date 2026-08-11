import math
import unittest

from comp_rarity import RarityUnavailable, calculate_card_rarity


class CompRarityTests(unittest.TestCase):
    def test_minion_rarity_uses_physical_pool_copies_and_shop_slots(self):
        cards = {
            "cards": {
                "1": {"id": 1, "name": "Target", "type": "minion", "tier": 1, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
                "2": {"id": 2, "name": "Other", "type": "minion", "tier": 1, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
            }
        }

        result = calculate_card_rarity(cards, 1)

        expected = 1 - math.comb(15, 3) / math.comb(30, 3)
        self.assertAlmostEqual(result["probability"], expected, places=6)
        self.assertEqual(result["basis"], "per refresh at Tavern Tier 1")
        self.assertEqual(result["assumption"], "uncontested full pool")

    def test_spell_rarity_uses_one_eligible_tavern_spell_offer(self):
        cards = {
            "cards": {
                "10": {"id": 10, "name": "Target Spell", "type": "spell", "tier": 2, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
                "11": {"id": 11, "name": "Other Spell", "type": "spell", "tier": 2, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
            }
        }

        result = calculate_card_rarity(cards, 10)

        self.assertEqual(result["probability"], 0.5)
        self.assertEqual(result["basis"], "per Tavern-spell offer at Tier 2")

    def test_tierless_categorized_spell_uses_its_generated_pool(self):
        cards = {
            "cards": {
                "12": {"id": 12, "name": "Gift", "type": "spell", "tier": None, "tribes": [], "pool": True, "categories": ["darkgift"], "modes": ["solo"]},
                "13": {"id": 13, "name": "Other Gift", "type": "spell", "tier": None, "tribes": [], "pool": True, "categories": ["darkgift"], "modes": ["solo"]},
                "14": {"id": 14, "name": "Tavern Spell", "type": "spell", "tier": 1, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
            }
        }

        result = calculate_card_rarity(cards, 12)

        self.assertEqual(result["probability"], 0.5)
        self.assertEqual(result["percent"], 50.0)
        self.assertEqual(result["basis"], "per random darkgift roll")

    def test_trinket_and_hero_power_rarity_use_four_choices(self):
        cards = {"cards": {}}
        for card_id in range(20, 28):
            cards["cards"][str(card_id)] = {"id": card_id, "name": f"Trinket {card_id}", "type": "trinket", "tier": None, "tribes": [], "pool": True, "modes": ["solo"]}
        for card_id in range(30, 38):
            cards["cards"][str(card_id)] = {"id": card_id, "name": f"Power {card_id}", "type": "hero_power", "tier": None, "tribes": [], "pool": True, "modes": ["solo"]}
        for card_id in range(40, 48):
            cards["cards"][str(card_id)] = {"id": card_id, "name": f"Hero {card_id}", "type": "hero", "tier": None, "tribes": [], "pool": True, "modes": ["solo"]}

        trinket = calculate_card_rarity(cards, 20)
        hero_power = calculate_card_rarity(cards, 30)

        self.assertEqual(trinket["probability"], 0.5)
        self.assertEqual(trinket["basis"], "catalog baseline per four-choice Trinket offer")
        self.assertTrue(trinket["estimate"])
        self.assertEqual(hero_power["probability"], 0.5)
        self.assertEqual(hero_power["basis"], "per four-choice Hero selection")

    def test_generated_minion_is_not_reported_as_zero_percent_tavern_rarity(self):
        cards = {
            "cards": {
                "50": {"id": 50, "name": "Water Droplet", "type": "minion", "tier": 1, "tribes": ["Elemental"], "pool": True, "categories": ["token"], "modes": ["solo"]},
            }
        }

        with self.assertRaisesRegex(RarityUnavailable, "not a Tavern-pool minion"):
            calculate_card_rarity(cards, 50)

    def test_tribal_minion_is_conditional_on_its_tribe_being_active(self):
        cards = {
            "cards": {
                "40": {"id": 40, "name": "Beast", "type": "minion", "tier": 2, "tribes": ["Beast"], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
                "41": {"id": 41, "name": "Neutral", "type": "minion", "tier": 2, "tribes": [], "pool": True, "categories": ["tavern"], "modes": ["solo"]},
            }
        }

        result = calculate_card_rarity(cards, 40)

        self.assertEqual(result["conditional_tribes"], ["beast"])
        self.assertIn("needed tribe active", result["assumption"])


if __name__ == "__main__":
    unittest.main()
