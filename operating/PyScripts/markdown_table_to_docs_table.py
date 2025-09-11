#!/usr/bin/env python3
"""Convert a Markdown table inside a zone (default AI) of a Google Doc tab into a real Google Docs table.

Workflow:
 1. Fetch document (includeTabsContent).
 2. Locate target tab and zone markers: <<<ZONE:AI:BEGIN>>> / <<<ZONE:AI:END>>>
 3. Scan zone paragraphs for first contiguous Markdown table block (lines starting and ending with '|').
 4. Parse header, separator line, and subsequent rows.
 5. BatchUpdate: delete original markdown block, insert an empty table at same location.
 6. Re-fetch doc, locate inserted table element by startIndex, then populate cell texts.

Usage:
  python3 markdown_table_to_docs_table.py --doc <DOC_ID> --tab "Membership and admin"
  Dry run (parsing only):
  python3 markdown_table_to_docs_table.py --doc <DOC_ID> --tab "Membership and admin" --dry-run

Limitations:
  - Converts only the first markdown table in the specified zone.
  - Assumes simple pipe-delimited table with header + separator line.
  - Does not preserve inline formatting.
"""
from __future__ import annotations
import argparse, os, sys, re, json
from typing import List, Tuple, Optional

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(SCRIPT_DIR, '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

BEGIN_PREFIX = '<<<ZONE:'
BEGIN_SUFFIX = ':BEGIN>>>'
END_SUFFIX = ':END>>>'


def parse_args():
    ap = argparse.ArgumentParser(description="Convert markdown table in a zone to Docs table")
    ap.add_argument('--doc', required=True, help='Google Doc ID')
    ap.add_argument('--tab', required=True, help='Tab title')
    ap.add_argument('--zone', default='AI', help='Zone key (default AI)')
    ap.add_argument('--dry-run', action='store_true')
    return ap.parse_args()


def flatten_tabs(doc: dict):
    mapping = {}
    def add(t):
        props = t.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            key = title.lower().strip()
            mapping[key] = t
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


def locate_zone_paragraphs(tab: dict, zone: str) -> List[Tuple[int, int, str]]:
    """Return list of (startIndex, endIndex, text) paragraphs inside the given zone."""
    content = tab.get('documentTab', {}).get('body', {}).get('content', []) or []
    inside = False
    begin_line = f"{BEGIN_PREFIX}{zone}{BEGIN_SUFFIX}"
    end_line = f"{BEGIN_PREFIX}{zone}{END_SUFFIX}".replace('BEGIN','END')
    out: List[Tuple[int,int,str]] = []
    for elem in content:
        para = elem.get('paragraph')
        if not para:
            continue
        start = elem.get('startIndex'); end = elem.get('endIndex')
        if start is None or end is None:
            continue
        text_full = paragraph_text(elem)
        stripped = text_full.strip()
        if stripped == begin_line:
            inside = True
            continue
        if stripped == end_line:
            inside = False
            continue
        if inside:
            out.append((start, end, text_full))
    return out


TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")


def detect_markdown_table(paragraphs: List[Tuple[int,int,str]]):
    """Return (start_index, end_index, lines, header, rows) or None."""
    lines_block: List[Tuple[int,int,str]] = []
    in_block = False
    for i, (s, e, txt) in enumerate(paragraphs):
        raw = txt.rstrip('\n')
        if TABLE_LINE_RE.match(raw):
            if not in_block:
                lines_block = []
                in_block = True
            lines_block.append((s, e, raw.strip()))
        else:
            if in_block:
                break
    if not lines_block:
        return None
    # Parse lines
    first = lines_block[0][2]
    if len(lines_block) < 2:
        return None
    # header separator detection (---)
    sep_line = lines_block[1][2]
    if '---' not in sep_line:
        return None
    header_cells = [c.strip() for c in first.strip('|').split('|')]
    body_lines = [ln[2] for ln in lines_block[2:]]
    rows = []
    for bl in body_lines:
        cells = [c.strip() for c in bl.strip('|').split('|')]
        if any(cells):
            # pad or trim to header length
            if len(cells) < len(header_cells):
                cells += [''] * (len(header_cells)-len(cells))
            elif len(cells) > len(header_cells):
                cells = cells[:len(header_cells)]
            rows.append(cells)
    start_index = lines_block[0][0]
    end_index = lines_block[-1][1]
    table_lines = [ln[2] for ln in lines_block]
    return start_index, end_index, table_lines, header_cells, rows


def insert_and_populate_table(docs_service, doc_id: str, tab_id: str, start_index: int, header: List[str], rows: List[List[str]]):
    requests = []
    # Insert empty table after deletion at start_index
    requests.append({
        'insertTable': {
            'rows': len(rows) + 1,
            'columns': len(header),
            'location': {'tabId': tab_id, 'index': start_index}
        }
    })
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    # Re-fetch to find table and populate cells
    doc2 = docs_service.documents().get(documentId=doc_id, includeTabsContent=True).execute()
    # Locate table element with matching start_index
    table_elem = None
    target_tab = None
    for t in doc2.get('tabs', []) or []:
        if t.get('tabProperties', {}).get('tabId') == tab_id:
            target_tab = t
            break
    if not target_tab:
        return
    for elem in target_tab.get('documentTab', {}).get('body', {}).get('content', []) or []:
        if elem.get('startIndex') == start_index and 'table' in elem:
            table_elem = elem['table']
            break
    if not table_elem:
        return
    # Collect cell start indices in row-major order
    cell_starts: List[Tuple[int,str]] = []  # (startIndex, text)
    for r_i, row in enumerate(table_elem.get('tableRows', []) or []):
        for c_i, cell in enumerate(row.get('tableCells', []) or []):
            # Each cell has content array; first paragraph startIndex is where we insert text
            cell_content = cell.get('content', []) or []
            if not cell_content:
                continue
            para_elem = cell_content[0]
            p_start = para_elem.get('startIndex')
            if p_start is not None:
                if r_i == 0:
                    text = header[c_i]
                else:
                    text = rows[r_i-1][c_i]
                cell_starts.append((p_start + 1, text))  # +1 to stay inside cell
    insert_reqs = []
    for idx, txt in cell_starts:
        if not txt:
            continue
        insert_reqs.append({'insertText': {'location': {'tabId': tab_id, 'index': idx}, 'text': txt}})
    if insert_reqs:
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': insert_reqs}).execute()


def main():
    args = parse_args()
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
    tab = tabs.get(args.tab.lower().strip())
    if not tab:
        print(f"Tab not found: {args.tab}")
        return 1
    tab_id = tab.get('tabProperties', {}).get('tabId')
    zone = args.zone.upper()
    paras = locate_zone_paragraphs(tab, zone)
    table_info = detect_markdown_table(paras)
    if not table_info:
        print('No markdown table detected in zone.')
        return 0
    start_index, end_index, table_lines, header, rows = table_info
    print(f"Detected table with {len(header)} columns and {len(rows)} data rows.")
    if args.dry_run:
        print('Dry run – parsed content:')
        print(json.dumps({'header': header, 'rows': rows}, indent=2))
        return 0
    # Delete markdown block
    delete_req = {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': start_index, 'endIndex': end_index}}}
    try:
        docs.documents().batchUpdate(documentId=args.doc, body={'requests': [delete_req]}).execute()
    except HttpError as e:
        print(f'Deletion failed: {e}')
        return 1
    # Insert & populate table
    try:
        insert_and_populate_table(docs, args.doc, tab_id, start_index, header, rows)
        print('Conversion complete.')
    except HttpError as e:
        print(f'Insertion failed: {e}')
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
