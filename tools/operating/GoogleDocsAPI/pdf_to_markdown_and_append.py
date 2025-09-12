#!/usr/bin/env python3
"""
PDF → Markdown → Google Doc appender with Accessibility Comments

- Extracts readable text from a PDF (slides) using pdfminer.six
- Converts to a clean Markdown outline
- Appends it to the specified Google Doc
- Calls OpenRouter (Grok-4 preferred; fallback to Claude 3.5 Sonnet) to
  generate teaching comments for students with limited math background,
  and appends those comments under a dedicated heading.

Usage:
  python3 operating/GoogleDocsAPI/pdf_to_markdown_and_append.py \
    --pdf "/abs/path/to/GCAP3226_week3_Regression.pdf" \
    --doc-id <google_doc_id> \
    [--model x-ai/grok-4] \
    [--add-comments]

Notes:
- Requires Google API credentials configured in this folder.
- Uses doc_roundtrip_update.build_replace_requests for Markdown rendering.
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / 'modules'))

THIS_DIR = Path(__file__).parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

import auth_setup  # type: ignore
from doc_roundtrip_update import build_replace_requests

# OpenRouter
try:
    from openRouterAI.client import post_chat_completions
    from openRouterAI.env import get_openrouter_api_key
    OPENROUTER_AVAILABLE = True
except Exception as e:
    print(f"⚠️  OpenRouter module not available: {e}")
    OPENROUTER_AVAILABLE = False

# PDF
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


def auth_services():
    from googleapiclient.discovery import build
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    docs = build('docs', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)
    return docs, drive


def pdf_to_text(pdf_path: Path) -> str:
    output = io.StringIO()
    with pdf_path.open('rb') as f:
        extract_text_to_fp(f, output, laparams=LAParams(), output_type='text', codec=None)
    return output.getvalue()


def text_to_markdown_outline(text: str, max_chars: int = 40000) -> str:
    # Very simple heuristic: split pages by form-feed and lines, create bullets for non-empty lines
    # and try to elevate lines that look like titles.
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... (truncated)"
    pages = text.split('\f')
    md_lines: List[str] = ["## Slides (extracted)"]
    for p_i, page in enumerate(pages, 1):
        lines = [ln.strip() for ln in page.splitlines()]
        # Remove obvious empties
        lines = [ln for ln in lines if ln]
        if not lines:
            continue
        # First non-empty as page heading if short; else keep as bullet
        first = lines[0]
        if 0 < len(first) <= 80:
            md_lines.append(f"### Page {p_i}: {first}")
            rest = lines[1:]
        else:
            md_lines.append(f"### Page {p_i}")
            rest = lines
        for ln in rest[:40]:  # cap per-page lines
            md_lines.append(f"- {ln}")
    return "\n".join(md_lines)


def call_llm_for_accessibility(slides_md: str, model: str) -> str:
    if not OPENROUTER_AVAILABLE:
        raise RuntimeError("OpenRouter client not available")
    if not get_openrouter_api_key():
        raise RuntimeError("Missing OPENROUTER_API_KEY")
    prompt = f"""
You are an instructional designer helping teach regression to students with limited math background.
Given the slide outline below, produce:

## Teaching Comments for Low-Math-Background Students
- 6–10 bullet points explaining how to simplify, scaffold, and make the session accessible
- Include concrete examples, metaphors, and checks for understanding
- Suggest what to skip or move to optional reading
- Avoid equations in the comments; focus on intuition and activities

SLIDES (Markdown):
---
{slides_md[:30000]}
---

Deliver only the heading and the bullets in Markdown (no code fences).
""".strip()
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1600,
        'temperature': 0.2,
    }
    print("📡 Requesting Grok-4 accessibility comments…")
    resp = post_chat_completions(payload)
    content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    if not content:
        raise RuntimeError('Empty response from LLM')
    return content


def append_markdown(docs, document_id: str, md: str) -> None:
    # Append at end by inserting at last index
    doc = docs.documents().get(documentId=document_id).execute()
    end_index = int(doc.get('body', {}).get('content', [])[-1].get('endIndex', 1)) if doc.get('body', {}).get('content') else 1
    reqs = build_replace_requests(md, initial_index=end_index - 1)
    CHUNK = 100
    for i in range(0, len(reqs), CHUNK):
        batch = reqs[i:i+CHUNK]
        docs.documents().batchUpdate(documentId=document_id, body={'requests': batch}).execute()


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Append PDF slides as Markdown to a Google Doc and add Grok-4 teaching comments')
    ap.add_argument('--pdf', required=True, help='Path to the slides PDF')
    ap.add_argument('--doc-id', required=True, help='Target Google Doc ID')
    ap.add_argument('--model', default='x-ai/grok-4', help='OpenRouter model to use (default: x-ai/grok-4)')
    ap.add_argument('--add-comments', action='store_true', help='Also request Grok-4 teaching comments and append them')
    args = ap.parse_args(argv)

    try:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            raise RuntimeError(f"PDF not found: {pdf_path}")

        print("📄 Extracting PDF text…")
        text = pdf_to_text(pdf_path)
        print(f"✅ Extracted {len(text):,} characters from PDF")

        print("📝 Converting to Markdown outline…")
        slides_md = text_to_markdown_outline(text)

        print("🧩 Authenticating Google APIs…")
        docs, _ = auth_services()

        print("📎 Appending slides Markdown to Google Doc…")
        append_markdown(docs, args.doc_id, slides_md)

        if args.add_comments:
            try:
                comments_md = call_llm_for_accessibility(slides_md, model=args.model)
            except Exception as e:
                print(f"⚠️  Grok-4 failed: {e}. Falling back to 'anthropic/claude-3.5-sonnet'.")
                comments_md = call_llm_for_accessibility(slides_md, model='anthropic/claude-3.5-sonnet')

            print("📎 Appending accessibility comments…")
            append_markdown(docs, args.doc_id, "\n" + comments_md)

        print("✅ Done. Check your Google Doc.")
        return 0
    except Exception as e:
        print(f"❌ Operation failed: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
