#!/usr/bin/env python3
"""Clean residual artifact lines across ALL tabs of the target Google Doc.

Targets:
  - Duplicated merged headings (e.g. "Student WorkspaceStudent Notes", "Instructor FeedbackFeedback | Date",
    "AI Support CommentsAI Suggestion | Date", partial truncated variants like "r FeedbackFeedback | Date").
  - Leftover markdown table header rows and empty table body pipe lines (e.g. "--- | ---", solitary '|').
  - Stray box / dash divider headings composed only of ─ / - (≥5 chars) that immediately precede a zone marker.
  - Artifact lines "AI Suggestion | Date", "Feedback | Date".
  - Convert zone marker and placeholder paragraphs that were accidentally styled as headings back to NORMAL_TEXT.

Safe operations:
  - Only deletes paragraphs fully matching the artifact patterns.
  - Truncation removes trailing duplicated tail after the canonical heading phrase.
  - No changes to tables or legitimate content text.

Usage:
  Dry run:  python3 cleanup_artifacts_all_tabs.py --doc <ID> --dry-run
  Live run: python3 cleanup_artifacts_all_tabs.py --doc <ID>
"""
from __future__ import annotations
import argparse, os, sys, re, unicodedata
from typing import Dict, List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

ZONE_MARKER_PREFIX = '<<<ZONE:'
PLACEHOLDER_LINE = '(Write here – add content)'

# Regex patterns for complete-line deletions (after strip)
DELETE_PATTERNS = [
    re.compile(r'^---+$'),                          # plain markdown hr
    re.compile(r'^[─\-]{5,}$'),                     # long dash/box divider
    re.compile(r'^---(\s*\|\s*---)+$'),           # markdown table header like --- | ---
    re.compile(r'^AI Suggestion \| Date$', re.I),
    re.compile(r'^Feedback \| Date$', re.I),
    re.compile(r'^.*FeedbackFeedback \| Date$', re.I),  # duplicated word artifact line
    re.compile(r'^\|$'),                            # solitary pipe
    re.compile(r'^\|\s+$'),                        # pipe + spaces
]

# Heading duplication fix specs: list of (base_label, duplication_regex)
DUPLICATION_FIXES = [
    ('🧑\u200d🎓 Student Workspace', re.compile(r'Student WorkspaceStudent Notes')),  # includes zero-width joiner char
    ('🧑\u200d🏫 Instructor Feedback', re.compile(r'Instructor FeedbackFeedback \| Date')),  # duplicated feedback
    ('🤖 AI Support Comments', re.compile(r'AI Support CommentsAI Suggestion \| Date')),
    ('🧑\u200d🏫 Instructor Feedback', re.compile(r'r FeedbackFeedback \| Date')),  # partial leading char case
]

# Normalize helper

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
    out: List[str] = []
    for r in para.get('elements', []) or []:
        tr = r.get('textRun')
        if tr:
            out.append(tr.get('content',''))
    return ''.join(out)


def plan_changes_for_tab(tab: dict):
    tab_id = tab.get('tabProperties', {}).get('tabId')
    body = tab.get('documentTab', {}).get('body', {})
    content = body.get('content', []) or []
    deletions: List[Tuple[int,int,str]] = []  # start,end,str
    truncations: List[Tuple[int,int,str]] = []
    downgrades: List[Tuple[int,int]] = []

    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        start = elem.get('startIndex'); end = elem.get('endIndex')
        if start is None or end is None:
            continue
        style = para.get('paragraphStyle', {}).get('namedStyleType') or ''
        raw = paragraph_text(elem)
        text = raw.rstrip('\n')
        stripped = text.strip()
        if not stripped:
            continue

        # Zone markers / placeholder style downgrade
        if style.startswith('HEADING_') and (stripped.startswith(ZONE_MARKER_PREFIX) or stripped == PLACEHOLDER_LINE):
            downgrades.append((start, end))
            continue

        # Deletion patterns (apply to any style if exact match)
        if any(p.match(stripped) for p in DELETE_PATTERNS):
            deletions.append((start, end-1, stripped))
            continue

        # Divider heading right before a zone marker -> remove (heuristic: only dashes and length >=5)
        if style.startswith('HEADING_') and all(ch in '─-' for ch in stripped) and len(stripped) >= 5:
            deletions.append((start, end-1, stripped))
            continue

        # Duplication truncations
        for base_label, dup_re in DUPLICATION_FIXES:
            if base_label in stripped and dup_re.search(stripped):
                # Keep only up to end of base_label occurrence
                keep_pos = stripped.index(base_label) + len(base_label)
                # Map to absolute positions relative to start
                rel = text.index(base_label) + len(base_label)
                del_start = start + rel
                del_end = end - 1
                if del_end > del_start:
                    truncations.append((del_start, del_end, base_label))
                break

    return tab_id, deletions, truncations, downgrades


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
    total_del = total_trunc = total_down = 0
    planned = []  # (title, tab_id, deletions, truncations, downgrades)
    for norm, tab in tab_map.items():
        tab_id, deletions, truncations, downgrades = plan_changes_for_tab(tab)
        if deletions or truncations or downgrades:
            title = tab.get('tabProperties', {}).get('title','')
            planned.append((title, tab_id, deletions, truncations, downgrades))
            total_del += len(deletions)
            total_trunc += len(truncations)
            total_down += len(downgrades)

    print(f"Tabs needing changes: {len(planned)} | deletions: {total_del} | truncations: {total_trunc} | downgrades: {total_down}")
    for title, _tid, dels, truncs, downs in planned:
        print(f"- {title}: del={len(dels)} trunc={len(truncs)} down={len(downs)}")
        if args.dry_run:
            for s,e,t in dels:
                print(f"   DELETE {s}..{e} '{t}'")
            for s,e,b in truncs:
                print(f"   TRUNC {s}..{e} keep '{b}'")
            for s,e in downs:
                print(f"   DOWNGRADE {s}..{e}")

    if args.dry_run or not planned:
        if not planned:
            print('No tabs require artifact cleanup.')
        return 0

    # Perform modifications per tab
    for title, tab_id, dels, truncs, downs in planned:
        # Phase 1: deletions + truncations
        delete_reqs = [ {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': s, 'endIndex': e}}} for s,e,_ in sorted(dels+truncs, key=lambda x: x[0], reverse=True) ]
        if delete_reqs:
            try:
                docs.documents().batchUpdate(documentId=args.doc, body={'requests': delete_reqs}).execute()
            except HttpError as e:
                print(f"  ❌ {title}: deletion phase failed: {e}")
                continue
        # Phase 2: style downgrades (refetch for this tab indices may shift after deletions)
        if downs:
            try:
                refreshed = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
                ref_tab = flatten_tabs(refreshed).get(normalize(title))
                if not ref_tab:
                    continue
                content2 = ref_tab.get('documentTab', {}).get('body', {}).get('content', []) or []
                downgrade_requests = []
                for elem in content2:
                    para = elem.get('paragraph')
                    if not para:
                        continue
                    st = elem.get('startIndex'); en = elem.get('endIndex')
                    if st is None or en is None:
                        continue
                    text2 = paragraph_text(elem).rstrip('\n').strip()
                    if text2.startswith(ZONE_MARKER_PREFIX) or text2 == PLACEHOLDER_LINE:
                        downgrade_requests.append({'updateParagraphStyle': {
                            'range': {'tabId': tab_id, 'startIndex': st, 'endIndex': en},
                            'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                            'fields': 'namedStyleType'
                        }})
                for i in range(0, len(downgrade_requests), 95):
                    docs.documents().batchUpdate(documentId=args.doc, body={'requests': downgrade_requests[i:i+95]}).execute()
            except HttpError as e:
                print(f"  ❌ {title}: downgrade phase failed: {e}")
                continue
    print('✅ Global artifact cleanup complete.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
