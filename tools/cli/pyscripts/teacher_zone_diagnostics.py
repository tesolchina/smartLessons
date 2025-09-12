#!/usr/bin/env python3
"""Diagnose TEACHER zones vs last replied hash.

Shows for each tab:
  - current teacher hash
  - stored replied hash (if any)
  - status: new / changed / same / empty / missing
  - first 120 chars of teacher content

Usage:
  python3 teacher_zone_diagnostics.py --doc <ID> --all
  python3 teacher_zone_diagnostics.py --doc <ID> --tab "Argumentative research paper"
"""
from __future__ import annotations
import argparse, os, sys, json, hashlib, unicodedata
from typing import Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BEGIN_PREFIX = '<<<ZONE:'
BEGIN_SUFFIX = ':BEGIN>>>'
END_SUFFIX = ':END>>>'
PLACEHOLDER = '(Write here – add content)'
STATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'interaction_state', 'teacher_response_state.json')


def norm_title(t: str) -> str:
    import unicodedata
    nf = unicodedata.normalize('NFKC', t or '')
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    def add(t: dict):
        props = t.get('tabProperties', {})
        title = props.get('title','')
        if title:
            out[norm_title(title)] = t
        for c in t.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return out


def paragraph_text(elem: dict) -> str:
    para = elem.get('paragraph')
    if not para:
        return ''
    parts = []
    for r in para.get('elements', []) or []:
        tr = r.get('textRun')
        if tr:
            parts.append(tr.get('content',''))
    return ''.join(parts)


def extract_zone(tab: dict, key: str) -> str:
    begin = f"{BEGIN_PREFIX}{key}{BEGIN_SUFFIX}"
    end = f"{BEGIN_PREFIX}{key}{END_SUFFIX.replace('BEGIN','END')}"
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    lines: List[str] = []
    collecting = False
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        for raw_line in paragraph_text(elem).splitlines():
            s = raw_line.strip()
            if s == begin:
                collecting = True
                continue
            if s == end:
                collecting = False
                continue
            if collecting:
                lines.append(raw_line.rstrip('\r'))
    return '\n'.join(lines).strip()


def hash_text(txt: str) -> str:
    if not txt.strip():
        return ''
    cleaned = '\n'.join(l.rstrip() for l in txt.strip().splitlines())
    return 'sha256:' + hashlib.sha256(cleaned.encode('utf-8')).hexdigest()


def load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {"tabs":{},"document_id":None,"version":1}
    try:
        with open(STATE_PATH,'r',encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"tabs":{},"document_id":None,"version":1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', action='append')
    ap.add_argument('--all', action='store_true')
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
    targets = []
    if args.all:
        targets = list(tabs.values())
    elif args.tab:
        for t in args.tab:
            ob = tabs.get(norm_title(t))
            if ob:
                targets.append(ob)
            else:
                print(f"⚠️ Tab not found: {t}")
    else:
        print('Provide --tab or --all')
        return 1

    state = load_state()
    print("Tab | Status | CurrentHash(8) | StoredHash(8) | Preview")
    print('-'*90)
    for tab in targets:
        title = tab.get('tabProperties', {}).get('title','')
        norm = norm_title(title)
        teacher = extract_zone(tab, 'TEACHER')
        if not teacher or teacher.strip() == PLACEHOLDER:
            status = 'empty'
            chash = ''
        else:
            chash = hash_text(teacher)
            stored = state.get('tabs', {}).get(norm, {}).get('teacher_hash_replied')
            if not stored:
                status = 'new'
            elif stored == chash:
                status = 'same'
            else:
                status = 'changed'
        stored_short = state.get('tabs', {}).get(norm, {}).get('teacher_hash_replied') or ''
        preview = teacher.replace('\n',' ')[:70]
        print(f"{title} | {status:7} | {chash[7:15] if chash else '--------'} | {stored_short[7:15] if stored_short else '--------'} | {preview}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
