#!/usr/bin/env python3
"""
Slides → Markdown + AI Accessibility Comments → Append to Google Doc

- Extracts Markdown from a slides PDF (simple per-page heading + text via pdfminer.six)
- Asks OpenRouter (Grok-4; fallback to Claude 3.5) for comments on teaching to students with little math background
- Appends both sections to a target Google Doc with basic formatting

Usage:
  python3 operating/GoogleDocsAPI/slides_to_md_append_and_ai_comments.py \
    --pdf "/abs/path/to/GCAP3226_week3_Regression.pdf" \
    --doc-id <google_doc_id> \
    [--model x-ai/grok-4] \
    [--dry-run]

Notes:
- Markdown is basic; each page becomes a `## Slide N` with extracted text.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, List

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


def build_ai_prompt(slides_md: str) -> str:
    return f"""
You are an instructional design assistant.

Context: The following Markdown captures text extracted from Week 3 slides on regression for a policy analysis course. Many students have limited mathematics background.

Task: Write two sections in Markdown (no code fences):

### Teaching Strategy for Low-Math Background Learners
- 6–10 concrete, student-friendly tactics (use visuals, intuitive language, minimal algebra, worked examples, think-pair-share, formative checks, etc.)

### Suggested Slide-level Edits
- For up to 10 specific slides, list concise edits (e.g., redefine jargon, add step-by-step annotation, show before/after visual, replace formula with analogy). Use bullets beginning with "Slide N:".

Slides (excerpt):
---
{slides_md[:6000]}
---

Deliver only the two sections requested.
""".strip()



def auth_services():
    from googleapiclient.discovery import build
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    docs = build('docs', 'v1', credentials=creds)
    return docs
    


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Convert slides PDF to Markdown and append with AI comments to a Google Doc')
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
        slides_md = pages_to_slide_markdown(pages) if pages else "(No text extracted from PDF)"

        print("🧠 Building AI prompt…")
        prompt = build_ai_prompt(slides_md)
        ai_md = chat_with_fallback(prompt, model=args.model, fallback_model='anthropic/claude-3.5-sonnet', max_tokens=2500, temperature=0.2)

        combined_md = (
            "## Slides (Markdown Extract)\n" + slides_md + "\n\n" +
            ai_md
        )

        print("\n=== PREVIEW (first ~80 lines) ===\n")
        print("\n".join(combined_md.splitlines()[:80]))
        print("\n=== END PREVIEW ===\n")

        if args.dry_run:
            print("🔎 Dry-run: not appending to Google Doc.")
            return 0

        print("🧩 Authenticating and appending to Google Doc…")
        docs = auth_services()
        append_markdown_formatted(docs, args.doc_id, combined_md, build_replace_requests)
        print("✅ Appended slides + AI comments")
        print(f"🔗 https://docs.google.com/document/d/{args.doc_id}/edit")
        return 0
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
