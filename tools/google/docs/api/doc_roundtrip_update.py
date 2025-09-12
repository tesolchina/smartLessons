#!/usr/bin/env python3
"""
Google Doc Round-Trip Updater

Reads a Google Doc and its Drive comments, sends both to OpenRouter for revision, 
and replaces the Doc content with a rendered version (headings, bullets, code blocks).

Usage:
  python3 operating/GoogleDocsAPI/doc_roundtrip_update.py \
    --doc-id 19LYdvuVJLaZ-MMm31jVc4hXo6tCrcWMk-Np4LiDUib8 \
    --model openrouter/auto \
    [--dry-run]

Notes:
  - Applies minimal formatting: H1–H3 from #/##/###, bulleted lists from '-' lines, 
    fenced code blocks rendered in monospace with light gray background.
  - If dry-run, prints preview without changing the Doc.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / 'modules'))

try:
    from openRouterAI.client import post_chat_completions
    from openRouterAI.env import get_openrouter_api_key
    OPENROUTER_AVAILABLE = True
except Exception as e:
    print(f"⚠️  OpenRouter module not available: {e}")
    OPENROUTER_AVAILABLE = False


def auth_services():
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        raise RuntimeError(f"Google API libraries not available: {e}")

    # Import auth from this folder
    this_dir = Path(__file__).parent
    if str(this_dir) not in sys.path:
        sys.path.insert(0, str(this_dir))
    import auth_setup  # type: ignore
    creds = auth_setup.authenticate_google_apis()
    if not creds:
        raise RuntimeError("Authentication failed")
    docs = build('docs', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)
    return docs, drive


def extract_text_from_doc_struct(doc: Dict[str, Any]) -> str:
    body = doc.get('body', {})
    content = body.get('content', [])
    full_text: List[str] = []
    for el in content:
        if 'paragraph' in el:
            parts = []
            for elem in el['paragraph'].get('elements', []):
                tr = elem.get('textRun')
                if tr and 'content' in tr:
                    parts.append(tr['content'])
            if parts:
                full_text.append(''.join(parts))
        elif 'table' in el:
            # flatten table cells as lines
            for row in el['table'].get('tableRows', []):
                row_text = []
                for cell in row.get('tableCells', []):
                    cell_parts = []
                    for c_el in cell.get('content', []):
                        if 'paragraph' in c_el:
                            for elem in c_el['paragraph'].get('elements', []):
                                tr = elem.get('textRun')
                                if tr and 'content' in tr:
                                    cell_parts.append(tr['content'])
                    row_text.append(''.join(cell_parts).strip())
                full_text.append(' | '.join(row_text))
    return '\n'.join(full_text)


def list_drive_comments(drive, file_id: str) -> List[Dict[str, Any]]:
    try:
        resp = drive.comments().list(fileId=file_id, fields='comments(author,content,htmlContent,createdTime,resolved)').execute()
        return resp.get('comments', [])
    except Exception as e:
        print(f"⚠️  Could not fetch comments: {e}")
        return []


def build_llm_prompt(doc_text: str, comments: List[Dict[str, Any]], protected_week: Optional[int] = None, protected_text: Optional[str] = None, additions_only_week: Optional[int] = None, additions_source: Optional[str] = None) -> str:
    comments_summary_lines = []
    for i, c in enumerate(comments, 1):
        author = c.get('author', {}).get('displayName', 'Unknown')
        resolved = c.get('resolved', False)
        content = c.get('content') or c.get('htmlContent') or ''
        comments_summary_lines.append(f"{i}. [{author}] resolved={resolved}: {content}")
    comments_summary = '\n'.join(comments_summary_lines) if comments_summary_lines else '(no comments)'

    protection_block = ""
    if protected_week is not None and protected_text:
        protection_block = f"""
PROTECTED SECTION (DO NOT MODIFY EXISTING WORDS):
---
Keep the following Week {protected_week} content exactly as-is. You may only propose additional material as bullet points under a subheading "Week {protected_week} — Additions". Do not paraphrase or delete any existing Week {protected_week} text.

BEGIN_PROTECTED_WEEK_{protected_week}
{protected_text}
END_PROTECTED_WEEK_{protected_week}
---
"""

    additions_block = ""
    if additions_only_week is not None and additions_source:
        additions_block = f"""
ADDITIONS-ONLY MODE:
---
Output only a short section for Week {additions_only_week} in Markdown containing:
1) A heading "### Week {additions_only_week} — Additions" and
2) 3–6 concise bullet points that extend the existing Week {additions_only_week} plan.
Do NOT repeat existing content; do NOT include any other weeks or headings. No code fences.

WEEK {additions_only_week} (for reference):
{additions_source}
---
"""

    instruction = f"""
You are an assistant editor for a policy course planning document.

Task: Integrate the following Google Doc content and reviewer comments into a single, improved version suitable for Google Docs.

Requirements:
- Preserve structure and clarity. Address comment requests where feasible.
- Output as Markdown headings and bullet lists (no raw triple-backticks).
- For code or command examples, present them as indented code blocks (we'll render monospace in Docs). Avoid ``` fences.
- Keep content self-contained; remove redundant sections, fix inconsistencies, and tighten wording.
 - If a protected Week is provided, do NOT rewrite it. Only add new items under a subheading "Week <n> — Additions" as concise bullet points.

COMMENTS:
---
{comments_summary}
---

CURRENT DOCUMENT TEXT:
---
{doc_text}
---

{protection_block}

{additions_block}

Deliver the revised document only.
"""
    return instruction


def call_llm(prompt: str, model: str) -> str:
    if not OPENROUTER_AVAILABLE:
        raise RuntimeError("OpenRouter client not available")
    if not get_openrouter_api_key():
        raise RuntimeError("Missing OPENROUTER_API_KEY")
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 4000,
        'temperature': 0.2,
    }
    print("📡 Sending content and comments to OpenRouter…")
    resp = post_chat_completions(payload)
    content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
    if not content:
        raise RuntimeError('Empty response from LLM')
    print("✅ Received revised content")
    return content


def parse_markdown_blocks(md: str) -> List[Tuple[str, str]]:
    """Parse markdown into blocks with simple types: heading1/2/3, bullet, codeblock, paragraph.
    Returns list of (type, text) preserving order. Code fences ``` are recognized.
    """
    lines = md.splitlines()
    blocks: List[Tuple[str, str]] = []
    i = 0
    in_code = False
    code_buf: List[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                # end code block
                blocks.append(('codeblock', '\n'.join(code_buf)))
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        # Headings
        if line.startswith('### '):
            blocks.append(('heading3', line[4:].strip()))
        elif line.startswith('## '):
            blocks.append(('heading2', line[3:].strip()))
        elif line.startswith('# '):
            blocks.append(('heading1', line[2:].strip()))
        elif line.strip().startswith('- '):
            blocks.append(('bullet', line.strip()[2:].strip()))
        elif line.strip() == '':
            blocks.append(('blank', ''))
        else:
            blocks.append(('paragraph', line))
        i += 1
    # In case of unterminated code block
    if in_code and code_buf:
        blocks.append(('codeblock', '\n'.join(code_buf)))
    return blocks


def _find_week_section_bounds_lines(lines: List[str], week_no: int) -> Tuple[int, int]:
    """Heuristically find the start/end line indices (exclusive) for a given 'Week N' section.
    Start at a line beginning with optional '#' then 'Week {n}'. End at the next 'Week X' or EOF.
    Returns (-1, -1) if not found.
    """
    week_pattern = re.compile(r"^\s*(?:#{1,6}\s*)?Week\s*%d\b" % week_no, re.IGNORECASE)
    any_week_pattern = re.compile(r"^\s*(?:#{1,6}\s*)?Week\s*(\d+)\b", re.IGNORECASE)
    start = -1
    for i, ln in enumerate(lines):
        if week_pattern.match(ln):
            start = i
            break
    if start == -1:
        return -1, -1
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = any_week_pattern.match(lines[j])
        if m:
            try:
                nxt = int(m.group(1))
            except Exception:
                nxt = -999
            if nxt != week_no:
                end = j
                break
    return start, end


def find_week_section(text: str, week_no: int) -> Tuple[int, int, str]:
    """Find a Week section by number. Return (start_char, end_char, section_text)."""
    lines = text.splitlines()
    s_idx, e_idx = _find_week_section_bounds_lines(lines, week_no)
    if s_idx == -1:
        return -1, -1, ""
    # compute char offsets accounting for newlines
    pos = 0
    starts: List[int] = []
    for ln in lines:
        starts.append(pos)
        pos += len(ln) + 1
    start_char = starts[s_idx]
    end_char = starts[e_idx] if e_idx < len(starts) else len(text)
    section_text = "\n".join(lines[s_idx:e_idx])
    return start_char, end_char, section_text


def extract_week_additions(week_section_md: str, week_no: int) -> str:
    """Extract an 'Additions' subsection for the given week from the LLM output.
    Captures from a heading containing 'Additions' (optionally prefixed with 'Week n —') up to the next heading.
    Returns the captured text (including heading) or empty string.
    """
    lines = week_section_md.splitlines()
    # Pattern accepts variations: 'Additions', 'Week 3 — Additions', '## Additions'
    additions_heading = re.compile(r"^\s*(?:#{1,6}\s*)?(?:Week\s*%d\s*[-:—]\s*)?Additions\b" % week_no, re.IGNORECASE)
    next_section = re.compile(r"^\s*(?:#{1,6}\s+|Week\s*\d+\b)", re.IGNORECASE)
    start = -1
    for i, ln in enumerate(lines):
        if additions_heading.match(ln):
            start = i
            break
    if start == -1:
        return ""
    collected: List[str] = []
    for j in range(start, len(lines)):
        if j > start and next_section.match(lines[j]):
            break
        collected.append(lines[j])
    if collected and not additions_heading.match(collected[0]):
        collected.insert(0, f"### Week {week_no} — Additions")
    return "\n".join(collected).strip()


def get_last_end_index(doc: Dict[str, Any]) -> int:
    body = doc.get('body', {})
    content = body.get('content', [])
    if not content:
        return 1
    last = content[-1]
    return int(last.get('endIndex', 1))


def iter_body_elements(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    return doc.get('body', {}).get('content', []) or []


def element_plain_text(el: Dict[str, Any]) -> str:
    if 'paragraph' in el:
        parts: List[str] = []
        for elem in el['paragraph'].get('elements', []):
            tr = elem.get('textRun')
            if tr and 'content' in tr:
                parts.append(tr['content'])
        return ''.join(parts)
    return ''


def find_week_struct_bounds(doc: Dict[str, Any], week_no: int) -> Tuple[int, int]:
    """Find Docs API indices for the start of 'Week N' section and the start of the next week (or doc end).
    Returns (start_index, next_week_start_or_end_index). If not found, returns (-1, -1).
    """
    content = iter_body_elements(doc)
    week_pat = re.compile(r"^\s*(?:#{1,6}\s*)?Week\s*%d\b" % week_no, re.IGNORECASE)
    any_week_pat = re.compile(r"^\s*(?:#{1,6}\s*)?Week\s*(\d+)\b", re.IGNORECASE)
    start_idx = -1
    next_idx = -1
    # locate start
    for el in content:
        txt = element_plain_text(el)
        if week_pat.match(txt or ''):
            start_idx = int(el.get('startIndex', -1))
            break
    if start_idx == -1:
        return -1, -1
    # locate next week
    started = False
    for el in content:
        if int(el.get('startIndex', -1)) == start_idx:
            started = True
            continue
        if not started:
            continue
        txt = element_plain_text(el)
        m = any_week_pat.match(txt or '')
        if m:
            try:
                num = int(m.group(1))
            except Exception:
                num = -999
            if num != week_no:
                next_idx = int(el.get('startIndex', -1))
                break
    if next_idx == -1:
        # end of doc
        next_idx = get_last_end_index(doc)
    return start_idx, next_idx


def apply_markdown_at_index(docs, document_id: str, md: str, insertion_index: int) -> None:
    """Insert a small Markdown fragment at a given Docs index with basic styling."""
    reqs = build_replace_requests(md, initial_index=insertion_index)
    CHUNK = 100
    for i in range(0, len(reqs), CHUNK):
        docs.documents().batchUpdate(documentId=document_id, body={'requests': reqs[i:i+CHUNK]}).execute()


def build_replace_requests(revised_md: str, initial_index: int = 1) -> List[Dict[str, Any]]:
    """Build Docs API requests to insert and style content derived from markdown.
    - Headings -> named styles (HEADING_1/2/3)
    - Bullets -> createParagraphBullets
    - Code blocks -> monospace font + light gray background
    """
    blocks = parse_markdown_blocks(revised_md)
    requests: List[Dict[str, Any]] = []
    cursor = max(1, initial_index)

    # Helper to add text and return (start, end)
    def add_text(text: str) -> Tuple[int, int]:
        nonlocal cursor, requests
        if not text.endswith('\n'):
            text += '\n'
        requests.append({'insertText': {'location': {'index': cursor}, 'text': text}})
        start, end = cursor, cursor + len(text)
        cursor = end
        return start, end

    bullet_ranges: List[Tuple[int, int]] = []

    for btype, text in blocks:
        if btype == 'heading1':
            s, e = add_text(text)
            requests.append({'updateParagraphStyle': {
                'range': {'startIndex': s, 'endIndex': e},
                'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                'fields': 'namedStyleType'
            }})
        elif btype == 'heading2':
            s, e = add_text(text)
            requests.append({'updateParagraphStyle': {
                'range': {'startIndex': s, 'endIndex': e},
                'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                'fields': 'namedStyleType'
            }})
        elif btype == 'heading3':
            s, e = add_text(text)
            requests.append({'updateParagraphStyle': {
                'range': {'startIndex': s, 'endIndex': e},
                'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                'fields': 'namedStyleType'
            }})
        elif btype == 'bullet':
            s, e = add_text(text)
            bullet_ranges.append((s, e))
        elif btype == 'codeblock':
            s, e = add_text(text)
            requests.append({'updateTextStyle': {
                'range': {'startIndex': s, 'endIndex': e},
                'textStyle': {
                    'fontFamily': 'Courier New',
                    'backgroundColor': {'color': {'rgbColor': {'red': 0.96, 'green': 0.96, 'blue': 0.96}}}
                },
                'fields': 'fontFamily,backgroundColor'
            }})
        elif btype == 'paragraph':
            add_text(text)
        elif btype == 'blank':
            add_text('')

    # Apply bullets after all bullet paragraphs inserted
    for s, e in bullet_ranges:
        requests.append({'createParagraphBullets': {
            'range': {'startIndex': s, 'endIndex': e},
            'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
        }})

    return requests


def roundtrip_update(doc_id: str, model: str, dry_run: bool, target_week: Optional[int] = None) -> bool:
    print("🧩 Authenticating and fetching document…")
    docs, drive = auth_services()
    document = docs.documents().get(documentId=doc_id).execute()
    current_text = extract_text_from_doc_struct(document)
    print(f"✅ Retrieved document text: {len(current_text):,} chars")

    print("🗨️  Fetching comments…")
    comments = list_drive_comments(drive, doc_id)
    print(f"✅ Retrieved {len(comments)} comment(s)")

    # Determine and protect Week 3 section from heavy edits
    protected_week = 3
    _, _, week3_text = find_week_section(current_text, protected_week)
    # If a target week is specified, switch to additions-only mode to avoid touching other sections
    if target_week is not None:
        # Find Week section bounds structurally for accurate insertion
        w_start, w_next = find_week_struct_bounds(document, target_week)
        _, _, week_text = find_week_section(current_text, target_week)
        if w_start == -1:
            raise RuntimeError(f"Week {target_week} section not found in document")
        prompt = build_llm_prompt(
            current_text,
            comments,
            protected_week=target_week,
            protected_text=week_text or None,
            additions_only_week=target_week,
            additions_source=week_text or None,
        )
        additions_md = call_llm(prompt, model=model)

        print("\n=== ADDITIONS PREVIEW ===\n")
        print(additions_md)
        print("\n=== END ADDITIONS PREVIEW ===\n")

        if dry_run:
            print("🔎 Dry-run: not modifying Google Doc.")
            return True

        # Insert just before the next-week start (i.e., at end of target week)
        insertion_index = w_next
        print(f"✍️ Inserting Week {target_week} additions at index {insertion_index}…")
        apply_markdown_at_index(docs, doc_id, additions_md, insertion_index)
        print("✅ Week additions inserted successfully")
        print(f"🔗 https://docs.google.com/document/d/{doc_id}/edit")
        return True

    # Full-document roundtrip (legacy mode)
    prompt = build_llm_prompt(current_text, comments, protected_week=protected_week, protected_text=week3_text or None)
    revised_md = call_llm(prompt, model=model)

    # Enforce preservation by splicing original Week 3 plus any 'Additions' proposed by the model
    r_s, r_e, r_week3 = find_week_section(revised_md, protected_week)
    final_md = revised_md
    if (week3_text or '').strip():
        if r_s != -1:
            additions = extract_week_additions(r_week3, protected_week)
            preserved_block = week3_text.rstrip()
            if additions:
                preserved_block += "\n\n" + additions.strip() + "\n"
            final_md = revised_md[:r_s] + preserved_block + revised_md[r_e:]
        else:
            # If model dropped the Week 3 heading, prepend the preserved block
            final_md = week3_text.rstrip() + "\n\n" + revised_md
    else:
        final_md = revised_md

    print("\n=== REVISED PREVIEW (first ~40 lines) ===\n")
    print('\n'.join(final_md.splitlines()[:40]))
    print("\n=== END PREVIEW ===\n")

    if dry_run:
        print("🔎 Dry-run: not modifying Google Doc.")
        return True

    print("🧹 Clearing existing document body…")
    end_index = get_last_end_index(document)
    delete_req = [{
        'deleteContentRange': {
            'range': {'startIndex': 1, 'endIndex': max(1, end_index - 1)}
        }
    }]
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': delete_req}).execute()

    print("✍️ Writing revised content with basic formatting…")
    insert_reqs = build_replace_requests(final_md, initial_index=1)
    # Batch in chunks to avoid request size limits
    CHUNK = 100
    for i in range(0, len(insert_reqs), CHUNK):
        batch = insert_reqs[i:i+CHUNK]
        docs.documents().batchUpdate(documentId=doc_id, body={'requests': batch}).execute()

    print("✅ Document updated successfully")
    print(f"🔗 https://docs.google.com/document/d/{doc_id}/edit")
    return True


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description='Round-trip a Google Doc via OpenRouter and replace content')
    ap.add_argument('--doc-id', required=True, help='Target Google Doc ID')
    ap.add_argument('--model', default='openrouter/auto', help='OpenRouter model')
    ap.add_argument('--dry-run', action='store_true', help='Preview changes without updating the Doc')
    ap.add_argument('--target-week', type=int, help='Edit only this week: generate and insert an "Additions" section without modifying other weeks')
    args = ap.parse_args(argv)

    try:
        ok = roundtrip_update(args.doc_id, args.model, args.dry_run, target_week=args.target_week)
        return 0 if ok else 1
    except Exception as e:
        print(f"❌ Round-trip failed: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
