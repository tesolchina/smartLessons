from pathlib import Path
import sys
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent / "projects" / "ZoteroPDF"
APP_PATH = PROJECT_ROOT / "app.py"

sys.path.append(str(PROJECT_ROOT))

# Import citation helpers by reading and executing minimal subset from app
# Safer alternative: refactor helpers into separate module; for now replicate logic.
from scripts.index import AcademicIndexer  # noqa: E402


def format_citations(results: List[Dict[str, Any]], style: str = "simple") -> str:
    lines = []
    for r in results:
        meta = r["document"]["metadata"]
        authors = meta.get("authors") or []
        year = meta.get("publication_year") or meta.get("year") or "n.d."
        title = meta.get("title") or r.get("title") or r['filename']
        if authors:
            if len(authors) > 2:
                auth_str = f"{authors[0]} et al."
            else:
                auth_str = ", ".join(authors)
        else:
            auth_str = "Unknown"
        lines.append(f"{auth_str} ({year}). {title}.")
    return "\n".join(lines)


def test_citation_formatter_handles_missing():
    dummy = [{
        "filename": "x.md",
        "title": "Fallback Title",
        "score": 0.9,
        "document": {"metadata": {}, "content": "", "filename": "x.md"}
    }]
    block = format_citations(dummy)
    assert "Unknown" in block
    assert "Fallback Title" in block
