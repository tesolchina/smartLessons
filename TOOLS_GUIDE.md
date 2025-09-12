# DailyAssistant Tools Guide

Authoritative guide for discovering, installing, and invoking automation tools in this repository.

## 1. Layout
```
repo/
  tools/
    cli/           # CLI utilities, index generators, orchestration helpers
    core/          # Shared utilities and abstractions (paths, IO, helpers)
    documents/     # Legacy/transition document manipulation scripts
    email/         # Email automation (ingestion, drafting, templating)
    google/        # Google API related scripts (Drive, Docs, Slides, etc.)
    openrouter/    # OpenRouter / LLM integration helpers
    pdf/           # PDF parsing, cleaning, conversion
    web/           # Web / crawling / scraping utilities
    specialized/   # Project-origin scripts pending generalization
  projects/        # Project-specific working directories (each with README)
```

## 2. Installation Options
Choose one approach based on your need:

| Scenario | Command |
|----------|---------|
| Use latest main (no clone) | `pip install git+https://github.com/tesolchina/DailyAssistant.git` |
| Pin to tag/commit | `pip install git+https://github.com/tesolchina/DailyAssistant.git@<tag_or_commit>` |
| Editable dev install | `git clone https://github.com/tesolchina/DailyAssistant.git && cd DailyAssistant && pip install -e .` |
| Ad-hoc without install | `PYTHONPATH=$(pwd) python tools/cli/toolbox_cli.py --help` |

After install you can import: `import dailyassistant`.

## 3. Discovery (Indexes)
- Tool indexes: run `python tools/cli/generate_tool_indexes.py` to refresh README tables inside each functional directory.
- Project indexes: run `python tools/cli/generate_project_indexes.py` to refresh per-project README inventories (includes tool access block).
- Each generated block is delimited by markers (`<!-- AUTO_TOOL_INDEX:START -->`). Safe to add custom text outside markers.

## 4. Invocation Modes
| Mode | Example |
|------|---------|
| Direct script | `python tools/email/send_digest.py` |
| Module path | `python -m tools.email.send_digest` |
| Package module (after install) | `python -m dailyassistant.email.send_digest` |
| CLI (planned) | `da email digest --date today` |
| Programmatic | `from dailyassistant.email import send_digest` |

## 5. Path Detection Snippet
```python
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR if (PROJECT_DIR / 'tools').exists() else PROJECT_DIR.parent
TOOLS_DIR = REPO_ROOT / 'tools'
```

## 6. Environment Variables (Optional)
| Variable | Purpose | Example |
|----------|---------|---------|
| DAILYASSISTANT_ROOT | Force explicit repo root resolution | `export DAILYASSISTANT_ROOT=/path/to/DailyAssistant` |
| DAILYASSISTANT_LOG_LEVEL | Adjust logging verbosity (future) | `export DAILYASSISTANT_LOG_LEVEL=INFO` |

## 7. Generalization Workflow
1. Prototype script lives in `projects/<proj>/...`
2. Promote to `tools/specialized/` if reused across >1 project
3. Refactor & move into a functional directory (e.g., `tools/google/`) with docstring + README entry
4. Add tests/examples (future step) and re-run index generator

## 8. Regenerating Documentation
```bash
python tools/cli/generate_tool_indexes.py --include-specialized
python tools/cli/generate_project_indexes.py
```

## 9. Future CLI (Planned)
Planned `da` subcommands (subject to pyproject entry point definition):
- `da index tools` (tool indexes)
- `da index projects`
- `da email ingest`
- `da google sync`

## 10. Safety / Idempotence
- Generators only replace content between markers; manual edits elsewhere are preserved.
- Safe to run repeatedly (used for CI freshness checks later).

## 11. Troubleshooting
| Issue | Symptom | Fix |
|-------|---------|-----|
| ImportError after move | Old path `operating.*` fails | Use new path `tools.documents.*` (shim exists short-term) |
| Stale README tables | Missing new script | Re-run generators (section 8) |
| Module not found when running in project subfolder | Relative imports fail | Export `PYTHONPATH` to repo root or install editable |

## 12. Minimal Example
```bash
git clone https://github.com/tesolchina/DailyAssistant.git
cd DailyAssistant
pip install -e .
python tools/cli/generate_tool_indexes.py
python -m dailyassistant.cli.generate_project_indexes
```

## 13. Support
Open an issue or inspect docstrings in each functional directory. Auto-indexes summarize entry points.

---
Generated manually (not auto-overwritten). Keep this file updated when structure changes.
