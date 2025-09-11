#!/usr/bin/env python3
"""Scan Google Doc tabs for zone markers and report change hashes.

Zone markers:
  <<<ZONE:<KEY>:BEGIN>>>
  ... content ...
  <<<ZONE:<KEY>:END>>>

Output:
  Table of zones with char count and first 60 chars, new/changed/unchanged status.

State file (JSON): operating/interaction_state/ai_zone_state.json
Structure:
{
  "document_id": "...",
  "version": 1,
  "tabs": {
     "argumentative research paper": {
        "zones": {
           "STUDENT_WORKSPACE": {"hash": "sha256:...", "last_ai_comment_iso": null}
        }
     }
  }
}

Usage:
  python3 zone_scanner.py --doc <ID> --tab "Argumentative research paper"
  python3 zone_scanner.py --doc <ID> --all --update-state  # writes baseline
"""
from __future__ import annotations
import argparse, json, os, sys, unicodedata, hashlib, datetime as dt
from typing import Dict, List, Tuple, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

STATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'interaction_state', 'ai_zone_state.json')
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), '..', 'interaction_state', 'snapshots')

BEGIN_PREFIX = '<<<ZONE:'
END_PREFIX = '<<<ZONE:'  # same start; we differentiate by suffix
BEGIN_SUFFIX = ':BEGIN>>>'
END_SUFFIX = ':END>>>'


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

def extract_zones_from_tab(tab: dict) -> List[Tuple[str,str]]:
    # Returns list of (zone_key, inner_text)
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    lines: List[str] = []
    for elem in content:
        t = paragraph_text(elem)
        if t:
            # Split by newline to ensure markers alone on lines are handled
            for ln in t.splitlines():
                lines.append(ln.rstrip('\r'))
    zones: List[Tuple[str,str]] = []
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if ln.startswith(BEGIN_PREFIX) and ln.endswith(BEGIN_SUFFIX):
            key = ln[len(BEGIN_PREFIX):-len(BEGIN_SUFFIX)]
            # Accumulate until matching END
            buf: List[str] = []
            j = i + 1
            while j < len(lines):
                ln2 = lines[j].strip()
                if ln2 == f"{BEGIN_PREFIX}{key}{END_SUFFIX.replace('BEGIN','END')}":
                    break
                buf.append(lines[j])
                j += 1
            if j < len(lines):  # found end
                inner = '\n'.join(buf).strip()
                zones.append((key, inner))
                i = j  # will advance by one below
        i += 1
    return zones

def load_state(document_id: str) -> dict:
    if not os.path.exists(STATE_PATH):
        return {"document_id": document_id, "version": 1, "tabs": {}}
    try:
        with open(STATE_PATH,'r',encoding='utf-8') as f:
            data = json.load(f)
        if data.get('document_id') != document_id:
            # Different document, archive old
            ts = dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')
            os.makedirs(SNAPSHOT_DIR, exist_ok=True)
            with open(os.path.join(SNAPSHOT_DIR, f"otherdoc_{ts}.json"),'w',encoding='utf-8') as o:
                json.dump(data,o,indent=2,ensure_ascii=False)
            return {"document_id": document_id, "version": 1, "tabs": {}}
        return data
    except Exception:
        return {"document_id": document_id, "version": 1, "tabs": {}}

def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    # snapshot
    ts = dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(os.path.join(SNAPSHOT_DIR, f"snapshot_{ts}.json"),'w',encoding='utf-8') as s:
        json.dump(state,s,indent=2,ensure_ascii=False)
    with open(STATE_PATH,'w',encoding='utf-8') as f:
        json.dump(state,f,indent=2,ensure_ascii=False)

def hash_text(txt: str) -> str:
    cleaned = '\n'.join(line.rstrip() for line in txt.strip().splitlines())
    h = hashlib.sha256(cleaned.encode('utf-8')).hexdigest()
    return f"sha256:{h}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', action='append', help='Specific tab(s) to scan')
    ap.add_argument('--all', action='store_true', help='Scan all tabs')
    ap.add_argument('--update-state', action='store_true', help='Persist new hashes to state file')
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
    target_tabs = []
    if args.all:
        target_tabs = list(tabs.values())
    elif args.tab:
        for t in args.tab:
            obj = tabs.get(normalize(t))
            if obj: target_tabs.append(obj)
            else: print(f"⚠️ Tab not found: {t}")
    else:
        print('Provide --tab or --all')
        return 1

    state = load_state(args.doc)
    changed_any = False

    rows_out: List[Tuple[str,str,str,int,str]] = []  # tab, zone, status, chars, preview
    for tab in target_tabs:
        title = tab.get('tabProperties', {}).get('title','')
        norm = normalize(title)
        zones = extract_zones_from_tab(tab)
        if not zones:
            continue
        tab_state = state.setdefault('tabs', {}).setdefault(norm, {}).setdefault('zones', {})
        for key, inner in zones:
            h = hash_text(inner)
            prev = tab_state.get(key, {}).get('hash')
            status = 'unchanged'
            if prev is None:
                status = 'new'
            elif prev != h:
                status = 'changed'
            if status != 'unchanged':
                changed_any = True
            rows_out.append((title, key, status, len(inner), inner[:60].replace('\n',' ')))
            if args.update_state:
                tab_state[key] = tab_state.get(key, {})
                tab_state[key]['hash'] = h
                tab_state[key].setdefault('last_ai_comment_iso', None)

    # Print report
    print(f"Zones scanned: {len(rows_out)}")
    for title, key, status, chars, preview in rows_out:
        print(f"[{status.upper():9}] {title} :: {key:24} chars={chars:4} preview={preview}")
    if args.update_state:
        save_state(state)
        print(f"State written to {STATE_PATH}")
    else:
        print("(Dry scan – state not updated; use --update-state to persist)")
    if not rows_out:
        print('No zones found.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
