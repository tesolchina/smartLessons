#!/usr/bin/env python3
"""Minimal OpenRouter client (networked)."""
from typing import Any, Dict
import json
import urllib.request, urllib.error, time

from .env import get_openrouter_base_url, get_openrouter_headers


def post_chat_completions(payload: Dict[str, Any], *, endpoint: str = "/chat/completions", retries: int = 2, backoff: float = 1.2) -> Dict[str, Any]:
    """POST to OpenRouter chat completions with minimal retries and diagnostics.

    Raises urllib.error.HTTPError on persistent failure.
    Returns parsed JSON dict otherwise.
    """
    base = get_openrouter_base_url().rstrip("/")
    url = f"{base}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=get_openrouter_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8", errors='replace')
                try:
                    parsed = json.loads(body)
                except json.JSONDecodeError:
                    raise RuntimeError(f"Non-JSON response from OpenRouter (status={resp.status}): {body[:500]}")
                # Surface API-level errors if present
                if 'error' in parsed:
                    raise RuntimeError(f"OpenRouter API error: {parsed['error']}")
                return parsed
        except urllib.error.HTTPError as e:
            body = ''
            try:
                body = e.read().decode('utf-8', errors='replace')
            except Exception:
                pass
            diag = body[:400]
            # Provide targeted hints for 401/403
            if e.code in (401, 403):
                msg = (
                    f"HTTP {e.code} calling OpenRouter. Possible causes: invalid/expired key, missing billing, or model access restrictions."
                    f" Payload model={payload.get('model')} diag_snippet={diag}"
                )
            else:
                msg = f"HTTP {e.code} error from OpenRouter (attempt {attempt+1}/{retries+1}). Snippet: {diag}"
            last_err = RuntimeError(msg)
        except urllib.error.URLError as e:
            last_err = e
        except Exception as e:
            last_err = e
        if attempt < retries:
            time.sleep(backoff * (attempt + 1))
    assert last_err is not None
    raise last_err
