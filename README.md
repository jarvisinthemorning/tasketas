# Tasketas

Static, mobile-first Hearthstone Battlegrounds comp guides generated from public YouTube videos and Reddit posts, with separate attribution for public composition directories used during discovery.

## Local setup

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

## Refresh the card catalogue

```bash
uv run python scripts/refresh_cards.py
```

The catalogue uses numeric card IDs and public card data/images from https://hsbg.cards. Minions link to their public HSReplay detail pages.

## Check card rarity

Package cards receive a simple card-level rarity status during publication—not a whole-comp completion score. Tavern minions assume the needed tribe is active with a full, uncontested Solo pool; generated minions are labeled rather than assigned a false shop percentage.

```bash
uv run python scripts/calculate_rarity.py <card-id> [<card-id> ...]
```

Tavern minions use tier pool copies and shop size. Tavern and categorized generated spells use their relevant catalog, Hero Powers use the selectable Solo hero count, and trinkets show a disclosed catalog baseline because their actual offer eligibility varies. The old power-model scripts remain in the repository for reference but are not part of guide publication.

## Preview a guide

Start from `templates/comp-guide.md`. Keep the original strategy evidence under `source`/`video`. When HSReplay or Firestone lists the same engine, record it separately under `discovery_sources`; directory listings are attribution and discovery signals, not substitutes for a demonstrated strategy source.

```yaml
discovery_sources:
  - type: hsreplay
    url: https://hsreplay.net/battlegrounds/comps/90/quilboar-bristlemane
    comp_id: '90'
  - type: firestone
    url: https://www.firestoneapp.com/battlegrounds/comps
    comp_id: quilboar_choose_one
supporting_sources:
  - type: youtube
    url: https://www.youtube.com/watch?v=SUPPORT_VIDEO_ID
    author: Creator name
    label: Optional package demonstration
    timestamp: 388
source:
  type: youtube
  url: https://www.youtube.com/watch?v=VIDEO_ID
  author: Creator name
```

HSReplay requires its public composition-specific URL and numeric comp ID. Firestone currently exposes stable public comp IDs but no composition-specific permalinks, so its directory URL and `comp_id` are stored together. `supporting_sources` records secondary public evidence for a specific package or variation; it never replaces the primary strategy source. The publisher validates and normalizes these forms, renders them beside the original strategy source, and preserves them in `registry.json`.

```bash
uv run python scripts/publish_comp.py content/<guide>.md \
  --base-url http://127.0.0.1:8000 \
  --preview

cd dist
python3 -m http.server 8000
```

## Publish a guide

```bash
uv run python scripts/publish_comp.py content/<guide>.md \
  --base-url https://jarvisinthemorning.github.io/tasketas \
  --push
```

GitHub Pages deploys the committed `dist/` directory. Each publication rebuilds the static `dist/index.html` shell and copies `registry.json` plus `cards.json` into `dist/data/`. The browser fetches the compact registry first so guide rows do not depend on the larger card catalogue; it loads card metadata only when the collapsed filter panel is opened. Tribe, tag, and contained-card filtering then runs locally in JavaScript; there is no API or server runtime.

Full-game video guides can also define source-verified `board_examples` for early, mid, and final boards. The renderer preserves board slots, displays the recorded attack/health beneath each card, links each example to its video timestamp, and places the section immediately before the original source.

The publisher also enforces explicit emergency bans that may not yet be reflected by the public catalogue. Hoarding Hyena (`133039`) is currently rejected from every guide field and board example.

## Homepage

https://jarvisinthemorning.github.io/tasketas/

## Season 14 library

The active catalogue currently contains three new-format reference guides. Thirteen older guides are preserved as public artifacts under `dist/legacy/` but are excluded from the homepage and active `data/registry.json`. `content/legacy/registry.json` is an internal migration record for those archived pages, not the active site registry.

The default test suite covers publisher, schema, registry, and rarity code with synthetic fixtures. It does not assert editorial choices inside live guides. See `tests/README.md` for the test policy and the explicitly opt-in legacy Power suite.

Unofficial, non-commercial fan project. Hearthstone and its assets belong to Blizzard Entertainment.
