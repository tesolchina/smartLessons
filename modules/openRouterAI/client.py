#!/usr/bin/env python3
"""Minimal OpenRouter client (networked)."""
from typing import Any, Dict
import json
import urllib.request

from .env import get_openrouter_base_url, get_openrouter_headers


def post_chat_completions(payload: Dict[str, Any], *, endpoint: str = "/chat/completions") -> Dict[str, Any]:
    base = get_openrouter_base_url().rstrip("/")
    url = f"{base}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=get_openrouter_headers(), method="POST")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)
