from __future__ import annotations

"""
Generate MASTER_Citation_Guide_v2.md by sending current context to Grok 4.

Prerequisites:
- Set XAI_API_KEY in your environment
  (optional) XAI_API_BASE, GROK_MODEL

Outputs:
- MASTER_Citation_Guide_v2.md updated with Grok's response
"""

import datetime as _dt
from pathlib import Path
import json
from typing import Dict, List

from context_builder import build_context, render_context_as_prompt
from grok_client import GrokClient


ROOT = Path(__file__).resolve().parent
OUT_FILE = ROOT / "MASTER_Citation_Guide_v2.md"


def build_messages() -> List[Dict[str, str]]:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    system_prompt = (
        "You are GitHub Copilot acting as a scholarly writing assistant. "
        "Task: produce a refined 'MASTER_Citation_Guide_v2.md' that: "
        "(1) increases targeted citations using the given RAG context, "
        "(2) strengthens cross-section echoes, and "
        "(3) keeps the action format with clear Before/After blocks and precise anchors. "
        "Focus on high-impact insertions and do not produce generic advice."
    )

    context = render_context_as_prompt(build_context())

    user_prompt = (
        "Using the provided CONTEXT, write a complete MASTER_Citation_Guide_v2.md.\n"
        "Requirements:\n"
        "- Keep a compact intro explaining what changed vs v1.\n"
        "- Provide 10-20 precise insertion points with section anchors and exact strings to search.\n"
        "- For each, include: Location, Anchor text, Before, After (with citations), Rationale, Priority.\n"
        "- Include an updated Section Echo Map.\n"
        "- Keep total under ~3,000 words.\n"
        f"- Timestamp the guide: {now}.\n\n"
        f"{context}\n\n"
        "Output only the markdown content of MASTER_Citation_Guide_v2.md."
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def main() -> None:
    client = GrokClient()
    messages = build_messages()
    meta_path = ROOT / "grok_last_call.json"

    # Report configuration
    try:
        print(f"[GROK] provider={getattr(client, 'provider', 'xai')} base={client.base_url} model={client.default_model}")
        print(f"[GROK] key_source={getattr(client, 'key_source', 'unknown')}")
    except Exception:
        pass

    # Report context sizes
    try:
        chunks = build_context()
        for title, content in chunks:
            print(f"[CTX] {title}: {len(content)} chars")
    except Exception:
        pass

    try:
        print(f"[GROK] attempting model={client.default_model}")
        content, usage = client.chat(messages=messages, temperature=0.2, max_tokens=4000)
    except Exception as e:
        print(f"[ERROR] primary attempt failed: {e}")
        # For OpenRouter, retry with a few known Grok slugs
        content = ""
        usage = {}
        if getattr(client, 'provider', 'xai') == 'openrouter':
            fallback_models = [
                "x-ai/grok-4",
                "x-ai/grok-4-latest",
                "x-ai/grok-4-mini",
                "x-ai/grok-2",
                "x-ai/grok-2-latest",
                "x-ai/grok-2-mini",
            ]
            for m in fallback_models:
                try:
                    print(f"[GROK] retrying with model={m}")
                    content, usage = client.chat(messages=messages, model=m, temperature=0.2, max_tokens=4000)
                    # Update default to the working model for the rest of this run
                    client.default_model = m
                    break
                except Exception as e2:
                    print(f"[ERROR] retry with {m} failed: {e2}")
                    continue
        if not content:
            # Graceful fallback if API key or network fails
            placeholder = (
                "# MASTER_Citation_Guide_v2\n\n"
                "Grok call did not complete. Reason:\n\n"
                f"- {e}\n\n"
                "Next steps:\n"
                "1) Ensure XAI_API_KEY is set.\n"
                "2) Optionally set XAI_API_BASE and GROK_MODEL.\n"
                "3) Re-run: python3 generate_guide_with_grok.py\n"
            )
            OUT_FILE.write_text(placeholder, encoding="utf-8")
            meta = {"error": str(e), "out_file": OUT_FILE.name}
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            return

    # Ensure we have a simple header if model returned plain text
    if not content.strip().startswith("# "):
        content = "# MASTER_Citation_Guide_v2\n\n" + content

    OUT_FILE.write_text(content, encoding="utf-8")

    print(f"[RESP] content_len={len(content)}")
    if usage:
        print(f"[USAGE] {usage}")
    meta = {"usage": usage, "out_file": OUT_FILE.name, "provider": getattr(client, 'provider', 'xai'), "base": client.base_url, "model": client.default_model, "key_source": getattr(client, 'key_source', 'unknown'), "content_len": len(content)}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
