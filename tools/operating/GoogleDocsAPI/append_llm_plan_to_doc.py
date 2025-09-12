#!/usr/bin/env python3
"""Append an LLM-generated event execution plan to a Google Doc from a local note.

Features:
  * Deterministic idempotency via HTML comment markers:
        <!-- LLM_PLAN_START:YYYY-MM-DD --> ... <!-- LLM_PLAN_END:YYYY-MM-DD -->
  * Skips appending if today's plan already exists (unless --force)
  * Uses existing OpenRouter-based helper (chat_with_fallback)
  * Fallback locally-crafted plan if LLM call fails
  * Dry-run mode prints the plan without touching Google Docs

Usage example:
  python3 operating/GoogleDocsAPI/append_llm_plan_to_doc.py \
      --note projects/BenSCMPGRF/NovEvent/note.md \
      --doc https://docs.google.com/document/d/1zNXRwDW05Ok_UrPk053pr3NX0hd949Tq28VjJuebhBk/edit \
      --model anthropic/claude-3.5-sonnet --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from googleapiclient.discovery import build  # type: ignore

# Auth + LLM helpers -------------------------------------------------------
sys.path.append(str(Path(__file__).parent))
from auth_setup import authenticate_google_apis  # type: ignore

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from modules.common_utils.llm import chat_with_fallback  # type: ignore

# Prompt template -----------------------------------------------------------
PLAN_PROMPT = (
    "You are an expert academic events producer. Using the note below, produce a concise, actionable execution plan for the event 'Letters to the Editor Symposium and Exhibition' scheduled for November 17 (assume today's date is {today}).\n\n"
    "Context Note (verbatim):\n---\n{note}\n---\n\n"
    "Requirements:\n"
    "- Output GitHub-flavored Markdown ONLY.\n"
    "- Use exactly these H2 headings in this order:\n"
    "  ## Executive Summary\n"
    "  ## Objectives (max 6 bullets)\n"
    "  ## Key Outcomes / Success Metrics\n"
    "  ## Workstreams\n"
    "  ## Detailed Timeline (week-by-week until event; ISO Monday starts)\n"
    "  ## Roles & Responsibilities\n"
    "  ## Content & Curation Plan\n"
    "  ## Logistics & Operations\n"
    "  ## Risk Register (table: Risk | Likelihood | Impact | Mitigation | Owner)\n"
    "  ## Immediate Next 7 Days (ordered list)\n"
    "  ## Open Questions\n"
    "- <= ~900 words; be concrete.\n"
    "- Mark unknowns with (TBD) or (?)\n"
    "Return ONLY the markdown (no preamble).\n"
)


# Utility functions ---------------------------------------------------------
def extract_doc_id(arg: str) -> str:
    """Return canonical doc id from raw id or full URL."""
    m = re.search(r"/d/([A-Za-z0-9_-]{20,})", arg)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{20,}", arg):
        return arg
    raise ValueError("Cannot parse Google Doc ID from input")


def fetch_end_index(docs_service, doc_id: str) -> int:
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = doc.get('body', {}).get('content', [])
    return int(content[-1].get('endIndex', 1)) if content else 1


def doc_contains_marker(docs_service, doc_id: str, marker: str) -> bool:
    doc = docs_service.documents().get(documentId=doc_id).execute()
    parts: list[str] = []
    for blk in doc.get('body', {}).get('content', []):
        p = blk.get('paragraph')
        if not p:
            continue
        for el in p.get('elements', []):
            t = el.get('textRun', {}).get('content')
            if t:
                parts.append(t)
    return marker in ''.join(parts)


def build_wrapped_section(plan_md: str, date_tag: str) -> str:
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    return (
        f"\n<!-- LLM_PLAN_START:{date_tag} -->\n"
        f"# LLM Generated Plan ({date_tag})\n"
        f"Generated at {ts}\n\n"
        f"{plan_md.strip()}\n"
        f"<!-- LLM_PLAN_END:{date_tag} -->\n"
    )


def append_text(docs_service, doc_id: str, text: str) -> None:
    end_index = fetch_end_index(docs_service, doc_id)
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            'requests': [
                {
                    'insertText': {
                        'location': {'index': end_index - 1},
                        'text': text,
                    }
                }
            ]
        },
    ).execute()


def fallback_plan(today: str) -> str:
    return f"""## Executive Summary
LLM unavailable; placeholder plan generated locally on {today}. (TBD refine with LLM)

## Objectives (max 6 bullets)
- (TBD) Confirm panel & speakers
- (TBD) Finalize venue logistics
- (TBD) Curate exhibition content
- (TBD) Launch promotion campaign
- (TBD) Prepare AV & materials
- (TBD) Risk mitigation readiness

## Key Outcomes / Success Metrics
- Target attendance (TBD)
- Engagement / Q&A rate (TBD)
- Diversity metrics (TBD)
- Media mentions (TBD)
- On-time milestone % (TBD)

## Workstreams
1. Curation & Content
2. Logistics & Operations
3. Marketing & Promotion
4. Stakeholder & Partners
5. Risk & Compliance

## Detailed Timeline
- Week 1: Draft shortlist & roles (TBD)
- Week 2: Confirm panel + venue (TBD)
- Week 3: Exhibition layout draft (TBD)
- Week 4: Promotion push (TBD)
- Week 5: Materials final + rehearsal (TBD)
- Event Week: Final checks & execution

## Roles & Responsibilities
- Event Lead (TBD)
- Academic Liaison (TBD)
- Tech / AV (TBD)
- Communications (TBD)
- Logistics Coordinator (TBD)

## Content & Curation Plan
- Gather candidate letters (TBD)
- Selection criteria (TBD)
- Permissions workflow (TBD)

## Logistics & Operations
- Venue booking (status TBD)
- AV checklist (TBD)
- Printing & materials (TBD)

## Risk Register
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|-----------|-------|
| Speaker cancellation | Med | High | Backup speakers list | (TBD) |
| Late content delivery | High | Med | Early internal deadline | (TBD) |
| AV failure | Low | High | Redundant equipment & test | (TBD) |

## Immediate Next 7 Days
1. Assign core leads (TBD)
2. Build initial curation shortlist (TBD)
3. Venue confirmation follow-up (TBD)
4. Draft milestone tracker (TBD)
5. Identify top 5 risks & owners (TBD)

## Open Questions
- Budget finalization? (TBD)
- Branding / design assets? (TBD)
- Press outreach needed? (TBD)
"""


# Main routine --------------------------------------------------------------
def generate_plan(note_text: str, today: str, model: str, fallback_model: str) -> str:
    prompt = PLAN_PROMPT.format(note=note_text, today=today)
    try:
        return chat_with_fallback(
            prompt,
            model=model,
            fallback_model=fallback_model,
            max_tokens=2300,
            temperature=0.25,
        ).strip()
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ LLM failed: {e}")
        return fallback_plan(today)


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Append an LLM-generated dated plan section to a Google Doc")
    ap.add_argument('--note', required=True, help='Path to source note (markdown / text)')
    ap.add_argument('--doc', required=True, help='Google Doc ID or full URL')
    ap.add_argument('--model', default='anthropic/claude-3.5-sonnet')
    ap.add_argument('--fallback-model', default='gpt-4o-mini')
    ap.add_argument('--dry-run', action='store_true', help='Print plan only; no Google API calls')
    ap.add_argument('--force', action='store_true', help='Append even if a plan for today already exists')
    args = ap.parse_args(argv)

    note_path = Path(args.note)
    if not note_path.exists():
        print(f"❌ Note file not found: {note_path}")
        return 1
    note_text = note_path.read_text(encoding='utf-8').strip()
    if not note_text:
        print("⚠️ Note file empty; proceeding but output may be generic.")

    try:
        doc_id = extract_doc_id(args.doc)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    today = datetime.utcnow().strftime('%Y-%m-%d')
    print("🧠 Generating plan via LLM…")
    plan_md = generate_plan(note_text, today, args.model, args.fallback_model)

    if args.dry_run:
        print(plan_md)
        return 0

    creds = authenticate_google_apis()
    if not creds:
        print('❌ Google authentication failed')
        return 1
    docs_service = build('docs', 'v1', credentials=creds)

    marker = f"LLM_PLAN_START:{today}"
    if doc_contains_marker(docs_service, doc_id, marker) and not args.force:
        print(f"⚠️ Plan for {today} already exists. Use --force to append another copy.")
        return 0

    section = build_wrapped_section(plan_md, today)
    try:
        append_text(docs_service, doc_id, section)
        print(f"✅ Plan appended to doc {doc_id}")
    except Exception as e:  # noqa: BLE001
        print(f"❌ Failed to append to Google Doc: {e}")
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
