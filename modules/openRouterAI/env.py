#!/usr/bin/env python3
"""
Environment loader for OpenRouter.
- Loads from os.environ
- If python-dotenv is available and a `.env` exists at repo root, load it.
"""

import os
from pathlib import Path
from typing import Dict

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    load_dotenv = None  # optional


def _load_dotenv_if_present() -> None:
    if load_dotenv is None:
        return
    # Look for a .env at repo root (../.. from openRouterAI dir -> DailyAssistant)
    module_dir = Path(__file__).resolve().parent
    # .../DailyAssistant/modules/openRouterAI -> parents[1] == .../DailyAssistant
    repo_root = module_dir.parents[1]
    env_path = repo_root / ".env"
    loaded = False
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        loaded = True
    # Fallback: allow default search from CWD
    if not loaded:
        load_dotenv(override=True)


# Load .env once on import
_load_dotenv_if_present()


def get_openrouter_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    return key


def get_openrouter_base_url() -> str:
    return os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()


def get_openrouter_model() -> str:
    return os.environ.get("OPENROUTER_MODEL", "openrouter/auto").strip()


def get_openrouter_headers() -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {get_openrouter_api_key()}",
        "Content-Type": "application/json",
    }
    # Optional metadata headers per OpenRouter docs
    app_name = os.environ.get("OPENROUTER_APP_NAME")
    app_url = os.environ.get("OPENROUTER_APP_URL")
    if app_name:
        headers["HTTP-Referer"] = app_url or "https://example.com"
        headers["X-Title"] = app_name
    return headers


def get_openrouter_config() -> Dict[str, str]:
    return {
        "base_url": get_openrouter_base_url(),
        "model": get_openrouter_model(),
        "has_key": str(bool(get_openrouter_api_key())),
    }
