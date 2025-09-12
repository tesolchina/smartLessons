#!/usr/bin/env python3
"""Remove trailing box-drawing art from heading paragraphs in a specific Google Doc tab.

Example problematic heading:
  🧑‍🎓 Student Workspace╔══════════════════════════════════════╗
We keep everything up to the first box character and delete the rest.

Usage:
  python3 clean_box_headings.py --doc <ID> --tab "Argumentative research paper" --dry-run
  python3 clean_box_headings.py --doc <ID> --tab "Argumentative research paper"
"""
from __future__ import annotations
import argparse, os, sys, unicodedata
from typing import Dict, List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BOX_CHARS = set('╔╗╚╝═║')

def normalize(title: str) -> str:
    nf = unicodedata.normalize('NFKC', title or '')
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
    ap.add_argument('--tab', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('Auth failed.')
        return 1
    docs = build('docs', 'v1', credentials=creds)
    try:
        doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
    except HttpError as e:
        print(f'Fetch failed: {e}')
        return 1

    tab = flatten_tabs(doc).get(normalize(args.tab))
    if not tab:
        print('Tab not found.')
        return 1
    tab_id = tab.get('tabProperties', {}).get('tabId')
    if not tab_id:
        print('Missing tabId.')
        return 1

    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    deletions: List[Tuple[int,int,str]] = []  # start,end,preview
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        style = para.get('paragraphStyle', {}).get('namedStyleType')
        if not (style and style.startswith('HEADING_')):
            continue
        text = paragraph_text(elem)
        # Find first box char index
        cut_pos = None
        for idx, ch in enumerate(text):
            if ch in BOX_CHARS:
                cut_pos = idx
                break
        if cut_pos is None:
            continue
        start_index = elem.get('startIndex')
        end_index = elem.get('endIndex')
        if start_index is None or end_index is None:
            continue
        # Deletion start is start_index + cut_pos
        del_start = start_index + cut_pos
        del_end = end_index - 1  # exclude trailing newline anchor
        if del_end > del_start:
            deletions.append((del_start, del_end, text[cut_pos:50]))

    if not deletions:
        print('Nothing to clean.')
        return 0

    print(f'Planned deletions: {len(deletions)}')
    for s,e,preview in deletions:
        print(f'  {s}..{e} remove "{preview}"')

    if args.dry_run:
        return 0

    # Build delete requests sorted descending by start to keep indices stable
    requests = [ {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': s, 'endIndex': e}}} for s,e,_ in sorted(deletions, key=lambda x: x[0], reverse=True) ]
    try:
        docs.documents().batchUpdate(documentId=args.doc, body={'requests': requests}).execute()
    except HttpError as e:
        print(f'Update failed: {e}')
        return 1
    print('✅ Headings cleaned.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
