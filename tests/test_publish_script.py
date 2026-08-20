import json
import tempfile
import unittest
from pathlib import Path

from scripts.calculate_rarity import active_cards_path
from scripts.publish_comp import resolve_patch_layout
from scripts.refresh_cards import active_output_path, reconcile_patch_pool


class PublishScriptTests(unittest.TestCase):
    def test_patch_helpers_reject_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data/site.json").write_text(
                json.dumps(
                    {
                        "latest_patch": "../../../victim",
                        "season": 14,
                        "public_base_url": "https://example.test",
                    }
                ),
                encoding="utf-8",
            )
            for helper in (resolve_patch_layout, active_output_path, active_cards_path):
                with self.subTest(helper=helper.__name__):
                    with self.assertRaisesRegex(ValueError, "Invalid patch"):
                        helper(root)

    def test_card_refresh_uses_latest_patch_catalogue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data/site.json").write_text(
                json.dumps({"latest_patch": "36.2.2"}), encoding="utf-8"
            )
            self.assertEqual(
                active_output_path(root),
                root / "data/patches/36.2.2/cards.json",
            )

    def test_card_refresh_uses_structured_after_state_for_all_returning_cards(self):
        cards = [
            {"id": 10, "name": "Still Current", "pool": True},
            {"id": 20, "name": "Just Removed", "pool": True},
        ]
        returning = [
            {
                "id": 30,
                "name": "Simple Return",
                "newCard": {"name": "Simple Return", "cardType": "minion", "tier": 2},
            },
            {
                "id": 40,
                "name": "Changed Return",
                "newCard": {
                    "name": "Changed Return",
                    "cardType": "minion",
                    "tier": 6,
                    "attack": 5,
                    "health": 6,
                    "text": "New patch text",
                },
            },
        ]
        removed = [{"id": 20, "name": "Just Removed", "newCard": None}]
        payload = (
            json.dumps(
                {"changeType": "returning", "label": "Returning Cards", "cards": returning},
                separators=(",", ":"),
            )
            + json.dumps(
                {"changeType": "removed", "label": "Removed Cards", "cards": removed},
                separators=(",", ":"),
            )
        )
        patch_html = (
            "<p>Visual changes: 1 removed, 2 returning</p>"
            f"<script>self.__next_f.push([1,{json.dumps(payload)}])</script>"
        )
        fetched = {
            30: {"id": 30, "name": "Simple Return", "pool": False, "tier": 1},
            40: {"id": 40, "name": "Changed Return", "pool": False, "tier": 5, "text": "Stale"},
        }

        reconciled = reconcile_patch_pool(cards, patch_html, fetched.__getitem__)
        by_id = {card["id"]: card for card in reconciled}

        self.assertEqual(sorted(by_id), [10, 30, 40])
        self.assertTrue(by_id[30]["pool"])
        self.assertEqual(by_id[30]["tier"], 2)
        self.assertTrue(by_id[40]["pool"])
        self.assertEqual(by_id[40]["tier"], 6)
        self.assertEqual(by_id[40]["text"], "New patch text")

    def test_rarity_uses_latest_patch_catalogue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data/site.json").write_text(
                json.dumps({"latest_patch": "36.2.2"}), encoding="utf-8"
            )
            self.assertEqual(
                active_cards_path(root),
                root / "data/patches/36.2.2/cards.json",
            )

    def test_resolves_all_inputs_and_outputs_under_latest_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "data/site.json").write_text(
                json.dumps(
                    {
                        "latest_patch": "36.2.2",
                        "season": 14,
                        "public_base_url": "https://example.test",
                    }
                ),
                encoding="utf-8",
            )

            layout = resolve_patch_layout(root)

            self.assertEqual(layout["patch"], "36.2.2")
            self.assertEqual(layout["content_dir"], root / "content/patches/36.2.2")
            self.assertEqual(layout["cards_path"], root / "data/patches/36.2.2/cards.json")
            self.assertEqual(layout["registry_path"], root / "data/patches/36.2.2/registry.json")
            self.assertEqual(layout["output_dir"], root / "dist/patches/36.2.2")
            self.assertEqual(layout["public_base_url"], "https://example.test/patches/36.2.2")


if __name__ == "__main__":
    unittest.main()
