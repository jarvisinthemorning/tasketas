#!/usr/bin/env python3
"""Roll the Tasketas guide library from one Battlegrounds patch to the next."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


PATCH_RE = re.compile(r"^\d+\.\d+\.\d+$")
ROOT = Path(__file__).resolve().parents[1]
EARLY_GAME_PATHS = (
    "dist/early-game.html",
    "templates/early-game.html",
    "scripts/build_early_game.py",
    "tests/test_early_game.py",
    "static/early-game.css",
    "dist/static/early-game.css",
)


def _validate_https_url(value: str, label: str, *, allow_path: bool = True) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or (not allow_path and parsed.path not in ("", "/"))
    ):
        raise ValueError(f"Invalid {label}: {value}")
    return value.rstrip("/")


def _read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _add_patch_frontmatter(path: Path, patch: str) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"(?m)^patch:\s*", text):
        return
    updated, count = re.subn(
        r"(?m)^(season:\s*[^\n]+)$",
        rf"\1\npatch: '{patch}'",
        text,
        count=1,
    )
    if count != 1:
        raise ValueError(f"Cannot add patch metadata to {path}: missing season frontmatter")
    path.write_text(updated, encoding="utf-8")


def _render_patch_index(
    *,
    template_path: Path,
    destination: Path,
    patch: str,
    season: int,
    status: str,
    rebuilding: bool,
    previous_patches: list[dict],
) -> None:
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
    )
    html = env.get_template(template_path.name).render(
        patch=patch,
        season=season,
        status=status,
        rebuilding=rebuilding,
        previous_patches=previous_patches,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def _write_latest_redirect(path: Path, target: str) -> None:
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta http-equiv=\"refresh\" content=\"0; url={target}\">
  <link rel=\"canonical\" href=\"{target}\">
  <title>Latest Battlegrounds guides</title>
</head>
<body>
  <p>Opening the <a href=\"{target}\">latest Battlegrounds guide patch</a>…</p>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def rollover_patch(
    *,
    root: Path,
    from_patch: str,
    to_patch: str,
    released_at: str,
    source_url: str,
    public_base_url: str,
    to_season: int | None = None,
    dry_run: bool = False,
) -> dict:
    """Freeze the current patch and initialize a new permanent latest patch."""
    root = root.resolve()
    for value, label in ((from_patch, "from patch"), (to_patch, "to patch")):
        if not PATCH_RE.fullmatch(value):
            raise ValueError(f"Invalid {label}: {value}")
    if from_patch == to_patch:
        raise ValueError("Source and destination patches must differ")
    try:
        date.fromisoformat(released_at)
    except ValueError as exc:
        raise ValueError(f"Invalid release date: {released_at}") from exc
    source_url = _validate_https_url(source_url, "source URL")
    public_base_url = _validate_https_url(public_base_url, "public base URL")
    if to_season is not None and (not isinstance(to_season, int) or to_season < 1):
        raise ValueError(f"Invalid destination season: {to_season}")

    archive_content = root / "content/patches" / from_patch
    archive_data = root / "data/patches" / from_patch
    archive_dist = root / "dist/patches" / from_patch
    latest_content = root / "content/patches" / to_patch
    latest_data = root / "data/patches" / to_patch
    latest_dist = root / "dist/patches" / to_patch
    initial_migration = (root / "data/registry.json").exists()
    history_path = root / "data/patches.json"
    history_payload = _read_json(history_path) if history_path.exists() else {"patches": []}
    existing_history = history_payload.get("patches", [])
    if any(str(item.get("patch")) == to_patch for item in existing_history):
        raise FileExistsError(f"Destination patch already exists in history: {to_patch}")
    if not initial_migration:
        site = _read_json(root / "data/site.json")
        active_patch = str(site.get("latest_patch"))
        history_active = str(history_payload.get("latest_patch"))
        if active_patch != from_patch or history_active != from_patch:
            raise ValueError(
                f"Source patch {from_patch!r} is not the active patch "
                f"(site={active_patch!r}, history={history_active!r})"
            )
        source_season = int(site["season"])
    else:
        source_season = 14

    if initial_migration:
        source_content_dir = root / "content"
        source_registry = root / "data/registry.json"
        source_cards = root / "data/cards.json"
        source_comps = root / "dist/comps"
        collisions = [archive_content, archive_data, archive_dist, latest_content, latest_data, latest_dist]
    else:
        source_content_dir = archive_content
        source_registry = archive_data / "registry.json"
        source_cards = archive_data / "cards.json"
        source_comps = archive_dist / "comps"
        collisions = [latest_content, latest_data, latest_dist]

    required = (
        source_content_dir,
        source_registry,
        source_cards,
        source_comps,
        root / "templates/index.html",
        root / "static",
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing rollover inputs: " + ", ".join(missing))
    existing = [path for path in collisions if path.exists()]
    if existing:
        raise FileExistsError("Patch destination already exists: " + ", ".join(map(str, existing)))

    source_content = sorted(source_content_dir.glob("*.md"))
    registry = _read_json(source_registry)
    cards = _read_json(source_cards)
    registry_patch = registry.get("patch")
    if registry_patch is not None and str(registry_patch) != from_patch:
        raise ValueError(
            f"Source registry patch {registry_patch!r} does not match --from {from_patch!r}"
        )
    for source in source_content:
        match = re.search(r"^patch:\s*['\"]?([^'\"\s]+)", source.read_text(encoding="utf-8"), re.MULTILINE)
        if match and match.group(1) != from_patch:
            raise ValueError(
                f"Source guide {source.name} patch {match.group(1)!r} does not match --from {from_patch!r}"
            )
    registry_pages = registry.get("pages", [])
    if initial_migration and registry_pages:
        guide_seasons = {int(page["season"]) for page in registry_pages}
        if len(guide_seasons) != 1:
            raise ValueError(f"Source registry contains multiple seasons: {sorted(guide_seasons)}")
        source_season = guide_seasons.pop()
    destination_season = to_season if to_season is not None else source_season
    if len(source_content) != len(registry_pages):
        raise ValueError(
            f"Guide count mismatch: {len(source_content)} Markdown files vs "
            f"{len(registry_pages)} registry pages"
        )
    rendered_pages = sorted(source_comps.glob("*.html"))
    if len(rendered_pages) != len(registry_pages):
        raise ValueError(
            f"Rendered page count mismatch: {len(rendered_pages)} HTML files vs "
            f"{len(registry_pages)} registry pages"
        )
    registry_slugs = {str(page.get("slug")) for page in registry_pages}
    if {path.stem for path in source_content} != registry_slugs:
        raise ValueError("Markdown filenames do not match registry slugs")
    if {path.stem for path in rendered_pages} != registry_slugs:
        raise ValueError("Rendered HTML filenames do not match registry slugs")

    report = {
        "from_patch": from_patch,
        "to_patch": to_patch,
        "guide_count": len(source_content),
        "initial_migration": initial_migration,
        "destinations": [
            str(path.relative_to(root))
            for path in (latest_content, latest_data, latest_dist)
        ],
        "remove": list(EARLY_GAME_PATHS),
    }
    if dry_run:
        return report

    public_base_url = public_base_url.rstrip("/")
    if initial_migration:
        archive_content.mkdir(parents=True)
        for source in source_content:
            destination = archive_content / source.name
            shutil.copy2(source, destination)
            _add_patch_frontmatter(destination, from_patch)

        archive_registry = dict(registry)
        archive_registry["schema_version"] = 4
        archive_registry["patch"] = from_patch
        for page in archive_registry.get("pages", []):
            page["patch"] = from_patch
            page["url"] = f"{public_base_url}/patches/{from_patch}/comps/{page['slug']}.html"
        _write_json(archive_data / "registry.json", archive_registry)
        _write_json(archive_data / "cards.json", cards)

        archive_dist.mkdir(parents=True)
        shutil.copytree(source_comps, archive_dist / "comps")
        old_static_prefix = f"{public_base_url}/static/"
        new_static_prefix = f"{public_base_url}/patches/{from_patch}/static/"
        for page in (archive_dist / "comps").glob("*.html"):
            page.write_text(
                page.read_text(encoding="utf-8")
                .replace(old_static_prefix, new_static_prefix)
                .replace(
                    f"Battlegrounds comp · Season {source_season}",
                    f"Battlegrounds comp · Season {source_season} · Patch {from_patch}",
                ),
                encoding="utf-8",
            )
        shutil.copytree(
            root / "static",
            archive_dist / "static",
            ignore=shutil.ignore_patterns("early-game.css"),
        )
        _write_json(archive_dist / "data/registry.json", archive_registry)
        _write_json(archive_dist / "data/cards.json", cards)
    else:
        archive_registry = registry

    latest_content.mkdir(parents=True)
    (latest_content / ".gitkeep").write_text("", encoding="utf-8")
    latest_registry = {"schema_version": 4, "patch": to_patch, "pages": []}
    latest_cards = {
        "schema_version": cards.get("schema_version", 1),
        "generated_at": None,
        "cards": {},
    }
    _write_json(latest_data / "registry.json", latest_registry)
    _write_json(latest_data / "cards.json", latest_cards)
    shutil.copytree(
        root / "static",
        latest_dist / "static",
        ignore=shutil.ignore_patterns("early-game.css"),
    )
    _write_json(latest_dist / "data/registry.json", latest_registry)
    _write_json(latest_dist / "data/cards.json", latest_cards)

    history = [dict(item) for item in existing_history if str(item.get("patch")) != from_patch]
    from_entry = next(
        (dict(item) for item in existing_history if str(item.get("patch")) == from_patch),
        {
            "patch": from_patch,
            "season": source_season,
            "url": f"{public_base_url}/patches/{from_patch}/",
        },
    )
    from_entry["status"] = "historical"
    history.append(from_entry)
    to_entry = {
        "patch": to_patch,
        "season": destination_season,
        "status": "rebuilding",
        "released_at": released_at,
        "source_url": source_url,
        "url": f"{public_base_url}/patches/{to_patch}/",
    }
    history.append(to_entry)
    previous = [item for item in history if item.get("status") == "historical"]

    _render_patch_index(
        template_path=root / "templates/index.html",
        destination=archive_dist / "index.html",
        patch=from_patch,
        season=int(from_entry.get("season", source_season)),
        status="historical",
        rebuilding=False,
        previous_patches=[item for item in previous if item.get("patch") != from_patch],
    )
    _render_patch_index(
        template_path=root / "templates/index.html",
        destination=latest_dist / "index.html",
        patch=to_patch,
        season=destination_season,
        status="rebuilding",
        rebuilding=True,
        previous_patches=previous,
    )
    _write_latest_redirect(root / "dist/index.html", f"patches/{to_patch}/")
    _write_json(
        root / "data/site.json",
        {
            "schema_version": 1,
            "latest_patch": to_patch,
            "season": destination_season,
            "public_base_url": public_base_url,
        },
    )
    _write_json(
        history_path,
        {"schema_version": 1, "latest_patch": to_patch, "patches": history},
    )

    if initial_migration:
        for source in source_content:
            source.unlink()
        shutil.rmtree(source_comps)
        for path in (root / "data/cards.json", root / "data/registry.json"):
            path.unlink()
        if (root / "dist/data").exists():
            shutil.rmtree(root / "dist/data")
    for relative in EARLY_GAME_PATHS:
        path = root / relative
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    return report


def _worktree_is_dirty(root: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="from_patch", required=True)
    parser.add_argument("--to", dest="to_patch", required=True)
    parser.add_argument("--released-at", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--season", dest="to_season", type=int, default=None)
    parser.add_argument("--public-base-url", default="https://jarvisinthemorning.github.io/tasketas")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.root.resolve() == ROOT.resolve() and _worktree_is_dirty(args.root):
        parser.error("Refusing to roll over a dirty worktree; commit or stash changes first")
    report = rollover_patch(
        root=args.root,
        from_patch=args.from_patch,
        to_patch=args.to_patch,
        released_at=args.released_at,
        source_url=args.source_url,
        public_base_url=args.public_base_url,
        to_season=args.to_season,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
