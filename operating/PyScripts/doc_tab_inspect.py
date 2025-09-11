#!/usr/bin/env python3
"""Inspect a specific Google Doc tab (with the new tabs feature) and print a concise summary.

Usage:
  python3 doc_tab_inspect.py --doc <DOCUMENT_ID> --tab "Argumentative research paper"
  python3 doc_tab_inspect.py --doc <DOCUMENT_ID>            # list all tabs
  python3 doc_tab_inspect.py --doc <DOCUMENT_ID> --tab "Argumentative research paper" --full  # full text dump

Outputs:
  - Lists discovered tabs when --tab not provided.
  - For a chosen tab, prints:
      * Basic stats (paragraph count, tables count)
      * Ordered headings (with start indices)
      * First N (default 25) non-empty lines or full text if --full
      * Detected potential zone markers (<<<ZONE:...>>>) if present

Relies on existing auth_setup.authenticate_google_apis helper.
"""
from __future__ import annotations
import argparse
import os
import sys
import unicodedata
from typing import Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore


def normalize(title: str) -> str:
    nf = unicodedata.normalize('NFKC', title or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    mapping: Dict[str, dict] = {}
    def add(tab: dict):
        props = tab.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            mapping[normalize(title)] = tab
        for c in tab.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return mapping


def extract_tab_summary(tab: dict):
    body = tab.get('documentTab', {}).get('body', {})
    content = body.get('content', []) or []
    headings = []
    lines = []
    tables = 0
    zone_markers = []
    for elem in content:
        if 'table' in elem:
            tables += 1
            continue
        para = elem.get('paragraph')
        if not para:
            continue
        style = para.get('paragraphStyle', {}).get('namedStyleType')
        text = ''.join(r.get('textRun', {}).get('content', '') for r in para.get('elements', []) if r.get('textRun'))
        clean = text.strip('\n')
        if not clean.strip():
            continue
        if style and style.startswith('HEADING_'):
            headings.append((clean.strip(), style, elem.get('startIndex')))
        if clean.startswith('<<<ZONE:') and clean.endswith('>>>'):
            zone_markers.append(clean)
        lines.append(clean)
    return {
        'headings': headings,
        'lines': lines,
        'tables': tables,
        'zone_markers': zone_markers,
        'paragraphs': len(lines)
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', help='Tab title to inspect (case-insensitive)')
    ap.add_argument('--full', action='store_true', help='Print full lines instead of head sample')
    ap.add_argument('--limit', type=int, default=25, help='Number of lines to show when not full')
    args = ap.parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('Auth failed: no credentials.')
        return 1
    docs = build('docs', 'v1', credentials=creds)
    try:
        doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
    except HttpError as e:
        print(f'Fetch failed: {e}')
        return 1

    tabs = flatten_tabs(doc)
    if not args.tab:
        print(f'Discovered {len(tabs)} tabs:')
        for norm, t in tabs.items():
            title = t.get('tabProperties', {}).get('title', '')
            print(' -', title)
        print('\nUse --tab "<title>" to inspect one.')
        return 0

    norm_target = normalize(args.tab)
    tab = tabs.get(norm_target)
    if not tab:
        print('Tab not found. Available titles:')
        for t in tabs.values():
            print(' -', t.get('tabProperties', {}).get('title'))
        return 1

    title = tab.get('tabProperties', {}).get('title')
    summary = extract_tab_summary(tab)
    print(f'=== Tab: {title} ===')
    print(f"Paragraphs: {summary['paragraphs']} | Tables: {summary['tables']}")
    if summary['headings']:
        print('Headings:')
        for h, style, idx in summary['headings']:
            print(f'  [{style}] @{idx}: {h}')
    else:
        print('No headings detected.')
    if summary['zone_markers']:
        print('Zone markers:')
        for z in summary['zone_markers']:
            print(' ', z)
    sample = summary['lines'] if args.full else summary['lines'][:args.limit]
    print('\n--- Text Sample ---')
    for ln in sample:
        print(ln)
    if not args.full and len(summary['lines']) > args.limit:
        remaining = len(summary['lines']) - args.limit
        print(f"... ({remaining} more lines hidden, use --full)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
