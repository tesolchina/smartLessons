#!/usr/bin/env python3
"""
Week 3 Materials Reviewer & Outline Generator

Reads local Week2/Week3 course materials, summarizes context, sends to an LLM
for a structured Week 3 outline and reviewer comments, and writes the result
to a new Google Doc in the target Drive folder.

Defaults:
- Model: xai/grok-2-latest (fallback to anthropic/claude-3.5-sonnet on error)
- Week 2 path: projects/GCAP3226/course_materials/Week2
- Week 3 path: projects/GCAP3226/course_materials/Week3
- Target folder: uses the same folder ID previously used for assignments

Usage:
  python3 operating/GoogleDocsAPI/week3_materials_review.py \
    [--week2 "/abs/path/to/Week2"] \
    [--week3 "/abs/path/to/Week3"] \
    [--folder-id <drive_folder_id>] \
    [--title "Week 3 Materials Review and Outline"] \
    [--model xai/grok-2-latest] \
    [--dry-run]

Notes:
- We only read lightweight previews (Week2 markdowns, Week3 CSV header/sample, notebook headings, PDF filenames).
- Output is rendered to Google Docs with basic formatting via existing helper.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / 'modules'))

# OpenRouter client
try:
    from openRouterAI.client import post_chat_completions
    from openRouterAI.env import get_openrouter_api_key
    OPENROUTER_AVAILABLE = True
except Exception as e:
    print(f"⚠️  OpenRouter module not available: {e}")
    OPENROUTER_AVAILABLE = False

# Google APIs auth and Docs helpers
THIS_DIR = Path(__file__).parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
import auth_setup  # type: ignore
from doc_roundtrip_update import build_replace_requests  # reuse renderer


DEFAULT_WEEK2 = REPO_ROOT / 'projects' / 'GCAP3226' / 'course_materials' / 'Week2'
DEFAULT_WEEK3 = REPO_ROOT / 'projects' / 'GCAP3226' / 'course_materials' / 'Week3'
DEFAULT_FOLDER_ID = '1XgV9YSG6vUI8YInABHr3IUV1v9B3pLon'  # Assumed same folder as assignments


def auth_services():
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        raise RuntimeError(f"Google API libraries not available: {e}")
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    docs = build('docs', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)
    return docs, drive


def safe_read_text(p: Path, max_chars: int = 12000) -> str:
    try:
        text = p.read_text(encoding='utf-8')
        if len(text) > max_chars:
            return text[:max_chars] + "\n... (truncated)"
        return text
    except Exception:
        return ''


def summarize_week2(week2_dir: Path) -> Dict[str, Any]:
    md_guide = safe_read_text(week2_dir / 'Week2_Materials_Guide.md')
    md_slides = safe_read_text(week2_dir / 'Week2_Lecture_Slides.md')
    notebooks = [p.name for p in week2_dir.glob('*.ipynb')]
    csvs = [p.name for p in week2_dir.glob('*.csv')]
    summary = {
        'guide_md': md_guide,
        'slides_md': md_slides,
        'notebooks': notebooks,
        'csvs': csvs,
    }
    return summary


def preview_csv(csv_path: Path, max_rows: int = 5) -> Dict[str, Any]:
    if not csv_path.exists():
        return {}
    try:
        with csv_path.open('r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = []
            for i, row in enumerate(reader):
                rows.append(row)
                if i >= max_rows:
                    break
        header = rows[0] if rows else []
        sample = rows[1:] if len(rows) > 1 else []
        return {'path': str(csv_path), 'header': header, 'sample': sample}
    except Exception:
        return {'path': str(csv_path), 'error': 'failed_to_read'}


def extract_notebook_outline(ipynb_path: Path, max_cells: int = 40) -> Dict[str, Any]:
    if not ipynb_path.exists():
        return {}
    try:
        nb = json.loads(ipynb_path.read_text(encoding='utf-8'))
        cells = nb.get('cells', [])
        outline: List[str] = []
        for c in cells[:max_cells]:
            ctype = c.get('cell_type')
            src_lines = c.get('source', [])
            if not src_lines:
                continue
            text = ''.join(src_lines).strip()
            if ctype == 'markdown':
                # Keep headings & first 120 chars
                for line in text.splitlines():
                    if line.strip().startswith(('#', '##', '###')):
                        outline.append(line.strip())
                        break
                else:
                    outline.append(text[:120])
            elif ctype == 'code':
                # Extract leading comment or function signature
                first_line = text.splitlines()[0]
                outline.append(f"[code] {first_line[:140]}")
        return {'path': str(ipynb_path), 'outline': outline}
    except Exception:
        return {'path': str(ipynb_path), 'error': 'failed_to_parse'}


def list_pdfs(dir_path: Path) -> List[str]:
    return [p.name for p in dir_path.glob('*.pdf')]


def build_prompt(context: Dict[str, Any]) -> str:
    week2 = context.get('week2', {})
    week3 = context.get('week3', {})
    csv_preview = week3.get('csv_preview', {})
    nb_outline = week3.get('notebook_outline', {})
    pdfs = week3.get('pdfs', [])

    header = """
You are designing a precise, 90–120 minute Week 3 session for GCAP3226 that builds on Week 2.
Create two deliverables in Markdown (no code fences):

1) Week 3 — Outline (H2) with subsections:
   - Learning Objectives (bullets, 3–5)
   - Session Flow (timeboxed segments; bullets with mm:ss or minutes)
   - Activities & Materials Mapping (bullets; reference dataset/notebook/handouts explicitly)
   - Assessment & Exit Ticket (bullets)
   - Homework/Prep for Week 4 (bullets)

2) Reviewer Comments on Materials (H2): a short paragraph plus bullets for each item, covering suitability, gaps, and concrete suggestions.

Constraints:
- Prefer regression concepts referenced by provided notebook and CSV.
- Connect to Week 2 themes and what students already saw.
- Keep language student-facing and concrete; avoid long prose.
""".strip()

    week2_block = "\n\n".join([
        "### Week 2 — Reference (snippets)",
        (week2.get('guide_md') or '')[:2000],
        (week2.get('slides_md') or '')[:2000],
        f"Week 2 notebooks: {', '.join(week2.get('notebooks') or [])}",
    ])

    csv_block = ""
    if csv_preview:
        header_row = ', '.join(csv_preview.get('header') or [])
        sample_rows = csv_preview.get('sample') or []
        sample_str = "\n".join([", ".join(r) for r in sample_rows[:4]])
        csv_block = f"""
### Week 3 — Dataset Preview
Header: {header_row}
Sample:
{sample_str}
""".strip()

    nb_block = ""
    if nb_outline and nb_outline.get('outline'):
        nb_block = "### Week 3 — Notebook Outline\n" + "\n".join(f"- {ln}" for ln in nb_outline['outline'][:20])

    pdf_block = ""
    if pdfs:
        pdf_block = "### Week 3 — PDFs\n" + "\n".join(f"- {name}" for name in pdfs)

    prompt = f"""
{header}

---
{week2_block}

---
{csv_block}

{nb_block}

{pdf_block}

Deliver only the two sections requested, as Markdown headings and bullets.
""".strip()
    return prompt


def call_llm(prompt: str, model: str) -> str:
    if not OPENROUTER_AVAILABLE:
        raise RuntimeError("OpenRouter client not available")
    if not get_openrouter_api_key():
        raise RuntimeError("Missing OPENROUTER_API_KEY")
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 3000,
        'temperature': 0.2,
    }
    print("📡 Sending Week2/Week3 context to OpenRouter…")
    resp = post_chat_completions(payload)
    content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    if not content:
        raise RuntimeError('Empty response from LLM')
    print("✅ Received outline and comments")
    return content


def create_doc_and_write(docs, drive, folder_id: str, title: str, md: str) -> str:
    file_metadata = {
        'name': title,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id],
    }
    file = drive.files().create(body=file_metadata, fields='id').execute()
    doc_id = file['id']
    # Insert content
    requests = build_replace_requests(md, initial_index=1)
    CHUNK = 100
    for i in range(0, len(requests), CHUNK):
        batch = requests[i:i+CHUNK]
        docs.documents().batchUpdate(documentId=doc_id, body={'requests': batch}).execute()
    return doc_id


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Generate Week 3 outline and materials comments into a Google Doc')
    ap.add_argument('--week2', type=str, default=str(DEFAULT_WEEK2), help='Path to Week 2 materials directory')
    ap.add_argument('--week3', type=str, default=str(DEFAULT_WEEK3), help='Path to Week 3 materials directory')
    ap.add_argument('--folder-id', type=str, default=DEFAULT_FOLDER_ID, help='Target Google Drive folder ID for the new doc')
    ap.add_argument('--title', type=str, default='Week 3 Materials Review and Outline', help='Title for the new Google Doc')
    ap.add_argument('--model', type=str, default='xai/grok-2-latest', help='OpenRouter model to use (e.g., xai/grok-2-latest)')
    ap.add_argument('--dry-run', action='store_true', help='Print the generated output without creating a doc')
    args = ap.parse_args(argv)

    try:
        week2_dir = Path(args.week2)
        week3_dir = Path(args.week3)
        if not week3_dir.exists():
            raise RuntimeError(f"Week 3 path not found: {week3_dir}")

        # Collect context
        print("🔎 Collecting Week 2 context…")
        w2 = summarize_week2(week2_dir)

        print("🔎 Collecting Week 3 assets…")
        csv_candidates = list(week3_dir.glob('*.csv'))
        csv_prev = preview_csv(csv_candidates[0]) if csv_candidates else {}
        nb_candidates = list(week3_dir.glob('*.ipynb'))
        nb_prev = extract_notebook_outline(nb_candidates[0]) if nb_candidates else {}
        pdfs = list_pdfs(week3_dir)

        context = {
            'week2': w2,
            'week3': {
                'csv_preview': csv_prev,
                'notebook_outline': nb_prev,
                'pdfs': pdfs,
            }
        }

        prompt = build_prompt(context)
        # Try preferred model, then fallback
        model = args.model
        try:
            md = call_llm(prompt, model=model)
        except Exception as e:
            print(f"⚠️  Model '{model}' failed: {e}. Falling back to 'anthropic/claude-3.5-sonnet'.")
            md = call_llm(prompt, model='anthropic/claude-3.5-sonnet')

        print("\n=== GENERATED PREVIEW (first ~60 lines) ===\n")
        print("\n".join(md.splitlines()[:60]))
        print("\n=== END PREVIEW ===\n")

        if args.dry_run:
            print("🔎 Dry-run: not creating Google Doc.")
            return 0

        print("🧩 Authenticating Google APIs…")
        docs, drive = auth_services()
        print("📝 Creating Google Doc and writing content…")
        doc_id = create_doc_and_write(docs, drive, args.folder_id, args.title, md)
        print("✅ Created document")
        print(f"🔗 https://docs.google.com/document/d/{doc_id}/edit")
        return 0
    except Exception as e:
        print(f"❌ Failed to generate Week 3 review: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
