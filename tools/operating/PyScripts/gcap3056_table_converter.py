#!/usr/bin/env python3
"""
Convert markdown-like table blocks inside specific Google Doc tabs into real Google Docs tables.

Strategy (per tab):
 1. Fetch doc (includeTabsContent).
 2. Traverse tab body paragraphs, detect table blocks:
      header line containing '|' and next line of dashes/col separators.
 3. Record block (startIndex, endIndex, parsed rows).
 4. For each block sequentially:
      a. deleteContentRange (remove markdown text)
      b. insertTable (rows=len(parsed_rows), columns=len(headers)) at startIndex
      c. refetch doc, locate inserted table, populate cells with insertText
      d. bold header row text

Limitations:
 - Processes sequentially; multiple refetches (slower but safer for index correctness).
 - Skips malformed tables (unequal column counts).

Usage:
  python3 gcap3056_table_converter.py --doc <DOC_ID> --tabs "Collecting publicly available info" "Request info from the gov"
  (omit --tabs to scan all tabs)
"""
from __future__ import annotations
import os, sys, argparse, unicodedata
from typing import List, Dict, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore


def normalize(title: str) -> str:
    return unicodedata.normalize('NFKC', title or '').strip().lower()


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    mapping: Dict[str, dict] = {}
    def add(tab: dict):
        props = tab.get('tabProperties', {})
        t = props.get('title', '')
        if t:
            mapping[normalize(t)] = tab
        for c in tab.get('childTabs', []) or []:
            add(c)
    for t in doc.get('tabs', []) or []:
        add(t)
    return mapping


def extract_paragraph_lines(tab: dict) -> List[Tuple[str, dict]]:
    lines: List[Tuple[str, dict]] = []
    body = tab.get('documentTab', {}).get('body', {})
    for elem in body.get('content', []) or []:
        para = elem.get('paragraph')
        if not para:
            continue
        text_runs = para.get('elements', [])
        text = ''.join(r.get('textRun', {}).get('content', '') for r in text_runs)
        if text.strip():
            lines.append((text, elem))
    return lines


def detect_markdown_tables(lines: List[Tuple[str, dict]]):
    i = 0
    blocks = []
    while i < len(lines)-1:
        header, header_elem = lines[i]
        sep, sep_elem = lines[i+1]
        if '|' in header and '|' in sep and set(sep.replace('|','').strip()) <= {'-',' ',':'}:
            header_cols = [c.strip() for c in header.split('|') if c.strip()]
            sep_cols = [c for c in sep.split('|') if c.strip()]
            if len(header_cols) >=2 and len(sep_cols) >= len(header_cols):
                rows = [header_cols]
                j = i+2
                while j < len(lines):
                    line_txt,_e = lines[j]
                    if '|' in line_txt:
                        row_cols = [c.strip() for c in line_txt.split('|') if c.strip()]
                        if len(row_cols)==len(header_cols):
                            rows.append(row_cols)
                            j+=1
                            continue
                    break
                start_index = header_elem.get('startIndex')
                end_index = lines[j-1][1].get('endIndex')
                if start_index and end_index and end_index> start_index:
                    blocks.append({
                        'start': start_index,
                        'end': end_index,
                        'rows': rows
                    })
                i = j
                continue
        i+=1
    return blocks


def find_table_at_index(tab: dict, approx_start: int):
    body = tab.get('documentTab', {}).get('body', {})
    for elem in body.get('content', []) or []:
        if 'table' in elem and elem.get('startIndex',0) >= approx_start:
            return elem
    return None


def main():
    ap = argparse.ArgumentParser(description='Convert markdown tables to real tables in tabs.')
    ap.add_argument('--doc', required=True)
    ap.add_argument('--tabs', nargs='*')
    args = ap.parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('Auth failed.')
        return 1
    docs = build('docs','v1', credentials=creds)
    try:
        doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
    except HttpError as e:
        print(f'Fetch failed: {e}')
        return 1

    tab_map = flatten_tabs(doc)
    targets = [normalize(t) for t in (args.tabs or tab_map.keys())]
    converted_total = 0
    for norm in targets:
        tab = tab_map.get(norm)
        if not tab:
            print(f'Skip (not found): {norm}')
            continue
        title = tab.get('tabProperties', {}).get('title','')
        lines = extract_paragraph_lines(tab)
        blocks = detect_markdown_tables(lines)
        if not blocks:
            print(f'No markdown tables in tab: {title}')
            continue
        print(f'Processing {len(blocks)} table block(s) in tab: {title}')
        for block in blocks:
            rows = block['rows']
            cols = len(rows[0])
            # delete markdown text
            del_req = [{
                'deleteContentRange': {
                    'range': {
                        'tabId': tab.get('tabProperties',{}).get('tabId'),
                        'startIndex': block['start'],
                        'endIndex': block['end']-1
                    }
                }
            }]
            try:
                docs.documents().batchUpdate(documentId=args.doc, body={'requests': del_req}).execute()
            except HttpError as e:
                print(f' delete failed: {e}')
                continue
            # insert empty table
            ins_req = [{
                'insertTable': {
                    'rows': len(rows),
                    'columns': cols,
                    'location': {
                        'tabId': tab.get('tabProperties',{}).get('tabId'),
                        'index': block['start']
                    }
                }
            }]
            try:
                docs.documents().batchUpdate(documentId=args.doc, body={'requests': ins_req}).execute()
            except HttpError as e:
                print(f' table insert failed: {e}')
                continue
            # refetch tab only
            doc = docs.documents().get(documentId=args.doc, includeTabsContent=True).execute()
            tab_map = flatten_tabs(doc)
            tab = tab_map.get(norm, tab)
            table_elem = find_table_at_index(tab, block['start'])
            if not table_elem:
                print(' could not locate inserted table; skip populate')
                continue
            table = table_elem.get('table', {})
            # Build cell insert requests
            cell_reqs = []
            for r_idx, table_row in enumerate(table.get('tableRows', [])[:len(rows)]):
                cells = table_row.get('tableCells', [])
                for c_idx, cell in enumerate(cells[:cols]):
                    para_elems = cell.get('content', [])
                    if not para_elems:
                        continue
                    first_para = para_elems[0].get('paragraph', {})
                    first_elem = first_para.get('elements', [])
                    if not first_elem:
                        continue
                    cell_start = para_elems[0].get('startIndex')
                    if cell_start is None:
                        continue
                    text = rows[r_idx][c_idx]
                    if not text:
                        continue
                    cell_reqs.append({
                        'insertText': {
                            'location': {
                                'tabId': tab.get('tabProperties',{}).get('tabId'),
                                'index': cell_start + 1
                            },
                            'text': text
                        }
                    })
                    # Bold header row
                    if r_idx == 0:
                        cell_reqs.append({
                            'updateTextStyle': {
                                'range': {
                                    'tabId': tab.get('tabProperties',{}).get('tabId'),
                                    'startIndex': cell_start + 1,
                                    'endIndex': cell_start + 1 + len(text)
                                },
                                'textStyle': {'bold': True},
                                'fields': 'bold'
                            }
                        })
            # Chunk if necessary
            for i in range(0, len(cell_reqs), 90):
                try:
                    docs.documents().batchUpdate(documentId=args.doc, body={'requests': cell_reqs[i:i+90]}).execute()
                except HttpError as e:
                    print(f' populate failed: {e}')
                    break
            else:
                converted_total += 1
    print(f'Completed. Converted {converted_total} table block(s).')
    return 0

if __name__ == '__main__':
    sys.exit(main())
