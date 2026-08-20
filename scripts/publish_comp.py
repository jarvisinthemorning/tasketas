#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comp_pipeline import (
    CompError,
    _parse_markdown,
    build_index,
    publish_comp,
    validate_patch_name,
)


def resolve_patch_layout(root: Path, base_url: str | None = None) -> dict:
    site_path = root / "data/site.json"
    with site_path.open(encoding="utf-8") as handle:
        site = json.load(handle)
    patch = validate_patch_name(site["latest_patch"])
    site_base = (base_url or site["public_base_url"]).rstrip("/")
    return {
        "patch": patch,
        "season": int(site["season"]),
        "content_dir": root / "content/patches" / patch,
        "cards_path": root / "data/patches" / patch / "cards.json",
        "registry_path": root / "data/patches" / patch / "registry.json",
        "output_dir": root / "dist/patches" / patch,
        "public_base_url": f"{site_base}/patches/{patch}",
    }


def _previous_patches(root: Path, latest_patch: str) -> list[dict]:
    path = root / "data/patches.json"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return [item for item in payload.get("patches", []) if str(item.get("patch")) != latest_patch]


def _replace_tree(source: Path, destination: Path) -> None:
    temporary = destination.with_name(destination.name + ".new")
    backup = destination.with_name(destination.name + ".old")
    for path in (temporary, backup):
        if path.exists():
            shutil.rmtree(path)
    shutil.copytree(source, temporary, ignore=shutil.ignore_patterns("early-game.css"))
    try:
        if destination.exists():
            destination.rename(backup)
        temporary.rename(destination)
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        if backup.exists():
            backup.rename(destination)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


def run_git_publish(root: Path, slug: str, paths: list[Path]) -> None:
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root).returncode != 0:
        raise RuntimeError("Refusing to publish with pre-existing staged changes")
    relative_paths = [str(path.resolve().relative_to(root.resolve())) for path in paths]
    subprocess.run(["git", "add", "--", *relative_paths], cwd=root, check=True)
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--"], cwd=root, text=True
    ).splitlines()
    allowed_files = {path for path in relative_paths if not (root / path).is_dir()}
    allowed_dirs = [path.rstrip("/") + "/" for path in relative_paths if (root / path).is_dir()]
    unexpected = [
        path for path in staged
        if path not in allowed_files and not any(path.startswith(prefix) for prefix in allowed_dirs)
    ]
    if unexpected:
        subprocess.run(["git", "reset"], cwd=root, check=True)
        raise RuntimeError(f"Refusing to publish unexpected staged paths: {unexpected}")
    subprocess.run(["git", "commit", "-m", f"Publish comp: {slug}"], cwd=root, check=True)
    subprocess.run(["git", "push"], cwd=root, check=True)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build and optionally publish one Battlegrounds comp guide")
    parser.add_argument("content", type=Path)
    parser.add_argument("--base-url", default=None, help="Override the site root URL; the patch path is appended")
    parser.add_argument("--update", action="store_true", help="Replace the existing registry entry for this source")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preview", action="store_true", help="Build locally without writing to the published registry")
    mode.add_argument("--push", action="store_true", help="Commit generated files and push the configured Git remote")
    args = parser.parse_args()
    if args.preview and args.update:
        parser.error("--preview and --update cannot be combined")
    layout = resolve_patch_layout(root, args.base_url)
    content_path = args.content.resolve()
    try:
        content_path.relative_to(layout["content_dir"].resolve())
    except ValueError:
        print(
            f"Error: active guides must live under {layout['content_dir']}",
            file=sys.stderr,
        )
        return 2

    try:
        result = publish_comp(
            content_path=content_path,
            cards_path=layout["cards_path"],
            registry_path=layout["registry_path"],
            template_path=root / "templates/comp.html",
            output_dir=layout["output_dir"],
            public_base_url=layout["public_base_url"],
            register=not args.preview,
            update=args.update,
            expected_patch=layout["patch"],
            project_root=root,
        )
        build_index(
            registry_path=layout["registry_path"],
            cards_path=layout["cards_path"],
            template_path=root / "templates/index.html",
            output_dir=layout["output_dir"],
            patch=layout["patch"],
            season=layout["season"],
            status="current",
            rebuilding=False,
            previous_patches=_previous_patches(root, layout["patch"]),
        )
    except (CompError, ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    _replace_tree(root / "static", layout["output_dir"] / "static")

    if args.push:
        metadata, _ = _parse_markdown(content_path)
        board_paths = [
            root / str(example["image"]).removeprefix("/")
            for example in metadata.get("board_examples", []) or []
        ]
        run_git_publish(
            root,
            result["slug"],
            [content_path, layout["registry_path"], layout["output_dir"], *board_paths],
        )
    print(result["url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
