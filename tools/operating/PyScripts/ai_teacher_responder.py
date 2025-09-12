#!/usr/bin/env python3
"""Respond to latest TEACHER zone updates by appending an AI reply inside the AI zone.

Logic:
  - Scan tabs (all or specific via --tab ... repeatable).
  - Extract TEACHER and AI zones delimited by markers: <<<ZONE:TEACHER:BEGIN>>> ... <<<ZONE:TEACHER:END>>>, etc.
  - Skip if TEACHER zone empty or only placeholder '(Write here – add content)'.
  - Compute sha256 hash of normalized TEACHER zone content.
  - Load state file interaction_state/teacher_response_state.json to see if this hash already replied.
  - If not replied: generate simple heuristic AI reply (summary + next-step prompt) and insert BEFORE the AI zone END marker (thus keeping existing AI content below).
  - Record responded hash + timestamp.

State file structure:
{
  "document_id": "...",
  "version": 1,
  "tabs": {
     "argumentative research paper": {
         "teacher_hash_replied": "sha256:...",
         "last_reply_iso": "2025-09-11T12:34:00Z"
     }
  }
}

Usage:
  Dry run all: python3 ai_teacher_responder.py --doc <ID> --all --dry-run
  Apply single tab: python3 ai_teacher_responder.py --doc <ID> --tab "Argumentative research paper"

Notes:
    - Idempotent per teacher content hash.
    - Only appends; does not modify existing AI replies.
    - Optional OpenRouter LLM integration via --use-openrouter (falls back to heuristic reply if API key missing or call fails).
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, unicodedata, datetime as dt
from datetime import timezone, timedelta
from typing import Dict, List, Tuple, Optional, Iterable
import difflib

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BEGIN_PREFIX = '<<<ZONE:'
BEGIN_SUFFIX = ':BEGIN>>>'
END_SUFFIX = ':END>>>'
PLACEHOLDER = '(Write here – add content)'

STATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'interaction_state', 'teacher_response_state.json')

HKT_OFFSET = timedelta(hours=8)

def now_hkt_str() -> str:
    """Return current time in HKT (UTC+8) formatted YYYY-MM-DD HH:MM HKT."""
    return (dt.datetime.utcnow() + HKT_OFFSET).strftime('%Y-%m-%d %H:%M HKT')


def normalize_title(t: str) -> str:
    nf = unicodedata.normalize('NFKC', t or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    mapping: Dict[str, dict] = {}
    def add(t: dict):
        props = t.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            mapping[normalize_title(title)] = t
        for c in t.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return mapping


def paragraph_text(elem: dict) -> str:
    para = elem.get('paragraph')
    if not para:
        return ''
    out: List[str] = []
    for r in para.get('elements', []) or []:
        tr = r.get('textRun')
        if tr:
            out.append(tr.get('content', ''))
    return ''.join(out)


def extract_zone_ranges(tab: dict) -> Dict[str, Dict[str, int]]:
    """Return mapping zone_key -> { 'content_start': idx, 'content_end': idx, 'end_marker_start': idx } indexes.
    content_start is first char index of inner content.
    content_end is last char index (exclusive) before END marker start.
    """
    result: Dict[str, Dict[str, int]] = {}
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    current_key: Optional[str] = None
    inside = False
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        start = elem.get('startIndex'); end = elem.get('endIndex')
        if start is None or end is None:
            continue
        txt_full = paragraph_text(elem)
        stripped = txt_full.strip()
        if stripped.startswith(BEGIN_PREFIX) and stripped.endswith(BEGIN_SUFFIX):
            raw_key = stripped[len(BEGIN_PREFIX):-len(BEGIN_SUFFIX)]
            current_key = raw_key.upper()
            inside = True
            # inner content begins at end of this paragraph
            result.setdefault(current_key, {})['content_start'] = end
            continue
        if inside and current_key and stripped == f"{BEGIN_PREFIX}{current_key}{END_SUFFIX.replace('BEGIN','END')}":
            # closing marker
            # content_end is start of this paragraph
            if 'content_end' not in result[current_key]:
                result[current_key]['content_end'] = start
            result[current_key]['end_marker_start'] = start
            inside = False
            current_key = None
            continue
        # normal inner paragraph
    return result


def extract_zone_text(tab: dict, key: str) -> str:
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    lines: List[str] = []
    collecting = False
    begin_line = f"{BEGIN_PREFIX}{key}{BEGIN_SUFFIX}"
    end_line = f"{BEGIN_PREFIX}{key}{END_SUFFIX.replace('BEGIN','END')}"
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        txt_full = paragraph_text(elem)
        for raw_line in txt_full.splitlines():
            line = raw_line.rstrip('\r')
            s = line.strip()
            if s == begin_line:
                collecting = True
                continue
            if s == end_line:
                collecting = False
                continue
            if collecting:
                lines.append(line)
    return '\n'.join(lines).strip()


def hash_text(txt: str) -> str:
    core = '\n'.join(l.rstrip() for l in txt.strip().splitlines()) if txt.strip() else ''
    return 'sha256:' + hashlib.sha256(core.encode('utf-8')).hexdigest()


def load_state(document_id: str) -> dict:
    if not os.path.exists(STATE_PATH):
        return {"document_id": document_id, "version": 1, "tabs": {}}
    try:
        with open(STATE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data.get('document_id') != document_id:
            # archive old
            archive_dir = os.path.join(os.path.dirname(STATE_PATH), 'snapshots')
            os.makedirs(archive_dir, exist_ok=True)
            ts = dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')
            with open(os.path.join(archive_dir, f"teacher_state_{ts}.json"), 'w', encoding='utf-8') as o:
                json.dump(data, o, indent=2, ensure_ascii=False)
            return {"document_id": document_id, "version": 1, "tabs": {}}
        return data
    except Exception:
        return {"document_id": document_id, "version": 1, "tabs": {}}


def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def compute_added_lines(prev: str, curr: str) -> List[str]:
    if not prev.strip():
        return [ln for ln in (l.strip() for l in curr.splitlines()) if ln]
    diff = difflib.unified_diff(prev.splitlines(), curr.splitlines(), lineterm='')
    added: List[str] = []
    for d in diff:
        if d.startswith('+') and not d.startswith('+++'):
            line = d[1:].strip()
            if line:
                added.append(line)
    return added


def build_ai_reply(teacher_text: str, prev_teacher_text: str, existing_ai_text: str, *, disable_table: bool=False) -> str:
    """Generate a heuristic (non-LLM) AI reply referencing only new teacher additions and avoiding duplicate artifacts.

    This is the fallback if OpenRouter usage is disabled or unavailable.
    """
    lines = [ln.rstrip() for ln in teacher_text.splitlines() if ln.strip()]
    lower_all = '\n'.join(lines).lower()
    added_lines = compute_added_lines(prev_teacher_text or '', teacher_text)
    ts = now_hkt_str()
    header = f"[AI Auto-Reply {ts}]\n"
    body_sections: List[str] = []
    if added_lines:
        # Summarize up to first 3 new lines
        limited = added_lines[:3]
        body_sections.append("New instructor additions detected:\n- " + "\n- ".join(limited))
    else:
        body_sections.append("No line-level additions detected; reiterating actionable guidance.")

    if not disable_table:
        table_requested = any(kw in lower_all for kw in [
            'membership table', 'generate a markdown table', 'list student name', 'student name, id, gmail'
        ])
        table_already_present = 'Student Name | Student ID' in existing_ai_text
        if table_requested and not table_already_present:
            body_sections.append(
                "Membership table template (populate and later we can convert to a real Docs table):\n\n"
                "| # | Student Name | Student ID | HKU Email | Alt/Gmail | Role | Notes |\n"
                "|---|--------------|------------|----------|-----------|------|-------|\n"
                "| 1 |              |            |          |           |      |       |\n"
                "| 2 |              |            |          |           |      |       |\n"
                "| 3 |              |            |          |           |      |       |\n"
                "\nAfter filling: we can auto-convert this Markdown to a real table and add role validation (e.g., unique primary role)."
            )
        elif table_requested and table_already_present:
            body_sections.append("Membership table already supplied earlier; proceed to fill in rows (avoid duplicate student names).")

    # Generic next step if not already included
    if not any('next step' in s.lower() for s in body_sections):
        body_sections.append("Next step: implement the requested changes and signal completion with a short note at top of TEACHER zone.")

    return header + '\n\n'.join(body_sections) + '\n'


def build_llm_reply(teacher_text: str, prev_teacher_text: str, existing_ai_text: str, *, mode: str = 'text', disable_table: bool=False, style: str = 'default') -> Optional[str]:
    """Attempt to generate an AI reply using OpenRouter LLM.

    Returns the reply string on success, or None on failure (caller should fallback).
    Keeps similar behavior: highlight new lines, optionally insert membership table once.
    """
    try:
        # Local import to avoid hard dependency if module path not set
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # ensure repo root
        from modules.openRouterAI.env import get_openrouter_api_key, get_openrouter_model  # type: ignore
        from modules.openRouterAI.client import post_chat_completions  # type: ignore
    except Exception:
        return None

    api_key = ''
    try:
        api_key = get_openrouter_api_key()
    except Exception:
        pass
    if not api_key:
        return None

    added_lines = compute_added_lines(prev_teacher_text or '', teacher_text)
    added_excerpt = '\n'.join(added_lines[:12]) if added_lines else '(No new individual line additions detected)'

    # Detect membership table request / duplication (optional)
    lower_all = teacher_text.lower()
    table_requested = False
    table_already_present = False
    if not disable_table:
        table_requested = any(kw in lower_all for kw in [
            'membership table', 'generate a markdown table', 'list student name', 'student name, id, gmail'
        ])
        table_already_present = 'Student Name | Student ID' in existing_ai_text

    if mode == 'actions':
        system_prompt = (
            "You are an assistant that outputs ONLY JSON (no markdown fences) describing how to update the AI zone in a Google Doc. "
            "Return an object with keys: ai_reply_markdown (string) and actions (array). "
            "Allowed action types: append_ai_zone {text}. Keep responses under 350 words. "
            "If membership table requested and not present, include it in ai_reply_markdown. "
            "Do NOT duplicate an existing membership table."
        )
    else:
        if style == 'elaborate':
            parts = [
                "You are an assistant augmenting the AI zone in a structured Google Doc (zones: STUDENT / TEACHER / AI). ",
                "Goals: (1) Briefly acknowledge ONLY the NEW teacher instructions (diff lines provided). ",
                "(2) Provide an ELABORATION section that expands on teacher rationale, clarifies intent, and highlights implications. ",
                "(3) Provide a STUDENT QUESTIONS section: 3-6 probing, specific questions students might ask to ensure understanding (no yes/no). ",
                "(4) Provide ACTIONABLE NEXT STEPS distilled into concise bullets referencing concrete tasks. ",
            ]
            if not disable_table:
                parts.append("(5) If a membership table is requested AND not already present, insert a minimal clean Markdown table template once. ")
            parts.append(
                "Formatting: Use markdown headings '### Elaboration', '### Student Questions', '### Next Steps'. Keep total under 400 words. "
                "End with a single NEXT STEP: line summarizing immediate action. No roleplay prefaces, no apologies."
            )
            system_prompt = ''.join(parts)
        else:
            parts = [
                "You are an assistant updating the AI zone in a structured Google Doc that has STUDENT, TEACHER, and AI zones. ",
                "Your goals: (1) Acknowledge only NEW teacher instructions (diff lines provided), (2) Provide concise, actionable next steps, ",
            ]
            if not disable_table:
                parts.append("(3) If a membership table is requested AND not already supplied in AI zone, output a clean Markdown table template. ")
            parts.append("(4) Keep answer under 350 words, no outside commentary, no roleplay. End with a one-line NEXT STEP directive.")
            system_prompt = ''.join(parts)

    user_prompt = (
        "FULL TEACHER ZONE (complete context):\n<<<TEACHER_FULL_BEGIN>>>\n"
        f"{teacher_text.strip()}\n<<<TEACHER_FULL_END>>>\n\n"
        "PREVIOUS TEACHER TEXT (for diff reference):\n<<<TEACHER_PREV_BEGIN>>>\n"
        f"{(prev_teacher_text or '').strip()}\n<<<TEACHER_PREV_END>>>\n\n"
        f"NEW / ADDED LINES (focus):\n{added_excerpt}\n\n"
        f"Membership table explicitly requested: {'YES' if table_requested else 'NO'}\n"
        f"Table already present in AI zone: {'YES' if table_already_present else 'NO'}\n"
        + ("Return ONLY JSON." if mode == 'actions' else ("Provide the AI zone update now (style=elaborate)." if style=='elaborate' else "Provide the AI zone update now."))
    )

    model = get_openrouter_model()
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
        'temperature': 0.3,
        'max_tokens': 600,
    }
    try:
        resp = post_chat_completions(payload)
        content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if not content:
            return None
        ts = now_hkt_str()
        if mode == 'actions':
            try:
                parsed = json.loads(content)
                ai_section = parsed.get('ai_reply_markdown', '').strip()
                actions = parsed.get('actions') or []
                if not ai_section:
                    ai_section = '(No ai_reply_markdown returned)'
                for act in actions:
                    if isinstance(act, dict) and act.get('type') == 'append_ai_zone':
                        extra = act.get('text', '')
                        if extra:
                            ai_section += "\n" + extra.strip()
                content = ai_section
            except Exception:
                pass
        if not disable_table and table_already_present and 'Student Name | Student ID' in content:
            lines = content.splitlines()
            filtered = []
            skip = False
            for ln in lines:
                if 'Student Name | Student ID' in ln and table_already_present:
                    skip = True
                if skip and not ln.strip():
                    skip = False
                    continue
                if not skip:
                    filtered.append(ln)
            content = '\n'.join(filtered).strip()
        return f"[AI Auto-Reply {ts}]\n{content}\n"
    except Exception as e:
        print(f"  ⚠️ OpenRouter call failed, falling back heuristic: {e}")
        return None


def apply_reply(docs_service, doc_id: str, tab: dict, ai_zone_ranges: Dict[str, int], reply_text: str):
    tab_id = tab.get('tabProperties', {}).get('tabId')
    if not tab_id:
        return
    end_marker_start = ai_zone_ranges.get('end_marker_start')
    if end_marker_start is None:
        return
    # Insert BEFORE end marker
    insert_req = {'insertText': {'location': {'tabId': tab_id, 'index': end_marker_start}, 'text': reply_text + '\n\n'}}
    try:
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [insert_req]}).execute()
    except HttpError as e:
        print(f"  ❌ Insert failed in tab '{tab.get('tabProperties', {}).get('title','')}' : {e}")


def process_tab(docs_service, doc_id: str, tab: dict, state: dict, dry_run: bool, force: bool=False, use_openrouter: bool=False, disable_table: bool=False, style: str='default') -> Tuple[str, str]:
    title = tab.get('tabProperties', {}).get('title','')
    norm = normalize_title(title)
    # Extract teacher content
    teacher_text = extract_zone_text(tab, 'TEACHER')
    if not teacher_text or teacher_text.strip() == PLACEHOLDER:
        return title, 'skip:no-teacher-content'
    teacher_hash = hash_text(teacher_text)
    tab_state = state.setdefault('tabs', {}).setdefault(norm, {})
    prev_teacher_text = tab_state.get('teacher_last_replied_text', '')
    if tab_state.get('teacher_hash_replied') == teacher_hash and not force:
        return title, 'skip:already-replied'

    # Fetch existing AI zone text to avoid repeating table
    existing_ai_text = extract_zone_text(tab, 'AI')
    # Build reply referencing new lines (LLM first if enabled)
    reply: Optional[str] = None
    if use_openrouter:
        reply = build_llm_reply(teacher_text, prev_teacher_text, existing_ai_text, disable_table=disable_table, style=style)
    if not reply:  # fallback or disabled
        reply = build_ai_reply(teacher_text, prev_teacher_text, existing_ai_text, disable_table=disable_table)
    if dry_run:
        return title, f"would-reply:{len(reply)} chars"

    # Need AI zone ranges for insertion
    ranges_map = extract_zone_ranges(tab)
    ai_ranges = ranges_map.get('AI')
    if not ai_ranges:
        return title, 'error:no-ai-zone'
    apply_reply(docs_service, doc_id, tab, ai_ranges, reply)
    tab_state['teacher_hash_replied'] = teacher_hash
    tab_state['teacher_last_replied_text'] = teacher_text
    tab_state['last_reply_iso'] = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    return title, 'replied'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', action='append')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true', help='Force reply even if teacher hash already replied (useful after improving AI logic).')
    ap.add_argument('--use-openrouter', action='store_true', help='Generate reply via OpenRouter LLM (falls back to heuristic if unavailable).')
    ap.add_argument('--no-table', action='store_true', help='Disable membership table detection/insertion logic.')
    ap.add_argument('--tabs-file', help='Path to file listing tab titles (one per line, # comments allowed).')
    ap.add_argument('--style', choices=['default','elaborate'], default='default', help='Reply style: default concise vs elaborate with student questions.')
    args = ap.parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('Auth failed.')
        return 1
    docs = build('docs','v1',credentials=creds)
    try:
        doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
    except HttpError as e:
        print(f'Fetch failed: {e}')
        return 1

    tabs = flatten_tabs(doc)
    targets: List[dict] = []
    file_tabs: List[str] = []
    if args.tabs_file:
        try:
            with open(args.tabs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line=line.strip()
                    if not line or line.startswith('#'):
                        continue
                    file_tabs.append(line)
        except FileNotFoundError:
            print(f"⚠️ tabs-file not found: {args.tabs_file}")
    merged_tabs: List[str] = []
    if args.tab:
        merged_tabs.extend(args.tab)
    if file_tabs:
        merged_tabs.extend(file_tabs)

    if args.all:
        targets = list(tabs.values())
    elif merged_tabs:
        for t in merged_tabs:
            obj = tabs.get(normalize_title(t))
            if obj:
                targets.append(obj)
            else:
                print(f"⚠️ Tab not found: {t}")
    else:
        print('Provide --tab or --all')
        return 1

    state = load_state(args.doc)
    results: List[Tuple[str,str]] = []
    for tab in targets:
        title, status = process_tab(docs, args.doc, tab, state, args.dry_run, force=args.force, use_openrouter=args.use_openrouter, disable_table=args.no_table, style=args.style)
        results.append((title, status))

    print(f"Tabs processed: {len(results)} (dry-run={args.dry_run})")
    for t, st in results:
        print(f"- {t}: {st}")

    if not args.dry_run:
        save_state(state)
        print(f"State saved to {STATE_PATH}")
    else:
        print('No changes applied (dry-run).')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
