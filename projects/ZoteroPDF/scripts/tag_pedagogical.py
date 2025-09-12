#!/usr/bin/env python3
"""Heuristic tagging for pedagogical implications (Phase 1 enrichment).

Adds/updates `pedagogical_implications` flag and evidence snippets into annotation_manifest.json.
No LLM calls; pure regex + keyword scoring.

Usage:
  python projects/ZoteroPDF/scripts/tag_pedagogical.py \
    --docs projects/ZoteroPDF/annotated_data \
    --manifest projects/ZoteroPDF/annotation_manifest.json \
    --out projects/ZoteroPDF/annotation_manifest.json

Scoring:
  score = heading_hits*3 + primary_hits*2 + secondary_hits + conclusion_bonus(2 if 'conclusion' or 'implication')
  If score >= threshold (default 8) => pedagogical_implications: true

Adds fields per file:
  pedagogical_implications: bool
  pedagogical_score: int
  pedagogical_evidence: [snippet,...]
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Any

PRIMARY = [
    "pedagogical", "instructional", "teaching practice", "classroom application",
    "educational practice", "curriculum design", "instructional strategy", "teaching implications"
]
SECONDARY = [
    "teacher training", "learner engagement", "classroom implementation", "educational outcome",
    "practical guidance", "lesson design", "learning intervention", "classroom context"
]
HEADING_PATTERN = re.compile(r"^#+\s.*(implication|instructional|pedagog|teaching|practice)", re.IGNORECASE | re.MULTILINE)
CONCLUSION_HINT = re.compile(r"(conclusion|implication|recommendation)s?", re.IGNORECASE)

WINDOW = 400  # chars for evidence snippet


def score_text(text: str) -> Dict[str, Any]:
    lower = text.lower()
    heading_hits = len(HEADING_PATTERN.findall(text))
    primary_hits = sum(lower.count(k) for k in PRIMARY)
    secondary_hits = sum(lower.count(k) for k in SECONDARY)
    conclusion_bonus = 2 if CONCLUSION_HINT.search(lower) else 0
    score = heading_hits * 3 + primary_hits * 2 + secondary_hits + conclusion_bonus

    # Collect up to 3 evidence snippets around first occurrences of primary keywords
    evidence: List[str] = []
    for kw in PRIMARY:
        idx = lower.find(kw)
        if idx != -1:
            start = max(0, idx - WINDOW // 2)
            end = min(len(text), idx + WINDOW // 2)
            snippet = text[start:end].replace('\n', ' ').strip()
            if snippet not in evidence:
                evidence.append(snippet[:WINDOW])
        if len(evidence) >= 3:
            break

    return {
        "score": score,
        "heading_hits": heading_hits,
        "primary_hits": primary_hits,
        "secondary_hits": secondary_hits,
        "conclusion_bonus": conclusion_bonus,
        "evidence": evidence,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--docs', required=True, help='Directory with markdown docs')
    ap.add_argument('--manifest', required=True, help='Existing manifest path')
    ap.add_argument('--out', required=True, help='Output manifest path (can overwrite)')
    ap.add_argument('--threshold', type=int, default=8, help='Score threshold for positive tag')
    args = ap.parse_args()

    docs_dir = Path(args.docs)
    manifest_path = Path(args.manifest)
    out_path = Path(args.out)

    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}. Run build_manifest.py first.")

    manifest = json.loads(manifest_path.read_text())
    files_map = manifest.get('files', {})

    updated = 0
    for file_path, meta in files_map.items():
        p = Path(file_path)
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        metrics = score_text(text)
        positive = metrics['score'] >= args.threshold
        meta['pedagogical_implications'] = positive
        meta['pedagogical_score'] = metrics['score']
        if positive:
            meta['pedagogical_evidence'] = metrics['evidence']
        else:
            meta.pop('pedagogical_evidence', None)
        updated += 1

    manifest['files'] = files_map
    manifest['pedagogical_threshold'] = args.threshold
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"✅ Updated {updated} records with pedagogical scoring (threshold={args.threshold})")

if __name__ == '__main__':
    main()
