#!/usr/bin/env python3
"""
Generate three simulated annotated video transcripts for LANG0026 Week 2.

Reads:
- projects/LANG0026/assessments/videoRubric.md
- projects/LANG0026/assessments/01_pre_course_video.md

Produces:
- projects/LANG0026/week2/simulated_videos.md (Markdown with John/Karen/Rachel)

LLM via OpenRouter (non-OpenAI model only). Uses OPENROUTER_API_KEY from .env.
"""

import argparse
from pathlib import Path
from typing import Dict, Any, List
import json
import sys

# Allow running directly from repo root without installing as a package
THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parents[3]
sys.path.append(str(REPO_ROOT / "modules"))

from openRouterAI.env import (
    get_openrouter_api_key,
    get_openrouter_model,
)
from openRouterAI.client import post_chat_completions


ASSESS_DIR = REPO_ROOT / "projects" / "LANG0026" / "assessments"
WEEK2_DIR = REPO_ROOT / "projects" / "LANG0026" / "week2"


def choose_safe_model(requested: str | None) -> str:
    """Ensure we do not use OpenAI models (see noOpenAI.md)."""
    req = (requested or "").lower()
    if not req or "openai" in req or req.startswith("gpt-") or "gpt-" in req:
        # Prefer a non-OpenAI default known on OpenRouter
        return "anthropic/claude-3.5-sonnet"
    return requested  # type: ignore[return-value]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Missing required file: {path}")


def build_messages(rubric_md: str, brief_md: str) -> List[Dict[str, Any]]:
    system = (
        "You are an experienced English speaking assessment assessor for higher education. "
        "Assess pre-course 2-minute speaking videos using the provided rubric. "
        "Follow instructions exactly. Avoid referencing OpenAI; use neutral language."
    )
    user = f"""
Context:
You will simulate three student video transcripts for LANG0026 Assessment 1 (Pre-course Video, 2%).

Students and proficiency target:
- John — Strong
- Karen — Medium
- Rachel — Weak

Task brief (verbatim):
---
{brief_md}
---

Rubric (verbatim):
---
{rubric_md}
---

Instructions:
- For each student, generate a 2-minute style transcript (around 250–300 words), natural spoken English.
- Then annotate the transcript, explicitly linking decisions to the rubric dimensions:
  A. Content; B. Lexical and grammatical range and accuracy; C. Fluency, coherence and pronunciation.
- Assign a score 1–5 for each dimension with a one-sentence justification.
- End with an overall brief comment and a total (sum of A,B,C) out of 15.
- Use strict Markdown structure:

### [Student Name] — [Level]

#### Transcript
<transcript text>

#### Annotations by Rubric
- Content (A): <notes> — Score: X/5
- Lexical/Grammar (B): <notes> — Score: X/5
- Fluency/Coherence/Pronunciation (C): <notes> — Score: X/5

#### Overall
Total: <A+B+C>/15
Comment: <1–2 sentences>

Deliver the three students in the order: John, Karen, Rachel.
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_llm(messages: List[Dict[str, Any]], model: str) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
    }
    resp = post_chat_completions(payload)
    # OpenAI-compatible schema
    try:
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected response schema: {e}\n{json.dumps(resp, indent=2)[:2000]}")


def write_output(path: Path, content: str) -> None:
    header = (
        "# Simulated Pre-course Video Transcripts (Annotated)\n\n"
        "Generated via OpenRouter (non-OpenAI model).\n\n"
    )
    path.write_text(header + content + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate simulated LANG0026 videos via OpenRouter")
    parser.add_argument("--output", default=str(WEEK2_DIR / "simulated_videos.md"), help="Output markdown path")
    parser.add_argument("--model", default=None, help="Override model id (non-OpenAI only)")
    parser.add_argument("--check", action="store_true", help="Only check config and inputs; no API call")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt preview and exit")
    args = parser.parse_args()

    # Pre-checks
    api_key = get_openrouter_api_key()
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found. Fill it in .env at repo root.")
        return 1

    rubric_md = read_text(ASSESS_DIR / "videoRubric.md")
    brief_md = read_text(ASSESS_DIR / "01_pre_course_video.md")
    messages = build_messages(rubric_md, brief_md)

    model = choose_safe_model(get_openrouter_model() if args.model is None else args.model)
    if "openai" in model.lower() or model.lower().startswith("gpt-"):
        print(f"Model '{model}' appears to be OpenAI, which is disallowed. Choose a non-OpenAI model.")
        return 1

    if args.check:
        print("Check OK:")
        print("- API key present: yes")
        print(f"- Model: {model}")
        print(f"- Output: {args.output}")
        print(f"- Inputs:\n  - {ASSESS_DIR / 'videoRubric.md'}\n  - {ASSESS_DIR / '01_pre_course_video.md'}")
        return 0

    if args.dry_run:
        # Show a shortened version of the user prompt for inspection
        user_msg = messages[1]["content"]
        preview = user_msg[:1000] + ("…" if len(user_msg) > 1000 else "")
        print("Prompt preview:\n" + preview)
        return 0

    print(f"Calling model: {model} (via OpenRouter)")
    try:
        output_md = call_llm(messages, model=model)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return 2

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_output(out_path, output_md)
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
