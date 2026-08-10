import json
import tempfile
import unittest
from pathlib import Path

from comp_pipeline import (
    RESULT_FIELDS,
    CardCatalog,
    CompError,
    _materialize_power_summary,
    _parse_markdown,
    analyze_board_examples,
    build_index,
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
        "133039": {
            "id": 133039,
            "slug": "hoarding-hyena",
            "name": "Hoarding Hyena",
            "type": "minion",
            "tier": 4,
            "tribes": ["Beast"],
            "pool": True,
            "image": "https://images.example/hoarding-hyena.png",
            "detail": "https://hsreplay.net/battlegrounds/minions/133039/hoarding-hyena",
            "hsreplay": "https://hsreplay.net/battlegrounds/minions/133039/hoarding-hyena",
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
    def test_power_summary_discloses_every_legacy_profile_assumption(self):
        metrics = {
            "probability": 0.1,
            "turns_to_online": 13,
            "p20_power": 100,
            "p50_power": 200,
            "p80_power": 300,
        }
        cases = [
            ([132796, 132808, 132800], "source-verified Headhunter Gryphon"),
            ([60630, 96786, 132955, 132957], "one immediate Chromadrake"),
            ([132981, 120674], "two Elementals"),
            ([132983, 126173], "Spirit Swap"),
            ([132893, 120905, 98588, 130298, 101314], "Drakkari repeats"),
            ([119942, 120905, 130298], "Meditative's spell bonus"),
            ([132762, 132925, 132921], "Only Castaway counts as a Discover"),
            ([133083, 133081, 95265], "Handless Forsaken Reborn"),
            ([133026, 132989, 98948, 126637], "Bream Counter in hand"),
            ([133329, 130298], "Maldraxxus Dagger"),
            ([127446, 90425], "five bounded removal uses"),
            ([127446, 90425], "Timewarped setup odds"),
            ([126671, 132320, 132636], "transfers them to Juggernaut"),
        ]

        for card_ids, phrase in cases:
            with self.subTest(phrase=phrase):
                summary = _materialize_power_summary(
                    metrics, [{"card_id": card_id} for card_id in card_ids]
                )
                self.assertTrue(any(phrase in note for note in summary["notes"]))

    def test_power_summary_explains_plaguerunner_and_warpwing_profiles(self):
        metrics = {
            "probability": 0.1,
            "turns_to_online": 13,
            "p20_power": 100,
            "p50_power": 200,
            "p80_power": 300,
        }
        undead = _materialize_power_summary(
            metrics,
            [
                {"card_id": 126451},
                {"card_id": 120104},
                {"card_id": 120219},
            ],
        )
        dragons = _materialize_power_summary(
            metrics,
            [
                {"card_id": 120301},
                {"card_id": 132953},
                {"card_id": 108463},
                {"card_id": 92413},
            ],
        )

        self.assertTrue(any("Butchering" in note for note in undead["notes"]))
        self.assertTrue(any("conditional" in note for note in undead["notes"]))
        self.assertTrue(any("trinket odds" in note for note in undead["notes"]))
        self.assertTrue(any("adjacent Dragons" in note for note in dragons["notes"]))
        self.assertTrue(any("doubles" in note for note in dragons["notes"]))
        self.assertTrue(any("does not assign" in note for note in dragons["notes"]))

    def test_board_analysis_calculates_observed_stats_and_growth(self):
        boards = [
            {
                "stage": "mid",
                "turn": 10,
                "units": [
                    {"attack": 100, "health": 120, "golden": False, "annotation": "Divine Shield"},
                    {"attack": "1.5k", "health": "2k", "golden": True, "annotation": ""},
                ],
            },
            {
                "stage": "end",
                "turn": 12,
                "units": [
                    {"attack": "4k", "health": "4k", "golden": True, "annotation": "Divine Shield"},
                    {"attack": 500, "health": 600, "golden": False, "annotation": "Reborn"},
                ],
            },
        ]

        result = analyze_board_examples(boards)

        self.assertEqual(result[0]["total_attack"], 1600)
        self.assertEqual(result[0]["total_health"], 2120)
        self.assertEqual(result[0]["total_stats"], 3720)
        self.assertEqual(result[0]["bodies_1000_plus"], 1)
        self.assertEqual(result[0]["divine_shields"], 1)
        self.assertEqual(result[1]["reborns"], 1)
        self.assertEqual(result[1]["turns_since_previous"], 2)
        self.assertAlmostEqual(result[1]["stats_multiplier_per_turn"], (9100 / 3720) ** 0.5, places=4)

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

    def test_index_fetches_registry_first_and_lazy_loads_card_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "slug": "tasty-lobstah",
                                "title": "Tasty Lobstah",
                                "url": "https://example.pages.dev/comps/tasty-lobstah.html",
                                "tribes": ["beast"],
                                "tags": ["deathrattle", "scaling"],
                                "minions": [
                                    {"card_id": 132796, "count": 1, "golden_count": 0}
                                ],
                                "spells": [],
                                "probability": 0.22,
                                "turns_to_online": 11,
                                "p20_power": 8200,
                                "p50_power": 16400,
                                "p80_power": 25700,
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

            self.assertIn('<details id="filters-panel" class="filters">', html)
            self.assertNotIn('<details id="filters-panel" class="filters" open', html)
            self.assertIn('id="tribe-filter"', html)
            self.assertIn('id="tag-filter"', html)
            self.assertIn('id="card-filter"', html)
            self.assertIn('data-sort="title"', html)
            self.assertIn('data-sort="probability"', html)
            self.assertIn('data-sort="power"', html)
            self.assertIn('data-sort="online"', html)
            self.assertIn("data/registry.json", html)
            self.assertIn("data/cards.json", html)
            self.assertNotIn("Promise.all", html)
            self.assertIn("addEventListener('toggle'", html)
            self.assertIn('<option value="date:desc" selected>Newest first</option>', html)
            self.assertNotIn("Tasty Lobstah", html)
            self.assertIn("Probability", html)
            self.assertIn("P80 power score", html)
            self.assertIn("Turns online", html)
            self.assertIn("not combat simulation or win probability", html)
            self.assertNotIn("Rating", html)
            self.assertNotIn("Difficulty", html)

    def test_build_index_publishes_json_files_without_embedding_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "slug": "tasty-lobstah",
                                "title": "Tasty Lobstah",
                                "url": "https://example.pages.dev/comps/tasty-lobstah.html",
                                "tribes": ["beast"],
                                "tags": ["deathrattle", "scaling"],
                                "minions": [
                                    {"card_id": 132796, "count": 1, "golden_count": 0}
                                ],
                                "spells": [],
                                "probability": 0.22,
                                "turns_to_online": 11,
                                "p20_power": 8200,
                                "p50_power": 16400,
                                "p80_power": 25700,
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

    def test_catalog_rejects_explicitly_banned_cards(self):
        catalog = CardCatalog(CARDS)
        with self.assertRaisesRegex(CompError, "Hoarding Hyena.*banned"):
            catalog.require_current(133039)

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
                    "attack": 4,
                    "health": 5,
                    "attackGold": 8,
                    "healthGold": 10,
                    "text": "<b>Battlecry:</b> Test.",
                    "textGold": "<b>Battlecry:</b> Test twice.",
                    "keywords": ["Reborn"],
                    "minionTypes": ["Beast"],
                    "pool": True,
                    "categories": ["tavern"],
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
        self.assertEqual(card["categories"], ["tavern"])
        self.assertEqual(card["attack"], 4)
        self.assertEqual(card["health"], 5)
        self.assertEqual(card["attack_gold"], 8)
        self.assertEqual(card["health_gold"], 10)
        self.assertEqual(card["text"], "<b>Battlecry:</b> Test.")
        self.assertEqual(card["text_gold"], "<b>Battlecry:</b> Test twice.")
        self.assertEqual(card["keywords"], ["reborn"])

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
            self.assertEqual(
                saved["pages"][0]["minions"],
                [
                    {"card_id": 132796, "count": 1, "golden_count": 0},
                    {"card_id": 97408, "count": 1, "golden_count": 0},
                ],
            )
            self.assertEqual(saved["pages"][0]["spells"], [])
            self.assertEqual(saved["pages"][0]["title"], "Tasty Lobstah")
            self.assertEqual(saved["pages"][0]["season"], 14)
            self.assertEqual(saved["pages"][0]["modes"], ["solo", "duos"])
            self.assertEqual(saved["pages"][0]["tribes"], ["beast"])
            self.assertEqual(saved["pages"][0]["tags"], ["deathrattle", "scaling"])
            self.assertNotIn("core", saved["pages"][0])
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

    def test_discovery_sources_render_and_register_alongside_original_video(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            discovery_yaml = """discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/90/quilboar-bristlemane
    comp_id: '90'
  - type: firestone
    url: https://www.firestoneapp.com/battlegrounds/comps
    comp_id: quilboar_choose_one
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", discovery_yaml + "source:\n"),
                encoding="utf-8",
            )
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
                public_base_url="https://example.pages.dev",
            )

            html = (root / "dist/comps/tasty-lobstah.html").read_text(encoding="utf-8")
            self.assertIn("https://www.youtube.com/watch?v=jCupcgaSjvo", html)
            self.assertIn("https://hsreplay.net/battlegrounds/comps/90/quilboar-bristlemane", html)
            self.assertIn("https://www.firestoneapp.com/battlegrounds/comps", html)
            self.assertIn("HSReplay composition guide", html)
            self.assertIn("Firestone composition directory", html)
            saved = json.loads(registry.read_text(encoding="utf-8"))["pages"][0]
            self.assertEqual(
                saved["discovery_sources"],
                [
                    {
                        "type": "hsreplay",
                        "url": "https://hsreplay.net/battlegrounds/comps/90/quilboar-bristlemane",
                        "comp_id": "90",
                        "label": "HSReplay composition guide",
                    },
                    {
                        "type": "firestone",
                        "url": "https://www.firestoneapp.com/battlegrounds/comps",
                        "comp_id": "quilboar_choose_one",
                        "label": "Firestone composition directory",
                    },
                ],
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

    def test_board_example_allows_useful_late_snapshot_without_known_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            board_yaml = """board_examples:
  - stage: late
    timestamp: 600
    note: A useful late-game Tavern board from a source whose overlay hides the turn number.
    units:
      - card_id: 132796
        attack: 900
        health: 901
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
            self.assertIn("Late game", html)
            self.assertNotIn("Late game · Turn", html)
            self.assertIn("watch?v=jCupcgaSjvo&t=600s", html)

    def test_compact_registry_metrics_render_without_guide_evaluation_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            composition_yaml = """composition_minions:
  - card_id: 132796
    count: 1
    golden_count: 0
composition_spells: []
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", composition_yaml + "source:\n"),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "source_id": "jCupcgaSjvo",
                                "tribes": ["beast"],
                                "minions": [
                                    {"card_id": 132796, "count": 1, "golden_count": 0}
                                ],
                                "spells": [],
                                "probability": 0.22,
                                "turns_to_online": 11,
                                "p20_power": 8200,
                                "p50_power": 16400,
                                "p80_power": 25700,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

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
            self.assertIn('class="power-badges"', html)
            self.assertIn("Common · 22%", html)
            self.assertIn("25.7k", html)
            self.assertIn("Turn 11", html)
            self.assertIn("P20", html)
            self.assertIn("power-v6", html)
            self.assertIn("8.2k", html)
            self.assertIn("P50", html)
            self.assertIn("16.4k", html)
            self.assertIn("among successful assemblies", html)
            self.assertIn("random tribe availability", html)
            self.assertIn("chance that one pool copy is held by a rival", html)
            self.assertNotIn("quant-evaluation", html)
            self.assertNotIn("Observed board trajectory", html)

    def test_composition_recipe_rejects_more_than_seven_board_bodies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            recipe = """composition_minions:
  - card_id: 132796
    count: 8
    golden_count: 0
composition_spells: []
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", recipe + "source:\n"),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 2, "pages": []}', encoding="utf-8")
            with self.assertRaisesRegex(CompError, "seven-slot"):
                publish_comp(
                    content_path=content,
                    cards_path=cards,
                    registry_path=registry,
                    template_path=Path("templates/comp.html"),
                    output_dir=root / "dist",
                    public_base_url="https://example.test",
                    register=False,
                )
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
            composition_yaml = """composition_minions:
  - card_id: 132796
    count: 1
    golden_count: 0
composition_spells: []
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", composition_yaml + "source:\n"),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "source_id": "jCupcgaSjvo",
                                "url": "https://old.example",
                                "published_at": "2026-08-01T00:00:00+00:00",
                                "tribes": ["demon"],
                                "minions": [
                                    {"card_id": 132796, "count": 1, "golden_count": 0}
                                ],
                                "spells": [],
                                "probability": 0.22,
                                "turns_to_online": 11,
                                "p20_power": 8200,
                                "p50_power": 16400,
                                "p80_power": 25700,
                            }
                        ],
                    }
                ),
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
            entry = saved["pages"][0]
            self.assertEqual(entry["url"], "https://example.pages.dev/comps/tasty-lobstah.html")
            self.assertEqual(
                entry["minions"],
                [{"card_id": 132796, "count": 1, "golden_count": 0}],
            )
            self.assertEqual(entry["spells"], [])
            self.assertEqual(entry["published_at"], "2026-08-01T00:00:00+00:00")
            for result_field in RESULT_FIELDS:
                self.assertNotIn(result_field, entry)
            for obsolete in ("evaluation", "core", "addons", "cycle", "cards"):
                self.assertNotIn(obsolete, entry)


if __name__ == "__main__":
    unittest.main()
