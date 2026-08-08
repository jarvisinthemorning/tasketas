import unittest
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
BANNED_CARD_ID = 133039
SEASON_RELEASE = date(2026, 8, 4)
EXPECTED_TRIBES = {
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
}


def load_guide(path: Path):
    text = path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


class Season14BatchTests(unittest.TestCase):
    def setUp(self):
        self.guides = [load_guide(path) for path in sorted(CONTENT.glob("*.md"))]

    def test_batch_has_one_distinct_guide_per_active_tribe(self):
        self.assertGreaterEqual(len(self.guides), 10)
        tribes = {tribe for meta, _ in self.guides for tribe in meta["tribes"]}
        self.assertEqual(EXPECTED_TRIBES, tribes)
        slugs = [meta["slug"] for meta, _ in self.guides]
        sources = [meta["source"]["url"] for meta, _ in self.guides]
        signatures = [tuple(meta["core"]) for meta, _ in self.guides]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(sources), len(set(sources)))
        self.assertEqual(len(signatures), len(set(signatures)))

    def test_every_source_is_public_and_post_launch(self):
        for meta, _ in self.guides:
            self.assertIn(meta["source"]["type"], {"youtube", "reddit"})
            self.assertTrue(meta["source"]["url"].startswith("https://"))
            source_date = date.fromisoformat(meta["source_published_at"])
            self.assertGreaterEqual(source_date, SEASON_RELEASE)

    def test_hyena_is_absent_from_all_guides_and_registry_fields(self):
        for meta, body in self.guides:
            all_cards = set(meta.get("core", [])) | set(meta.get("addons", [])) | set(meta.get("cycle", []))
            self.assertNotIn(BANNED_CARD_ID, all_cards)
            self.assertNotIn("Hoarding Hyena", body)
            self.assertNotIn("[[card:133039", body)


if __name__ == "__main__":
    unittest.main()
