import json
import tempfile
import unittest
from pathlib import Path

from comp_pipeline import (
    CardCatalog,
    CompError,
    build_index,
    _parse_markdown,
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
            "detail": "https://hsreplay.net/battlegrounds/minions/132796/tasty-lobster",
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
        "97408": {
            "id": 97408,
            "slug": "titus-rivendare",
            "name": "Titus Rivendare",
            "type": "minion",
            "tier": 5,
            "tribes": [],
            "pool": True,
            "image": "https://images.example/BG25_354.png",
            "detail": "https://hsreplay.net/battlegrounds/minions/97408/titus-rivendare",
            "hsreplay": "https://hsreplay.net/battlegrounds/minions/97408/titus-rivendare",
        },
    },
}


VALID_MARKDOWN = """---
title: Tasty Lobstah
slug: tasty-lobstah
season: 14
modes: [solo, duos]
tribes: [beast]
tags: [deathrattle, scaling]
core: [132796]
addons: []
cycle: []
flex: [97408]
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

Trigger the [[card:132796|Tasty Lobster]] repeatedly.

## When to commit

Find the lobster early.
"""


class PipelineTests(unittest.TestCase):
    def test_guide_requires_nonempty_tribes(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp) / "guide.md"
            content.write_text(VALID_MARKDOWN.replace("tribes: [beast]", "tribes: []"), encoding="utf-8")
            with self.assertRaisesRegex(CompError, "tribes must be a non-empty list"):
                _parse_markdown(content)

    def test_guide_requires_nonempty_tags(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = Path(tmp) / "guide.md"
            content.write_text(VALID_MARKDOWN.replace("tags: [deathrattle, scaling]", "tags: []"), encoding="utf-8")
            with self.assertRaisesRegex(CompError, "tags must be a non-empty list"):
                _parse_markdown(content)

    def test_index_template_fetches_both_json_files_on_page_load_without_embedded_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "pages": [
                            {
                                "slug": "tasty-lobstah",
                                "title": "Tasty Lobstah",
                                "url": "https://example.pages.dev/comps/tasty-lobstah.html",
                                "tribes": ["beast"],
                                "tags": ["deathrattle", "scaling"],
                                "core": [132796],
                                "cards": [132796, 97408],
                                "verified_at": "2026-08-08",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")

            output = build_index(
                registry_path=registry,
                cards_path=cards,
                template_path=Path(__file__).parents[1] / "templates" / "index.html",
                output_dir=root / "dist",
            )
            html = output.read_text(encoding="utf-8")

            self.assertIn('<details class="filters">', html)
            self.assertNotIn('<details class="filters" open', html)
            self.assertIn('id="tribe-filter"', html)
            self.assertIn('id="tag-filter"', html)
            self.assertIn('id="card-filter"', html)
            self.assertIn('data-sort="title"', html)
            self.assertIn("data/registry.json", html)
            self.assertIn("data/cards.json", html)
            self.assertIn("Promise.all", html)
            self.assertNotIn("details.addEventListener", html)
            self.assertIn('<option value="date:desc" selected>Newest first</option>', html)
            self.assertNotIn("Tasty Lobstah", html)
            self.assertNotIn("Power", html)
            self.assertNotIn("Rating", html)
            self.assertNotIn("Difficulty", html)

    def test_build_index_publishes_json_files_without_embedding_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "pages": [
                            {
                                "slug": "tasty-lobstah",
                                "title": "Tasty Lobstah",
                                "url": "https://example.pages.dev/comps/tasty-lobstah.html",
                                "tribes": ["beast"],
                                "tags": ["deathrattle", "scaling"],
                                "core": [132796],
                                "cards": [132796, 97408],
                                "verified_at": "2026-08-08",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            template = root / "index.html"
            template.write_text("<p>Static shell</p>", encoding="utf-8")

            output = build_index(
                registry_path=registry,
                cards_path=cards,
                template_path=template,
                output_dir=root / "dist",
            )

            html = output.read_text(encoding="utf-8")
            self.assertEqual(html, "<p>Static shell</p>\n")
            self.assertNotIn("Tasty Lobstah", html)
            self.assertEqual(
                json.loads((root / "dist/data/registry.json").read_text(encoding="utf-8")),
                json.loads(registry.read_text(encoding="utf-8")),
            )
            self.assertEqual(
                json.loads((root / "dist/data/cards.json").read_text(encoding="utf-8")),
                CARDS,
            )

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
            self.assertIn('class="card-ref"', html)
            self.assertIn('class="card-ref-trigger"', html)
            self.assertIn('class="card-popover"', html)
            self.assertIn("https://images.example/BG36_202.png", html)
            self.assertFalse(any(line.endswith((" ", "\t")) for line in html.splitlines()))
            self.assertEqual(result["url"], "https://example.pages.dev/comps/tasty-lobstah.html")
            saved = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(saved["pages"][0]["source_id"], "jCupcgaSjvo")
            self.assertEqual(saved["pages"][0]["cards"], [132796, 97408])
            self.assertEqual(saved["pages"][0]["title"], "Tasty Lobstah")
            self.assertEqual(saved["pages"][0]["season"], 14)
            self.assertEqual(saved["pages"][0]["modes"], ["solo", "duos"])
            self.assertEqual(saved["pages"][0]["tribes"], ["beast"])
            self.assertEqual(saved["pages"][0]["tags"], ["deathrattle", "scaling"])
            self.assertEqual(saved["pages"][0]["core"], [132796])
            self.assertEqual(saved["pages"][0]["source_author"], "Shadybunny")

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

    def test_source_section_is_rendered_after_the_guide(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")

            publish_comp(
                content_path=content,
                cards_path=cards,
                registry_path=registry,
                template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                output_dir=root / "dist",
                public_base_url="http://127.0.0.1:8000",
                register=False,
            )

            html = (root / "dist/comps/tasty-lobstah.html").read_text(encoding="utf-8")
            self.assertLess(
                html.index('<article class="guide-copy">'),
                html.index('<section class="source-card"'),
            )

    def test_video_board_examples_render_ordered_cards_and_stats_before_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            board_yaml = """board_examples:
  - stage: early
    turn: 6
    timestamp: 180
    note: Lobster starts scaling beside protected support.
    units:
      - card_id: 132796
        slot: 2
        attack: 8
        health: 12
        golden: false
        annotation: Reborn
      - card_id: 97408
        slot: 5
        attack: 3
        health: 6
        golden: true
      - card_id: 132796
        slot: 7
        attack: 1.2k
        health: 1.3k
  - stage: mid
    turn: 9
    timestamp: 300
    units:
      - card_id: 132796
        attack: 100
        health: 101
  - stage: end
    turn: 12
    timestamp: 600
    units:
      - card_id: 97408
        attack: 2
        health: 14
        golden: true
"""
            content.write_text(VALID_MARKDOWN.replace("source:\n", board_yaml + "source:\n"), encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")

            publish_comp(
                content_path=content,
                cards_path=cards,
                registry_path=registry,
                template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                output_dir=root / "dist",
                public_base_url="http://127.0.0.1:8000",
                register=False,
            )

            html = (root / "dist/comps/tasty-lobstah.html").read_text(encoding="utf-8")
            board_html = html[html.index('<section class="board-examples"'):html.index('<section class="source-card"')]
            self.assertIn('<section class="board-examples"', html)
            self.assertNotIn('loading="lazy"', board_html)
            self.assertIn('class="board-unit"', html)
            self.assertIn('class="board-stats">8 / 12', html)
            self.assertIn('<small>Reborn</small>', html)
            self.assertIn('class="board-stats">1.2k / 1.3k', html)
            self.assertIn('class="board-badge">Golden', html)
            self.assertNotIn('style="grid-column:', html)
            self.assertIn('class="board-position">2', html)
            self.assertIn('class="board-position">5', html)
            self.assertIn("watch?v=jCupcgaSjvo&t=180s", html)
            self.assertIn("Last Tavern turn before winning · Turn 12", html)
            self.assertLess(html.index("Tasty Lobster"), html.index("Titus Rivendare"))
            self.assertLess(html.index('<section class="board-examples"'), html.index('<section class="source-card"'))

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

    def test_update_replaces_an_existing_source_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps({"schema_version": 1, "pages": [{"source_id": "jCupcgaSjvo", "url": "https://old.example"}]}),
                encoding="utf-8",
            )
            template = root / "comp.html"
            template.write_text("{{ body_html|safe }}", encoding="utf-8")

            publish_comp(
                content_path=content,
                cards_path=cards,
                registry_path=registry,
                template_path=template,
                output_dir=root / "dist",
                public_base_url="https://example.pages.dev",
                update=True,
            )

            saved = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(len(saved["pages"]), 1)
            self.assertEqual(saved["pages"][0]["url"], "https://example.pages.dev/comps/tasty-lobstah.html")


if __name__ == "__main__":
    unittest.main()
