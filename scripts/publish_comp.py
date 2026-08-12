#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comp_pipeline import CompError, build_index, publish_comp


def run_git_publish(root: Path, slug: str) -> None:
    commands = [
        ["git", "add", "content", "data/cards.json", "data/registry.json", "dist", "scripts", "static", "templates", "tests"],
        ["git", "commit", "-m", f"Publish comp: {slug}"],
        ["git", "push"],
    ]
    for command in commands:
        subprocess.run(command, cwd=root, check=True)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build and optionally publish one Battlegrounds comp guide")
    parser.add_argument("content", type=Path)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--preview", action="store_true", help="Build locally without writing to the published registry")
    parser.add_argument("--update", action="store_true", help="Replace the existing registry entry for this source")
    parser.add_argument("--push", action="store_true", help="Commit generated files and push the configured Git remote")
    args = parser.parse_args()

    try:
        result = publish_comp(
            content_path=args.content.resolve(),
            cards_path=root / "data/cards.json",
            registry_path=root / "data/registry.json",
            template_path=root / "templates/comp.html",
            output_dir=root / "dist",
            public_base_url=args.base_url,
            register=not args.preview,
            update=args.update,
        )
        build_index(
            registry_path=root / "data/registry.json",
            cards_path=root / "data/cards.json",
            template_path=root / "templates/index.html",
            output_dir=root / "dist",
        )
        from build_early_game import build as build_early_game

        build_early_game(
            root / "data/cards.json",
            root / "templates/early-game.html",
            root / "dist/early-game.html",
        )
    except (CompError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    static_source = root / "static"
    static_destination = root / "dist/static"
    if static_destination.exists():
        shutil.rmtree(static_destination)
    shutil.copytree(static_source, static_destination)

    if args.push:
        run_git_publish(root, result["slug"])
    print(result["url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
