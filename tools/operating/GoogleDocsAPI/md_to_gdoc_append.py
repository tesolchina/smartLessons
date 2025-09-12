#!/usr/bin/env python3
"""
Append a local Markdown file to a Google Doc as a new section with markers.

Usage:
  python3 operating/GoogleDocsAPI/md_to_gdoc_append.py \
    --input projects/GCAP3226/weeks3_14_draft.md \
    --doc-id 19LYdvuVJLaZ-MMm31jVc4hXo6tCrcWMk-Np4LiDUib8 \
    --section-title "Weeks 3–13 Plan (Draft)" \
    --section-key weeks3-13-plan

Flags:
  --dry-run   Only print what would happen; do not modify the document.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        text = path.read_text(encoding='utf-8')
        print(f"✅ Read input file: {path} ({len(text):,} chars, {len(text.split()):,} words)")
        return text
    except Exception as e:
        print(f"❌ Failed to read input file '{path}': {e}")
        raise


def get_last_end_index(document: dict) -> int:
    body = document.get('body', {})
    content = body.get('content', [])
    if not content:
        return 1
    last = content[-1]
    return int(last.get('endIndex', 1))


def append_markdown_to_doc(doc_id: str, md_text: str, section_title: str, section_key: str, dry_run: bool = False) -> bool:
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        print(f"❌ Google API libraries not available: {e}")
        return False

    # Import auth from this folder
    try:
        this_dir = Path(__file__).parent
        if str(this_dir) not in sys.path:
            sys.path.insert(0, str(this_dir))
        import auth_setup  # type: ignore
        authenticate_google_apis = getattr(auth_setup, 'authenticate_google_apis')
    except Exception as e:
        print(f"❌ Could not import auth_setup.authenticate_google_apis: {e}")
        return False

    print("🧩 Authenticating Google APIs…")
    creds = authenticate_google_apis()
    if not creds:
        print("❌ Authentication failed")
        return False

    docs = build('docs', 'v1', credentials=creds)

    print(f"📖 Fetching document: {doc_id}")
    try:
        doc = docs.documents().get(documentId=doc_id).execute()
    except Exception as e:
        print(f"❌ Failed to fetch document: {e}")
        return False

    end_index = get_last_end_index(doc)
    header = f"\n[LLM:START {section_key}]\n{section_title}\n"
    footer = f"\n[LLM:END {section_key}]\n"
    insertion_text = header + md_text.strip() + footer

    print("✍️ Preparing append request at document end…")
    if dry_run:
        print("🔎 Dry-run mode: no changes will be applied.")
        print(f"• Insert index: {max(1, end_index - 1)}")
        print(f"• Section key: {section_key}")
        print(f"• Section title: {section_title}")
        return True

    try:
        requests = [{
            'insertText': {
                'location': {'index': max(1, end_index - 1)},
                'text': "\n" + insertion_text + "\n"
            }
        }]
        docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        print("✅ Successfully appended to Google Doc")
        print(f"🔗 https://docs.google.com/document/d/{doc_id}/edit")
        return True
    except Exception as e:
        print(f"❌ Failed to append: {e}")
        return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Append a Markdown file to a Google Doc")
    p.add_argument('--input', required=True, help='Path to Markdown file to append')
    p.add_argument('--doc-id', required=True, help='Target Google Doc ID')
    p.add_argument('--section-title', default='## Appended Section', help='Title line inserted before content')
    p.add_argument('--section-key', default='md-import', help='Marker key for the inserted block')
    p.add_argument('--dry-run', action='store_true', help='Preview without modifying the document')
    args = p.parse_args(argv)

    md_path = Path(args.input)
    print("📦 MD → Google Docs Appender")
    print("=" * 34)
    print(f"📂 Input: {md_path}")
    print(f"📝 Doc ID: {args.doc_id}")
    print(f"🔖 Section key: {args.section_key}")
    print(f"🏷️  Section title: {args.section_title}")

    md_text = read_text(md_path)
    ok = append_markdown_to_doc(args.doc_id, md_text, args.section_title, args.section_key, dry_run=args.dry_run)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
