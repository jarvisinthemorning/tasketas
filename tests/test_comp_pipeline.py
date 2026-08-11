import json
import tempfile
import unittest
from pathlib import Path

from comp_pipeline import (
    CardCatalog,
    CompError,
    _parse_markdown,
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
            self.assertNotIn('data-sort="probability"', html)
            self.assertNotIn('data-sort="power"', html)
            self.assertNotIn('data-sort="online"', html)
            self.assertIn("data/registry.json", html)
            self.assertIn("data/cards.json", html)
            self.assertNotIn("Promise.all", html)
            self.assertIn("addEventListener('toggle'", html)
            self.assertIn('<option value="date:desc" selected>Newest first</option>', html)
            self.assertNotIn("Tasty Lobstah", html)
            self.assertNotIn("Probability", html)
            self.assertNotIn("P80 power score", html)
            self.assertNotIn("Turns online", html)
            self.assertNotIn("not combat simulation or win probability", html)
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

    def test_canonical_source_rejects_reddit_lookalike_hosts(self):
        for host in ("notreddit.com", "evilreddit.com"):
            with self.subTest(host=host), self.assertRaisesRegex(CompError, "public YouTube video or Reddit post"):
                canonical_source(f"https://{host}/r/BobsTavern/comments/abc123/title/")

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

    def test_custom_visual_packages_render_with_purpose_and_optional_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            packages = """packages:
  - title: Commit
    purpose: No separate pre-core commitment signal; assemble Core before staying on this route.
    badge: No early commit
    optional: false
    cards: []
  - title: Core
    purpose: Trigger Lobster scaling repeatedly during combat.
    badge: Required core
    optional: false
    cards: [132796]
  - title: Add-ons
    purpose: Improve the engine when offered.
    optional: true
    cards: [97408, 64040]
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", packages + "source:\n"),
                encoding="utf-8",
            )
            cards = root / "cards.json"
            card_fixture = json.loads(json.dumps(CARDS))
            card_fixture["cards"]["64040"] = {
                "id": 64040,
                "name": "Water Droplet",
                "type": "minion",
                "tier": 1,
                "tribes": ["Elemental"],
                "pool": True,
                "categories": ["token"],
                "modes": ["solo"],
                "image": "https://example.com/water-droplet.png",
                "detail": "https://example.com/water-droplet",
            }
            cards.write_text(json.dumps(card_fixture), encoding="utf-8")
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
            self.assertIn("No separate pre-core commitment signal", html)
            self.assertIn("No early commit", html)
            self.assertLess(html.index(">Commit</h2>"), html.index(">Core</h2>"))
            self.assertIn("Trigger Lobster scaling repeatedly during combat.", html)
            self.assertIn("Required core", html)
            self.assertIn("Improve the engine when offered.", html)
            self.assertIn("Optional package", html)
            self.assertIn("Titus Rivendare", html)
            self.assertIn('class="card-rarity"', html)
            self.assertIn('% / refresh', html)
            self.assertIn('class="card-rarity unavailable"', html)
            self.assertIn('Generated', html)
            self.assertNotIn('>0.0% / refresh<', html)
            self.assertIn("needed tribe active", html)
            self.assertIn('<article class="guide-copy">', html)
            self.assertNotIn('<details class="guide-details">', html)

    def test_custom_packages_require_fixed_commit_and_core(self):
        invalid_packages = (
            (
                "packages:\n"
                "  - title: Core\n"
                "    purpose: Required engine.\n"
                "    optional: false\n"
                "    cards: [132796]\n",
                "packages must start with fixed Commit and Core sections",
            ),
            (
                "packages:\n"
                "  - title: Commit\n"
                "    purpose: No separate commitment signal.\n"
                "    optional: false\n"
                "    cards: []\n"
                "  - title: Core\n"
                "    purpose: Required engine.\n"
                "    optional: false\n"
                "    cards: []\n",
                "Core cards must be a non-empty list",
            ),
        )
        for packages, message in invalid_packages:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                content = root / "guide.md"
                content.write_text(
                    VALID_MARKDOWN.replace("source:\n", packages + "source:\n"),
                    encoding="utf-8",
                )
                cards = root / "cards.json"
                cards.write_text(json.dumps(CARDS), encoding="utf-8")
                registry = root / "registry.json"
                registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")
                with self.assertRaisesRegex(CompError, message):
                    publish_comp(
                        content_path=content,
                        cards_path=cards,
                        registry_path=registry,
                        template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                        output_dir=root / "dist",
                        public_base_url="http://127.0.0.1:8000",
                        register=False,
                    )

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

    def test_related_route_renders_distinct_core_cards_and_link_before_guide(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            related = """related_routes:
  - title: Alternative deathrattle route
    slug: beast-alternative
    purpose: Switch when these core cards arrive first.
    cards: [132796, 97408]
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", related + "source:\n"),
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
                public_base_url="http://127.0.0.1:8000",
                register=False,
            )

            html = (root / "dist/comps/tasty-lobstah.html").read_text(encoding="utf-8")
            self.assertIn('class="related-routes"', html)
            self.assertIn("Alternative deathrattle route", html)
            self.assertIn("Switch when these core cards arrive first.", html)
            self.assertIn("Tasty Lobster", html)
            self.assertIn("Titus Rivendare", html)
            self.assertIn('href="beast-alternative.html"', html)
            self.assertLess(html.index('class="related-routes"'), html.index('class="guide-copy"'))

    def test_related_routes_rejects_falsy_non_list_values(self):
        for invalid_yaml in ("{}", "''", "0", "false"):
            with self.subTest(invalid_yaml=invalid_yaml), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                content = root / "guide.md"
                content.write_text(
                    VALID_MARKDOWN.replace("source:\n", f"related_routes: {invalid_yaml}\nsource:\n"),
                    encoding="utf-8",
                )
                cards = root / "cards.json"
                cards.write_text(json.dumps(CARDS), encoding="utf-8")
                registry = root / "registry.json"
                registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")

                with self.assertRaisesRegex(CompError, "related_routes must be a list"):
                    publish_comp(
                        content_path=content,
                        cards_path=cards,
                        registry_path=registry,
                        template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                        output_dir=root / "dist",
                        public_base_url="http://127.0.0.1:8000",
                        register=False,
                    )

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

    def test_supporting_strategy_source_renders_and_registers_with_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            supporting_yaml = """supporting_sources:
  - type: youtube
    url: https://youtu.be/8d42ovfpwBw?si=tracking
    author: BeterBabbit
    label: Plaguerunner Portrait variation
    timestamp: 388
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", supporting_yaml + "source:\n"),
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
            self.assertIn("Supporting strategy sources", html)
            self.assertIn("Plaguerunner Portrait variation — BeterBabbit", html)
            self.assertIn("https://www.youtube.com/watch?v=8d42ovfpwBw&t=388s", html)
            saved = json.loads(registry.read_text(encoding="utf-8"))["pages"][0]
            self.assertEqual(
                saved["supporting_sources"],
                [
                    {
                        "type": "youtube",
                        "url": "https://www.youtube.com/watch?v=8d42ovfpwBw",
                        "source_id": "8d42ovfpwBw",
                        "author": "BeterBabbit",
                        "label": "Plaguerunner Portrait variation",
                        "timestamp": 388,
                    }
                ],
            )

    def test_supporting_source_cannot_reuse_another_guides_primary_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            supporting_yaml = """supporting_sources:
  - type: youtube
    url: https://www.youtube.com/watch?v=8d42ovfpwBw
    author: BeterBabbit
    label: Portrait variation
"""
            content.write_text(
                VALID_MARKDOWN.replace("source:\n", supporting_yaml + "source:\n"),
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
                                "slug": "existing-guide",
                                "source_id": "8d42ovfpwBw",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(CompError, "already published as the primary source"):
                publish_comp(
                    content_path=content,
                    cards_path=cards,
                    registry_path=registry,
                    template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                    output_dir=root / "dist",
                    public_base_url="https://example.pages.dev",
                )

    def test_video_board_examples_render_tavern_crops_before_guide_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            board_yaml = """board_examples:
  - stage: early
    turn: 6
    timestamp: 180
    phase: tavern
    note: Lobster starts scaling beside protected support.
    image: /static/boards/early.webp
  - stage: mid
    turn: 9
    timestamp: 300
    phase: tavern
    image: /static/boards/mid.webp
  - stage: end
    turn: 12
    timestamp: 600
    phase: start_of_turn
    image: /static/boards/end.webp
"""
            content.write_text(VALID_MARKDOWN.replace("source:\n", board_yaml + "source:\n"), encoding="utf-8")
            board_dir = root / "static/boards"
            board_dir.mkdir(parents=True)
            for name in ("early.webp", "mid.webp", "end.webp"):
                (board_dir / name).write_bytes(b"test-image")
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
            board_html = html[html.index('<section class="board-examples"'):html.index('<article class="guide-copy">')]
            self.assertIn('<section class="board-examples"', html)
            self.assertNotIn('loading="lazy"', board_html)
            self.assertIn('class="board-frame-image"', html)
            self.assertIn('src="http://127.0.0.1:8000/static/boards/early.webp"', html)
            self.assertIn('src="http://127.0.0.1:8000/static/boards/mid.webp"', html)
            self.assertIn('src="http://127.0.0.1:8000/static/boards/end.webp"', html)
            self.assertNotIn('class="board-unit"', html)
            self.assertNotIn('class="board-stats"', html)
            self.assertIn("watch?v=jCupcgaSjvo&t=180s", html)
            self.assertIn("Last Tavern turn before winning · Turn 12", html)
            self.assertLess(html.index('<section class="board-examples"'), html.index('<article class="guide-copy">'))
            self.assertLess(html.index('<section class="board-examples"'), html.index('<section class="source-card"'))

    def test_board_example_allows_useful_late_snapshot_without_known_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            board_yaml = """board_examples:
  - stage: late
    timestamp: 600
    phase: tavern
    note: A useful late-game Tavern board from a source whose overlay hides the turn number.
    image: /static/boards/late.webp
"""
            content.write_text(VALID_MARKDOWN.replace("source:\n", board_yaml + "source:\n"), encoding="utf-8")
            board_dir = root / "static/boards"
            board_dir.mkdir(parents=True)
            (board_dir / "late.webp").write_bytes(b"test-image")
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

    def test_board_examples_reject_transcribed_units_and_unsafe_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text('{"schema_version": 1, "pages": []}', encoding="utf-8")

            for board_yaml, error in (
                ("""board_examples:\n  - stage: early\n    timestamp: 180\n    phase: tavern\n    image: /static/boards/early.webp\n    units: []\n""", "screenshot-only"),
                ("""board_examples:\n  - stage: early\n    timestamp: 180\n    phase: tavern\n    image: ../secret.webp\n""", "image must be"),
            ):
                content.write_text(VALID_MARKDOWN.replace("source:\n", board_yaml + "source:\n"), encoding="utf-8")
                with self.assertRaisesRegex(CompError, error):
                    publish_comp(
                        content_path=content,
                        cards_path=cards,
                        registry_path=registry,
                        template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                        output_dir=root / "dist",
                        public_base_url="http://127.0.0.1:8000",
                        register=False,
                    )

    def test_legacy_power_metrics_are_not_rendered_or_republished(self):
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
                register=True,
                update=True,
            )

            html = (root / "dist/comps/tasty-lobstah.html").read_text(encoding="utf-8")
            self.assertNotIn('class="power-summary"', html)
            self.assertNotIn("P80 power", html)
            saved = json.loads(registry.read_text(encoding="utf-8"))["pages"][0]
            for obsolete in ("probability", "turns_to_online", "p20_power", "p50_power", "p80_power"):
                self.assertNotIn(obsolete, saved)

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

    def test_publish_refuses_source_already_used_as_supporting_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "slug": "existing-guide",
                                "source_id": "different1",
                                "supporting_sources": [
                                    {
                                        "type": "youtube",
                                        "source_id": "jCupcgaSjvo",
                                        "url": "https://www.youtube.com/watch?v=jCupcgaSjvo",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(CompError, "already used as supporting evidence"):
                publish_comp(
                    content_path=content,
                    cards_path=cards,
                    registry_path=registry,
                    template_path=Path(__file__).resolve().parents[1] / "templates/comp.html",
                    output_dir=root / "dist",
                    public_base_url="https://example.pages.dev",
                )

    def test_source_collision_keys_include_source_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "guide.md"
            content.write_text(VALID_MARKDOWN, encoding="utf-8")
            cards = root / "cards.json"
            cards.write_text(json.dumps(CARDS), encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "pages": [
                            {
                                "slug": "reddit-guide",
                                "source_type": "reddit",
                                "source_id": "jCupcgaSjvo",
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
                public_base_url="https://example.pages.dev",
            )
            saved = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(len(saved["pages"]), 2)

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
                                "source_id": "oldVideo123",
                                "slug": "tasty-lobstah",
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
                            },
                            {
                                "source_id": "jCupcgaSjvo",
                                "slug": "tasty-lobstah",
                                "url": "https://duplicate.example",
                                "published_at": "2026-08-02T00:00:00+00:00",
                            },
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
            self.assertEqual(entry["source_id"], "jCupcgaSjvo")
            self.assertEqual(entry["url"], "https://example.pages.dev/comps/tasty-lobstah.html")
            self.assertEqual(
                entry["minions"],
                [{"card_id": 132796, "count": 1, "golden_count": 0}],
            )
            self.assertEqual(entry["spells"], [])
            self.assertEqual(entry["published_at"], "2026-08-01T00:00:00+00:00")
            for result_field in ("probability", "turns_to_online", "p20_power", "p50_power", "p80_power"):
                self.assertNotIn(result_field, entry)
            for obsolete in ("evaluation", "core", "addons", "cycle", "cards"):
                self.assertNotIn(obsolete, entry)


if __name__ == "__main__":
    unittest.main()
