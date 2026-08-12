import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("build_early_game", ROOT / "scripts/build_early_game.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load early-game builder")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class EarlyGameGuideTests(unittest.TestCase):
    def test_live_catalogue_packages_validate_and_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "early-game.html"
            MODULE.build(ROOT / "data/cards.json", ROOT / "templates/early-game.html", output)
            page = output.read_text(encoding="utf-8")
            self.assertIn("Survive to Core", page)
            self.assertIn("Dark Gifts change the curve", page)
            self.assertIn("Emergency stabilization", page)
            self.assertIn("132806-wolf-pup.png", page)
            self.assertNotIn("{{PACKAGES}}", page)

    def test_rejects_rotated_displayed_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = json.loads((ROOT / "data/cards.json").read_text(encoding="utf-8"))
            source["cards"]["110101"]["pool"] = False
            cards = Path(tmp) / "cards.json"
            cards.write_text(json.dumps(source), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "current Tavern minion"):
                MODULE.build(cards, ROOT / "templates/early-game.html", Path(tmp) / "out.html")

    def test_homepage_links_guide(self):
        template = (ROOT / "templates/index.html").read_text(encoding="utf-8")
        self.assertIn('href="early-game.html"', template)
        self.assertIn("Survive to Core", template)


if __name__ == "__main__":
    unittest.main()
