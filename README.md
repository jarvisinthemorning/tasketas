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
uv run python scripts/publish_comp.py content/end-of-turn-tasty-lobster.md \
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

GitHub Pages deploys the committed `dist/` directory. Each publication rebuilds the static `dist/index.html` shell and copies `registry.json` plus `cards.json` into `dist/data/`. The browser fetches the registry on page load, sorts newest-first, and fetches the card catalogue only when the collapsed filter section is expanded. Tribe, tag, and contained-card filtering then runs locally in JavaScript; there is no API or server runtime.

## Homepage

https://jarvisinthemorning.github.io/tasketas/

## First guide

https://jarvisinthemorning.github.io/tasketas/comps/end-of-turn-tasty-lobster.html

Unofficial, non-commercial fan project. Hearthstone and its assets belong to Blizzard Entertainment.
