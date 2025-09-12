#!/usr/bin/env python3
"""
Generic Toolbox CLI

Unified entry point for common operations across the operating tools.

Examples:
  python3 operating/toolbox_cli.py slides:append-md --pdf projects/GCAP3226/course_materials/Week3/GCAP3226_week3_Regression.pdf --doc-id <ID>
  python3 operating/toolbox_cli.py slides:clean-and-append --pdf <PDF> --doc-id <ID>
  python3 operating/toolbox_cli.py audit:dups --output operating/DUPLICATES_REPORT.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_slides_append(args):
    from tools.google.docs.api.slides_to_md_append_and_ai_comments import main as run
    return run([
        '--pdf', args.pdf,
        '--doc-id', args.doc_id,
        '--model', args.model,
    ] + (['--dry-run'] if args.dry_run else []))


def run_slides_clean(args):
    from tools.google.docs.api.slides_md_cleaner_append import main as run
    return run([
        '--pdf', args.pdf,
        '--doc-id', args.doc_id,
        '--model', args.model,
    ] + (['--dry-run'] if args.dry_run else []))


def run_audit_dups(args):
    from tools.operating.duplicate_functions_audit import main as run  # still in legacy location
    return run()

def run_pdf_to_clean_md(args):
    from tools.pdf.md_cleaner.run import main as run
    argv = [
        '--input', args.input,
        '--model', args.model,
        '--max-pages', str(args.max_pages),
        '--chunk-chars', str(args.chunk_chars),
        '--max-tokens', str(args.max_tokens),
    ]
    if args.output_md:
        argv += ['--output-md', args.output_md]
    if args.output_clean:
        argv += ['--output-clean', args.output_clean]
    if args.force:
        argv += ['--force']
    return run(argv)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='DailyAssistant Toolbox CLI')
    sub = p.add_subparsers(dest='cmd', required=True)

    # slides:append-md
    sp1 = sub.add_parser('slides:append-md', help='Extract slides → Markdown and append with AI comments')
    sp1.add_argument('--pdf', required=True)
    sp1.add_argument('--doc-id', required=True)
    sp1.add_argument('--model', default='x-ai/grok-4')
    sp1.add_argument('--dry-run', action='store_true')
    sp1.set_defaults(func=run_slides_append)

    # slides:clean-and-append
    sp2 = sub.add_parser('slides:clean-and-append', help='Clean slides Markdown via LLM and append')
    sp2.add_argument('--pdf', required=True)
    sp2.add_argument('--doc-id', required=True)
    sp2.add_argument('--model', default='x-ai/grok-4')
    sp2.add_argument('--dry-run', action='store_true')
    sp2.set_defaults(func=run_slides_clean)

    # audit:dups
    sp3 = sub.add_parser('audit:dups', help='Run duplicate functions audit')
    sp3.set_defaults(func=run_audit_dups)

    # pdf:to-clean-md
    sp4 = sub.add_parser('pdf:to-clean-md', help='Convert PDF → Markdown, then clean via LLM')
    sp4.add_argument('--input', required=True)
    sp4.add_argument('--model', default='anthropic/claude-3.2')
    sp4.add_argument('--max-pages', type=int, default=200)
    sp4.add_argument('--chunk-chars', type=int, default=6000)
    sp4.add_argument('--max-tokens', type=int, default=1200)
    sp4.add_argument('--output-md')
    sp4.add_argument('--output-clean')
    sp4.add_argument('--force', action='store_true')
    sp4.set_defaults(func=run_pdf_to_clean_md)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
