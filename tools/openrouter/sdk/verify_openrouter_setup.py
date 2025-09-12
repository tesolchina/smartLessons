#!/usr/bin/env python3
"""Quick verifier for OpenRouter environment setup."""
import sys
from pathlib import Path

# Allow running directly (python3 modules/openRouterAI/verify_openrouter_setup.py)
if __package__ is None or __package__ == "":
    # add repo_root/modules to sys.path
    this = Path(__file__).resolve()
    sys.path.append(str(this.parents[1]))
    from openRouterAI.env import get_openrouter_api_key, get_openrouter_config
else:
    from .env import get_openrouter_api_key, get_openrouter_config


def mask(key: str) -> str:
    if not key:
        return "(missing)"
    if len(key) <= 8:
        return "****"
    return key[:6] + "…" + key[-4:]


def main() -> int:
    api_key = get_openrouter_api_key()
    cfg = get_openrouter_config()
    print("OpenRouter API key:", mask(api_key))
    print("Base URL:", cfg["base_url"]) 
    print("Default Model:", cfg["model"]) 
    print("Key Present:", api_key != "")
    if not api_key:
        print("\nNext steps:\n1) Copy .env.example to .env at repo root\n2) Fill OPENROUTER_API_KEY=sk-or-...\n3) Re-run this verifier")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
