#!/usr/bin/env python3
"""
Convert a teacher-editable Markdown bot config into JSON.

Input MD format:
---
name: "..."
styleClass: "..."
model: "..."
teacherEmail:
  - "email1@..."
  - "email2@..."
---

## Welcome prompt
...

## Report generation instructions
...

## System prompt
...

Usage:
  python tools/botconfig/md_to_json.py \
    --in projects/Jackie/botConfig/GCAP3187-emily.EDITABLE.md \
    --out projects/Jackie/botConfig/GCAP3187-emily.json
"""
import argparse
import json
import os
import re
from typing import Dict, Any, Tuple
import sys

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


SECTION_HEADERS = {
    'welcome': re.compile(r'^##\s+Welcome prompt\s*$', re.IGNORECASE),
    'report': re.compile(r'^##\s+Report generation instructions\s*$', re.IGNORECASE),
    'system': re.compile(r'^##\s+System prompt\s*$', re.IGNORECASE),
}


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    # Parses YAML front-matter if present and returns (data, remaining_text)
    if not text.startswith('---'):
        return {}, text
    parts = text.split('\n', 1)[1]
    if '---\n' not in parts:
        return {}, text
    fm_text, rest = parts.split('---\n', 1)
    data = {}
    if yaml:
        try:
            data = yaml.safe_load(fm_text) or {}
        except Exception:
            data = {}
    return data, rest


def extract_sections(md: str) -> Dict[str, str]:
    lines = md.splitlines()
    sections: Dict[str, str] = {k: '' for k in SECTION_HEADERS}
    current_key = None
    buffer: list[str] = []

    def flush():
        nonlocal buffer, current_key
        if current_key is not None:
            # Trim trailing blank lines
            while buffer and buffer[-1].strip() == '':
                buffer.pop()
            sections[current_key] = '\n'.join(buffer).strip()
        buffer = []

    for line in lines:
        matched_key = None
        for key, rx in SECTION_HEADERS.items():
            if rx.match(line):
                matched_key = key
                break
        if matched_key:
            flush()
            current_key = matched_key
            buffer = []
            continue
        if current_key is not None:
            buffer.append(line)

    flush()
    return sections


def build_json(front: Dict[str, Any], sections: Dict[str, str]) -> Dict[str, Any]:
    required_keys = ['name', 'styleClass', 'model']
    for k in required_keys:
        if not front.get(k):
            raise ValueError(f"Missing required front-matter field: {k}")
    teacher_email = front.get('teacherEmail') or []
    if isinstance(teacher_email, str):
        teacher_email = [teacher_email]
    data = {
        'name': front['name'],
        'styleClass': front['styleClass'],
        'model': front['model'],
        'welcomePrompt': sections.get('welcome', ''),
        'reportGenerationInstructions': sections.get('report', ''),
        'systemPrompt': sections.get('system', ''),
        'teacherEmail': teacher_email,
    }
    return data


def main():
    ap = argparse.ArgumentParser(description='Convert bot-config Markdown to JSON')
    ap.add_argument('--in', dest='inp', required=True, help='Path to the teacher-editable .md')
    ap.add_argument('--out', dest='out', required=True, help='Path to write JSON file')
    args = ap.parse_args()

    with open(args.inp, 'r', encoding='utf-8') as f:
        text = f.read()

    if yaml is None:
        print('ERROR: PyYAML is required. Install with: pip install pyyaml', file=sys.stderr)
        sys.exit(1)

    front, rest = parse_frontmatter(text)
    sections = extract_sections(rest)
    data = build_json(front, sections)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote JSON: {args.out}")


if __name__ == '__main__':
    main()
