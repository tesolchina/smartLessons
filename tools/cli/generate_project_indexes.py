"""Generate or update README indexes for each directory under `projects/`.

For each immediate subdirectory of `projects/`, this script creates/updates a README.md
containing a generated section (between markers) listing Markdown / data / other assets.

Markers:
    <!-- AUTO_PROJECT_INDEX:START --> ... <!-- AUTO_PROJECT_INDEX:END -->

Listed items:
    - Markdown files (.md)
    - Python files (note: main code has been migrated; remaining should be docs or data)
    - Other notable assets (csv, pdf, html)

Usage:
    python tools/cli/generate_project_indexes.py              # all projects
    python tools/cli/generate_project_indexes.py --dirs GCAP3226 screening_test

Idempotent: only the generated block is replaced.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
from pathlib import Path
import re
from typing import Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECTS_ROOT = REPO_ROOT / "projects"
MARKER_START = "<!-- AUTO_PROJECT_INDEX:START -->"
MARKER_END = "<!-- AUTO_PROJECT_INDEX:END -->"

INCLUDE_EXTS = {".md", ".py", ".csv", ".pdf", ".html", ".txt"}
MAX_FILES_PER_SECTION = 500


def collect_files(project_dir: Path) -> List[Path]:
    files: List[Path] = []
    for p in project_dir.rglob('*'):
        if p.is_file() and p.suffix.lower() in INCLUDE_EXTS:
            # keep path relative to project dir
            try:
                files.append(p.relative_to(project_dir))
            except ValueError:
                continue
    files.sort(key=lambda x: (x.parts[0] if len(x.parts) > 0 else '', str(x)))
    return files[:MAX_FILES_PER_SECTION]


def build_table(files: List[Path]) -> str:
    if not files:
        return "_No tracked content files (md/py/csv/pdf/html/txt) found._"
    header = "| File | Type | Size (bytes) |"
    sep = "|------|------|-------------|"
    rows = [header, sep]
    for rel in files:
        abs_path = rel
        # will compute size after reconstructing absolute
        size = (PROJECTS_ROOT / current_project / rel).stat().st_size if 'current_project' in globals() else 0
        rows.append(f"| `{rel}` | {rel.suffix or '(none)'} | {size} |")
    return "\n".join(rows)


def inject(readme: Path, content: str) -> None:
    if readme.exists():
        original = readme.read_text(encoding='utf-8', errors='ignore')
    else:
        original = f"# {readme.parent.name}\n\n(Initial project README created by index generator)\n\n"
    if MARKER_START in original and MARKER_END in original:
        pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)
        new_text = pattern.sub(f"{MARKER_START}\n{content}\n{MARKER_END}", original)
    else:
        sep = "\n" if original.endswith('\n') else '\n\n'
        new_text = original + sep + MARKER_START + "\n" + content + "\n" + MARKER_END + "\n"
    readme.write_text(new_text, encoding='utf-8')


def process_project(name: str) -> bool:
    global current_project
    current_project = name  # used in build_table size calc
    pdir = PROJECTS_ROOT / name
    if not pdir.is_dir():
        return False
    files = collect_files(pdir)
    timestamp = _dt.datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    table = build_table(files)
    abs_tools_path = (REPO_ROOT / 'tools').as_posix()
    content = (
    f"Auto-generated index for project `{name}` at {timestamp} UTC.\n"
    "<!-- DAILYASSISTANT_TOOLS_PATH=../tools -->\n"
    "Regenerate with: `python tools/cli/generate_project_indexes.py --dirs " + name + "`\n\n"
    "## Tool Access\n"
    "- Tools directory (relative): `../tools` (packaged import: `import dailyassistant` after editable install)\n"
        f"- Tools directory (absolute at generation time): `{abs_tools_path}`\n"
    "- Root quick start: see `../README.md` and `../QUICK_START_GUIDE.md`\n"
    "- CLI (if installed): run `da --help` or regenerate indexes with `da index projects` (future)\n"
    "- Environment variable (optional): `export DAILYASSISTANT_ROOT=\u0060git rev-parse --show-toplevel\u0060`\n"
        "\n### Install & Use\n"
        "1. Editable install (recommended while developing):\n"
        f"   ````bash\n   pip install -e {REPO_ROOT.as_posix()}\n   ````\n"
        "2. Run a tool script directly (without install):\n"
        f"   ````bash\n   python {abs_tools_path}/cli/generate_tool_indexes.py\n   ````\n"
        "3. Via package module after install:\n"
        "   ````bash\n   python -m dailyassistant.cli.generate_tool_indexes\n   ````\n"
        "4. Via CLI (if entry point installed):\n"
        "   ````bash\n   da tool-index\n   ````\n"
        "5. Ad-hoc PYTHONPATH (no install):\n"
        f"   ````bash\n   PYTHONPATH={REPO_ROOT.as_posix()} python {abs_tools_path}/cli/generate_project_indexes.py --dirs {name}\n   ````\n"
        "\n### Programmatic Path Detection\n"
    "- Programmatic path detection snippet:\n\n"
    "```python\nfrom pathlib import Path\nPROJECT_DIR = Path(__file__).resolve().parent\nREPO_ROOT = PROJECT_DIR.parent  # contains 'tools' and 'projects'\nTOOLS_DIR = REPO_ROOT / 'tools'\n```\n\n"
    f"{table}\n"
    )
    inject(pdir / 'README.md', content)
    return True


def parse_args(argv: Optional[Iterable[str]] = None):
    ap = argparse.ArgumentParser(description='Generate project directory indexes')
    ap.add_argument('--dirs', nargs='*', help='Specific project dirs to update')
    return ap.parse_args(list(argv) if argv is not None else None)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    if not PROJECTS_ROOT.exists():
        print('No projects/ directory found.')
        return 0
    targets = args.dirs if args.dirs else [d.name for d in PROJECTS_ROOT.iterdir() if d.is_dir()]
    updated = []
    for name in targets:
        if process_project(name):
            updated.append(name)
        else:
            print(f"[skip] {name}")
    if updated:
        print('Updated project indexes:', ', '.join(updated))
    else:
        print('No project indexes updated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
