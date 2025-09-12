#!/usr/bin/env python3
"""Restructure repository so only two top-level folders remain: tools/ and projects/.

Usage:
  python3 restructure_repo.py --dry-run   # Show planned moves
  python3 restructure_repo.py             # Execute moves

What it does:
  * Creates tools/ (if missing) and subfolders: tools/scripts, tools/legacy
  * Moves code/tool directories (operating/, modules/) into tools/
  * Moves project/content directories (HKBUchatbot, deadline_files, paperTrail, obsidian_notes,
    synced_docs, screeningTest, screening_test) into projects/ (retaining names)
  * Moves standalone utility python scripts (e.g., gdrive_sync.py) into tools/scripts/
  * Leaves existing projects/ directory untouched
  * Skips if target already exists (prints warning)

Safe:
  * Won't overwrite existing targets
  * You can revert via git if committed

Limitations:
  * Does not update import paths yet (sys.path hacks will still find moved modules when run from repo root)
  * After verification, follow-up step should adjust imports & package-ify tools.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

TOOL_DIRS = ["operating", "modules"]
PROJECT_DIRS = [
    "HKBUchatbot",
    "deadline_files",
    "paperTrail",
    "obsidian_notes",
    "synced_docs",
    "screeningTest",
    "screening_test",
]
STANDALONE_TOOL_FILES = [
    "gdrive_sync.py",
    "email_retrieval_script.py",
    "update_paper_trail.py",
    "setup_obsidian_integration.py",
]


def plan_moves():
    moves: list[tuple[Path, Path]] = []
    tools_root = REPO_ROOT / "tools"
    scripts_root = tools_root / "scripts"

    # Tool directories
    for name in TOOL_DIRS:
        src = REPO_ROOT / name
        if src.exists():
            dest = tools_root / name
            moves.append((src, dest))

    # Project/content directories (keep inside projects/)
    proj_root = REPO_ROOT / "projects"
    for name in PROJECT_DIRS:
        src = REPO_ROOT / name
        if src.exists():
            dest = proj_root / name
            moves.append((src, dest))

    # Standalone tool scripts
    for fname in STANDALONE_TOOL_FILES:
        src = REPO_ROOT / fname
        if src.exists():
            dest = scripts_root / fname
            moves.append((src, dest))

    return moves


def execute(moves: list[tuple[Path, Path]], dry_run: bool):
    for src, dest in moves:
        if not src.exists():
            continue
        if dest.exists():
            print(f"⚠️ Skip (exists): {dest}")
            continue
        if dry_run:
            print(f"DRY-RUN: {src} -> {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
            print(f"✅ Moved {src} -> {dest}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Restructure repo into tools/ and projects/")
    ap.add_argument("--dry-run", action="store_true", help="Show planned moves only")
    args = ap.parse_args(argv)

    moves = plan_moves()
    if not moves:
        print("No moves pending. Structure may already be consolidated.")
        return 0
    execute(moves, args.dry_run)
    if args.dry_run:
        print("\nReview the above. Re-run without --dry-run to apply.")
    else:
        print("\nDone. Next: run tests / scripts from new locations, then commit & push.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
