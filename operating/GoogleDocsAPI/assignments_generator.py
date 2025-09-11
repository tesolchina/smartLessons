#!/usr/bin/env python3
"""
Generate tentative instructions and rubrics for major assignments using LLM context and update Google Docs.

Features
- Collect local course context (syllabus, intro, week plans, quick refs)
- Ask LLM to draft per-assignment instructions + rubric in Markdown
- Locate existing Google Docs in a target Drive folder and replace their content
- Render Markdown to Google Docs styles (H1-3, bullets, code blocks)

Usage
  python3 operating/GoogleDocsAPI/assignments_generator.py \
    --model anthropic/claude-3.5-sonnet \
    --folder-id <GOOGLE_DRIVE_FOLDER_ID> \
    [--assignments "Project Proposal, Midterm Presentation, Final Project Report"] \
    [--dry-run]

Notes
- If multiple Docs match an assignment name, the best match by title substring is chosen.
- Set OPENROUTER_API_KEY in environment. Google auth must be set up (auth_setup.py).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / 'modules'
if str(MODULES_DIR) not in sys.path:
    sys.path.insert(0, str(MODULES_DIR))

GOOG_API_DIR = Path(__file__).parent
if str(GOOG_API_DIR) not in sys.path:
    sys.path.insert(0, str(GOOG_API_DIR))

try:
    from openRouterAI.client import post_chat_completions
    from openRouterAI.env import get_openrouter_api_key
    OPENROUTER_AVAILABLE = True
except Exception as e:
    print(f"⚠️  OpenRouter module not available: {e}")
    OPENROUTER_AVAILABLE = False

# Reuse Markdown -> Docs renderer from roundtrip tool
try:
    from doc_roundtrip_update import build_replace_requests
except Exception:
    # Fallback: minimal local import if needed later
    build_replace_requests = None  # type: ignore


def auth_services():
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        raise RuntimeError(f"Google API libraries not available: {e}")
    import auth_setup  # type: ignore
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    docs = build('docs', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)
    return docs, drive


def read_text(path: Path, max_chars: int = 20000) -> str:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        return text[:max_chars]
    except Exception:
        return ''


def collect_course_context() -> Dict[str, str]:
    base = REPO_ROOT / 'projects' / 'GCAP3226'
    ctx: Dict[str, str] = {}
    # Preferred sources
    files = {
        'intro_html': base / 'course_materials' / 'intro.html',
        'syllabus': base / 'course_materials' / 'syllabus' / 'syllabus_analysis.md',
        'weeks_draft': base / 'weeks3_14_draft.md',
        'quick_ref': REPO_ROOT / 'operating' / 'GoogleDocsAPI' / 'GCAP3226_Quick_Reference.md',
    }
    for k, p in files.items():
        if p.exists():
            ctx[k] = read_text(p, max_chars=25000 if k == 'syllabus' else 15000)
    return ctx


def build_prompt(assignments: List[str], context: Dict[str, str]) -> str:
    intro = context.get('intro_html', '')
    syllabus = context.get('syllabus', '')
    weeks = context.get('weeks_draft', '')
    quick_ref = context.get('quick_ref', '')
    assignments_list = '\n'.join([f"- {a}" for a in assignments])

    return f"""
You are an assessment designer for a policy analytics course (GCAP 3226).

Goal: Draft tentative instructions and grading rubrics for the major assignments below.
Output must be in clean Markdown with headings, bullet lists, and tables if helpful. Do NOT use raw triple-backtick fences; for any code or command examples, indent lines instead.

Assignments:
{assignments_list}

For EACH assignment, include these sections:
1) H2 heading with the assignment name (e.g., "## Project Proposal")
2) Purpose & Learning Outcomes (aligned to CILOs)
3) Deliverables (what to submit: format, length, required components)
4) Timeline & Milestones (with suggested in-class checkpoints if relevant)
5) Submission & Academic Integrity (AI usage policy and citation expectations)
6) Detailed Rubric (criteria with 4 performance levels; weights totaling 100%)
7) Feedback & Resubmission Policy (if applicable)

Keep tone concise and student-facing. Use consistent structure across assignments. Ensure feasibility with the provided course resources.

Course Context (extracts):
--- INTRO.HTML (excerpt) ---
{intro[:4000]}
--- SYLLABUS (excerpt) ---
{syllabus[:8000]}
--- WEEKS DRAFT (excerpt) ---
{weeks[:4000]}
--- QUICK REFERENCE (excerpt) ---
{quick_ref[:3000]}
"""


def call_llm(prompt: str, model: str) -> str:
    if not OPENROUTER_AVAILABLE:
        raise RuntimeError("OpenRouter client not available")
    if not get_openrouter_api_key():
        raise RuntimeError("Missing OPENROUTER_API_KEY")
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 5000,
        'temperature': 0.3,
    }
    print("📡 Sending assignment drafting prompt to LLM…")
    resp = post_chat_completions(payload)
    content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    if not content:
        raise RuntimeError('Empty response from LLM')
    print("✅ Received assignment drafts")
    return content


def split_assignments(md: str) -> Dict[str, str]:
    """Split Markdown by H2 sections. Return mapping title -> section markdown."""
    lines = md.splitlines()
    sections: Dict[str, List[str]] = {}
    current_title: Optional[str] = None
    for ln in lines:
        if ln.startswith('## '):
            current_title = ln[3:].strip()
            sections[current_title] = [ln]
        else:
            if current_title is not None:
                sections[current_title].append(ln)
    return {k: '\n'.join(v).strip() for k, v in sections.items()}


def drive_list_folder_files(drive, folder_id: str) -> List[Dict]:
    files: List[Dict] = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"
    while True:
        resp = drive.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name, mimeType)", pageToken=page_token).execute()
        files.extend(resp.get('files', []))
        page_token = resp.get('nextPageToken')
        if not page_token:
            break
    return files


def fuzzy_find_doc(files: List[Dict], title_key: str) -> Optional[Dict]:
    """Find a Google Doc whose name best contains title_key (case-insensitive)."""
    title_key_lower = title_key.lower()
    candidates = [f for f in files if f.get('mimeType') == 'application/vnd.google-apps.document']
    # Exact contains first
    for f in candidates:
        if title_key_lower in f.get('name', '').lower():
            return f
    # Try simplified keywords
    keywords = re.findall(r"[a-zA-Z]+", title_key_lower)
    if not keywords:
        return None
    scored: List[Tuple[int, Dict]] = []
    for f in candidates:
        name = f.get('name', '').lower()
        score = sum(1 for kw in keywords if kw in name)
        scored.append((score, f))
    scored.sort(key=lambda x: (-x[0], x[1].get('name', '')))
    return scored[0][1] if scored and scored[0][0] > 0 else None


def create_google_doc(drive, name: str, folder_id: str) -> Dict:
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id],
    }
    created = drive.files().create(body=file_metadata, fields='id, name, mimeType').execute()
    return created


def replace_doc_with_markdown(docs, document_id: str, md: str):
    # Clear body safely (avoid empty-range errors)
    document = docs.documents().get(documentId=document_id).execute()
    content = document.get('body', {}).get('content', []) or []
    end_index = int(content[-1].get('endIndex', 1)) if content else 1
    if end_index > 2:
        delete_req = [{
            'deleteContentRange': {
                'range': {'startIndex': 1, 'endIndex': end_index - 1}
            }
        }]
        docs.documents().batchUpdate(documentId=document_id, body={'requests': delete_req}).execute()

    # Insert rendered Markdown
    if build_replace_requests is None:
        raise RuntimeError("Markdown renderer not available")
    insert_reqs = build_replace_requests(md, initial_index=1)
    CHUNK = 100
    for i in range(0, len(insert_reqs), CHUNK):
        docs.documents().batchUpdate(documentId=document_id, body={'requests': insert_reqs[i:i+CHUNK]}).execute()


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Draft assignment instructions and rubrics, then update Google Docs')
    ap.add_argument('--folder-id', required=True, help='Google Drive folder ID containing the assignment docs to update')
    ap.add_argument('--assignments', help='Comma-separated assignment names to generate (defaults to common set)')
    ap.add_argument('--model', default='anthropic/claude-3.5-sonnet', help='OpenRouter model')
    ap.add_argument('--dry-run', action='store_true', help='Preview drafts and targets without updating Docs')
    args = ap.parse_args(argv)

    assignments = [a.strip() for a in (args.assignments.split(',') if args.assignments else []) if a.strip()]
    if not assignments:
        # Reasonable defaults for GCAP3226
        assignments = [
            'Project Proposal',
            'Midterm Presentation',
            'Final Project Report',
            'Reflective Learning Journal',
        ]

    # Gather context and draft via LLM
    ctx = collect_course_context()
    prompt = build_prompt(assignments, ctx)
    drafts_md = call_llm(prompt, model=args.model)
    per_assignment = split_assignments(drafts_md)

    # Auth and list folder docs
    docs, drive = auth_services()
    files = drive_list_folder_files(drive, args.folder_id)

    # Map and update
    for title, md in per_assignment.items():
        print(f"\n📄 Processing: {title}")
        target = fuzzy_find_doc(files, title)
        if not target:
            # Create a new doc with a sensible name
            safe_name = f"{title} - Instructions & Rubric"
            print(f"   ➜ No existing doc found; creating: {safe_name}")
            target = create_google_doc(drive, safe_name, args.folder_id)
            # refresh file list cache not strictly necessary for immediate use
        print(f"   ➜ Target Doc: {target.get('name')} ({target.get('id')})")
        print(f"   ✨ Preview snippet:\n{md.splitlines()[0:10]}")
        if args.dry_run:
            continue
        replace_doc_with_markdown(docs, target.get('id'), md)
        print("   ✅ Updated")

    print("\n✅ Assignment drafting completed.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
