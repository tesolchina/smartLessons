#!/usr/bin/env python3
"""Simplify all tabs to a uniform three-zone structure (STUDENT / TEACHER / AI).

Actions per tab (default all tabs unless --tab specified multiple times):
  1. Parse existing zone markers (<<<ZONE:<KEY>:BEGIN/END>>>).
  2. Map legacy zone keys to canonical: STUDENT, TEACHER, AI.
  3. Concatenate content by target zone preserving original order across legacy zones.
     - If multiple legacy zones map to same canonical zone, insert delimiter lines:
       --- Merged from <OLD_KEY> ---
  4. Remove ALL tables (capture plain-text fallback appended to STUDENT zone).
  5. Replace entire tab body with only the three canonical zones (in order STUDENT, TEACHER, AI).
  6. If a zone has no content, insert placeholder line: (Write here – add content)

Safety:
  - Dry-run mode prints planned operations; no document changes.
  - Full replacement of tab body is destructive (original non-zone headings/sections removed).
  - Use --preserve-outside to keep non-zone text at the top (wrapped above zones).

Usage:
  Dry run all tabs:
    python3 simplify_structure.py --doc <ID> --dry-run
  Apply to specific tab:
    python3 simplify_structure.py --doc <ID> --tab "Argumentative research paper"
  Apply to all with outside content preserved:
    python3 simplify_structure.py --doc <ID> --all --preserve-outside
"""
from __future__ import annotations
import argparse, os, sys, unicodedata, datetime as dt
from typing import Dict, List, Tuple, Optional
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BEGIN_PREFIX = '<<<ZONE:'
BEGIN_SUFFIX = ':BEGIN>>>'
END_SUFFIX = ':END>>>'
PLACEHOLDER = '(Write here – add content)'
MERGE_DELIM = '--- Merged from {legacy} ---'

LEGACY_MAP = {
    # student
    'STUDENT_WORKSPACE': 'STUDENT',
    'STUDENT_NOTES': 'STUDENT',
    'STUDENT': 'STUDENT',
    # instructor/teacher
    'INSTRUCTOR_FEEDBACK': 'TEACHER',
    'FEEDBACK': 'TEACHER',
    'MESSAGES_TO_INSTRUCTOR': 'TEACHER',
    'MESSAGES_TO_TEACHER': 'TEACHER',
    'TEACHER': 'TEACHER',
    # ai
    'AI_SUPPORT_COMMENTS': 'AI',
    'AI_SUPPORT': 'AI',
    'AI_SUGGESTIONS': 'AI',
    'AI': 'AI',
}

CANONICAL_ORDER = ['STUDENT', 'TEACHER', 'AI']


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
            out.append(tr.get('content', ''))
    return ''.join(out)


def extract_full_text_lines(tab: dict) -> List[Tuple[str, dict]]:
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    lines: List[Tuple[str, dict]] = []  # (line_text, raw_elem)
    for elem in content:
        if 'paragraph' in elem:
            txt = paragraph_text(elem)
            if txt:
                for ln in txt.splitlines():
                    lines.append((ln.rstrip('\r'), elem))
        elif 'table' in elem:
            # Represent table as special placeholder line; actual extraction later.
            lines.append(('__TABLE_BLOCK__', elem))
    return lines


def extract_tables(tab: dict) -> List[dict]:
    return [elem['table'] for elem in tab.get('documentTab', {}).get('body', {}).get('content', []) if 'table' in elem]


def table_plain_text(table: dict) -> str:
    rows_out: List[str] = []
    for row in table.get('tableRows', []) or []:
        cell_texts: List[str] = []
        for cell in row.get('tableCells', []) or []:
            pieces: List[str] = []
            for celem in cell.get('content', []) or []:
                pieces.append(paragraph_text(celem))
            cell_texts.append(' '.join(p.strip() for p in pieces if p.strip()))
        rows_out.append(' | '.join(cell_texts))
    return '\n'.join(rows_out).strip()


def parse_legacy_zones(lines: List[Tuple[str, dict]]) -> Dict[str, List[str]]:
    zones: Dict[str, List[str]] = {}
    current_key: Optional[str] = None
    buf: List[str] = []
    for line, _ in lines:
        stripped = line.strip()
        if stripped.startswith(BEGIN_PREFIX) and stripped.endswith(BEGIN_SUFFIX):
            # flush previous (should not happen if well-formed)
            if current_key and buf:
                zones.setdefault(current_key, []).append('\n'.join(buf).strip())
            buf = []
            raw_key = stripped[len(BEGIN_PREFIX):-len(BEGIN_SUFFIX)]
            current_key = raw_key.upper()
            continue
        if current_key and stripped == f"{BEGIN_PREFIX}{current_key}{END_SUFFIX.replace('BEGIN','END')}":
            zones.setdefault(current_key, []).append('\n'.join(buf).strip())
            buf = []
            current_key = None
            continue
        if current_key:
            buf.append(line)
    return zones


def build_canonical_content(legacy_zone_blobs: Dict[str, List[str]], tables_plain: List[str], preserve_outside_text: str) -> str:
    buckets: Dict[str, List[str]] = {k: [] for k in CANONICAL_ORDER}

    # Migrate legacy zones
    for legacy_key, blobs in legacy_zone_blobs.items():
        target = LEGACY_MAP.get(legacy_key, None)
        if not target:
            # Unmapped zones go to STUDENT by default
            target = 'STUDENT'
        first = True
        for blob in blobs:
            if blob:
                if not first:
                    buckets[target].append(MERGE_DELIM.format(legacy=legacy_key))
                else:
                    # Add a migration marker only once per legacy zone if multiple blobs
                    if len(blobs) > 1:
                        buckets[target].append(MERGE_DELIM.format(legacy=legacy_key))
                buckets[target].append(blob)
                first = False

    # Append removed table fallbacks to STUDENT
    for idx, plain in enumerate(tables_plain, start=1):
        if plain:
            buckets['STUDENT'].append(f"[Removed table {idx}]\n{plain}")

    # Construct final text
    parts: List[str] = []
    if preserve_outside_text.strip():
        parts.append(preserve_outside_text.rstrip())
        parts.append('')
    for key in CANONICAL_ORDER:
        body = '\n\n'.join(x.strip() for x in buckets[key] if x.strip())
        if not body:
            body = PLACEHOLDER
        parts.append(f"{BEGIN_PREFIX}{key}{BEGIN_SUFFIX}")
        parts.append(body)
        parts.append(f"{BEGIN_PREFIX}{key}{END_SUFFIX.replace('BEGIN','END')}")
        parts.append('')
    return '\n'.join(parts).rstrip() + '\n'


def collect_outside_text(lines: List[Tuple[str, dict]]) -> str:
    # Currently we drop all non-zone, non-table text if not preserving. When preserving, gather those lines not inside zones or table placeholder
    outside: List[str] = []
    in_zone = False
    current_key: Optional[str] = None
    for line, _ in lines:
        stripped = line.strip()
        if stripped.startswith(BEGIN_PREFIX) and stripped.endswith(BEGIN_SUFFIX):
            in_zone = True
            current_key = stripped[len(BEGIN_PREFIX):-len(BEGIN_SUFFIX)]
            continue
        if in_zone and current_key and stripped == f"{BEGIN_PREFIX}{current_key}{END_SUFFIX.replace('BEGIN','END')}":
            in_zone = False
            current_key = None
            continue
        if not in_zone and stripped and stripped != '__TABLE_BLOCK__':
            outside.append(line)
    return '\n'.join(outside).strip()


def simplify_tab(docs_service, doc_id: str, tab: dict, preserve_outside: bool, dry_run: bool) -> Tuple[str, Dict[str, int]]:
    title = tab.get('tabProperties', {}).get('title','')
    tab_id = tab.get('tabProperties', {}).get('tabId')
    lines = extract_full_text_lines(tab)
    legacy_zones = parse_legacy_zones(lines)
    tables = extract_tables(tab)
    tables_plain = [table_plain_text(t) for t in tables]

    outside_text = collect_outside_text(lines) if preserve_outside else ''

    # Detect if already canonical (only canonical keys present, no tables, no outside text unless preserve requested)
    legacy_keys = set(legacy_zones.keys())
    already_canonical = legacy_keys != set() and legacy_keys.issubset(set(CANONICAL_ORDER)) and not tables_plain and (not outside_text.strip())
    canonical_text = '' if already_canonical else build_canonical_content(legacy_zones, tables_plain, outside_text)

    stats = {
        'legacy_zone_count': sum(len(v) for v in legacy_zones.values()),
        'legacy_zone_types': len(legacy_zones),
        'tables_removed': len(tables),
        'student_chars': len(canonical_text),
    }

    if dry_run:
        # Mark skip in stats if already canonical
        if already_canonical:
            stats['skip'] = 1
        return title, stats

    # Delete entire body (excluding final document end index may require capturing last endIndex)
    body = tab.get('documentTab', {}).get('body', {})
    content = body.get('content', []) or []
    if already_canonical:
        # Nothing to do
        return title, stats

    if content:
        first_start = content[0].get('startIndex', 1)
        last_end = content[-1].get('endIndex', first_start + 1)
        # Exclude the trailing newline sentinel: use last_end - 1
        deletion_end = max(first_start, last_end - 1)
        if deletion_end > first_start:
            delete_req = {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': first_start, 'endIndex': deletion_end}}}
            insert_req = {'insertText': {'location': {'tabId': tab_id, 'index': first_start}, 'text': canonical_text}}
            try:
                docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [delete_req, insert_req]}).execute()
            except HttpError as e:
                print(f"  ❌ Failed simplifying tab '{title}': {e}")
    return title, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tab', action='append', help='Specific tab title (can repeat)')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--preserve-outside', action='store_true', help='Keep non-zone non-table text at top')
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
    if args.all:
        targets = list(tabs.values())
    elif args.tab:
        for t in args.tab:
            obj = tabs.get(normalize(t))
            if obj:
                targets.append(obj)
            else:
                print(f"⚠️ Tab not found: {t}")
    else:
        print('Provide --tab or --all')
        return 1

    summary: List[Tuple[str, Dict[str,int]]] = []
    for tab in targets:
        title, stats = simplify_tab(docs, args.doc, tab, args.preserve_outside, args.dry_run)
        summary.append((title, stats))

    print(f"Tabs processed: {len(summary)} (dry-run={args.dry_run})")
    for title, st in summary:
        print(f"- {title}: legacy_zone_types={st['legacy_zone_types']} legacy_zone_blobs={st['legacy_zone_count']} tables_removed={st['tables_removed']}")

    if args.dry_run:
        print('No changes applied.')
    else:
        print('✅ Simplification attempt complete (check for any ❌ lines above).')
        print('Consider re-running zone_scanner.py --all --update-state to rebuild hashes.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
