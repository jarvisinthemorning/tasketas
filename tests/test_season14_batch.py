import unittest
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
BANNED_CARD_ID = 133039
# Official Season 14 early-access footage started before the public launch.
# It is valid current-season evidence when the guide uses the released card pool.
SEASON_14_EARLY_ACCESS = date(2026, 8, 1)
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
ALLOWED_TRIBES = EXPECTED_TRIBES | {"menagerie"}


def load_guide(path: Path):
    text = path.read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


class Season14BatchTests(unittest.TestCase):
    def setUp(self):
        self.guides = [load_guide(path) for path in sorted(CONTENT.glob("*.md"))]

    def test_guides_are_uniquely_sourced_and_categorized(self):
        for meta, _ in self.guides:
            self.assertTrue(meta["tribes"])
            self.assertTrue(set(meta["tribes"]).issubset(ALLOWED_TRIBES))
        slugs = [meta["slug"] for meta, _ in self.guides]
        sources = [meta["source"]["url"] for meta, _ in self.guides]
        signatures = [tuple(meta["core"]) for meta, _ in self.guides]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(sources), len(set(sources)))
        self.assertEqual(len(signatures), len(set(signatures)))

    def test_every_source_is_public_and_from_season_14_access(self):
        for meta, _ in self.guides:
            self.assertIn(meta["source"]["type"], {"youtube", "reddit"})
            self.assertTrue(meta["source"]["url"].startswith("https://"))
            source_date = date.fromisoformat(str(meta["source_published_at"])[:10])
            self.assertGreaterEqual(source_date, SEASON_14_EARLY_ACCESS)

    def test_hyena_is_absent_from_all_guides_and_registry_fields(self):
        for meta, body in self.guides:
            all_cards = set(meta.get("core", [])) | set(meta.get("addons", [])) | set(meta.get("cycle", []))
            self.assertNotIn(BANNED_CARD_ID, all_cards)
            self.assertNotIn("Hoarding Hyena", body)
            self.assertNotIn("[[card:133039", body)


if __name__ == "__main__":
    unittest.main()
