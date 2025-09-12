#!/usr/bin/env python3
"""
PDF → Markdown converter (generic)

Prefers PyMuPDF (markdown extraction). Falls back to pdfminer.six (plain text
framed as pages). Produces a .md file for downstream use.

Usage:
  python3 operating/pdf_to_markdown.py \
    --input "/abs/path/to/file.pdf" \
    [--output "/abs/path/to/output.md"] \
    [--max-pages 200]
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List


def extract_markdown_pymupdf(pdf_path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except Exception as e:
        raise RuntimeError("PyMuPDF not available")
    doc = fitz.open(str(pdf_path))
    parts: List[str] = []
    for i, page in enumerate(doc, 1):
        md = page.get_text("markdown") or ""
        if md.strip():
            parts.append(f"## Page {i}\n\n{md.strip()}\n")
    doc.close()
    return "\n".join(parts).strip()


def extract_markdown_pdfminer(pdf_path: Path, max_pages: int) -> str:
    from pdfminer.high_level import extract_text
    parts: List[str] = []
    for i in range(max_pages):
        try:
            text = extract_text(str(pdf_path), page_numbers=[i])
        except Exception:
            break
        if not text or not text.strip():
            if i == 0:
                break
            else:
                break
        parts.append(f"## Page {i+1}\n\n{text.strip()}\n")
    if not parts:
        all_text = extract_text(str(pdf_path)) or ''
        if all_text.strip():
            parts.append(f"## Full Document\n\n{all_text.strip()}\n")
    return "\n".join(parts).strip()


def convert_pdf_to_markdown(pdf_path: Path, max_pages: int = 200) -> str:
    try:
        return extract_markdown_pymupdf(pdf_path)
    except Exception:
        return extract_markdown_pdfminer(pdf_path, max_pages=max_pages)


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Convert a PDF to Markdown')
    ap.add_argument('--input', required=True, help='Path to PDF file')
    ap.add_argument('--output', help='Path to output .md (default: alongside input)')
    ap.add_argument('--max-pages', type=int, default=200, help='Max pages to scan with pdfminer fallback')
    args = ap.parse_args(argv)

    pdf_path = Path(args.input)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return 1
    out_path = Path(args.output) if args.output else pdf_path.with_suffix('.md')

    print("🔎 Converting PDF → Markdown…")
    md = convert_pdf_to_markdown(pdf_path, max_pages=args.max_pages)
    out_path.write_text(md, encoding='utf-8')
    print(f"✅ Wrote Markdown: {out_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
