#!/usr/bin/env python3
"""
List all processed Markdown files and optionally mark original PDFs as done.

Creates/updates an INDEX.md (default in the doneProcess folder) linking to every
`.clean.md` and its source PDF if found. Optionally renames processed PDFs by
adding ' done' before the .pdf extension.

Usage:
  python3 operating/pdf_md_cleaner/list_and_mark_done.py \
    --done-dir projects/goal-setting-chatbot-paper/literature/doneProcess \
    --source-dirs \
      projects/goal-setting-chatbot-paper/literature/papersToAddressinDiscussion \
      projects/goal-setting-chatbot-paper/literature/references \
    [--rename-pdf]

Idempotent: re-running won't duplicate entries or re-rename PDFs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Dict, Optional
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def find_clean_files(done_dir: Path) -> List[Path]:
    return sorted(done_dir.glob('*.clean.md'))


def find_source_pdf(base: str, source_dirs: List[Path]) -> Optional[Path]:
    target = base + '.pdf'
    for d in source_dirs:
        candidate = d / target
        if candidate.exists():
            return candidate
        # Attempt forgiving match (case-insensitive, spaces variants)
        lowered = target.lower()
        for p in d.glob('*.pdf'):
            if p.name.lower() == lowered:
                return p
    return None


def rename_pdf(pdf_path: Path) -> Path:
    if pdf_path.stem.endswith(' done'):
        return pdf_path  # already renamed
    new_path = pdf_path.with_name(pdf_path.stem + ' done' + pdf_path.suffix)
    # Avoid collision
    if new_path.exists():
        return pdf_path
    pdf_path.rename(new_path)
    return new_path


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def generate_index(rows: List[Dict], index_path: Path) -> None:
    lines = [
        '# Processed Papers Index',
        '',
        'Auto-generated list of cleaned Markdown files and their original PDFs.',
        '',
        '| Title | Cleaned Markdown | Original PDF | PDF Renamed |',
        '|-------|------------------|--------------|-------------|',
    ]
    for r in rows:
        if r['pdf_rel']:
            pdf_link = f"[{r['pdf_name']}]({r['pdf_rel']})"
        else:
            pdf_link = '—'
        lines.append(
            f"| {r['title']} | [{r['clean_name']}]({r['clean_rel']}) | {pdf_link} | {r['pdf_renamed']} |"
        )
    index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='List processed .clean.md and optionally rename original PDFs')
    ap.add_argument('--done-dir', required=True, help='Directory containing .clean.md outputs')
    ap.add_argument('--source-dirs', nargs='+', required=True, help='Source directories to search for original PDFs')
    ap.add_argument('--rename-pdf', action='store_true', help="Rename original PDFs by appending ' done' before extension")
    ap.add_argument('--index-name', default='INDEX.md', help='Name of index markdown file to write inside done-dir')
    args = ap.parse_args(argv)

    done_dir = (REPO_ROOT / args.done_dir).resolve() if not args.done_dir.startswith('/') else Path(args.done_dir)
    if not done_dir.exists():
        print(f"❌ done-dir not found: {done_dir}")
        return 1
    source_dirs: List[Path] = []
    for s in args.source_dirs:
        p = (REPO_ROOT / s).resolve() if not s.startswith('/') else Path(s)
        if p.exists():
            source_dirs.append(p)
        else:
            print(f"⚠️  source dir missing: {p}")

    clean_files = find_clean_files(done_dir)
    if not clean_files:
        print('No .clean.md files found.')
        return 0

    rows: List[Dict] = []
    for cf in clean_files:
        base = cf.name[:-len('.clean.md')]
        src_pdf = find_source_pdf(base, source_dirs)
        pdf_renamed_flag = 'no'
        pdf_rel = None
        pdf_name = None
        if src_pdf:
            orig_before = src_pdf
            if args.rename_pdf:
                renamed = rename_pdf(src_pdf)
                pdf_renamed_flag = 'yes' if renamed != orig_before else ('already' if orig_before.stem.endswith(' done') else 'no')
                src_pdf = renamed
            pdf_rel = rel(src_pdf)
            pdf_name = src_pdf.name
        rows.append({
            'title': base,
            'clean_rel': rel(cf),
            'clean_name': cf.name,
            'pdf_rel': pdf_rel,
            'pdf_name': pdf_name,
            'pdf_renamed': pdf_renamed_flag,
        })

    index_path = done_dir / args.index_name
    generate_index(rows, index_path)
    print(f"✅ Wrote index: {index_path}")
    if args.rename_pdf:
        print('Renaming complete (where applicable).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
