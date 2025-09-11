#!/usr/bin/env python3
"""Fix known truncated zone headings in a Google Doc tab.

Specifically restores:
  🧑‍🎓 Student Workspa  -> 🧑‍🎓 Student Workspace
  🧑‍🏫 Instructor Feedba -> 🧑‍🏫 Instructor Feedback

Usage:
  python3 fix_truncated_headings.py --doc <ID> --tab "Argumentative research paper" --dry-run
  python3 fix_truncated_headings.py --doc <ID> --tab "Argumentative research paper"
"""
from __future__ import annotations
import argparse, os, sys, unicodedata
from typing import Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

TRUNCATED_MAP: Dict[str, str] = {
    '🧑‍🎓 Student Workspa': '🧑‍🎓 Student Workspace',
    '🧑‍🏫 Instructor Feedba': '🧑‍🏫 Instructor Feedback',
    '🧑‍🏫 Instructor Feedckba': '🧑‍🏫 Instructor Feedback',
}

def normalize(title: str) -> str:
    nf = unicodedata.normalize('NFKC', title or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')

def flatten_tabs(doc: dict):
    m = {}
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
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []

    requests = []
    fixes = 0
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        style = para.get('paragraphStyle', {}).get('namedStyleType')
        if not (style and style.startswith('HEADING_')):
            continue
        text = paragraph_text(elem)
        # Remove trailing newline for compare
        base = text.rstrip('\n')
        for truncated, full in TRUNCATED_MAP.items():
            if base == truncated:
                # Insert missing suffix at end before newline.
                if full.startswith(truncated):
                    suffix = full[len(truncated):]
                    if not suffix:
                        continue
                    insert_at = elem.get('endIndex') - 1  # before newline
                    if insert_at:
                        requests.append({'insertText': {'location': {'tabId': tab_id, 'index': insert_at}, 'text': suffix}})
                        fixes += 1
                else:
                    # fallback: replace entire paragraph
                    start = elem.get('startIndex'); end = elem.get('endIndex')
                    if start and end and end>start:
                        requests.append({'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': start, 'endIndex': end-1}}})
                        requests.append({'insertText': {'location': {'tabId': tab_id, 'index': start}, 'text': full + '\n'}})
                        fixes += 1
    if not requests:
        print('No truncated headings found.')
        return 0

    print(f'Planned fixes: {fixes}')
    if args.dry_run:
        for r in requests:
            if 'insertText' in r:
                print('  INSERT', r['insertText']['text'])
            else:
                rng = r['deleteContentRange']['range']
                print(f"  DELETE {rng['startIndex']}..{rng['endIndex']}")
        return 0

    # Execute
    try:
        docs.documents().batchUpdate(documentId=args.doc, body={'requests': requests}).execute()
    except HttpError as e:
        print(f'Update failed: {e}')
        return 1
    print('✅ Headings fixed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
