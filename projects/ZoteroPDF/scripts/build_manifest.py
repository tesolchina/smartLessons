#!/usr/bin/env python3
"""Build or update an annotation manifest (no LLM calls yet).

Scans annotated_data directory (or raw docs directory) for markdown files and records:
- file_path
- filename
- size_bytes
- annotated (bool heuristic: has YAML front matter with at least one key OR explicit required keys)
- keys_present (list)
- last_modified

Usage:
  python projects/ZoteroPDF/scripts/build_manifest.py \
    --docs projects/ZoteroPDF/annotated_data \
    --out projects/ZoteroPDF/annotation_manifest.json

Subsequent runs will merge & preserve existing per-file flags (e.g., future confidence, errors).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import time
from typing import Dict, Any

RE_FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

REQUIRED_KEYS = {"title", "authors", "publication_year"}


def parse_front_matter(text: str) -> Dict[str, Any] | None:
    match = RE_FRONT_MATTER.match(text)
    if not match:
        return None
    block = match.group(1)
    data: Dict[str, Any] = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip()
    return data


def scan_docs(docs_dir: Path):
    for md in docs_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        fm = parse_front_matter(text)
        keys_present = sorted(list(fm.keys())) if fm else []
        annotated = bool(fm and (REQUIRED_KEYS & set(fm.keys())))
        yield {
            "file_path": str(md),
            "filename": md.name,
            "size_bytes": md.stat().st_size,
            "annotated": annotated,
            "keys_present": keys_present,
            "last_modified": int(md.stat().st_mtime),
        }


def load_existing(out_path: Path) -> Dict[str, Any]:
    if out_path.exists():
        try:
            return json.loads(out_path.read_text())
        except Exception:
            return {"files": {}, "generated_at": int(time.time())}
    return {"files": {}, "generated_at": int(time.time())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--docs', required=True, help='Directory containing markdown files')
    ap.add_argument('--out', required=True, help='Output manifest JSON file')
    args = ap.parse_args()

    docs_dir = Path(args.docs)
    out_path = Path(args.out)

    existing = load_existing(out_path)

    files_map = existing.get('files', {})

    count_total = 0
    count_annotated = 0
    for rec in scan_docs(docs_dir):
        count_total += 1
        if rec['annotated']:
            count_annotated += 1
        files_map[rec['file_path']] = rec

    manifest = {
        "generated_at": int(time.time()),
        "total_files": count_total,
        "annotated_files": count_annotated,
        "files": files_map,
        "required_keys": sorted(list(REQUIRED_KEYS)),
        "version": 1,
    }

    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"✅ Manifest written: {out_path} ({count_annotated}/{count_total} annotated)")

if __name__ == '__main__':
    main()
