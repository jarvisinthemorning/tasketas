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

## Recalculate modeled probability and power

Evaluated guides declare only `composition_minions` and `composition_spells` in frontmatter. Minion entries support `count` and `golden_count`; model constants and card/effect handlers live in `comp_power.py`.

```bash
uv run python scripts/recalculate_power.py
```

One deterministic run updates only `probability`, `turns_to_online`, `p20_power`, `p50_power`, and `p80_power` in `data/registry.json`, writes every full simulation to `data/simulations/<slug>.json.gz`, and rebuilds the evaluated detail pages plus the homepage. Probability requires every listed minion copy, including the three physical copies represented by a Golden body, and applies the centrally configured light-contention model. Power is a versioned mechanics-aware board-strength score, not combat simulation or win probability. Change `CHECKPOINT_TURN` in `comp_power.py` to move the global checkpoint, then rerun this command. Use `--no-render` only when deliberately updating data without static pages.

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
source:
  type: youtube
  url: https://www.youtube.com/watch?v=VIDEO_ID
  author: Creator name
```

HSReplay requires its public composition-specific URL and numeric comp ID. Firestone currently exposes stable public comp IDs but no composition-specific permalinks, so its directory URL and `comp_id` are stored together. The publisher validates and normalizes both forms, renders them beside the original strategy source, and preserves them in `registry.json`.

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

The current public library contains 13 source-backed Season 14 guides. The homepage and `data/registry.json` are the authoritative guide count.

Unofficial, non-commercial fan project. Hearthstone and its assets belong to Blizzard Entertainment.
