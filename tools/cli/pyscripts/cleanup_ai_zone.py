#!/usr/bin/env python3
"""Cleanup & summarize AI zone for a specific tab.

Actions:
  - Fetch TEACHER + AI zone texts.
  - Preserve first markdown table (if any) in existing AI zone.
  - Summarize overall conversation (teacher + prior AI) via OpenRouter LLM.
  - Replace AI zone content with: (table if present) + structured summary sections.
  - Update teacher response state (hash + last text) to keep system consistent.

Requires OpenRouter API key (.env) and Google Docs auth.

Usage:
  python3 cleanup_ai_zone.py --doc <DOC_ID> --tab "Membership and admin" --use-openrouter
  (Dry run to preview replacement content)
  python3 cleanup_ai_zone.py --doc <DOC_ID> --tab "Membership and admin" --use-openrouter --dry-run
"""
from __future__ import annotations
import argparse, os, sys, json, datetime as dt, re
from datetime import timedelta
from typing import List, Optional

SCRIPT_DIR = os.path.dirname(__file__)
# Add Google Docs API helpers path
sys.path.append(os.path.join(SCRIPT_DIR, '..', 'GoogleDocsAPI'))
# Add project root so `modules` package is discoverable
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

# Reuse helpers from responder
sys.path.append(SCRIPT_DIR)
from ai_teacher_responder import (
    flatten_tabs,
    normalize_title,
    extract_zone_text,
    extract_zone_ranges,
    load_state,
    save_state,
    hash_text,
)  # type: ignore

TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")

def parse_args():
    ap = argparse.ArgumentParser(description="Summarize and clean AI zone, preserving first markdown table.")
    ap.add_argument('--doc', required=True, help='Google Doc ID')
    ap.add_argument('--tab', required=True, help='Tab title')
    ap.add_argument('--dry-run', action='store_true', help='Preview only; do not modify document')
    ap.add_argument('--use-openrouter', action='store_true', help='Use OpenRouter LLM (required for real summary)')
    return ap.parse_args()


def find_first_markdown_table(lines: List[str]) -> Optional[List[str]]:
    block: List[str] = []
    in_block = False
    for ln in lines:
        if TABLE_LINE_RE.match(ln.strip()):
            if not in_block:
                in_block = True
            block.append(ln.rstrip())
        else:
            if in_block:
                break
    return block if block else None


def call_llm(teacher_text: str, ai_history: str) -> str:
    """Call OpenRouter; on failure return heuristic fallback summary."""
    system_prompt = (
        "You clean and condense an AI collaboration document. Output ONLY a structured markdown summary with sections:"\
        "\n## Context\n## Key Decisions\n## Action Items\n## Open Questions\n## Next Step\n"\
        "Each section concise; action items as bullet list with owners if present. No preamble, no apologies, <= 250 words total." \
    )
    user_prompt = (
        f"TEACHER CONTENT:\n<<<TEACHER_BEGIN>>>\n{teacher_text.strip()}\n<<<TEACHER_END>>>\n\n"\
        f"PRIOR AI CONTENT (for context):\n<<<AI_HISTORY_BEGIN>>>\n{ai_history.strip()}\n<<<AI_HISTORY_END>>>\n"\
        "Produce the summarized sections now." \
    )
    try:
        from modules.openRouterAI.env import get_openrouter_api_key, get_openrouter_model
        from modules.openRouterAI.client import post_chat_completions
        if not get_openrouter_api_key():
            raise RuntimeError("OPENROUTER_API_KEY not set")
        model = get_openrouter_model()
        payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            'temperature': 0.3,
            'max_tokens': 600,
        }
        resp = post_chat_completions(payload)
        content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if content:
            return content
        raise RuntimeError('Empty LLM response')
    except Exception as e:
        # Heuristic fallback
        teacher_lines = [l.strip() for l in teacher_text.splitlines() if l.strip()]
        ai_lines = [l.strip() for l in ai_history.splitlines() if l.strip()]
        key_decisions = teacher_lines[-5:]
        actions = [l for l in teacher_lines + ai_lines if l.lower().startswith(('todo','action','next'))][-8:]
        fallback = [
            '## Context',
            f'(LLM unavailable: {e}) Condensed from {len(teacher_lines)} teacher + {len(ai_lines)} AI lines.',
            '## Key Decisions',
            *(key_decisions or ['(No recent decisions extracted)']),
            '## Action Items',
            *(actions or ['(No explicit action lines found)']),
            '## Open Questions',
            '(Not extracted in fallback mode)',
            '## Next Step',
            'Resume normal incremental replies after review.'
        ]
        return '\n'.join(fallback)


HKT_OFFSET = timedelta(hours=8)

def hkt_now() -> str:
    return (dt.datetime.utcnow() + HKT_OFFSET).strftime('%Y-%m-%d %H:%M HKT')

def main():
    args = parse_args()
    if not args.use_openrouter:
        print('❌ --use-openrouter required for cleanup (no heuristic summary implemented).')
        return 1
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
    tab = tabs.get(normalize_title(args.tab))
    if not tab:
        print(f"Tab not found: {args.tab}")
        return 1

    teacher_text = extract_zone_text(tab, 'TEACHER')
    ai_text = extract_zone_text(tab, 'AI')
    ai_lines = ai_text.splitlines()
    table_block = find_first_markdown_table(ai_lines)

    try:
        summary_md = call_llm(teacher_text, ai_text)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return 1

    ts = hkt_now()
    new_ai_content_parts: List[str] = [f"[AI Cleanup Summary {ts}]"]
    if table_block:
        new_ai_content_parts.append('\n'.join(table_block))
    new_ai_content_parts.append(summary_md.strip())
    final_text = '\n\n'.join(part for part in new_ai_content_parts if part).rstrip() + '\n'

    if args.dry_run:
        print('--- DRY RUN: Replacement AI content preview ---')
        print(final_text)
        print('--- END PREVIEW ---')
        return 0

    # Replace AI zone content
    ranges = extract_zone_ranges(tab)
    ai_ranges = ranges.get('AI')
    if not ai_ranges:
        print('No AI zone ranges found.')
        return 1
    content_start = ai_ranges.get('content_start')
    content_end = ai_ranges.get('content_end')
    tab_id = tab.get('tabProperties', {}).get('tabId')
    if content_start is None or content_end is None or not tab_id:
        print('AI zone indices incomplete.')
        return 1

    requests = [
        {'deleteContentRange': {'range': {'tabId': tab_id, 'startIndex': content_start, 'endIndex': content_end}}},
        {'insertText': {'location': {'tabId': tab_id, 'index': content_start}, 'text': final_text}},
    ]
    try:
        docs.documents().batchUpdate(documentId=args.doc, body={'requests': requests}).execute()
        print('✅ AI zone cleaned & summarized.')
    except HttpError as e:
        print(f'Update failed: {e}')
        return 1

    # Update state to reflect current teacher hash so responder won’t immediately append again
    state = load_state(args.doc)
    norm = normalize_title(args.tab)
    tab_state = state.setdefault('tabs', {}).setdefault(norm, {})
    tab_state['teacher_last_replied_text'] = teacher_text
    tab_state['teacher_hash_replied'] = hash_text(teacher_text)
    tab_state['last_reply_iso'] = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    save_state(state)
    print('State updated.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
