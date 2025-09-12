#!/usr/bin/env python3
"""
Batch PDF → Clean Markdown runner with de-duplication and reporting.

- Scans one or more input folders for PDFs.
- Skips duplicates by basename (case-insensitive) across all input folders.
- Runs the routine pipeline on each unique PDF.
- Moves final `.clean.md` (and optionally the original PDF) to an output folder `doneProcess`.
- Writes a Markdown report listing all converted files with timing and usage estimates.

Example:
  python3 operating/pdf_md_cleaner/batch/run_folder.py \
    --inputs \
      projects/goal-setting-chatbot-paper/literature/papersToAddressinDiscussion \
      projects/goal-setting-chatbot-paper/literature/references \
    --output projects/goal-setting-chatbot-paper/literature/doneProcess \
    --model anthropic/claude-3.2 \
    --delete-raw-md
"""
from __future__ import annotations

import argparse
import shutil
import time
from pathlib import Path
from typing import List, Dict, Set
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / 'modules') not in sys.path:
    sys.path.insert(0, str(ROOT / 'modules'))

from operating.pdf_md_cleaner.run import run_pipeline
from operating.markdown_cleanup_via_llm import cleanup_markdown


def find_pdfs(folders: List[Path]) -> List[Path]:
    pdfs: List[Path] = []
    for d in folders:
        if not d.exists():
            continue
        for p in d.rglob('*.pdf'):
            if p.is_file():
                pdfs.append(p)
    return sorted(pdfs)


def dedupe_by_basename(paths: List[Path]) -> List[Path]:
    seen: Set[str] = set()
    unique: List[Path] = []
    for p in paths:
        key = p.name.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return unique


def write_report(report_path: Path, rows: List[Dict]):
    lines = [
        "# Batch PDF → Clean Markdown Report",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| File | Tokens (approx) | Time (s) | Output |",
        "| --- | ---: | ---: | --- |",
    ]
    for r in rows:
        rel_out = r['output']
        lines.append(f"| {r['name']} | {r['tokens']} | {r['time']:.1f} | {rel_out} |")
    report_path.write_text("\n".join(lines), encoding='utf-8')


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Batch run PDF → Clean Markdown on folders')
    ap.add_argument('--inputs', nargs='+', required=True, help='One or more input folders')
    ap.add_argument('--output', required=True, help='Destination folder for processed outputs (doneProcess)')
    ap.add_argument('--model', default='anthropic/claude-3.2')
    ap.add_argument('--chunk-chars', type=int, default=4000)
    ap.add_argument('--max-tokens', type=int, default=900)
    ap.add_argument('--delete-raw-md', action='store_true')
    ap.add_argument('--move-pdf', action='store_true', help='Also move original PDFs into output folder')
    args = ap.parse_args(argv)

    input_dirs = [Path(p).resolve() for p in args.inputs]
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    all_pdfs = find_pdfs(input_dirs)
    unique_pdfs = dedupe_by_basename(all_pdfs)

    rows: List[Dict] = []
    for pdf in unique_pdfs:
        t0 = time.time()
        # Run pipeline with idempotence
        from operating.pdf_md_cleaner.run import run_pipeline
        md_path, clean_path = run_pipeline(pdf, args.model, 200, args.chunk_chars, args.max_tokens, None, None, force=False)
        elapsed = time.time() - t0

        # Move outputs to out_dir
        dest_clean = out_dir / clean_path.name
        shutil.move(str(clean_path), str(dest_clean))
        if args.move_pdf:
            dest_pdf = out_dir / pdf.name
            shutil.copy2(str(pdf), str(dest_pdf))
        if args.delete_raw_md and md_path.exists():
            try:
                md_path.unlink()
            except Exception:
                pass

        rows.append({
            'name': pdf.name,
            'tokens': 'n/a',  # token estimate already printed during cleaning; could be parsed if needed
            'time': elapsed,
            'output': str(dest_clean),
        })

    report_path = out_dir / 'BATCH_REPORT.md'
    write_report(report_path, rows)
    print(f"✅ Batch complete. Report: {report_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
