from __future__ import annotations

import html
import json
import math
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from comp_rarity import RarityUnavailable, calculate_card_rarity


class CompError(ValueError):
    """Raised when a comp source or guide cannot be published safely."""


def _recorded_stat_number(value: int | str) -> int:
    """Convert an exact stat or the game's rounded `1.2k` display to a number."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+(?:\.\d+)?k", value):
        return round(float(value[:-1]) * 1000)
    raise CompError(f"Unsupported recorded stat: {value!r}")


def analyze_board_examples(board_examples: list[dict]) -> list[dict]:
    """Derive reproducible raw-board metrics from recorded Tavern snapshots.

    Values abbreviated by the client (for example ``1.5k``) remain estimates;
    the rendered evaluation labels the resulting totals accordingly.
    """
    analyzed: list[dict] = []
    previous: dict | None = None
    for board in board_examples:
        units = board.get("units", [])
        stats = [
            (_recorded_stat_number(unit["attack"]), _recorded_stat_number(unit["health"]))
            for unit in units
        ]
        annotations = [str(unit.get("annotation", "")).lower() for unit in units]
        result = {
            "stage": board.get("stage"),
            "turn": board.get("turn"),
            "total_attack": sum(attack for attack, _ in stats),
            "total_health": sum(health for _, health in stats),
            "total_stats": sum(attack + health for attack, health in stats),
            "largest_body_stats": max((attack + health for attack, health in stats), default=0),
            "bodies_100_plus": sum(max(attack, health) >= 100 for attack, health in stats),
            "bodies_500_plus": sum(max(attack, health) >= 500 for attack, health in stats),
            "bodies_1000_plus": sum(max(attack, health) >= 1000 for attack, health in stats),
            "golden_units": sum(bool(unit.get("golden", False)) for unit in units),
            "divine_shields": sum("divine shield" in annotation for annotation in annotations),
            "reborns": sum("reborn" in annotation for annotation in annotations),
            "estimated_from_abbreviated_stats": any(
                isinstance(unit.get(stat_name), str)
                for unit in units
                for stat_name in ("attack", "health")
            ),
            "turns_since_previous": None,
            "stats_multiplier_per_turn": None,
        }
        turn = result["turn"]
        if previous and isinstance(turn, int) and isinstance(previous["turn"], int) and turn > previous["turn"]:
            elapsed = turn - previous["turn"]
            result["turns_since_previous"] = elapsed
            if previous["total_stats"] > 0:
                result["stats_multiplier_per_turn"] = math.pow(
                    result["total_stats"] / previous["total_stats"], 1 / elapsed
                )
        analyzed.append(result)
        previous = result
    return analyzed


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

    if host == "reddit.com" or host.endswith(".reddit.com"):
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
            "attack": raw.get("attack"),
            "health": raw.get("health"),
            "attack_gold": raw.get("attackGold"),
            "health_gold": raw.get("healthGold"),
            "text": raw.get("text"),
            "text_gold": raw.get("textGold"),
            "keywords": sorted({str(keyword).strip().lower() for keyword in raw.get("keywords", []) if str(keyword).strip()}),
            "tribes": (raw.get("minionTypes") or []) if card_type == "minion" else [],
            "categories": sorted({str(category).lower() for category in raw.get("categories", [])}),
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


def _normalize_discovery_sources(raw_sources: object) -> list[dict]:
    if raw_sources is None:
        return []
    if not isinstance(raw_sources, list):
        raise CompError("discovery_sources must be a list")

    normalized: list[dict] = []
    for index, raw in enumerate(raw_sources, start=1):
        if not isinstance(raw, dict):
            raise CompError(f"discovery_sources[{index}] must be a mapping")
        source_type = str(raw.get("type", "")).strip().lower()
        parsed = urlparse(str(raw.get("url", "")).strip())
        host = parsed.netloc.lower().removeprefix("www.")
        comp_id = str(raw.get("comp_id", "")).strip()

        if parsed.scheme != "https":
            raise CompError(f"discovery_sources[{index}].url must use https")
        if source_type == "hsreplay":
            match = re.fullmatch(r"/battlegrounds/comps/(\d+)/[a-z0-9-]+/?", parsed.path)
            if host != "hsreplay.net" or not match:
                raise CompError(f"discovery_sources[{index}] must be a public HSReplay comp URL")
            inferred_id = match.group(1)
            if comp_id and comp_id != inferred_id:
                raise CompError(f"discovery_sources[{index}].comp_id does not match its HSReplay URL")
            comp_id = inferred_id
            url = f"https://hsreplay.net{parsed.path.rstrip('/')}"
            label = "HSReplay composition guide"
        elif source_type == "firestone":
            if host != "firestoneapp.com" or parsed.path.rstrip("/") != "/battlegrounds/comps":
                raise CompError(f"discovery_sources[{index}] must use Firestone's public comp directory")
            if not comp_id:
                raise CompError(f"discovery_sources[{index}].comp_id is required for Firestone")
            url = "https://www.firestoneapp.com/battlegrounds/comps"
            label = "Firestone composition directory"
        else:
            raise CompError(f"discovery_sources[{index}].type must be hsreplay or firestone")

        normalized.append(
            {
                "type": source_type,
                "url": url,
                "comp_id": comp_id,
                "label": label,
            }
        )
    return normalized


def _normalize_supporting_sources(raw_sources: object) -> list[dict]:
    if raw_sources is None:
        return []
    if not isinstance(raw_sources, list):
        raise CompError("supporting_sources must be a list")

    normalized: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for index, raw in enumerate(raw_sources, start=1):
        if not isinstance(raw, dict):
            raise CompError(f"supporting_sources[{index}] must be a mapping")
        declared_type = str(raw.get("type", "")).strip().lower()
        source_type, source_id, source_url = canonical_source(str(raw.get("url", "")))
        if declared_type and declared_type != source_type:
            raise CompError(f"supporting_sources[{index}].type must be {source_type}")
        author = str(raw.get("author", "")).strip()
        label = str(raw.get("label", "")).strip()
        if not author:
            raise CompError(f"supporting_sources[{index}].author is required")
        if not label:
            raise CompError(f"supporting_sources[{index}].label is required")
        raw_timestamp = raw.get("timestamp", 0)
        if isinstance(raw_timestamp, bool) or not isinstance(raw_timestamp, int) or raw_timestamp < 0:
            raise CompError(f"supporting_sources[{index}].timestamp must be a non-negative integer")
        if raw_timestamp and source_type != "youtube":
            raise CompError(f"supporting_sources[{index}].timestamp is only valid for YouTube")
        key = (source_type, source_id)
        if key in seen:
            raise CompError(f"supporting_sources[{index}] duplicates source {source_id}")
        seen.add(key)
        normalized.append(
            {
                "type": source_type,
                "url": source_url,
                "source_id": source_id,
                "author": author,
                "label": label,
                "timestamp": raw_timestamp,
            }
        )
    return normalized


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


def _normalize_composition_cards(
    raw: object,
    *,
    field: str,
    expected_type: str | None,
    catalog: CardCatalog,
) -> list[dict]:
    if not isinstance(raw, list):
        raise CompError(f"{field} must be a list")
    normalized: list[dict] = []
    for index, item in enumerate(raw, start=1):
        if isinstance(item, int) and not isinstance(item, bool):
            item = {"card_id": item}
        if not isinstance(item, dict):
            raise CompError(f"{field}[{index}] must be a card ID or mapping")
        card_id = item.get("card_id")
        count = item.get("count", 1)
        golden_count = item.get("golden_count", 0)
        if not isinstance(card_id, int) or isinstance(card_id, bool):
            raise CompError(f"{field}[{index}].card_id must be an integer")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise CompError(f"{field}[{index}].count must be a positive integer")
        if (
            not isinstance(golden_count, int)
            or isinstance(golden_count, bool)
            or golden_count < 0
            or golden_count > count
        ):
            raise CompError(f"{field}[{index}].golden_count must be from 0 to count")
        card = catalog.require_current(card_id)
        if expected_type is not None and card.get("type") != expected_type:
            raise CompError(f"{field}[{index}] must reference a {expected_type}")
        value = {"card_id": int(card["id"]), "count": count}
        if expected_type == "minion":
            value["golden_count"] = golden_count
        normalized.append(value)
    return normalized


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
    registry_pages = registry.get("pages", [])
    source_indices = [
        index
        for index, page in enumerate(registry_pages)
        if page.get("source_id") == source_id
        and page.get("source_type", source_type) == source_type
    ]
    supporting_source_indices = [
        index
        for index, page in enumerate(registry_pages)
        if any(
            supporting.get("source_id") == source_id
            and supporting.get("type", source_type) == source_type
            for supporting in page.get("supporting_sources", [])
            if isinstance(supporting, dict)
        )
    ]
    foreign_supporting_indices = [
        index
        for index in supporting_source_indices
        if registry_pages[index].get("slug") != metadata["slug"]
    ]
    if register and foreign_supporting_indices:
        owner = registry_pages[foreign_supporting_indices[0]].get("slug", "another guide")
        raise CompError(f"Source {source_id} is already used as supporting evidence by {owner}")
    slug_indices = [
        index for index, page in enumerate(registry_pages) if page.get("slug") == metadata["slug"]
    ]
    if register and not update and source_indices:
        raise CompError(f"Source {source_id} was already published")
    if register and not update and slug_indices:
        raise CompError(f"Slug {metadata['slug']} was already published; use update")
    existing_indices = sorted(set(source_indices + (slug_indices if update else [])))
    if update and len(existing_indices) > 1:
        conflicting_slugs = {
            registry_pages[index].get("slug")
            for index in existing_indices
            if registry_pages[index].get("slug") not in (None, metadata["slug"])
        }
        if conflicting_slugs:
            raise CompError(
                f"Update would merge source {source_id} across different slugs: {sorted(conflicting_slugs)}"
            )
    existing_index = existing_indices[0] if existing_indices else None
    existing_entry = (
        registry_pages[existing_index] if existing_index is not None else None
    )

    cards_payload = _load_json(cards_path)
    catalog = CardCatalog(cards_payload)

    def package_card(card_id: int) -> dict:
        card = dict(catalog.require_current(card_id))
        try:
            rarity = calculate_card_rarity(cards_payload, card_id)
        except RarityUnavailable as error:
            rarity = {
                "percent": None,
                "display": "Generated",
                "basis": "no direct offer percentage",
                "assumption": str(error),
            }
        if rarity.get("percent") is not None:
            rarity["short_basis"] = "/ refresh" if card.get("type") == "minion" else "/ offer"
        card["rarity"] = rarity
        return card
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

    raw_packages = metadata.get("packages")
    packages: list[dict] = []
    if raw_packages is not None:
        if not isinstance(raw_packages, list) or not raw_packages:
            raise CompError("packages must be a non-empty list")
        fixed_titles = [
            package.get("title") if isinstance(package, dict) else None
            for package in raw_packages[:2]
        ]
        if len(raw_packages) < 2 or fixed_titles != ["Commit", "Core"]:
            raise CompError("packages must start with fixed Commit and Core sections")
        for package_index, raw_package in enumerate(raw_packages, start=1):
            if not isinstance(raw_package, dict):
                raise CompError(f"packages[{package_index}] must be a mapping")
            title = raw_package.get("title")
            purpose = raw_package.get("purpose")
            optional = raw_package.get("optional", package_index > 2)
            badge = raw_package.get("badge")
            ids = raw_package.get("cards")
            if not isinstance(title, str) or not title.strip():
                raise CompError(f"packages[{package_index}].title must be non-empty text")
            if not isinstance(purpose, str) or not purpose.strip():
                raise CompError(f"packages[{package_index}].purpose must be non-empty text")
            if not isinstance(optional, bool):
                raise CompError(f"packages[{package_index}].optional must be true or false")
            if badge is not None and (not isinstance(badge, str) or not badge.strip()):
                raise CompError(f"packages[{package_index}].badge must be non-empty text")
            if not isinstance(ids, list):
                raise CompError(f"packages[{package_index}].cards must be a non-empty list of card IDs")
            if not ids and package_index != 1:
                if package_index == 2:
                    raise CompError("Core cards must be a non-empty list")
                raise CompError(f"packages[{package_index}].cards must be a non-empty list of card IDs")
            cards = [package_card(card_id) for card_id in ids]
            packages.append(
                {
                    "title": title.strip(),
                    "purpose": purpose.strip(),
                    "optional": optional,
                    "badge": badge.strip() if badge is not None else (
                        "Optional package" if optional else "Required"
                    ),
                    "cards": cards,
                }
            )
            for card in cards:
                card_id = int(card["id"])
                if card_id not in all_ids:
                    all_ids.append(card_id)
    else:
        package_defaults = {
            "core": ("Core", "The engine pieces that make the comp work.", False),
            "addons": ("Add-ons", "Permanent support and scaling pieces.", True),
            "cycle": ("Cycle", "Temporary cards or repeatable resources that accelerate the board.", True),
        }
        for key in ("core", "addons", "cycle"):
            if sections[key]:
                title, purpose, optional = package_defaults[key]
                packages.append(
                    {
                        "title": title,
                        "purpose": purpose,
                        "optional": optional,
                        "badge": "Optional package" if optional else "Required",
                        "cards": [package_card(card["id"]) for card in sections[key]],
                    }
                )

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

    raw_related_routes = metadata.get("related_routes")
    if raw_related_routes is None:
        raw_related_routes = []
    if not isinstance(raw_related_routes, list):
        raise CompError("related_routes must be a list")
    related_routes: list[dict] = []
    for route_index, raw_route in enumerate(raw_related_routes, start=1):
        if not isinstance(raw_route, dict):
            raise CompError(f"related_routes[{route_index}] must be a mapping")
        title = raw_route.get("title")
        slug = raw_route.get("slug")
        purpose = raw_route.get("purpose")
        ids = raw_route.get("cards")
        if not isinstance(title, str) or not title.strip():
            raise CompError(f"related_routes[{route_index}].title must be non-empty text")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise CompError(f"related_routes[{route_index}].slug must be a lowercase guide slug")
        if slug == metadata["slug"]:
            raise CompError(f"related_routes[{route_index}].slug cannot link to the current guide")
        if not isinstance(purpose, str) or not purpose.strip():
            raise CompError(f"related_routes[{route_index}].purpose must be non-empty text")
        if not isinstance(ids, list) or not 1 <= len(ids) <= 3:
            raise CompError(f"related_routes[{route_index}].cards must contain one to three card IDs")
        related_routes.append(
            {
                "title": title.strip(),
                "slug": slug,
                "purpose": purpose.strip(),
                "cards": [dict(catalog.require_current(card_id)) for card_id in ids],
            }
        )

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

    discovery_sources = _normalize_discovery_sources(metadata.get("discovery_sources"))
    supporting_sources = _normalize_supporting_sources(metadata.get("supporting_sources"))
    if any(item["type"] == source_type and item["source_id"] == source_id for item in supporting_sources):
        raise CompError("supporting_sources must not repeat the primary source")
    if register:
        for supporting in supporting_sources:
            supporting_id = supporting["source_id"]
            for page in registry_pages:
                if page.get("slug") == metadata["slug"]:
                    continue
                if (
                    page.get("source_id") == supporting_id
                    and page.get("source_type", supporting["type"]) == supporting["type"]
                ):
                    raise CompError(
                        f"Supporting source {supporting_id} was already published as the primary source of {page.get('slug', 'another guide')}"
                    )
                if any(
                    existing.get("source_id") == supporting_id
                    and existing.get("type", supporting["type"]) == supporting["type"]
                    for existing in page.get("supporting_sources", [])
                    if isinstance(existing, dict)
                ):
                    raise CompError(
                        f"Supporting source {supporting_id} is already used by {page.get('slug', 'another guide')}"
                    )
    body, inline_ids = _render_inline_cards(body, catalog)
    for card_id in inline_ids:
        if card_id not in all_ids:
            all_ids.append(card_id)
    body_html = markdown.markdown(body, extensions=["extra", "sane_lists"])

    raw_minions = metadata.get("composition_minions")
    raw_spells = metadata.get("composition_spells")
    raw_hand_minions = metadata.get("composition_hand_minions", [])
    raw_prerequisites = metadata.get("composition_prerequisites", [])
    if raw_minions is None:
        if board_examples:
            stage_order = {"early": 0, "mid": 1, "late": 2, "end": 3}
            reference_board = max(
                board_examples,
                key=lambda board: (stage_order[board["stage"]], board.get("turn") or -1),
            )
            grouped: dict[int, dict] = {}
            for unit in reference_board["units"]:
                card_id = int(unit["card"]["id"])
                item = grouped.setdefault(
                    card_id,
                    {"card_id": card_id, "count": 0, "golden_count": 0},
                )
                item["count"] += 1
                item["golden_count"] += int(unit["golden"])
            raw_minions = list(grouped.values())
        else:
            raw_minions = [
                card_id
                for card_id in all_ids
                if catalog.require_current(card_id).get("type") == "minion"
            ]
            if len(raw_minions) > 7:
                raise CompError(
                    "composition_minions is required when guide mentions exceed seven minions"
                )
    if raw_spells is None:
        raw_spells = [card_id for card_id in all_ids if catalog.require_current(card_id).get("type") == "spell"]
    minions = _normalize_composition_cards(
        raw_minions,
        field="composition_minions",
        expected_type="minion",
        catalog=catalog,
    )
    spells = _normalize_composition_cards(
        raw_spells,
        field="composition_spells",
        expected_type="spell",
        catalog=catalog,
    )
    hand_minions = _normalize_composition_cards(
        raw_hand_minions,
        field="composition_hand_minions",
        expected_type="minion",
        catalog=catalog,
    )
    prerequisites = _normalize_composition_cards(
        raw_prerequisites,
        field="composition_prerequisites",
        expected_type=None,
        catalog=catalog,
    )
    if sum(item["count"] for item in minions) > 7:
        raise CompError("composition_minions must fit the seven-slot Battlegrounds board")
    for field, items in (
        ("composition_minions", minions),
        ("composition_spells", spells),
        ("composition_hand_minions", hand_minions),
        ("composition_prerequisites", prerequisites),
    ):
        card_ids = [item["card_id"] for item in items]
        if len(card_ids) != len(set(card_ids)):
            raise CompError(f"{field} must combine duplicate card IDs into one count")
    comp = dict(metadata)
    comp["discovery_sources"] = discovery_sources
    comp["supporting_sources"] = supporting_sources
    comp["sections"] = sections
    comp["packages"] = packages
    comp["related_routes"] = related_routes
    comp["board_examples"] = board_examples
    comp["minions"] = minions
    comp["spells"] = spells
    comp["hand_minions"] = hand_minions
    comp["prerequisites"] = prerequisites
    comp.pop("evaluation", None)
    comp["source"]["type"] = source_type
    comp["source"]["url"] = source_url

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
        "minions": minions,
        "spells": spells,
        "hand_minions": hand_minions,
        "prerequisites": prerequisites,
        "verified_at": str(metadata["verified_at"]),
        "source_type": source_type,
        "source_url": source_url,
        "source_author": metadata["source"].get("author", "Original source"),
        "source_id": source_id,
        "discovery_sources": discovery_sources,
        "supporting_sources": supporting_sources,
        "published_at": (
            existing_entry.get("published_at")
            if existing_entry and existing_entry.get("published_at")
            else datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        ),
    }
    if register:
        registry["schema_version"] = 2
        pages = registry.setdefault("pages", [])
        if existing_index is None:
            pages.append(entry)
        else:
            pages[existing_index] = entry
            for duplicate_index in reversed(existing_indices[1:]):
                del pages[duplicate_index]
        registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry
