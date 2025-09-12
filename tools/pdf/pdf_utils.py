from __future__ import annotations

from pathlib import Path
from typing import List
import re


def extract_pdf_text_per_page(pdf_path: Path, max_pages: int = 200) -> List[str]:
    from pdfminer.high_level import extract_text
    pages: List[str] = []
    for i in range(0, max_pages):
        try:
            txt = extract_text(str(pdf_path), page_numbers=[i])
        except Exception:
            break
        if not txt or not txt.strip():
            if i == 0:
                break
            break
        pages.append(txt)
    if not pages:
        all_text = extract_text(str(pdf_path)) or ''
        return [all_text]
    return pages


def pages_to_slide_markdown(pages: List[str]) -> str:
    parts: List[str] = []
    for idx, raw in enumerate(pages, 1):
        text = raw.replace('\r', '')
        lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
        lines = [ln for ln in lines if ln]
        parts.append(f"## Slide {idx}\n" + "\n".join(lines))
    return "\n\n".join(parts).strip()
