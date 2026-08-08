# Tasketas

Static, mobile-first Hearthstone Battlegrounds comp guides generated from public YouTube videos and Reddit posts.

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

## Preview a guide

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

GitHub Pages deploys the committed `dist/` directory. Each publication rebuilds the static `dist/index.html` shell and copies `registry.json` plus `cards.json` into `dist/data/`. The browser fetches both static JSON files together on page load, renders card names/thumbnails immediately, and sorts newest-first while the filter section remains collapsed. Tribe, tag, and contained-card filtering then runs locally in JavaScript; there is no API or server runtime.

Full-game video guides can also define source-verified `board_examples` for early, mid, and final boards. The renderer preserves board slots, displays the recorded attack/health beneath each card, links each example to its video timestamp, and places the section immediately before the original source.

The publisher also enforces explicit emergency bans that may not yet be reflected by the public catalogue. Hoarding Hyena (`133039`) is currently rejected from every guide field and board example.

## Homepage

https://jarvisinthemorning.github.io/tasketas/

## Season 14 library

The checked-in batch contains ten post-launch, source-backed guides: one distinct engine for each active tribe.

Unofficial, non-commercial fan project. Hearthstone and its assets belong to Blizzard Entertainment.
