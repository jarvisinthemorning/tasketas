from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


class CompError(ValueError):
    """Raised when a comp source or guide cannot be published safely."""


def canonical_source(url: str) -> tuple[str, str, str]:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    if host in {"youtu.be", "youtube.com", "m.youtube.com"}:
        if host == "youtu.be":
            source_id = parsed.path.strip("/").split("/")[0]
        else:
            source_id = parse_qs(parsed.query).get("v", [""])[0]
            if not source_id and parsed.path.startswith("/shorts/"):
                source_id = parsed.path.split("/")[2]
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", source_id):
            raise CompError(f"Invalid YouTube URL: {url}")
        return "youtube", source_id, f"https://www.youtube.com/watch?v={source_id}"

    if host.endswith("reddit.com"):
        match = re.search(r"/comments/([A-Za-z0-9]+)", parsed.path)
        if not match:
            raise CompError(f"Invalid Reddit post URL: {url}")
        source_id = match.group(1).lower()
        return "reddit", source_id, f"https://www.reddit.com/comments/{source_id}"

    raise CompError("Source must be a public YouTube video or Reddit post")


@dataclass(frozen=True)
class CardCatalog:
    payload: dict

    def require_current(self, card_id: int | str) -> dict:
        card = self.payload.get("cards", {}).get(str(card_id))
        if not card:
            raise CompError(f"Unknown card ID: {card_id}")
        if not card.get("pool"):
            raise CompError(f"{card['name']} ({card_id}) is not in the current pool")
        return card


def normalize_api_cards(cards: list[dict], *, generated_at: str) -> dict:
    """Reduce hsbg.cards API records to a deterministic local catalog."""
    normalized: dict[str, dict] = {}
    for raw in cards:
        card_id = raw.get("id")
        slug = raw.get("slug")
        name = str(raw.get("name", "")).strip()
        if not card_id or not slug or not name:
            continue
        card_type = str(raw.get("cardType") or "unknown").lower()
        image_path = raw.get("image")
        image = f"https://hsbg.cards{image_path}" if image_path else None
        if card_type == "minion":
            detail = f"https://hsreplay.net/battlegrounds/minions/{card_id}/{slug}"
        else:
            detail = f"https://hsbg.cards/card/{slug}"
        if raw.get("isDuosOnly"):
            modes = ["duos"]
        elif raw.get("isSolosOnly"):
            modes = ["solo"]
        else:
            modes = ["solo", "duos"]
        normalized[str(card_id)] = {
            "id": int(card_id),
            "card_id": raw.get("externalId"),
            "slug": slug,
            "name": name,
            "type": card_type,
            "tier": raw.get("tier"),
            "tribes": (raw.get("minionTypes") or []) if card_type == "minion" else [],
            "pool": bool(raw.get("pool")),
            "modes": modes,
            "image": image,
            "detail": detail,
            "hsreplay": detail,
        }
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "source": "https://hsbg.cards/api-docs",
        "cards": dict(sorted(normalized.items(), key=lambda item: int(item[0]))),
    }


def _parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.DOTALL)
    if not match:
        raise CompError("Guide must begin with YAML frontmatter enclosed by ---")
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise CompError("Guide frontmatter must be a mapping")
    for field in ("title", "slug", "season", "source", "verified_at"):
        if field not in metadata:
            raise CompError(f"Missing required frontmatter field: {field}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(metadata["slug"])):
        raise CompError("slug must contain lowercase letters, numbers, and hyphens only")
    if not isinstance(metadata["source"], dict) or not metadata["source"].get("url"):
        raise CompError("source.url is required")
    return metadata, match.group(2).strip()


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CompError(f"Unable to read {path}: {exc}") from exc


def _render_inline_cards(body: str, catalog: CardCatalog) -> tuple[str, list[int]]:
    inline_ids: list[int] = []
    occurrence = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal occurrence
        card = catalog.require_current(match.group(1))
        card_id = int(card["id"])
        if card_id not in inline_ids:
            inline_ids.append(card_id)
        occurrence += 1
        popover_id = f"card-popover-{card_id}-{occurrence}"
        label = html.escape((match.group(2) or card["name"]).strip())
        name = html.escape(card["name"])
        image = html.escape(card["image"], quote=True)
        detail = html.escape(card.get("detail") or card["hsreplay"], quote=True)
        tier = f"Tier {card['tier']}" if card.get("tier") else card.get("type", "Card").title()
        return (
            '<span class="card-ref">'
            f'<button type="button" class="card-ref-trigger" aria-describedby="{popover_id}">{label}</button>'
            f'<span class="card-popover" id="{popover_id}" role="tooltip">'
            f'<a class="card-popover-link" href="{detail}" target="_blank" rel="noopener noreferrer">'
            f'<img src="{image}" alt="{name}" loading="lazy">'
            f'<span class="card-popover-meta"><strong>{name}</strong><small>{html.escape(tier)}</small></span>'
            '</a></span></span>'
        )

    rendered = re.sub(r"\[\[card:(\d+)(?:\|([^\]]+))?\]\]", replace, body)
    return rendered, inline_ids


def publish_comp(
    *,
    content_path: Path,
    cards_path: Path,
    registry_path: Path,
    template_path: Path,
    output_dir: Path,
    public_base_url: str,
    register: bool = True,
    update: bool = False,
) -> dict:
    metadata, body = _parse_markdown(content_path)
    source_type, source_id, source_url = canonical_source(metadata["source"]["url"])
    declared_type = metadata["source"].get("type")
    if declared_type and declared_type != source_type:
        raise CompError(f"source.type must be {source_type}")

    registry = _load_json(registry_path)
    existing_index = next(
        (index for index, page in enumerate(registry.get("pages", [])) if page.get("source_id") == source_id),
        None,
    )
    if register and existing_index is not None and not update:
        raise CompError(f"Source {source_id} was already published")

    catalog = CardCatalog(_load_json(cards_path))
    sections: dict[str, list[dict]] = {}
    all_ids: list[int] = []
    for section in ("core", "addons", "cycle"):
        ids = metadata.get(section, []) or []
        if not isinstance(ids, list):
            raise CompError(f"{section} must be a list of card IDs")
        cards = [catalog.require_current(card_id) for card_id in ids]
        sections[section] = cards
        for card in cards:
            card_id = int(card["id"])
            if card_id not in all_ids:
                all_ids.append(card_id)

    comp = dict(metadata)
    comp["sections"] = sections
    comp["source"]["type"] = source_type
    comp["source"]["url"] = source_url
    body, inline_ids = _render_inline_cards(body, catalog)
    for card_id in inline_ids:
        if card_id not in all_ids:
            all_ids.append(card_id)
    body_html = markdown.markdown(body, extensions=["extra", "sane_lists"])

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
    )
    html = env.get_template(template_path.name).render(comp=comp, body_html=body_html)
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"

    destination = output_dir / "comps" / f"{metadata['slug']}.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")

    url = f"{public_base_url.rstrip('/')}/comps/{metadata['slug']}.html"
    entry = {
        "slug": metadata["slug"],
        "url": url,
        "source_type": source_type,
        "source_url": source_url,
        "source_id": source_id,
        "cards": all_ids,
        "published_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if register:
        registry.setdefault("schema_version", 1)
        pages = registry.setdefault("pages", [])
        if existing_index is None:
            pages.append(entry)
        else:
            pages[existing_index] = entry
        registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry
