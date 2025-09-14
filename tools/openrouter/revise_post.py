#!/usr/bin/env python3
"""
Revise a JRE tutoring draft post via OpenRouter with model fallback and price recommendation.

Usage:
  python tools/openrouter/revise_post.py \
    --in projects/AItutor/JREtutoring/draftPost1.md \
    --out projects/AItutor/JREtutoring/draftPost1_revised_gpt.md \
    --model openai/gpt-5 --fallback x-ai/grok-3 \
    --chunked --max-chunks 6 --end-tag <END_OF_OUTPUT>

Environment:
  - Requires OPENROUTER_API_KEY in environment or .env at repo root.
  - Optional OPENROUTER_BASE_URL (default https://openrouter.ai/api/v1)
  - Optional OPENROUTER_APP_NAME / OPENROUTER_APP_URL for metadata headers.
"""
from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
import textwrap
from typing import List, Dict, Any

# Optional dotenv
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None

DEFAULT_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.environ.get("REVISION_MODEL", "openai/gpt-5")  # primary per user request
FALLBACK_MODEL = os.environ.get("REVISION_FALLBACK_MODEL", "x-ai/grok-3")  # fallback per user request
DEFAULT_IN = "projects/AItutor/JREtutoring/draftPost1.md"
DEFAULT_OUT = "projects/AItutor/JREtutoring/draftPost1_revised_gpt.md"
DEFAULT_END_TAG = "<END_OF_OUTPUT>"


def load_env() -> None:
    if load_dotenv is not None:
        load_dotenv(override=False)
    else:
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def build_prompt(draft_text: str, *, end_tag: str, chunk_hint_tokens: int) -> str:
    return textwrap.dedent(f"""
    You are a senior editor and growth strategist for Patreon content aimed at candidates of the Hong Kong Joint Recruitment Examination (JRE).

    TASK:
    - Revise the following DRAFT POST into a polished, reader-ready English article for a one-off paid post.
    - Strengthen clarity, structure, and persuasion while keeping the author's voice reasonable and professional.
    - Incorporate: (1) the author's track record (123/200 English paper; shortlisted for AO interview), (2) the next JRE date (29 Nov 2025), (3) the English CSB link: https://www.csb.gov.hk/english/admin/grade/ao/447.html, (4) that this is a one-off purchase (not a membership), (5) note that membership may come later.
    - Highlight practical tactics and insights for writing the JRE English paper, including: objectives-first framing; balanced pros/cons; using annexes; time management; civil-service tone; mitigation/alternatives.
    - Provide an actionable section with weekly prep plan and exam-day steps.

    PRICING REQUEST:
    - Suggest a reasonable Patreon price in HKD for this one-off post tailored to JRE candidates in Hong Kong, with a short rationale and 2 price-testing variants (intro price vs. standard price).
    - Label this pricing section exactly as: "Recommended Patreon Price (HKD)" and include: one primary price, rationale (willingness to pay, value vs alternatives), and two testing variants.

    OUTPUT FORMAT:
    1) Title options (3–5 variants)
    2) Final Revised Post (Markdown, ready to publish)
    3) Recommended Patreon Price (HKD)
    4) CTA suggestions (2–3)

    CHUNKING PROTOCOL (important):
    - Output the result in chunks of approximately {chunk_hint_tokens} tokens per chunk.
    - Do NOT repeat previous content in later chunks.
    - On the LAST chunk, append exactly this tag on a new line: {end_tag}

    DRAFT POST (verbatim below):
    ---
    {draft_text}
    ---
    """)


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment or .env")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if os.environ.get("OPENROUTER_APP_URL"):
        headers["HTTP-Referer"] = os.environ["OPENROUTER_APP_URL"]
    if os.environ.get("OPENROUTER_APP_NAME"):
        headers["X-Title"] = os.environ["OPENROUTER_APP_NAME"]
    return headers


def call_openrouter_messages(messages: List[Dict[str, Any]], *, model: str, base_url: str, max_tokens: int = 2200, temperature: float = 0.3) -> str:
    import requests
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    url = f"{base_url.rstrip('/')}/chat/completions"
    resp = requests.post(url, headers=_headers(), data=json.dumps(payload), timeout=120)
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Unexpected response format: {data}") from e


def main(argv: list[str] | None = None) -> int:
    load_env()

    parser = argparse.ArgumentParser(description="Revise a draft post via OpenRouter and suggest Patreon pricing.")
    parser.add_argument("--in", dest="in_path", default=DEFAULT_IN, help="Path to draft markdown")
    parser.add_argument("--out", dest="out_path", default=DEFAULT_OUT, help="Path to save revised output")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Primary model (e.g., openai/gpt-5)")
    parser.add_argument("--fallback", default=FALLBACK_MODEL, help="Fallback model if primary fails")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="OpenRouter base URL")
    parser.add_argument("--chunked", action="store_true", help="Enable chunked multi-call to avoid truncation")
    parser.add_argument("--max-chunks", type=int, default=6, help="Maximum chunks to request when chunked")
    parser.add_argument("--end-tag", default=DEFAULT_END_TAG, help="Completion end tag to detect final chunk")
    parser.add_argument("--chunk-hint-tokens", type=int, default=1200, help="Approx tokens per chunk to hint model")
    args = parser.parse_args(argv)

    in_path = Path(args.in_path)
    if not in_path.exists():
        print(f"ERROR: draft not found: {in_path}")
        return 2

    draft_text = in_path.read_text(encoding="utf-8")
    prompt = build_prompt(draft_text, end_tag=args.end_tag, chunk_hint_tokens=args.chunk_hint_tokens)

    messages: List[Dict[str, Any]] = [{"role": "user", "content": prompt}]

    def try_with_model(model_id: str) -> str:
        combined = ""
        last_chunk = None
        if not args.chunked:
            return call_openrouter_messages(messages, model=model_id, base_url=args.base_url, max_tokens=2200)
        # chunked loop
        for i in range(args.max_chunks):
            chunk = call_openrouter_messages(messages, model=model_id, base_url=args.base_url, max_tokens=2200)
            # prevent infinite loop if model repeats
            if chunk == last_chunk:
                break
            combined += ("\n" if combined else "") + chunk
            if args.end_tag in chunk:
                break
            # ask to continue
            messages.append({"role": "assistant", "content": chunk})
            messages.append({
                "role": "user",
                "content": f"Continue the previous answer with the next chunk only. Do not repeat earlier content. Append {args.end_tag} at the very end when finished."
            })
            last_chunk = chunk
        return combined

    # Try primary model; on error, try fallback
    try:
        content = try_with_model(args.model)
    except Exception as e1:
        print(f"Warning: primary model failed ({args.model}):", e1)
        print("Trying fallback:", args.fallback)
        try:
            content = try_with_model(args.fallback)
        except Exception as e2:
            print("ERROR: both primary and fallback models failed.")
            print("Primary error:", e1)
            print("Fallback error:", e2)
            return 3

    # Strip end tag if present
    content = content.replace(args.end_tag, "").strip()

    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = (
        f"# Revised JRE Draft Post\n\n"
        f"- Primary model: {args.model}\n"
        f"- Fallback: {args.fallback}\n"
        f"- Chunked: {'yes' if args.chunked else 'no'} (max {args.max_chunks} chunks)\n"
        f"- Timestamp: {stamp}\n\n---\n\n"
    )
    out_path.write_text(header + content + "\n", encoding="utf-8")
    print("✅ Saved revised post to", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
