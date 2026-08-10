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

from comp_power import (
    AIR_REVENANT,
    BALINDA,
    BARRIER_BANSHEE,
    BRANN,
    BRONZE_TIMEWALKER,
    CHECKPOINT_TURN,
    CHORAL_MRGLR,
    CLEVER_CASTAWAY,
    CONTENTION_HOLD_CHANCE,
    CRIMSON_VINDICATOR,
    DEATHSTRIDER,
    DRAKKARI_ENCHANTER,
    DRUSTFALLEN_BUTCHER,
    ENTERPRISING_ESCAPEE,
    EXPERT_AVIATOR,
    FAUNA_WHISPERER,
    FIRE_FORGED_EVOKER,
    FRIENDLY_GEIST,
    GATEKEEPER_AMALGAM,
    GLAMBOT,
    HANDLESS_FORSAKEN,
    HOGRIDER,
    HOOKTUSK,
    JAILBIRD_JUGGERNAUT,
    KALECGOS,
    LEEROY,
    MANA_SURGE,
    MOAT_CUSTODIAN,
    MODEL_VERSION,
    PERSISTENT_POET,
    PLAGUERUNNER,
    ROLL_START_TURN,
    ROLL_TURNS,
    SHAMANIC_TIDECALLER,
    SKY_HATCH_RUNAWAY,
    SNAZZY_PHANTOM,
    TASTY_LOBSTER,
    TIMEWARPED_EMBALMER,
    TRANQUIL_MEDITATIVE,
    TRENCH_FIGHTER,
    TWILIGHT_TIDEHUNTER,
    UNBOUND_TEMPEST,
    UTILITY_DRONE,
    VIGILANT_BRISTLEMANE,
    WARPWING,
)


class CompError(ValueError):
    """Raised when a comp source or guide cannot be published safely."""


RESULT_FIELDS = ("probability", "turns_to_online", "p20_power", "p50_power", "p80_power")


def probability_label(probability: float) -> str:
    if probability >= 0.20:
        return "Common"
    if probability >= 0.05:
        return "Regular"
    if probability >= 0.01:
        return "Rare"
    if probability >= 0.001:
        return "High-roll"
    return "Lottery"


def format_power(value: int) -> str:
    if value < 1_000:
        return str(value)
    compact = f"{value / 1_000:.1f}".rstrip("0").rstrip(".")
    return f"{compact}k"


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


def _materialize_power_summary(metrics: dict | None, minions: list[dict]) -> dict | None:
    if not metrics or not all(field in metrics for field in RESULT_FIELDS):
        return None
    probability = metrics["probability"]
    turns = metrics["turns_to_online"]
    powers = [metrics[field] for field in ("p20_power", "p50_power", "p80_power")]
    if (
        isinstance(probability, bool)
        or not isinstance(probability, (int, float))
        or not 0 <= probability <= 1
        or isinstance(turns, bool)
        or not isinstance(turns, int)
        or turns < 1
        or any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in powers)
        or powers != sorted(powers)
    ):
        raise CompError("registry power result values are invalid")
    minion_ids = {item["card_id"] for item in minions}
    notes: list[str] = []
    if BALINDA in minion_ids:
        notes.append(
            "Balinda makes targeted spells cast twice, multiplying both spell effects and the triggers they cause."
        )
    if {TASTY_LOBSTER, DEATHSTRIDER} <= minion_ids:
        notes.append(
            "A source-verified Headhunter Gryphon Rally triggers one Lobster Deathrattle per combat; "
            "combat buffs do not persist and Lobster's hidden future-improvement scalar is unmodeled."
        )
    if {KALECGOS, BRANN, BRONZE_TIMEWALKER, SKY_HATCH_RUNAWAY} <= minion_ids:
        notes.append(
            "Sky-hatch Runaway supplies one immediate Chromadrake on assembly; two natural Timewalker "
            "Rallies resolve in combat and their Chromadrakes become playable next recruit turn."
        )
    if {MOAT_CUSTODIAN, MANA_SURGE} <= minion_ids:
        notes.append(
            "The trace plays two Elementals per recruit phase through Mana Surge, then credits one "
            "Moat Custodian Rally improvement; extra cycle and Rally-enabler odds are excluded."
        )
    if {UNBOUND_TEMPEST, AIR_REVENANT} <= minion_ids:
        notes.append(
            "This source-demonstrated line is conditional on Spirit Swap; hero-selection odds and "
            "random Dark Gifts, repeated Elemental fuel, and cycle-card acquisition odds are excluded. "
            "The assembly turn grants no loop. On each later recruit turn the trace adds one Air Revenant "
            "activation, distributes every active Easterly Winds randomly across six Tavern slots, and "
            "selects the slot with the most hits while excluding its base minion stats. Spirit Swap then "
            "adds the strongest friendly Attack before one Tempest trigger after three Elemental plays."
        )
    if {GLAMBOT, FAUNA_WHISPERER, UTILITY_DRONE, BALINDA, DRAKKARI_ENCHANTER} <= minion_ids:
        notes.append(
            "Fauna targets adjacent Mechs; Balinda repeats each Natural Blessing and Drakkari repeats "
            "the end-of-turn sequence before Utility Drone counts each resulting Magnetization."
        )
    if {TRANQUIL_MEDITATIVE, FAUNA_WHISPERER, BALINDA} <= minion_ids:
        notes.append(
            "Each turn resolves Meditative's spell bonus before Fauna's generated Natural Blessings; "
            "Balinda repeats targeted casts and generated-spell offer odds are excluded."
        )
    if {ENTERPRISING_ESCAPEE, HOOKTUSK, CLEVER_CASTAWAY} <= minion_ids:
        notes.append(
            "The trace spends 10 Gold per turn and tracks Lockbox openings separately from Clever "
            "Castaway Activates. Only Castaway counts as a Discover for Hooktusk; the random Lockbox "
            "body and Hooktusk's hidden Golden-minion improvement scalar are unmodeled."
        )
    if {SNAZZY_PHANTOM, BARRIER_BANSHEE, HANDLESS_FORSAKEN} <= minion_ids:
        notes.append(
            "One Handless Forsaken Reborn event gives Barrier Banshee itself +7/+7 and Divine Shield, "
            "while Snazzy gives +2/+2 to the right-most Undead; all combat gains remain temporary."
        )
    if {SHAMANIC_TIDECALLER, TWILIGHT_TIDEHUNTER, CHORAL_MRGLR, EXPERT_AVIATOR} <= minion_ids:
        notes.append(
            "The trace requires a separately declared Bream Counter in hand, one targetable Tavern "
            "spell, and one Murloc cycle per turn; Choral and Expert Aviator gains are combat-only."
        )
    if {GATEKEEPER_AMALGAM, BALINDA} <= minion_ids:
        notes.append(
            "This line is conditional on already owning Maldraxxus Dagger. Amalgamation is cast "
            "twice through Balinda on assembly; Dagger copies begin on the next recruit turn."
        )
    if {TIMEWARPED_EMBALMER, LEEROY} <= minion_ids:
        notes.append(
            "Two Embalmers, two Leeroys, and Reborn Rites provide five bounded removal uses. The "
            "score measures available removal capacity—not guaranteed kills or a combat-win rate—and "
            "Timewarped setup odds are excluded."
        )
    if {TRENCH_FIGHTER, VIGILANT_BRISTLEMANE, JAILBIRD_JUGGERNAUT} <= minion_ids:
        notes.append(
            "Trench Fighter's generated Gem Confiscation becomes usable one turn later. The trace "
            "banks Gems through Bristlemane, then transfers them to Juggernaut at the checkpoint."
        )
    if HOGRIDER in minion_ids:
        notes.append(
            "Each Turbo Hogrider turns every Choose One card into Blood Gems for the rest of the Quilboar board."
        )
    if {PLAGUERUNNER, DRUSTFALLEN_BUTCHER, FRIENDLY_GEIST} <= minion_ids:
        notes.append(
            "Butchering and Plaguerunner add permanent Attack to every Undead; "
            "Friendly Geist increases the Tavern-spell portion of later loops."
        )
        notes.append(
            "The acquisition probability is conditional on already owning Plaguerunner Portrait; "
            "it excludes Portrait and optional trinket odds."
        )
    if {FIRE_FORGED_EVOKER, CRIMSON_VINDICATOR, PERSISTENT_POET, WARPWING} <= minion_ids:
        notes.append(
            "Persistent Poet makes adjacent Dragons—including Vindicator and Warpwing—retain "
            "Fire-forged Evoker and Crimson Vindicator combat gains between fights; each "
            "combat-cast Mighty Dragonbreath doubles the Evoker buff for the next fight. "
            "The score does not assign extra utility to Warpwing being Immune while attacking."
        )
    return {
        "probability": probability,
        "probability_percent": round(probability * 100),
        "probability_label": probability_label(probability),
        "turns_to_online": turns,
        "checkpoint_turn": CHECKPOINT_TURN,
        "probability_note": (
            f"Probability includes random tribe availability and finding every listed minion over "
            f"{ROLL_TURNS} Tavern 6 recruit phases from Turn {ROLL_START_TURN}. "
            f"Each required card has a {round(CONTENTION_HOLD_CHANCE * 100)}% chance that one "
            "pool copy is held by a rival. Online is the median turn among successful assemblies."
        ),
        "score_note": (
            f"Power model {MODEL_VERSION} is a mechanics-aware board-strength score, not combat simulation "
            "or win probability. Percentiles include only successful assemblies."
        ),
        "p20": powers[0],
        "p50": powers[1],
        "p80": powers[2],
        "p20_label": format_power(powers[0]),
        "p50_label": format_power(powers[1]),
        "p80_label": format_power(powers[2]),
        "notes": notes,
    }


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
    existing_entry = (
        registry.get("pages", [])[existing_index] if existing_index is not None else None
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

    discovery_sources = _normalize_discovery_sources(metadata.get("discovery_sources"))
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
    composition_unchanged = bool(
        existing_entry
        and existing_entry.get("minions") == minions
        and existing_entry.get("spells") == spells
        and existing_entry.get("hand_minions", []) == hand_minions
        and existing_entry.get("prerequisites", []) == prerequisites
        and existing_entry.get("tribes") == metadata["tribes"]
    )
    metrics = (
        {field: existing_entry[field] for field in RESULT_FIELDS}
        if composition_unchanged
        and existing_entry is not None
        and all(field in existing_entry for field in RESULT_FIELDS)
        else None
    )

    comp = dict(metadata)
    comp["discovery_sources"] = discovery_sources
    comp["sections"] = sections
    comp["board_examples"] = board_examples
    comp["minions"] = minions
    comp["spells"] = spells
    comp["hand_minions"] = hand_minions
    comp["prerequisites"] = prerequisites
    comp["power_summary"] = _materialize_power_summary(metrics, minions)
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
        "published_at": (
            existing_entry.get("published_at")
            if existing_entry and existing_entry.get("published_at")
            else datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        ),
    }
    if metrics:
        entry.update(metrics)
    if register:
        registry["schema_version"] = 2
        pages = registry.setdefault("pages", [])
        if existing_index is None:
            pages.append(entry)
        else:
            pages[existing_index] = entry
        registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry
