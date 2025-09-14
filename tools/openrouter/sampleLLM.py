#!/usr/bin/env python3
"""
Send the JRE tutoring plan to Grok-4 (via OpenRouter) and save the response.

Usage:
  python tools/openrouter/sampleLLM.py \
      --plan projects/AItutor/JREtutoring/plan.md \
      --out projects/AItutor/JREtutoring/grok4_response.md \
      --model x-ai/grok-4

Environment:
  - Expects OPENROUTER_API_KEY in .env or environment.
  - Optional: OPENROUTER_BASE_URL (default https://openrouter.ai/api/v1)
  - Optional: OPENROUTER_APP_NAME, OPENROUTER_APP_URL for headers.

Notes:
  - Does NOT print secrets.
  - Graceful error messages with exit codes.
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
import textwrap

# Try to load dotenv if available, but do not fail if missing
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None

DEFAULT_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.environ.get("GROK_MODEL", "x-ai/grok-4")
DEFAULT_PLAN = "projects/AItutor/JREtutoring/plan.md"
DEFAULT_OUT = "projects/AItutor/JREtutoring/grok4_response.md"


def load_env() -> None:
    # Prefer dotenv if present
    if load_dotenv is not None:
        load_dotenv(override=False)
    else:
        # Minimal .env loader fallback
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def build_prompt(plan_text: str) -> str:
    return textwrap.dedent(f"""
    You are a senior education venture strategist. Based on the user's background and goals below, propose 2–3 practical organizational frameworks to launch a Joint Recruitment Exam (JRE) tutoring initiative in Hong Kong, including free & paid offerings.

    Context (verbatim):
    ---
    {plan_text}
    ---

    Deliverables (concise but actionable):
    1) Business model & product ladder (free → low-ticket → core → premium); pricing bands in HKD; value props.
    2) Content & program architecture (Patreon tiers, WeChat/XHS community flows, email cadence, weekly posting plan up to Nov 29 exam date); sample 2-week calendar.
    3) Funnel & ops blueprint (lead magnets, onboarding, payment, scheduling, feedback loops); required tools stack.
    4) Compliance & outside-practice checklist (key steps to apply, disclaimers, risk controls for a university employee).
    5) Milestone timeline (now → Nov 29) with 5–8 checkpoints; KPI targets.
    6) Interview preparation products (AO interviews), including mock formats & rubric.

    Keep it skimmable with bullet points and tables where useful. Optimize for speed-to-first-dollar while ensuring quality.
    Prefer Cantonese localization notes where relevant (platform norms, payment habits).
    """)


def call_openrouter(prompt: str, *, model: str, base_url: str) -> str:
    import requests

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment or .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # Optional metadata headers (do not expose secrets)
    if os.environ.get("OPENROUTER_APP_URL"):
        headers["HTTP-Referer"] = os.environ["OPENROUTER_APP_URL"]
    if os.environ.get("OPENROUTER_APP_NAME"):
        headers["X-Title"] = os.environ["OPENROUTER_APP_NAME"]

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 1800,
    }

    url = f"{base_url.rstrip('/')}/chat/completions"
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"Unexpected response format: {data}") from e

    return content


def main(argv: list[str] | None = None) -> int:
    load_env()

    parser = argparse.ArgumentParser(description="Send JRE plan to Grok-4 via OpenRouter and save the response.")
    parser.add_argument("--plan", default=DEFAULT_PLAN, help="Path to plan markdown file")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Path to save Grok response markdown")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenRouter model ID (e.g., x-ai/grok-4)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="OpenRouter base URL")
    args = parser.parse_args(argv)

    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"ERROR: plan file not found: {plan_path}")
        return 2

    plan_text = plan_path.read_text(encoding="utf-8")
    prompt = build_prompt(plan_text)

    try:
        response = call_openrouter(prompt, model=args.model, base_url=args.base_url)
    except Exception as e:
        print("ERROR calling OpenRouter:", e)
        return 3

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    out_md = f"# Grok Planning Response\n\n- Model: {args.model}\n- Timestamp: {stamp}\n\n---\n\n{response}\n"
    out_path.write_text(out_md, encoding="utf-8")
    print("✅ Saved LLM response to", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())