import json
import tempfile
import unittest
from pathlib import Path

from scripts.start_patch import rollover_patch


class PatchRolloverTests(unittest.TestCase):
    def make_root(self, base: Path) -> Path:
        root = base / "repo"
        for directory in (
            "content",
            "data",
            "dist/comps",
            "dist/data",
            "dist/static",
            "dist/legacy",
            "static",
            "templates",
            "scripts",
            "tests",
        ):
            (root / directory).mkdir(parents=True, exist_ok=True)
        (root / "content/example.md").write_text("---\npatch: '36.2.0'\n---\n", encoding="utf-8")
        cards = {"schema_version": 1, "generated_at": "before", "cards": {}}
        registry = {
            "schema_version": 3,
            "pages": [
                {
                    "slug": "example",
                    "title": "Example",
                    "url": "https://example.test/comps/example.html",
                    "season": 14,
                    "patch": "36.2.0",
                }
            ],
        }
        (root / "data/cards.json").write_text(json.dumps(cards), encoding="utf-8")
        (root / "data/registry.json").write_text(json.dumps(registry), encoding="utf-8")
        (root / "dist/comps/example.html").write_text(
            '<p>Battlegrounds comp · Season 14</p>'
            '<img src="https://example.test/static/boards/example.webp">',
            encoding="utf-8",
        )
        (root / "dist/index.html").write_text("old root", encoding="utf-8")
        (root / "dist/data/cards.json").write_text(json.dumps(cards), encoding="utf-8")
        (root / "dist/data/registry.json").write_text(json.dumps(registry), encoding="utf-8")
        (root / "static/index.css").write_text("body{}", encoding="utf-8")
        (root / "dist/static/index.css").write_text("body{}", encoding="utf-8")
        (root / "dist/legacy/keep.html").write_text("legacy", encoding="utf-8")
        (root / "templates/index.html").write_text(
            "<h1>Patch {{ patch }}</h1>{% if rebuilding %}<p>Rebuilding for patch {{ patch }}</p>{% endif %}",
            encoding="utf-8",
        )
        for relative in (
            "dist/early-game.html",
            "templates/early-game.html",
            "scripts/build_early_game.py",
            "tests/test_early_game.py",
            "static/early-game.css",
            "dist/static/early-game.css",
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("early", encoding="utf-8")
        return root

    def test_dry_run_does_not_modify_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            before = sorted(str(path.relative_to(root)) for path in root.rglob("*"))

            report = rollover_patch(
                root=root,
                from_patch="36.2.0",
                to_patch="36.2.2",
                released_at="2026-08-18",
                source_url="https://hearthstone.blizzard.com/en-us/news/24293284/3622-patch-notes",
                public_base_url="https://example.test",
                dry_run=True,
            )

            after = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            self.assertEqual(after, before)
            self.assertEqual(report["from_patch"], "36.2.0")
            self.assertEqual(report["to_patch"], "36.2.2")

    def test_rollover_creates_permanent_patch_directories_and_latest_redirect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))

            rollover_patch(
                root=root,
                from_patch="36.2.0",
                to_patch="36.2.2",
                released_at="2026-08-18",
                source_url="https://hearthstone.blizzard.com/en-us/news/24293284/3622-patch-notes",
                public_base_url="https://example.test",
            )

            self.assertTrue((root / "content/patches/36.2.0/example.md").is_file())
            self.assertTrue((root / "content/patches/36.2.2/.gitkeep").is_file())
            archived = json.loads((root / "data/patches/36.2.0/registry.json").read_text())
            self.assertEqual(archived["patch"], "36.2.0")
            self.assertEqual(
                archived["pages"][0]["url"],
                "https://example.test/patches/36.2.0/comps/example.html",
            )
            latest = json.loads((root / "data/patches/36.2.2/registry.json").read_text())
            self.assertEqual(latest, {"schema_version": 4, "patch": "36.2.2", "pages": []})
            self.assertFalse((root / "data/registry.json").exists())
            self.assertFalse((root / "data/cards.json").exists())
            self.assertFalse((root / "dist/comps").exists())
            root_index = (root / "dist/index.html").read_text()
            self.assertIn("patches/36.2.2/", root_index)
            self.assertIn("http-equiv=\"refresh\"", root_index)
            self.assertIn("Rebuilding for patch 36.2.2", (root / "dist/patches/36.2.2/index.html").read_text())
            self.assertEqual((root / "dist/legacy/keep.html").read_text(), "legacy")
            archived_page = (root / "dist/patches/36.2.0/comps/example.html").read_text()
            self.assertIn("/patches/36.2.0/static/boards/example.webp", archived_page)
            self.assertIn("Season 14 · Patch 36.2.0", archived_page)

    def test_future_rollover_keeps_existing_patch_urls_and_creates_a_new_latest_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            common = {
                "root": root,
                "released_at": "2026-08-18",
                "source_url": "https://hearthstone.blizzard.com/patch-notes",
                "public_base_url": "https://example.test",
            }
            rollover_patch(from_patch="36.2.0", to_patch="36.2.2", **common)
            (root / "content/patches/36.2.2/new-guide.md").write_text(
                "---\nseason: 14\npatch: '36.2.2'\n---\n", encoding="utf-8"
            )
            registry_path = root / "data/patches/36.2.2/registry.json"
            registry = json.loads(registry_path.read_text())
            registry["pages"] = [
                {
                    "slug": "new-guide",
                    "title": "New Guide",
                    "url": "https://example.test/patches/36.2.2/comps/new-guide.html",
                    "season": 14,
                    "patch": "36.2.2",
                }
            ]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            comps = root / "dist/patches/36.2.2/comps"
            comps.mkdir()
            (comps / "new-guide.html").write_text("guide", encoding="utf-8")

            rollover_patch(
                root=root,
                from_patch="36.2.2",
                to_patch="36.2.3",
                released_at="2026-08-25",
                source_url="https://hearthstone.blizzard.com/next-patch",
                public_base_url="https://example.test",
            )

            self.assertTrue((root / "content/patches/36.2.2/new-guide.md").is_file())
            self.assertTrue((root / "dist/patches/36.2.2/comps/new-guide.html").is_file())
            self.assertTrue((root / "data/patches/36.2.3/registry.json").is_file())
            self.assertIn("patches/36.2.3/", (root / "dist/index.html").read_text())

    def test_future_rollover_rejects_non_latest_source_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            common = {
                "root": root,
                "released_at": "2026-08-18",
                "source_url": "https://hearthstone.blizzard.com/patch-notes",
                "public_base_url": "https://example.test",
            }
            rollover_patch(from_patch="36.2.0", to_patch="36.2.2", **common)
            with self.assertRaisesRegex(ValueError, "active patch"):
                rollover_patch(from_patch="36.2.0", to_patch="36.2.3", **common)

    def test_future_rollover_can_change_season_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            common = {
                "root": root,
                "released_at": "2026-08-18",
                "source_url": "https://hearthstone.blizzard.com/patch-notes",
                "public_base_url": "https://example.test",
            }
            rollover_patch(from_patch="36.2.0", to_patch="36.2.2", **common)
            (root / "content/patches/36.2.2/new-guide.md").write_text(
                "---\nseason: 14\npatch: '36.2.2'\n---\n", encoding="utf-8"
            )
            registry_path = root / "data/patches/36.2.2/registry.json"
            registry = json.loads(registry_path.read_text())
            registry["pages"] = [{"slug": "new-guide", "patch": "36.2.2"}]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            comps = root / "dist/patches/36.2.2/comps"
            comps.mkdir()
            (comps / "new-guide.html").write_text("guide", encoding="utf-8")

            rollover_patch(
                from_patch="36.2.2",
                to_patch="36.2.3",
                to_season=15,
                **common,
            )
            site = json.loads((root / "data/site.json").read_text())
            self.assertEqual(site["season"], 15)
            patches = json.loads((root / "data/patches.json").read_text())["patches"]
            self.assertEqual(next(item for item in patches if item["patch"] == "36.2.3")["season"], 15)

    def test_rollover_rejects_rendered_page_count_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            (root / "dist/comps/example.html").unlink()
            with self.assertRaisesRegex(ValueError, "Rendered page count"):
                rollover_patch(
                    root=root,
                    from_patch="36.2.0",
                    to_patch="36.2.2",
                    released_at="2026-08-18",
                    source_url="https://hearthstone.blizzard.com/patch-notes",
                    public_base_url="https://example.test",
                )

    def test_rollover_rejects_source_patch_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            with self.assertRaisesRegex(ValueError, "Source (guide|registry)"):
                rollover_patch(
                    root=root,
                    from_patch="36.2.1",
                    to_patch="36.2.2",
                    released_at="2026-08-18",
                    source_url="https://hearthstone.blizzard.com/patch-notes",
                    public_base_url="https://example.test",
                )

    def test_rollover_removes_early_game_experiment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(Path(tmp))
            rollover_patch(
                root=root,
                from_patch="36.2.0",
                to_patch="36.2.2",
                released_at="2026-08-18",
                source_url="https://hearthstone.blizzard.com/en-us/news/24293284/3622-patch-notes",
                public_base_url="https://example.test",
            )
            for relative in (
                "dist/early-game.html",
                "templates/early-game.html",
                "scripts/build_early_game.py",
                "tests/test_early_game.py",
                "static/early-game.css",
                "dist/static/early-game.css",
            ):
                self.assertFalse((root / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
