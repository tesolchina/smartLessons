"""
Build the prompt context to send to Grok, pulling from the current workspace.

It collects:
- MASTER_Citation_Guide.md (current guide)
- RAG_Annotated_Manuscript.md (from archive)
- RAG_Citation_Summary.md (from archive)
- manuscript_0902.md (markdown manuscript, from archive)

It trims each file to an approximate token budget using simple heuristics
(~4 chars/token). You can adjust limits via constants below.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple
import os

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "archive"

# Approximate character budgets per section
GUIDE_CHAR_LIMIT = 40_000
ANNOTATED_CHAR_LIMIT = 30_000
SUMMARY_CHAR_LIMIT = 12_000
MANUSCRIPT_CHAR_LIMIT = 60_000

# RAG sources (literature) inclusion from ZoteroPDF/LitonGoalChatbot
_rag_env = os.getenv("RAG_SOURCES_DIR")
# Default to DailyAssistant/projects/ZoteroPDF/LitonGoalChatbot
RAG_DIR_DEFAULT = (
    Path(_rag_env)
    if _rag_env
    else (ROOT.parents[2] / "ZoteroPDF" / "LitonGoalChatbot")
)
RAG_MAX_SOURCES = int(os.getenv("RAG_MAX_SOURCES", "12"))
RAG_SOURCE_CHAR_LIMIT = int(os.getenv("RAG_SOURCE_CHAR_LIMIT", "8000"))
RAG_FILENAME_KEYWORDS = [
    s.strip().lower()
    for s in os.getenv(
        "RAG_FILENAME_KEYWORDS",
        "goal, goals, SRL, self-regulated, chatbot, chatbots, SMART, TAM, usefulness, ease of use, proximal",
    ).split(",")
]


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def trim_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    head = text[: limit // 2]
    tail = text[-limit // 2 :]
    return f"{head}\n\n…\n\n{tail}"


def build_context() -> List[Tuple[str, str]]:
    """Return a list of (title, content) chunks to embed in the system/user prompt."""
    chunks: List[Tuple[str, str]] = []

    guide = ROOT / "MASTER_Citation_Guide.md"
    annotated = ARCHIVE / "RAG_Annotated_Manuscript.md"
    summary = ARCHIVE / "RAG_Citation_Summary.md"
    manuscript = ARCHIVE / "manuscript_0902.md"

    if guide.exists():
        chunks.append(("MASTER_Citation_Guide.md", trim_text(read_text_safe(guide), GUIDE_CHAR_LIMIT)))
    if annotated.exists():
        chunks.append(("RAG_Annotated_Manuscript.md", trim_text(read_text_safe(annotated), ANNOTATED_CHAR_LIMIT)))
    if summary.exists():
        chunks.append(("RAG_Citation_Summary.md", trim_text(read_text_safe(summary), SUMMARY_CHAR_LIMIT)))
    if manuscript.exists():
        chunks.append(("manuscript_0902.md", trim_text(read_text_safe(manuscript), MANUSCRIPT_CHAR_LIMIT)))

    # Add selected RAG sources (.md files) from the literature folder
    try:
        rag_dir = RAG_DIR_DEFAULT
        if rag_dir.exists() and rag_dir.is_dir():
            md_files = sorted([p for p in rag_dir.glob("**/*.md")])
            # Simple relevance: prioritize filenames with any keyword
            def score(p: Path) -> int:
                name = p.name.lower()
                return sum(1 for kw in RAG_FILENAME_KEYWORDS if kw and kw in name)

            ranked = sorted(md_files, key=score, reverse=True)
            selected = ranked[:RAG_MAX_SOURCES]
            for p in selected:
                chunks.append((f"RAG:{p.name}", trim_text(read_text_safe(p), RAG_SOURCE_CHAR_LIMIT)))
    except Exception:
        pass

    return chunks


def render_context_as_prompt(chunks: List[Tuple[str, str]]) -> str:
    """Render context chunks into a single string for the system prompt."""
    parts: List[str] = [
        "You are acting as a meticulous, citation-aware manuscript editor.",
        "Use the following project files to propose improved citation placements, cross-section echoes, and a refined v2 of the MASTER_Citation_Guide.",
        "Keep outputs concise and actionable with Before/After blocks and section anchors.",
        "--- CONTEXT START ---",
    ]
    for title, content in chunks:
        parts.append(f"\n<<<FILE {title}>>>\n{content}\n<<<END {title}>>>\n")
    parts.append("--- CONTEXT END ---")
    return "\n".join(parts)


if __name__ == "__main__":
    ctx = render_context_as_prompt(build_context())
    print(f"Built context ({len(ctx)} chars)")
