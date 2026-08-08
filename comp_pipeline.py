from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


class CompError(ValueError):
    """Raised when a comp source or guide cannot be published safely."""


EXPLICITLY_BANNED_CARDS = {
    133039: "Hoarding Hyena",
}


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
        numeric_card_id = int(card_id)
        if numeric_card_id in EXPLICITLY_BANNED_CARDS:
            name = EXPLICITLY_BANNED_CARDS[numeric_card_id]
            raise CompError(f"{name} ({numeric_card_id}) is banned and cannot be published")
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
    for field in ("title", "slug", "season", "tribes", "tags", "source", "verified_at"):
        if field not in metadata:
            raise CompError(f"Missing required frontmatter field: {field}")
    for field in ("tribes", "tags"):
        if not isinstance(metadata[field], list) or not metadata[field]:
            raise CompError(f"{field} must be a non-empty list")
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


def build_index(
    *,
    registry_path: Path,
    cards_path: Path,
    template_path: Path,
    output_dir: Path,
) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
    )
    rendered = env.get_template(template_path.name).render()
    rendered = "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "index.html"
    destination.write_text(rendered, encoding="utf-8")
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(registry_path, data_dir / "registry.json")
    shutil.copy2(cards_path, data_dir / "cards.json")
    return destination


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

    # Keep the aggregate future-proof: any top-level list of numeric card IDs
    # participates in validation and local index filtering, even if the guide
    # template does not yet give that section a dedicated visual block.
    for value in metadata.values():
        if not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, int) and not isinstance(item, bool):
                catalog.require_current(item)
                if item not in all_ids:
                    all_ids.append(item)

    raw_boards = metadata.get("board_examples", []) or []
    if not isinstance(raw_boards, list):
        raise CompError("board_examples must be a list")
    board_examples: list[dict] = []
    stage_labels = {
        "early": "Early game",
        "mid": "Mid game",
        "late": "Late game",
        "end": "Last Tavern turn before winning",
    }
    for board_index, raw_board in enumerate(raw_boards, start=1):
        if not isinstance(raw_board, dict):
            raise CompError(f"board_examples[{board_index}] must be a mapping")
        stage = raw_board.get("stage")
        if stage not in stage_labels:
            raise CompError(f"board_examples[{board_index}].stage must be early, mid, late, or end")
        turn = raw_board.get("turn")
        timestamp = raw_board.get("timestamp")
        if turn is not None and (not isinstance(turn, int) or isinstance(turn, bool) or turn < 1):
            raise CompError(f"board_examples[{board_index}].turn must be a positive integer when provided")
        if not isinstance(timestamp, int) or isinstance(timestamp, bool) or timestamp < 0:
            raise CompError(f"board_examples[{board_index}].timestamp must be a non-negative integer")
        raw_units = raw_board.get("units")
        if not isinstance(raw_units, list) or not 1 <= len(raw_units) <= 7:
            raise CompError(f"board_examples[{board_index}].units must contain 1 to 7 units")
        units: list[dict] = []
        used_slots: set[int] = set()
        for unit_index, raw_unit in enumerate(raw_units, start=1):
            if not isinstance(raw_unit, dict):
                raise CompError(f"board_examples[{board_index}].units[{unit_index}] must be a mapping")
            card_id = raw_unit.get("card_id")
            if not isinstance(card_id, int) or isinstance(card_id, bool):
                raise CompError(
                    f"board_examples[{board_index}].units[{unit_index}].card_id must be an integer"
                )
            card_data = catalog.require_current(card_id)
            slot = raw_unit.get("slot", unit_index)
            if not isinstance(slot, int) or isinstance(slot, bool) or not 1 <= slot <= 7:
                raise CompError(f"board_examples[{board_index}].units[{unit_index}].slot must be from 1 to 7")
            if slot in used_slots:
                raise CompError(f"board_examples[{board_index}] contains duplicate board slot {slot}")
            used_slots.add(slot)
            attack = raw_unit.get("attack")
            health = raw_unit.get("health")
            for stat_name, stat in (("attack", attack), ("health", health)):
                is_exact = isinstance(stat, int) and not isinstance(stat, bool) and stat >= 0
                is_game_display = isinstance(stat, str) and re.fullmatch(r"\d+(?:\.\d+)?k", stat)
                if not is_exact and not is_game_display:
                    raise CompError(
                        f"board_examples[{board_index}].units[{unit_index}].{stat_name} "
                        "must be a non-negative integer or a recorded value such as 1.2k"
                    )
            golden = raw_unit.get("golden", False)
            annotation = raw_unit.get("annotation", "")
            if not isinstance(golden, bool):
                raise CompError(f"board_examples[{board_index}].units[{unit_index}].golden must be true or false")
            if not isinstance(annotation, str):
                raise CompError(f"board_examples[{board_index}].units[{unit_index}].annotation must be text")
            units.append(
                {
                    "card": card_data,
                    "slot": slot,
                    "attack": attack,
                    "health": health,
                    "golden": golden,
                    "annotation": annotation.strip(),
                }
            )
            numeric_card_id = int(card_data["id"])
            if numeric_card_id not in all_ids:
                all_ids.append(numeric_card_id)
        board_examples.append(
            {
                "stage": stage,
                "label": stage_labels[stage],
                "turn": turn,
                "timestamp": timestamp,
                "note": str(raw_board.get("note", "")).strip(),
                "units": units,
            }
        )

    comp = dict(metadata)
    comp["sections"] = sections
    comp["board_examples"] = board_examples
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
        "title": metadata["title"],
        "url": url,
        "season": metadata["season"],
        "modes": metadata.get("modes", []) or [],
        "tribes": metadata.get("tribes", []) or [],
        "tags": metadata.get("tags", []) or [],
        "core": [int(card["id"]) for card in sections["core"]],
        "addons": [int(card["id"]) for card in sections["addons"]],
        "cycle": [int(card["id"]) for card in sections["cycle"]],
        "verified_at": str(metadata["verified_at"]),
        "source_type": source_type,
        "source_url": source_url,
        "source_author": metadata["source"].get("author", "Original source"),
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
