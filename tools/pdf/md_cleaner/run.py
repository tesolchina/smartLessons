#!/usr/bin/env python3
"""
PDF → Clean Markdown pipeline

Takes a PDF, converts to Markdown, then cleans via LLM, writing `.md` and `.clean.md`.

Example:
  python3 operating/pdf_md_cleaner/run.py \
    --input "/abs/path/to/file.pdf" \
    --model anthropic/claude-3.2
"""
from __future__ import annotations

import argparse
from pathlib import Path
import time
from typing import List

# Allow imports from project modules
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / 'modules') not in sys.path:
    sys.path.insert(0, str(ROOT / 'modules'))

# Reuse existing converters/cleaners
from operating.pdf_to_markdown import convert_pdf_to_markdown
from operating.markdown_cleanup_via_llm import cleanup_markdown


def _is_newer(a: Path, b: Path) -> bool:
    try:
        return a.stat().st_mtime >= b.stat().st_mtime
    except FileNotFoundError:
        return False


def run_pipeline(pdf_path: Path, model: str, max_pages: int, chunk_chars: int, max_tokens: int, out_md: Path | None, out_clean: Path | None, force: bool = False) -> tuple[Path, Path]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    md_path = out_md if out_md else pdf_path.with_suffix('.md')
    clean_path = out_clean if out_clean else pdf_path.with_suffix('.clean.md')

    # Step 1: PDF → Markdown (skip if up-to-date and not forced)
    if not force and md_path.exists() and _is_newer(md_path, pdf_path):
        print(f"⏭️  Using existing Markdown (up-to-date): {md_path}")
        md = md_path.read_text(encoding='utf-8', errors='ignore')
    else:
        print("🔎 Converting PDF → Markdown…")
        md = convert_pdf_to_markdown(pdf_path, max_pages=max_pages)
        md_path.write_text(md, encoding='utf-8')
        print(f"✅ Wrote Markdown: {md_path}")

    # Step 2: Markdown → Clean Markdown (skip if up-to-date and not forced)
    need_clean = True
    if not force and clean_path.exists():
        # If clean is newer than both PDF and MD, skip
        newer_than_pdf = _is_newer(clean_path, pdf_path)
        newer_than_md = _is_newer(clean_path, md_path)
        if newer_than_pdf and newer_than_md:
            print(f"⏭️  Using existing cleaned Markdown (up-to-date): {clean_path}")
            need_clean = False

    if need_clean:
        print("🧹 Cleaning Markdown via LLM…")
        t0 = time.time()
        cleaned = cleanup_markdown(md, model=model, chunk_chars=chunk_chars, max_tokens=max_tokens)
        elapsed = time.time() - t0
        clean_path.write_text(cleaned, encoding='utf-8')
        print(f"✅ Wrote cleaned Markdown: {clean_path}")
        print(f"⏱️  Cleaning time: {elapsed:.1f}s (see above for usage estimate)")
    return md_path, clean_path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='PDF → Clean Markdown pipeline')
    p.add_argument('--input', required=True, help='Path to input PDF')
    p.add_argument('--model', default='anthropic/claude-3.2', help='OpenRouter model')
    p.add_argument('--max-pages', type=int, default=200, help='Max pages for pdfminer fallback')
    p.add_argument('--chunk-chars', type=int, default=6000, help='Approx max characters per chunk (split on headings)')
    p.add_argument('--max-tokens', type=int, default=1200, help='LLM max_tokens per chunk')
    p.add_argument('--output-md', help='Optional path for intermediate .md')
    p.add_argument('--output-clean', help='Optional path for final .clean.md')
    p.add_argument('--force', action='store_true', help='Rebuild outputs even if up-to-date')
    p.add_argument('--delete-raw-md', action='store_true', help='Delete the intermediate .md after successful cleaning')
    return p


def main(argv: List[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)

    pdf_path = Path(args.input)
    out_md = Path(args.output_md) if args.output_md else None
    out_clean = Path(args.output_clean) if args.output_clean else None

    try:
        md_path, clean_path = run_pipeline(pdf_path, args.model, args.max_pages, args.chunk_chars, args.max_tokens, out_md, out_clean, force=args.force)
        if args.delete_raw_md and md_path.exists():
            try:
                # Only delete if cleaned file exists (successful cleaning)
                if clean_path.exists():
                    md_path.unlink()
                    print(f"🗑️  Deleted intermediate Markdown: {md_path}")
            except Exception as e:
                print(f"⚠️  Could not delete intermediate Markdown: {e}")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
