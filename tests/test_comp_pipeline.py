import json
import tempfile
import unittest
from pathlib import Path

from comp_pipeline import (
    CardCatalog,
    CompError,
    canonical_source,
    normalize_api_cards,
    publish_comp,
)


CARDS = {
    "schema_version": 1,
    "source": "test",
    "cards": {
        "132796": {
            "id": 132796,
            "slug": "tasty-lobster",
            "name": "Tasty Lobster",
            "type": "minion",
            "tier": 3,
            "tribes": ["Beast"],
            "pool": True,
            "image": "https://images.example/BG36_202.png",
            "hsreplay": "https://hsreplay.net/battlegrounds/minions/132796/tasty-lobster",
        },
        "62230": {
            "id": 62230,
            "slug": "monstrous-macaw",
            "name": "Monstrous Macaw",
            "type": "minion",
            "tier": 4,
            "tribes": ["Beast"],
            "pool": False,
            "image": "https://images.example/BG21_014.png",
            "hsreplay": "https://hsreplay.net/battlegrounds/minions/62230/monstrous-macaw",
        },
    },
}


VALID_MARKDOWN = """---
title: Tasty Lobstah
slug: tasty-lobstah
season: 14
modes: [solo, duos]
tribes: [beast]
core: [132796]
addons: []
cycle: []
source:
  type: youtube
  url: https://youtu.be/jCupcgaSjvo?is=tracking
  author: Shadybunny
video:
  id: jCupcgaSjvo
  timestamp: 42
verified_at: 2026-08-08
---

## Description

Trigger the lobster repeatedly.

## When to commit

Find the lobster early.
"""


class PipelineTests(unittest.TestCase):
    def test_canonical_source_normalizes_youtube_and_reddit(self):
        self.assertEqual(
            canonical_source("https://youtu.be/jCupcgaSjvo?is=tracking"),
            ("youtube", "jCupcgaSjvo", "https://www.youtube.com/watch?v=jCupcgaSjvo"),
        )
        self.assertEqual(
            canonical_source("https://www.reddit.com/r/BobsTavern/comments/abc123/title/?utm_source=x"),
            ("reddit", "abc123", "https://www.reddit.com/comments/abc123"),
        )

    def test_catalog_rejects_rotated_cards(self):
        catalog = CardCatalog(CARDS)
        self.assertEqual(catalog.require_current(132796)["name"], "Tasty Lobster")
        with self.assertRaisesRegex(CompError, "not in the current pool"):
            catalog.require_current(62230)

    def test_normalize_api_cards_builds_public_image_and_detail_links(self):
        payload = normalize_api_cards(
            [
                {
                    "id": 132796,
                    "externalId": "BG36_202",
                    "slug": "tasty-lobster",
                    "name": "Tasty Lobster",
                    "cardType": "minion",
                    "tier": 3,
                    "minionTypes": ["Beast"],
                    "pool": True,
                    "image": "/cards/production/pngs/full/minions/beast/132796-tasty-lobster.png",
                    "isDuosOnly": False,
                    "isSolosOnly": False,
                }
            ],
            generated_at="2026-08-08T10:00:00+00:00",
        )
        card = payload["cards"]["132796"]
        self.assertEqual(card["image"], "https://hsbg.cards/cards/production/pngs/full/minions/beast/132796-tasty-lobster.png")
        self.assertEqual(card["detail"], "https://hsreplay.net/battlegrounds/minions/132796/tasty-lobster")
        self.assertEqual(card["modes"], ["solo", "duos"])

    def test_normalize_api_cards_does_not_assign_tribes_to_trinkets(self):
        payload = normalize_api_cards(
            [
                {
                    "id": 133400,
                    "externalId": "BG_TRINKET_133400",
                    "slug": "wolfhead-flail",
                    "name": "Wolfhead Flail",
                    "cardType": "trinket",
                    "tier": None,
                    "minionTypes": ["Beast"],
                    "pool": True,
                    "image": "/cards/wolfhead-flail.png",
                }
            ],
            generated_at="2026-08-08T10:00:00+00:00",
        )
        card = payload["cards"]["133400"]
        self.assertEqual(card["tribes"], [])
        self.assertEqual(card["detail"], "https://hsbg.cards/card/wolfhead-flail")

    def test_publish_renders_mobile_page_and_updates_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")
            template = root / "comp.html"
            template.write_text(
                "<meta name=viewport content='width=device-width, initial-scale=1'>  \n"
                "<h1>{{ comp.title }}</h1>"
                "{% for card in comp.sections.core %}"
                "<a href='{{ card.hsreplay }}'><img src='{{ card.image }}' alt='{{ card.name }}'></a>"
                "{% endfor %}"
                "<article>{{ body_html|safe }}</article>",
                encoding="utf-8",
            )
            output = root / "dist"

            result = publish_comp(
                content_path=content,
                cards_path=cards,
                registry_path=registry,
                template_path=template,
                output_dir=output,
                public_base_url="https://example.pages.dev",
            )

            html = (output / "comps" / "tasty-lobstah.html").read_text(encoding="utf-8")
            self.assertIn("width=device-width", html)
            self.assertIn("Tasty Lobster", html)
            self.assertIn("hsreplay.net/battlegrounds/minions/132796", html)
            self.assertIn("Trigger the lobster repeatedly.", html)
            self.assertFalse(any(line.endswith((" ", "\t")) for line in html.splitlines()))
            self.assertEqual(result["url"], "https://example.pages.dev/comps/tasty-lobstah.html")
            saved = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(saved["pages"][0]["source_id"], "jCupcgaSjvo")
            self.assertEqual(saved["pages"][0]["cards"], [132796])

    def test_preview_build_does_not_update_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")
            template = root / "comp.html"
            template.write_text("{{ comp.title }}", encoding="utf-8")

            publish_comp(
                content_path=content,
                cards_path=cards,
                registry_path=registry,
                template_path=template,
                output_dir=root / "dist",
                public_base_url="http://127.0.0.1:8000",
                register=False,
            )

            saved = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(saved["pages"], [])
            self.assertTrue((root / "dist/comps/tasty-lobstah.html").exists())

    def test_publish_refuses_duplicate_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps({"schema_version": 1, "pages": [{"source_id": "jCupcgaSjvo"}]}),
                encoding="utf-8",
            )
            template = root / "comp.html"
            template.write_text("{{ comp.title }}", encoding="utf-8")

            with self.assertRaisesRegex(CompError, "already published"):
                publish_comp(
                    content_path=content,
                    cards_path=cards,
                    registry_path=registry,
                    template_path=template,
                    output_dir=root / "dist",
                    public_base_url="https://example.pages.dev",
                )


if __name__ == "__main__":
    unittest.main()
