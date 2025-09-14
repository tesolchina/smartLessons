"""
Minimal Grok (xAI) API client using only the Python standard library.

Configuration (via environment variables):
- XAI_API_KEY (required): Your xAI API key.
- XAI_API_BASE (optional): Base URL, default "https://api.x.ai/v1".
- GROK_MODEL (optional): Model name, default "grok-4".

Usage:
    from grok_client import GrokClient
    client = GrokClient()
    content, usage = client.chat(
        messages=[{"role": "user", "content": "Hello Grok"}],
        temperature=0.2,
        max_tokens=1500,
    )
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


class GrokClient:
    def __init__(
        self,
        api_key_env: str = "XAI_API_KEY",
        base_url_env: str = "XAI_API_BASE",
        default_model_env: str = "GROK_MODEL",
    ) -> None:
        self.key_source = "unknown"
        self.api_key = self._load_api_key(api_key_env)
        # Determine provider base URL and default model (xAI vs OpenRouter)
        env_base = os.getenv(base_url_env)
        or_base = os.getenv("OPENROUTER_API_BASE")
        or_key = os.getenv("OPENROUTER_API_KEY")
        using_openrouter = bool(or_key) or (env_base and "openrouter.ai" in env_base) or bool(or_base) or (
            isinstance(self.key_source, str) and ("openrouter" in self.key_source.lower())
        )

        if using_openrouter:
            self.base_url = or_base or env_base or "https://openrouter.ai/api/v1"
            self.default_model = os.getenv(default_model_env) or "x-ai/grok-4"
            self.is_openrouter = True
            self.provider = "openrouter"
        else:
            self.base_url = env_base or "https://api.x.ai/v1"
            self.default_model = os.getenv(default_model_env, "grok-4")
            self.is_openrouter = False
            self.provider = "xai"

        # Prepare opener with SSL context
        ctx = ssl.create_default_context()
        https_handler = urllib.request.HTTPSHandler(context=ctx)
        self.opener = urllib.request.build_opener(https_handler)

    def _load_api_key(self, api_key_env: str) -> Optional[str]:
        accepted_keys = [
            api_key_env,
            "OPENROUTER_API_KEY",
            "GROK_API_KEY",
            "XAI_KEY",
            "OPENAI_API_KEY_XAI",
            "OPENAI_API_KEY",
            "XAI_TOKEN",
        ]
        # 1) Direct env var (including common aliases)
        for key_name in accepted_keys:
            direct = os.getenv(key_name)
            if direct:
                self.key_source = f"env:{key_name}"
                return direct

        # 2) Key file: XAI_API_KEY_FILE or OPENROUTER_API_KEY_FILE
        key_file = os.getenv("XAI_API_KEY_FILE") or os.getenv("OPENROUTER_API_KEY_FILE")
        if key_file and os.path.isfile(key_file):
            try:
                with open(key_file, "r", encoding="utf-8") as f:
                    self.key_source = f"file:{key_file}"
                    return f.read().strip()
            except Exception:
                pass

        # 3) .env files (XAI_DOTENV_PATH, local .env, shared tools/.env and tools/openrouter/.env)
        dotenv_candidates: List[str] = []
        xai_dotenv = os.getenv("XAI_DOTENV_PATH")
        if xai_dotenv:
            dotenv_candidates.append(xai_dotenv)

        # local .env in current script directory
        here = os.path.dirname(os.path.abspath(__file__))
        dotenv_candidates.append(os.path.join(here, ".env"))

        # shared tools .envs at repo root if structure matches DailyAssistant/tools/.env
        # Path depth: citationAdvice -> writing -> goal-setting-chatbot-paper -> projects -> DailyAssistant
        dailyassistant_root = os.path.abspath(os.path.join(here, "..", "..", "..", ".."))
        tools_env = os.path.join(dailyassistant_root, "tools", ".env")
        tools_or_env = os.path.join(dailyassistant_root, "tools", "openrouter", ".env")
        dotenv_candidates.extend([tools_env, tools_or_env])

        # Optional: direct key files in tools/openrouter
        for candidate in [
            os.path.join(dailyassistant_root, "tools", "openrouter", "key.txt"),
            os.path.join(dailyassistant_root, "tools", "openrouter", "OPENROUTER_API_KEY.txt"),
        ]:
            if os.path.isfile(candidate):
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        self.key_source = f"file:{candidate}"
                        return f.read().strip()
                except Exception:
                    pass

        for path in dotenv_candidates:
            try:
                if path and os.path.isfile(path):
                    with open(path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            if "=" in line:
                                k, v = line.split("=", 1)
                                if k.strip() in accepted_keys:
                                    self.key_source = f".env:{path}:{k.strip()}"
                                    return v.strip().strip('"').strip("'")
            except Exception:
                continue

        return None

    def _post_json(self, path: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError(
                "XAI_API_KEY is not set. Please export your xAI API key to proceed."
            )

        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        # OpenRouter recommends adding referer and title headers
        if getattr(self, "is_openrouter", False):
            req.add_header("HTTP-Referer", "https://localhost")
            req.add_header("Referer", "https://localhost")
            req.add_header("X-Title", "CitationAdvice Local")

        try:
            with self.opener.open(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            detail: Optional[str] = None
            try:
                detail = e.read().decode("utf-8")
            except Exception:
                pass
            raise RuntimeError(f"HTTPError {e.code}: {detail or e.reason}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"URLError: {e.reason}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}") from e

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2500,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> Tuple[str, Dict[str, Any]]:
        """Call the OpenAI-compatible chat completions endpoint.

        Returns (content, usage_dict).
        """
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }

        resp = self._post_json(
            "/chat/completions" if self.base_url.endswith("/v1") else "/v1/chat/completions",
            payload,
        )

        # Support both OpenAI-compatible and strict forms
        choices = resp.get("choices") or []
        if not choices:
            # Some providers nest responses differently; fall back to raw text
            text = resp.get("text") or resp.get("content") or json.dumps(resp)
            return text, resp.get("usage", {})

        message = choices[0].get("message", {})
        content = message.get("content", "")
        usage = resp.get("usage", {})
        return content, usage


def _demo() -> None:
    client = GrokClient()
    try:
        content, usage = client.chat(
            messages=[{"role": "user", "content": "Reply with 'pong'"}],
            temperature=0.0,
            max_tokens=10,
        )
        print("RESPONSE:", content)
        print("USAGE:", usage)
    except Exception as e:
        print("Error:", e, file=sys.stderr)


if __name__ == "__main__":
    _demo()
