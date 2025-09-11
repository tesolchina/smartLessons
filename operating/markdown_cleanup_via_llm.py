#!/usr/bin/env python3
"""
Markdown Cleanup via LLM (Claude 3.2)

Cleans and normalizes a Markdown document using an LLM. Handles long files by
chunking on headings and joins results. Outputs a .clean.md alongside input by default.

Usage:
  python3 operating/markdown_cleanup_via_llm.py \
    --input "/abs/path/to/file.md" \
    [--output "/abs/path/to/output.clean.md"] \
    [--model anthropic/claude-3.2]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / 'modules'))

from common_utils.llm import chat_with_fallback


PROMPT = (
    "You are a meticulous Markdown editor for academic texts.\n\n"
    "Clean and normalize the provided Markdown while preserving meaning and citation integrity.\n"
    "Rules:\n"
    "- Keep headings structure; ensure a single H1 title (if obvious), H2/H3 for sections.\n"
    "- Merge broken lines and fix hyphenation at line breaks (e.g., 'learn-\n' 'ing' -> 'learning').\n"
    "- Normalize bullets to '- ' and numbered lists to '1.' style.\n"
    "- Preserve references, DOIs, URLs, tables, and quotes; do not invent content.\n"
    "- Remove page footers/headers and slide/page numbers.\n"
    "- Keep equations and inline math as-is; do not add code fences.\n"
    "- Do not summarize—only clean and format the given text.\n\n"
    "Return only cleaned Markdown."
)


def split_on_headings(text: str, max_chunk_chars: int = 6000) -> List[str]:
    parts: List[str] = []
    current: List[str] = []
    size = 0
    for line in text.splitlines():
        if size >= max_chunk_chars and line.startswith('#'):
            parts.append('\n'.join(current).strip())
            current, size = [], 0
        current.append(line)
        size += len(line) + 1
    if current:
        parts.append('\n'.join(current).strip())
    return [p for p in parts if p]

def _local_cleanup(text: str) -> str:
    """Conservative local cleanup when LLM is unavailable.
    - Merge hyphenation at line breaks (e.g., learn-\n ing -> learning)
    - Collapse multiple blank lines to max 2
    - Normalize bullet prefixes to '- '
    - Remove standalone page numbers like '12' or 'Page 12'
    - Join broken lines within paragraphs
    """
    # Fix hyphenation across line breaks
    s = re.sub(r"(\w+)-\n\s*(\w+)", r"\1\2", text)
    # Normalize bullets (common variants to '- ')
    s = re.sub(r"^\s*[•·◦]\s+", "- ", s, flags=re.MULTILINE)
    s = re.sub(r"^\s*\*\s+", "- ", s, flags=re.MULTILINE)
    # Remove page headers/footers
    s = re.sub(r"^\s*Page\s+\d+\s*$", "", s, flags=re.IGNORECASE | re.MULTILINE)
    s = re.sub(r"^\s*\d+\s*/\s*\d+\s*$", "", s, flags=re.MULTILINE)
    # Join lines within paragraphs but keep headings and list items intact
    lines = s.splitlines()
    out_lines: List[str] = []
    buf: List[str] = []
    def flush_buf():
        nonlocal out_lines, buf
        if buf:
            # Join with spaces
            joined = re.sub(r"\s+", " ", " ".join(buf)).strip()
            if joined:
                out_lines.append(joined)
            buf = []
    for ln in lines:
        if not ln.strip():
            flush_buf()
            out_lines.append("")
            continue
        if ln.lstrip().startswith(('#', '-', '1.', '2.', '3.', '4.', '5.', '>')):
            flush_buf()
            out_lines.append(ln)
        else:
            buf.append(ln)
    flush_buf()
    # Collapse excessive blank lines
    res = re.sub(r"\n{3,}", "\n\n", "\n".join(out_lines))
    return res.strip()


def cleanup_markdown(md: str, model: str, chunk_chars: int = 6000, max_tokens: int = 1200, return_metrics: bool = False):
    chunks = split_on_headings(md, max_chunk_chars=chunk_chars)
    cleaned: List[str] = []
    total_prompt_chars = 0
    total_output_chars = 0
    for i, ch in enumerate(chunks, 1):
        prompt = f"{PROMPT}\n\n---\n{ch}\n---"
        try:
            out = chat_with_fallback(prompt, model=model, fallback_model='anthropic/claude-3.5-sonnet', max_tokens=max_tokens, temperature=0.1)
            out_s = out.strip()
            cleaned.append(out_s)
            total_prompt_chars += len(prompt)
            total_output_chars += len(out_s)
            print(f"  • Chunk {i}/{len(chunks)} cleaned via LLM (prompt {len(prompt)} chars → output {len(out_s)} chars)")
        except Exception as e:
            # Retry once with even smaller token budget
            try:
                out = chat_with_fallback(prompt, model=model, fallback_model='anthropic/claude-3.5-sonnet', max_tokens=800, temperature=0.1)
                out_s = out.strip()
                cleaned.append(out_s)
                total_prompt_chars += len(prompt)
                total_output_chars += len(out_s)
                print(f"  • Chunk {i}/{len(chunks)} cleaned via LLM (retry) (prompt {len(prompt)} chars → output {len(out_s)} chars)")
            except Exception:
                # Fallback to local cleanup to ensure progress
                local = _local_cleanup(ch)
                cleaned.append(local)
                total_prompt_chars += len(prompt)
                # treat local as output too for estimation
                total_output_chars += len(local)
                print(f"  • Chunk {i}/{len(chunks)} cleaned locally (LLM unavailable) (approx output {len(local)} chars)")
    # Ensure single top-level title if first chunk starts with H1
    joined = '\n\n'.join(cleaned).strip()
    # De-duplicate adjacent H1s
    lines = joined.splitlines()
    normalized: List[str] = []
    h1_seen = False
    for ln in lines:
        if ln.startswith('# '):
            if h1_seen:
                # downgrade to H2
                ln = '##' + ln[1:]
            else:
                h1_seen = True
        normalized.append(ln)
    result = '\n'.join(normalized)
    # Rough token estimate (chars/4 heuristic)
    approx_tokens = int((total_prompt_chars + total_output_chars) / 4)
    print(f"ℹ️  LLM usage estimate: prompt ~{total_prompt_chars} chars, output ~{total_output_chars} chars, ≈ {approx_tokens} tokens total")
    if return_metrics:
        return result, {
            'prompt_chars': total_prompt_chars,
            'output_chars': total_output_chars,
            'approx_tokens': approx_tokens,
        }
    return result


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Clean Markdown via Claude 3.2 (with robust fallbacks)')
    ap.add_argument('--input', required=True, help='Path to input .md')
    ap.add_argument('--output', help='Path to output .clean.md')
    ap.add_argument('--model', default='anthropic/claude-3.2', help='OpenRouter model')
    ap.add_argument('--chunk-chars', type=int, default=6000, help='Approx max characters per chunk (split on headings)')
    ap.add_argument('--max-tokens', type=int, default=1200, help='LLM max_tokens per chunk')
    args = ap.parse_args(argv)

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"❌ Markdown not found: {in_path}")
        return 1
    out_path = Path(args.output) if args.output else in_path.with_suffix('.clean.md')

    md = in_path.read_text(encoding='utf-8', errors='ignore')
    print('🧹 Cleaning Markdown via LLM…')
    cleaned = cleanup_markdown(md, model=args.model, chunk_chars=args.chunk_chars, max_tokens=args.max_tokens)
    out_path.write_text(cleaned, encoding='utf-8')
    print(f"✅ Wrote cleaned Markdown: {out_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
