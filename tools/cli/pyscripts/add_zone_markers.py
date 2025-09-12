#!/usr/bin/env python3
"""Add BEGIN/END zone markers to a specific Google Doc tab and remove ASCII box artifacts.

Zones inserted (if matching heading exists and markers absent):
  Student Workspace -> STUDENT_WORKSPACE
  Messages to Instructor -> MESSAGES_TO_INSTRUCTOR
  Instructor Feedback -> INSTRUCTOR_FEEDBACK
  AI Support Comments -> AI_SUPPORT_COMMENTS

Markers pattern (each on its own line):
  <<<ZONE:<KEY>:BEGIN>>>
  (Write here – add content)
  <<<ZONE:<KEY>:END>>>

Safety:
  - Skips insertion if BEGIN marker already present in tab.
  - Deletes only paragraphs styled as headings that contain box-drawing chars.

Usage:
  python3 add_zone_markers.py --doc <ID> --tab "Argumentative research paper"
"""
from __future__ import annotations
import sys, os, unicodedata, argparse, re
from typing import Dict, List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BOX_CHARS = set('╔╗╚╝═║')

ZONE_MAP = {
    'student workspace': 'STUDENT_WORKSPACE',
    'messages to instructor': 'MESSAGES_TO_INSTRUCTOR',
    'instructor feedback': 'INSTRUCTOR_FEEDBACK',
    'ai support comments': 'AI_SUPPORT_COMMENTS'
}

MARKER_TEMPLATE = """<<<ZONE:{key}:BEGIN>>>
(Write here – add content)
<<<ZONE:{key}:END>>>
"""

def normalize(s: str) -> str:
    nf = unicodedata.normalize('NFKC', s or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    mapping: Dict[str, dict] = {}
    def add(t: dict):
        props = t.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            mapping[normalize(title)] = t
        for c in t.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return mapping


def collect_paragraphs(tab: dict) -> List[dict]:
    body = tab.get('documentTab', {}).get('body', {})
    return body.get('content', []) or []


def paragraph_text(elem: dict) -> str:
    para = elem.get('paragraph')
    if not para:
        return ''
    out = []
    for r in para.get('elements', []) or []:
        tr = r.get('textRun')
        if tr:
            out.append(tr.get('content', ''))
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', action='append', help='Tab title to modify (repeatable, case-insensitive)')
    ap.add_argument('--all', action='store_true', help='Process all tabs in the document')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('❌ Auth failed.')
        return 1
    docs = build('docs', 'v1', credentials=creds)
    try:
        doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
    except HttpError as e:
        print(f'❌ Fetch failed: {e}')
        return 1

    tabs = flatten_tabs(doc)
    target_tabs = []
    if args.all:
        target_tabs = list(tabs.values())
    elif args.tab:
        for t in args.tab:
            tab_obj = tabs.get(normalize(t))
            if tab_obj:
                target_tabs.append(tab_obj)
            else:
                print(f"⚠️ Tab not found (skip): {t}")
    else:
        print('❌ Provide --tab or --all')
        return 1

    total_inserts = 0
    total_deletes = 0
    for tab in target_tabs:
        title = tab.get('tabProperties', {}).get('title','')
        tab_id = tab.get('tabProperties', {}).get('tabId')
        if not tab_id:
            continue
        elements = collect_paragraphs(tab)
        full_tab_text = ''.join(paragraph_text(e) for e in elements)
        deletions: List[Tuple[int,int]] = []
        heading_positions = []
        for elem in elements:
            para = elem.get('paragraph')
            if not para:
                continue
            style = para.get('paragraphStyle', {}).get('namedStyleType')
            raw_text = paragraph_text(elem).strip('\n')
            if style and style.startswith('HEADING_'):
                core = raw_text
                for i,ch in enumerate(core):
                    if ch in BOX_CHARS:
                        core = core[:i]
                        break
                lower = normalize(core.replace('🧑‍🎓','').replace('📨','').replace('🧑‍🏫','').replace('🤖',''))
                if any(c in BOX_CHARS for c in raw_text) and lower == '':
                    start = elem.get('startIndex'); end = elem.get('endIndex')
                    if start is not None and end is not None and end>start:
                        deletions.append((start, end-1))
                    continue
                for human_label, key in ZONE_MAP.items():
                    if lower.startswith(human_label):
                        insert_at = elem.get('endIndex')
                        if insert_at:
                            heading_positions.append((key, insert_at))
        to_insert = []
        for key, insert_at in heading_positions:
            if f"<<<ZONE:{key}:BEGIN>>>" in full_tab_text:
                continue
            to_insert.append((insert_at, MARKER_TEMPLATE.format(key=key)))
        if not deletions and not to_insert:
            continue
        print(f"Tab: {title} -> delete {len(deletions)}; insert {len(to_insert)}")
        if args.dry_run:
            for s,e in sorted(deletions, key=lambda x: x[0], reverse=True):
                print(f"  DELETE {s}..{e}")
            for i_at, blk in sorted(to_insert, key=lambda x: x[0]):
                print(f"  INSERT @{i_at}: {blk.splitlines()[0]} ...")
            continue
        # Phase 1 deletions
        delete_reqs = [ {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': s, 'endIndex': e}}} for s,e in sorted(deletions, key=lambda x: x[0], reverse=True) ]
        if delete_reqs:
            try:
                docs.documents().batchUpdate(documentId=args.doc, body={'requests': delete_reqs}).execute()
            except HttpError as e:
                print(f"  ❌ Deletions failed: {e}")
                continue
        # Refetch this tab only if we inserted anything
        new_inserts = []
        if to_insert:
            try:
                refreshed = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
                ref_map = flatten_tabs(refreshed)
                tab2 = ref_map.get(normalize(title))
                if tab2:
                    elems2 = collect_paragraphs(tab2)
                    for elem in elems2:
                        para = elem.get('paragraph')
                        if not para:
                            continue
                        style = para.get('paragraphStyle', {}).get('namedStyleType')
                        if not (style and style.startswith('HEADING_')):
                            continue
                        raw_text2 = paragraph_text(elem).strip('\n')
                        core2 = raw_text2
                        for i,ch in enumerate(core2):
                            if ch in BOX_CHARS:
                                core2 = core2[:i]
                                break
                        lower2 = normalize(core2.replace('🧑‍🎓','').replace('📨','').replace('🧑‍🏫','').replace('🤖',''))
                        for human_label, key in ZONE_MAP.items():
                            if lower2.startswith(human_label):
                                if f"<<<ZONE:{key}:BEGIN>>>" in paragraph_text(elem):
                                    continue
                                new_inserts.append((elem.get('endIndex'), MARKER_TEMPLATE.format(key=key)))
            except HttpError as e:
                print(f"  ❌ Refetch failed: {e}")
                continue
        if new_inserts:
            insert_reqs = [ {'insertText': {'location': {'tabId': tab_id, 'index': idx}, 'text': block}} for idx,block in sorted(new_inserts, key=lambda x: x[0], reverse=True) ]
            try:
                docs.documents().batchUpdate(documentId=args.doc, body={'requests': insert_reqs}).execute()
            except HttpError as e:
                print(f"  ❌ Insert failed: {e}")
                continue
        total_inserts += len(new_inserts)
        total_deletes += len(deletions)
    if args.dry_run:
        print('Dry-run complete.')
    else:
        print(f'✅ Completed. Total deletes: {total_deletes}; total marker blocks inserted: {total_inserts}.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
