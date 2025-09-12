#!/usr/bin/env python3
"""
Duplicate Functions Audit

Scans Python scripts under `operating/` for functions with identical or highly
similar bodies (normalized) and outputs a Markdown report suggesting refactors
into `modules/common_utils/`.

Usage:
  python3 operating/duplicate_functions_audit.py [--output REPORT.md]
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def normalize_source(src: str) -> str:
    # Remove comments and docstrings, normalize whitespace
    try:
        tree = ast.parse(src)
        # Build a new source without top-level docstrings using AST positions
        lines = src.splitlines(True)
        to_strip = []
        for node in ast.walk(tree):
            val = getattr(node, 'value', None)
            if isinstance(node, ast.Expr) and isinstance(val, ast.Constant) and isinstance(getattr(val, 'value', None), str):
                # Likely a docstring expression; record its line range for stripping
                start = getattr(node, 'lineno', None)
                end = getattr(node, 'end_lineno', start)
                if start is not None and end is not None:
                    to_strip.append((start-1, end))
        for s, e in sorted(to_strip, reverse=True):
            del lines[s:e]
        src = ''.join(lines)
    except Exception:
        pass
    src = re.sub(r"#[^\n]*", "", src)
    src = re.sub(r"\s+", " ", src).strip()
    return src


def find_functions(py_path: Path) -> List[Tuple[str, int, str]]:
    code = py_path.read_text(encoding='utf-8', errors='ignore')
    try:
        tree = ast.parse(code)
    except Exception:
        return []
    results: List[Tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = getattr(node, 'lineno', 0)
            end = getattr(node, 'end_lineno', start)
            lines = code.splitlines()
            body_src = "\n".join(lines[start-1:end])
            results.append((node.name, start, body_src))
    return results


def scan_operating() -> Dict[str, List[Tuple[Path, int]]]:
    dup_map: Dict[str, List[Tuple[Path, int]]] = {}
    for py in (ROOT / 'operating').rglob('*.py'):
        if py.name.endswith('_audit.py'):
            continue
        funcs = find_functions(py)
        for name, lineno, src in funcs:
            sig = hashlib.sha256(normalize_source(src).encode('utf-8')).hexdigest()
            key = f"{name}|{sig}"
            dup_map.setdefault(key, []).append((py, lineno))
    return dup_map


def build_report(dup_map: Dict[str, List[Tuple[Path, int]]]) -> str:
    groups = [items for items in dup_map.values() if len(items) > 1]
    lines: List[str] = []
    lines.append("# Duplicate Functions Audit")
    lines.append("")
    if not groups:
        lines.append("No duplicate function bodies detected across operating/.")
        return "\n".join(lines)
    lines.append("The following functions appear to be duplicated. Consider consolidating into `modules/common_utils/`.")
    lines.append("")
    for i, items in enumerate(groups, 1):
        lines.append(f"## Group {i}")
        for path, lineno in items:
            rel = path.relative_to(ROOT)
            lines.append(f"- `{rel}`: line {lineno}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default=str(ROOT / 'operating' / 'DUPLICATES_REPORT.md'))
    args = ap.parse_args()
    dup_map = scan_operating()
    report = build_report(dup_map)
    out_path = Path(args.output)
    out_path.write_text(report, encoding='utf-8')
    print(f"✅ Wrote duplicate audit to {out_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
