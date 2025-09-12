#!/usr/bin/env python3
"""Clean the 'Collecting publicly available info' tab.

Actions:
  - Truncate merged headings (Student WorkspaceStudent Notes -> Student Workspace).
  - Truncate Instructor FeedbackFeedback | Date -> Instructor Feedback.
  - Remove stray markdown table remnants and separator headings (---, --- | ---, solitary | lines, AI Suggestion | Date, Feedback | Date, dashed lines of ─, etc.).
  - Downgrade zone marker paragraphs and placeholder '(Write here – add content)' lines from HEADING_* to NORMAL_TEXT.

Safe: Only mutates the specified tab.

Usage:
  python3 cleanup_collecting_public.py --doc <ID> --dry-run
  python3 cleanup_collecting_public.py --doc <ID>
"""
from __future__ import annotations
import argparse, os, sys, re, unicodedata
from typing import List, Tuple, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

TARGET_TAB_NORM = 'collecting publicly available info'

REMOVE_PATTERNS = [
    re.compile(r'^---+$'),
    re.compile(r'^[─﹘\-]{5,}$'),
    re.compile(r'^---(\s*\|\s*---)+$'),
    re.compile(r'^\|$'),
    re.compile(r'^AI Suggestion \| Date$', re.I),
    re.compile(r'^Feedback \| Date$', re.I),
    re.compile(r'^--- \| ---$'),
    re.compile(r'^\|\s+$'),
]

ZONE_MARKER_PREFIX = '<<<ZONE:'
PLACEHOLDER_LINE = '(Write here – add content)'


def normalize(s: str) -> str:
    nf = unicodedata.normalize('NFKC', s or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    m: Dict[str, dict] = {}
    def add(t: dict):
        props = t.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            m[normalize(title)] = t
        for c in t.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return m


def paragraph_text(elem: dict) -> str:
    para = elem.get('paragraph')
    if not para:
        return ''
    out: List[str] = []
    for r in para.get('elements', []) or []:
        tr = r.get('textRun')
        if tr:
            out.append(tr.get('content',''))
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--dry-run', action='store_true')
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

    tab_map = flatten_tabs(doc)
    tab = tab_map.get(TARGET_TAB_NORM)
    if not tab:
        print('Target tab not found.')
        return 1
    tab_id = tab.get('tabProperties', {}).get('tabId')
    if not tab_id:
        print('Missing tabId.')
        return 1

    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []

    deletions: List[Tuple[int,int,str]] = []
    truncations: List[Tuple[int,int,str]] = []  # start,end,desc
    style_downgrades: List[Tuple[int,int]] = []  # start,end for zone marker paragraphs

    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        start = elem.get('startIndex')
        end = elem.get('endIndex')
        if start is None or end is None:
            continue
        style = para.get('paragraphStyle', {}).get('namedStyleType') or ''
        text = paragraph_text(elem).rstrip('\n')
        stripped = text.strip()

        # Skip empty
        if not stripped:
            continue

        # Truncate merged headings
        if stripped.startswith('🧑‍🎓 Student Workspace') and 'Student WorkspaceStudent Notes' in stripped:
            base = '🧑‍🎓 Student Workspace'
            offset = text.index('Student Workspace') + len('Student Workspace')
            del_start = start + offset
            del_end = end - 1
            if del_end > del_start:
                truncations.append((del_start, del_end, 'trim student workspace tail'))
                continue
        if stripped.startswith('🧑‍🏫 Instructor Feedback') and 'Instructor FeedbackFeedback | Date' in stripped:
            base = '🧑‍🏫 Instructor Feedback'
            offset = text.index('Instructor Feedback') + len('Instructor Feedback')
            del_start = start + offset
            del_end = end - 1
            if del_end > del_start:
                truncations.append((del_start, del_end, 'trim instructor feedback tail'))
                continue

        # Delete unwanted headings or artifacts
        if style.startswith('HEADING_'):
            if any(pat.match(stripped) for pat in REMOVE_PATTERNS):
                deletions.append((start, end-1, stripped))
                continue
            # Zone markers & placeholder lines should be downgraded
            if stripped.startswith(ZONE_MARKER_PREFIX) or stripped == PLACEHOLDER_LINE:
                style_downgrades.append((start, end))
                continue
        else:
            # Non-heading artifacts like table leftover lines containing only '|'
            if any(pat.match(stripped) for pat in REMOVE_PATTERNS):
                deletions.append((start, end-1, stripped))
                continue

    print(f"Planned truncations: {len(truncations)}; deletions: {len(deletions)}; downgrades: {len(style_downgrades)}")
    if args.dry_run:
        for s,e,d in truncations:
            print(f"  TRUNCATE {s}..{e} ({d})")
        for s,e,t in deletions:
            print(f"  DELETE {s}..{e} '{t}'")
        for s,e in style_downgrades:
            print(f"  DOWNGRADE {s}..{e}")
        return 0

    requests = []
    # Apply deletions & truncations first (descending)
    for s,e,_ in sorted(deletions + truncations, key=lambda x: x[0], reverse=True):
        requests.append({'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': s, 'endIndex': e}}})
    if requests:
        try:
            docs.documents().batchUpdate(documentId=args.doc, body={'requests': requests}).execute()
        except HttpError as e:
            print(f'Deletion/truncation update failed: {e}')
            return 1
    # Refetch for style downgrades
    if style_downgrades:
        try:
            refreshed = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
            ref_tab = flatten_tabs(refreshed).get(TARGET_TAB_NORM)
            if ref_tab:
                # Build downgrade requests anew using NEW indices (simpler: rescan paragraphs)
                downgrade_requests = []
                content2 = ref_tab.get('documentTab', {}).get('body', {}).get('content', []) or []
                for elem in content2:
                    para = elem.get('paragraph')
                    if not para:
                        continue
                    st = elem.get('startIndex'); en = elem.get('endIndex')
                    if st is None or en is None: continue
                    text2 = paragraph_text(elem).rstrip('\n').strip()
                    if text2.startswith(ZONE_MARKER_PREFIX) or text2 == PLACEHOLDER_LINE:
                        downgrade_requests.append({'updateParagraphStyle': {
                            'range': {'tabId': tab_id, 'startIndex': st, 'endIndex': en},
                            'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                            'fields': 'namedStyleType'
                        }})
                # Chunk
                for i in range(0, len(downgrade_requests), 95):
                    docs.documents().batchUpdate(documentId=args.doc, body={'requests': downgrade_requests[i:i+95]}).execute()
        except HttpError as e:
            print(f'Downgrade phase failed: {e}')
            return 1
    print('✅ Cleanup complete.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
