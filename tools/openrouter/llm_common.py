from __future__ import annotations

from typing import Dict, Optional
import os
import sys
from pathlib import Path

# Ensure local modules/ path is importable when used from various entry points
MOD_DIR = Path(__file__).resolve().parents[1]
if str(MOD_DIR) not in sys.path:
    sys.path.insert(0, str(MOD_DIR))

post_chat_completions = None  # type: ignore
get_openrouter_api_key = None  # type: ignore
try:
    from openRouterAI.client import post_chat_completions  # type: ignore
    from openRouterAI.env import get_openrouter_api_key  # type: ignore
    OPENROUTER_AVAILABLE = True
except Exception:
    OPENROUTER_AVAILABLE = False


def ensure_openrouter_ready() -> None:
    if OPENROUTER_AVAILABLE:
        if get_openrouter_api_key is None or not get_openrouter_api_key():
            # Try loading from key files
            _maybe_load_key_from_files()
            if get_openrouter_api_key is None or not get_openrouter_api_key():
                raise RuntimeError("Missing OPENROUTER_API_KEY")
        return
    # HTTP fallback path: ensure API key exists
    if not os.environ.get('OPENROUTER_API_KEY'):
        _maybe_load_key_from_files()
        if not os.environ.get('OPENROUTER_API_KEY'):
            raise RuntimeError("OpenRouter client not available and OPENROUTER_API_KEY not set")


def _maybe_load_key_from_files() -> None:
    if os.environ.get('OPENROUTER_API_KEY'):
        return
    # Search common key locations
    repo_root = Path(__file__).resolve().parents[2]
    candidates = [
        repo_root / 'modules' / 'openRouterAI' / 'key.txt',
        repo_root / 'operating' / 'modules' / 'openRouterAI' / 'key.txt',
    ]
    for p in candidates:
        try:
            if p.exists():
                key = p.read_text(encoding='utf-8').strip()
                if key:
                    os.environ['OPENROUTER_API_KEY'] = key
                    return
        except Exception:
            continue


def chat(prompt: str, model: str, max_tokens: int = 3000, temperature: float = 0.2) -> str:
    ensure_openrouter_ready()
    payload: Dict = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }
    # Prefer local client when available
    if OPENROUTER_AVAILABLE and post_chat_completions is not None:
        resp = post_chat_completions(payload)
        content = resp.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if not content:
            raise RuntimeError('Empty response from LLM')
        return content
    # HTTP fallback using requests
    import time
    import requests
    headers = {
        'Authorization': f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
        'Content-Type': 'application/json',
    }
    last_err: Optional[Exception] = None
    for attempt in range(3):
        try:
            resp = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30,
            )
            if resp.status_code == 429:
                # rate limited
                time.sleep(1 + attempt)
                continue
            resp.raise_for_status()
            data = resp.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            if not content:
                raise RuntimeError('Empty response from LLM (HTTP fallback)')
            return content
        except Exception as e:
            last_err = e
            time.sleep(0.3 * (attempt + 1))
    # If we are here, all retries failed
    raise RuntimeError(f"OpenRouter HTTP call failed after retries: {last_err}")


def chat_with_fallback(prompt: str, model: str, fallback_model: Optional[str] = 'anthropic/claude-3.5-sonnet', max_tokens: int = 3000, temperature: float = 0.2) -> str:
    try:
        return chat(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
    except Exception:
        if not fallback_model:
            raise
        return chat(prompt, model=fallback_model, max_tokens=max_tokens, temperature=temperature)
