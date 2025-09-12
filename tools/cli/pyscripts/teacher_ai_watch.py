#!/usr/bin/env python3
"""Continuous watcher that detects new TEACHER zone changes and updates AI zone.

Features:
  - Polls a Google Doc's tabs at a fixed interval (default 90s).
  - Reuses hashing + diff logic from `ai_teacher_responder.py` (imports its helpers).
  - Optional OpenRouter LLM reply generation (`--use-openrouter`). Falls back to heuristic reply if unavailable.
  - Select specific tabs via repeated --tab arguments or process all with --all.
  - Graceful exit after N loops with --max-loops (omit for continuous).

Usage examples:
  Single tab (heuristic):
    python3 teacher_ai_watch.py --doc <DOC_ID> --tab "Membership and admin"

  All tabs w/ OpenRouter every 2 minutes:
    python3 teacher_ai_watch.py --doc <DOC_ID> --all --use-openrouter --interval 120

  Dry run (no writes):
    python3 teacher_ai_watch.py --doc <DOC_ID> --tab "Membership and admin" --dry-run

Implementation notes:
  - Loads & persists the same state file as responder (`teacher_response_state.json`).
  - Only issues write requests when a tab status is `replied`.
  - Basic rate limit: processes sequentially; future improvement could add backoff.
"""
from __future__ import annotations
import argparse, os, sys, time, datetime as dt
from typing import List, Dict

# Ensure we can import sibling responder script
SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)

sys.path.append(os.path.join(SCRIPT_DIR, '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

# Import internal helpers from ai_teacher_responder
from ai_teacher_responder import (
    flatten_tabs,
    normalize_title,
    load_state,
    save_state,
    process_tab,
)  # type: ignore


def parse_args():
    ap = argparse.ArgumentParser(description="Watch TEACHER zones and update AI replies when changes occur.")
    ap.add_argument('--doc', required=True, help='Google Doc ID')
    ap.add_argument('--tab', action='append', help='Tab title (repeatable)')
    ap.add_argument('--all', action='store_true', help='Process all tabs')
    ap.add_argument('--interval', type=int, default=90, help='Polling interval seconds (default 90)')
    ap.add_argument('--max-loops', type=int, default=0, help='Stop after N loops (0 = infinite)')
    ap.add_argument('--use-openrouter', action='store_true', help='Use OpenRouter LLM for replies')
    ap.add_argument('--no-table', action='store_true', help='Disable membership table detection/insertion logic.')
    ap.add_argument('--tabs-file', help='Path to file with tab titles (one per line, # for comments).')
    ap.add_argument('--dry-run', action='store_true', help='Do not write to document')
    ap.add_argument('--force-first', action='store_true', help='Force reply on first loop even if content previously replied')
    return ap.parse_args()


def fetch_doc(docs_service, doc_id: str):
    return docs_service.documents().get(documentId=doc_id, includeTabsContent=True).execute()


def main():
    args = parse_args()

    creds = authenticate_google_apis()
    if not creds:
        print('❌ Auth failed.')
        return 1
    docs_service = build('docs','v1',credentials=creds)

    state = load_state(args.doc)
    loop = 0
    print(f"👀 Watching document {args.doc} (interval={args.interval}s, openrouter={args.use_openrouter}, dry_run={args.dry_run})")

    try:
        while True:
            loop += 1
            loop_start = dt.datetime.utcnow()
            try:
                doc = fetch_doc(docs_service, args.doc)
            except HttpError as e:
                print(f"⚠️ Fetch failed (loop {loop}): {e}")
                time.sleep(args.interval)
                continue

            tabs_map = flatten_tabs(doc)
            targets: List[Dict] = []
            file_tabs: List[str] = []
            if args.tabs_file:
                try:
                    with open(args.tabs_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line=line.strip()
                            if not line or line.startswith('#'):
                                continue
                            file_tabs.append(line)
                except FileNotFoundError:
                    print(f"⚠️ tabs-file not found: {args.tabs_file}")
            merged_tabs: List[str] = []
            if args.tab:
                merged_tabs.extend(args.tab)
            if file_tabs:
                merged_tabs.extend(file_tabs)
            if args.all:
                targets = list(tabs_map.values())
            elif merged_tabs:
                for t in merged_tabs:
                    obj = tabs_map.get(normalize_title(t))
                    if obj:
                        targets.append(obj)
                    else:
                        print(f"⚠️ Tab not found: {t}")
            else:
                print('⚠️ Provide --tab/--tabs-file or --all (exiting watcher).')
                return 1

            print(f"\n[Loop {loop} @ {loop_start.strftime('%H:%M:%S')}Z] Processing {len(targets)} tab(s)...")
            any_reply = False
            for tab in targets:
                title = tab.get('tabProperties', {}).get('title','')
                # Force only on very first loop if requested
                force_flag = args.force_first and loop == 1
                tab_title, status = process_tab(
                    docs_service,
                    args.doc,
                    tab,
                    state,
                    args.dry_run,
                    force=force_flag,
                    use_openrouter=args.use_openrouter,
                    disable_table=args.no_table,
                )
                print(f"  - {tab_title}: {status}")
                if status == 'replied':
                    any_reply = True

            if any_reply and not args.dry_run:
                save_state(state)
                print('  ✅ State persisted.')
            elif args.dry_run:
                print('  (dry-run: state not saved)')

            if args.max_loops and loop >= args.max_loops:
                print('🏁 Reached max loops, exiting.')
                break

            elapsed = (dt.datetime.utcnow() - loop_start).total_seconds()
            sleep_for = max(0, args.interval - elapsed)
            print(f"⏱  Sleeping {int(sleep_for)}s...")
            time.sleep(sleep_for)

    except KeyboardInterrupt:
        print('\n👋 Interrupted by user; exiting watcher.')

    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
