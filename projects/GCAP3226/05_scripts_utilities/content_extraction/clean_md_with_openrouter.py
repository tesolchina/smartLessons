#!/usr/bin/env python3
"""Clean a Markdown file using OpenRouter LLM.

Usage:
  python clean_md_with_openrouter.py input.md output.md

Requires OPENROUTER_API_KEY via .env or modules/openRouterAI/key.txt.
"""
import sys
from pathlib import Path
import json

# Allow import: repo_root/DailyAssistant/modules on sys.path
THIS = Path(__file__).resolve()
MODULES = THIS.parents[3] / 'DailyAssistant' / 'modules'
if str(MODULES) not in sys.path:
    sys.path.insert(0, str(MODULES))

from openRouterAI.client import post_chat_completions
from openRouterAI.env import get_openrouter_model


CLEAN_PROMPT = (
    "You are a professional editor. Clean and format the following Markdown syllabus. "
    "Preserve headings and list structure, remove page-number artifacts and repeated headers/footers, "
    "fix broken words, normalize spacing, and keep URLs intact. Return only cleaned Markdown."
)


def run_clean(md_text: str) -> str:
    model = get_openrouter_model()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": CLEAN_PROMPT},
            {"role": "user", "content": md_text[:180000]}  # safety cap
        ],
        "max_tokens": 4000,
        "temperature": 0.2,
    }
    resp = post_chat_completions(payload)
    # OpenRouter response format similar to OpenAI
    content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
    return content


def main():
    if len(sys.argv) < 3:
        print("Usage: python clean_md_with_openrouter.py input.md output.md")
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    text = src.read_text(encoding="utf-8")
    cleaned = run_clean(text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(cleaned, encoding="utf-8")
    print(f"Cleaned Markdown written to: {dst}")


if __name__ == "__main__":
    main()
