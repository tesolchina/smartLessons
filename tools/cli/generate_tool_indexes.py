"""Generate or update tool index sections inside functional tool directories.

This script scans Python files in each functional directory under `tools/` and
injects/updates an auto-generated section (between markers) inside that
directory's `README.md` (creating one if missing).

Markers:
    <!-- AUTO_TOOL_INDEX:START -->
    ... generated content ...
    <!-- AUTO_TOOL_INDEX:END -->

Usage:
    python tools/cli/generate_tool_indexes.py            # update all
    python tools/cli/generate_tool_indexes.py --dirs google pdf      # subset
    python tools/cli/generate_tool_indexes.py --include-specialized  # include specialized tree (top-level summary only)

Generated Content:
    - Timestamp (UTC)
    - Brief instructions to re-run
    - Table of scripts (script path relative to dir, short docstring summary, run hints)
    - For packages with subpackages (e.g., google/docs/api) a nested bullet summary (future enhancement)

The script is idempotent: only the content between markers is replaced.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_ROOT = REPO_ROOT / "tools"
MARKER_START = "<!-- AUTO_TOOL_INDEX:START -->"
MARKER_END = "<!-- AUTO_TOOL_INDEX:END -->"

DEFAULT_FUNCTIONAL_DIRS = [
    "cli",
    "core",
    "documents",
    "email",
    "google",
    "openrouter",
    "pdf",
    "web",
]

SKIP_DIR_NAMES = {"__pycache__", "data", "logs", "interaction_state"}
SKIP_FILE_NAMES = {"__init__.py"}


@dataclass
class ScriptInfo:
    rel_path: Path
    module_path: str
    summary: str
    runnable: bool


def discover_scripts(base_dir: Path) -> List[ScriptInfo]:
    scripts: List[ScriptInfo] = []
    for p in base_dir.rglob("*.py"):
        if p.name in SKIP_FILE_NAMES:
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        rel = p.relative_to(base_dir)
        module_path = module_for(p)
        summary = extract_summary(p)
        runnable = has_main_guard(p)
        scripts.append(ScriptInfo(rel, module_path, summary, runnable))
    scripts.sort(key=lambda s: str(s.rel_path))
    return scripts


def module_for(path: Path) -> str:
    rel_repo = path.relative_to(REPO_ROOT).with_suffix("")
    return ".".join(rel_repo.parts)


def extract_summary(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "(unreadable)"
    doc_match = re.match(r"\s*[ur]?['\"]{3}(.+?)(['\"]{3})", text, re.DOTALL)
    if doc_match:
        first_line = doc_match.group(1).strip().splitlines()[0].strip()
        return truncate(first_line, 120)
    for line in text.splitlines():
        ls = line.strip()
        if not ls:
            continue
        if ls.startswith("#"):
            return truncate(ls.lstrip("# "), 120)
        break
    return "(no summary)"


def has_main_guard(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return "if __name__ == '__main__'" in text or "def main(" in text


def truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 3] + "..."


def build_table(scripts: List[ScriptInfo]) -> str:
    if not scripts:
        return "_No Python scripts detected._"
    header = "| Script | Summary | Run Hint |\n|--------|---------|----------|"
    rows = []
    for s in scripts:
        hint = f"python -m {s.module_path}" if s.runnable else f"import {s.module_path}"
        rows.append(f"| `{s.rel_path}` | {s.summary} | `{hint}` |")
    return "\n".join([header, *rows])


def inject_section(readme_path: Path, content: str) -> None:
    if readme_path.exists():
        original = readme_path.read_text(encoding="utf-8", errors="ignore")
    else:
        original = f"# {readme_path.parent.name}\n\n(Initial README created by tool index generator.)\n\n"
    if MARKER_START in original and MARKER_END in original:
        new_text = re.sub(
            rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
            f"{MARKER_START}\n{content}\n{MARKER_END}",
            original,
            flags=re.DOTALL,
        )
    else:
        sep = "\n" if original.endswith("\n") else "\n\n"
        new_text = original + sep + MARKER_START + "\n" + content + "\n" + MARKER_END + "\n"
    readme_path.write_text(new_text, encoding="utf-8")


def generate_for_dir(functional_dir: Path) -> bool:
    scripts = discover_scripts(functional_dir)
    timestamp = _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    rel = functional_dir.relative_to(REPO_ROOT)
    table = build_table(scripts)
    content = (
        f"Auto-generated tool index for `{rel}` (UTC {timestamp}).\n\n"
        f"Regenerate with: `python tools/cli/generate_tool_indexes.py --dirs {functional_dir.name}`\n\n"
        f"{table}\n"
    )
    inject_section(functional_dir / "README.md", content)
    return True


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate tool index READMEs.")
    p.add_argument("--dirs", nargs="*", help="Subset of functional dirs to update.")
    p.add_argument(
        "--include-specialized",
        action="store_true",
        help="Also add/update a high-level index for tools/specialized (top-level scripts only).",
    )
    return p.parse_args(list(argv) if argv is not None else None)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    dirs = args.dirs if args.dirs else DEFAULT_FUNCTIONAL_DIRS
    updated: List[str] = []
    for d in dirs:
        target = TOOLS_ROOT / d
        if not target.exists():
            print(f"[skip] {d} (not found)")
            continue
        generate_for_dir(target)
        updated.append(d)
    if args.include_specialized:
        spec = TOOLS_ROOT / "specialized"
        if spec.exists():
            scripts: List[ScriptInfo] = []
            for p in spec.glob("*.py"):
                if p.name in SKIP_FILE_NAMES:
                    continue
                scripts.append(
                    ScriptInfo(
                        rel_path=Path(p.name),
                        module_path=module_for(p),
                        summary=extract_summary(p),
                        runnable=has_main_guard(p),
                    )
                )
            timestamp = _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
            table = build_table(scripts)
            content = (
                f"Auto-generated high-level index for specialized scripts (UTC {timestamp}).\n"
                "This directory holds project-origin scripts not yet generalized.\n\n"
                f"{table}\n"
            )
            inject_section(spec / "README.md", content)
            updated.append("specialized (top-level)")
    if updated:
        print("Updated indexes:", ", ".join(updated))
    else:
        print("No directories updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
