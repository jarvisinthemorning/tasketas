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

GitHub Pages deploys the committed `dist/` directory. The site intentionally has no index page yet; guides are shared using their direct URLs.

## First guide

https://jarvisinthemorning.github.io/tasketas/comps/end-of-turn-tasty-lobster.html

Unofficial, non-commercial fan project. Hearthstone and its assets belong to Blizzard Entertainment.
