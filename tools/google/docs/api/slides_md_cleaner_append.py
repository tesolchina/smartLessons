#!/usr/bin/env python3
"""
Slides Markdown Cleaner (Grok-4) → Append to Google Doc

Re-extracts Markdown from a slides PDF, asks an LLM (Grok-4 with fallback) to
normalize and structure it into clean Markdown (headings + bullets, no code
fences), and appends it to a Google Doc.

Usage:
  python3 operating/GoogleDocsAPI/slides_md_cleaner_append.py \
    --pdf "/abs/path/to/GCAP3226_week3_Regression.pdf" \
    --doc-id <google_doc_id> \
    [--model x-ai/grok-4] \
    [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / 'modules'))

from common_utils.llm import chat_with_fallback
from common_utils.pdf_utils import extract_pdf_text_per_page, pages_to_slide_markdown
from common_utils.gdocs_utils import append_markdown_formatted

# Google APIs auth and Docs helpers
THIS_DIR = Path(__file__).parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
import auth_setup  # type: ignore
from doc_roundtrip_update import build_replace_requests  # reuse renderer


def to_markdown_from_pages(pages: List[str]) -> str:
    return pages_to_slide_markdown(pages)


def build_cleanup_prompt(noisy_md: str) -> str:
    return f"""
You are a Markdown formatter for Google Docs rendering.

Task: Clean and structure the following noisy slide text into well-formed Markdown:
- Use headings only (# for deck title if present, ## for slide titles, ### for subsections).
- Convert bullets like •, ◦, –, —, o into standard "- " bullets.
- Merge broken lines and fix hyphenations; remove slide numbers/footers.
- Keep content concise; do not add new topics.
- Do NOT use code fences.

Output strictly the cleaned Markdown only.

Noisy slides markdown (excerpt up to ~8k chars):
---
{noisy_md[:8000]}
---
""".strip()


def call_llm(prompt: str, model: str) -> str:
    print("📡 Sending noisy Markdown to OpenRouter for cleanup…")
    md = chat_with_fallback(prompt, model=model, fallback_model='anthropic/claude-3.5-sonnet', max_tokens=3500, temperature=0.1)
    print("✅ Received cleaned Markdown")
    return md


def auth_docs():
    from googleapiclient.discovery import build
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    return build('docs', 'v1', credentials=creds)


def get_last_end_index(doc: dict) -> int:
    body = doc.get('body', {})
    content = body.get('content', [])
    if not content:
        return 1
    last = content[-1]
    return int(last.get('endIndex', 1))


def append_markdown(docs, doc_id: str, md: str, section_title: str) -> None:
    full_md = f"\n## {section_title}\n\n" + md.strip() + "\n"
    append_markdown_formatted(docs, doc_id, full_md, build_replace_requests)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Clean slides Markdown via Grok-4 and append to Google Doc')
    ap.add_argument('--pdf', required=True, help='Path to slides PDF')
    ap.add_argument('--doc-id', required=True, help='Target Google Doc ID')
    ap.add_argument('--model', default='x-ai/grok-4', help='OpenRouter model (e.g., x-ai/grok-4)')
    ap.add_argument('--dry-run', action='store_true', help='Preview without modifying the document')
    args = ap.parse_args(argv)

    try:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            raise RuntimeError(f"PDF not found: {pdf_path}")
        print("🔎 Extracting slides text…")
        pages = extract_pdf_text_per_page(pdf_path)
        noisy_md = to_markdown_from_pages(pages)

        print("🧠 Building cleanup prompt…")
        prompt = build_cleanup_prompt(noisy_md)
        try:
            cleaned_md = call_llm(prompt, model=args.model)
        except Exception as e:
            print(f"⚠️  Model '{args.model}' failed: {e}. Falling back to 'anthropic/claude-3.5-sonnet'.")
            cleaned_md = call_llm(prompt, model='anthropic/claude-3.5-sonnet')

        print("\n=== CLEANED MARKDOWN PREVIEW (first ~80 lines) ===\n")
        print("\n".join(cleaned_md.splitlines()[:80]))
        print("\n=== END PREVIEW ===\n")

        if args.dry_run:
            print("🔎 Dry-run: not appending to Google Doc.")
            return 0

        print("🧩 Authenticating and appending to Google Doc…")
        docs = auth_docs()
        append_markdown(docs, args.doc_id, cleaned_md, section_title='Slides (Cleaned Markdown)')
        print("✅ Appended cleaned Markdown")
        print(f"🔗 https://docs.google.com/document/d/{args.doc_id}/edit")
        return 0
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
