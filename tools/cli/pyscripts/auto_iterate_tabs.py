#!/usr/bin/env python3
"""Auto-iterate tabs and generate AI replies (one-by-one) with optional elaborate style.

Features:
  - Sequential processing (avoids burst rate to LLM).
  - Per-tab delay (--delay seconds, float).
  - Supports --all, repeated --tab, or --tabs-file list.
  - LLM elaborate style adds elaboration + student questions + next steps.
  - Skips tabs whose TEACHER zone hash already replied unless --force.
  - Optional --limit to cap number of tabs processed in a run.

Usage examples:
  Dry run first 5 changed tabs (elaborate):
    python3 auto_iterate_tabs.py --doc <DOC_ID> --all --use-openrouter --style elaborate --limit 5 --dry-run

  Real run across listed tabs file with 1s delay:
    python3 auto_iterate_tabs.py --doc <DOC_ID> --tabs-file tabs.txt --use-openrouter --style elaborate --delay 1.0
"""
from __future__ import annotations
import argparse, os, sys, time, datetime as dt
from typing import List, Tuple

SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(SCRIPT_DIR, '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

# Reuse logic from responder
from ai_teacher_responder import (
    flatten_tabs,
    normalize_title,
    load_state,
    save_state,
    process_tab,
)  # type: ignore

def parse_args():
    ap = argparse.ArgumentParser(description='Sequentially process tabs and append AI replies.')
    ap.add_argument('--doc', required=True, help='Google Doc ID')
    ap.add_argument('--all', action='store_true', help='Process all tabs')
    ap.add_argument('--tab', action='append', help='Specific tab title (repeatable)')
    ap.add_argument('--tabs-file', help='File listing tab titles (one per line)')
    ap.add_argument('--delay', type=float, default=0.8, help='Seconds delay between tabs (default 0.8)')
    ap.add_argument('--limit', type=int, help='Stop after processing this many tabs (only counting replied)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true', help='Force re-reply even if teacher hash unchanged')
    ap.add_argument('--use-openrouter', action='store_true', help='Use LLM (recommended for elaborate style)')
    ap.add_argument('--style', choices=['default','elaborate'], default='elaborate', help='Reply style (default elaborate)')
    ap.add_argument('--no-table', action='store_true', help='Disable membership table logic')
    return ap.parse_args()


def load_tab_names_from_file(path: str) -> List[str]:
    tabs: List[str] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith('#'): continue
                tabs.append(line)
    except FileNotFoundError:
        print(f"⚠️ tabs file not found: {path}")
    return tabs


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

    tabs_map = flatten_tabs(doc)
    targets = []
    manual: List[str] = []
    if args.tabs_file:
        manual.extend(load_tab_names_from_file(args.tabs_file))
    if args.tab:
        manual.extend(args.tab)

    if args.all:
        targets = list(tabs_map.values())
    elif manual:
        for name in manual:
            obj = tabs_map.get(normalize_title(name))
            if obj:
                targets.append(obj)
            else:
                print(f"⚠️ Tab not found: {name}")
    else:
        print('Provide --all or at least one --tab / --tabs-file entry.')
        return 1

    state = load_state(args.doc)
    replied_count = 0
    results: List[Tuple[str,str]] = []
    start_ts = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"▶️ Auto-iterate start {start_ts} | tabs queued: {len(targets)} | style={args.style} | delay={args.delay}s")

    for idx, tab in enumerate(targets, 1):
        title = tab.get('tabProperties', {}).get('title','')
        print(f"[{idx}/{len(targets)}] Processing: {title} …")
        t_title, status = process_tab(
            docs, args.doc, tab, state, args.dry_run,
            force=args.force, use_openrouter=args.use_openrouter,
            disable_table=args.no_table, style=args.style
        )
        results.append((t_title, status))
        if status == 'replied':
            replied_count += 1
        print(f"  → {status}")
        # Respect limit
        if args.limit and replied_count >= args.limit:
            print(f"Limit {args.limit} reached; stopping early.")
            break
        # Delay only if more remain
        if idx < len(targets):
            time.sleep(args.delay)

    if not args.dry_run:
        save_state(state)
        print('State saved.')
    else:
        print('Dry-run: state NOT saved.')

    print('\nSummary:')
    print(f"  Tabs visited: {len(results)} | Replies inserted: {replied_count}")
    for t, st in results:
        print(f"  - {t}: {st}")
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
