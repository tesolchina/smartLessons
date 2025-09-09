# OpenRouterAI Module

Small helper to load and use the OpenRouter API key from environment variables.

## Setup
1. Copy `.env.example` at repo root to `.env` and fill your key:
   - `OPENROUTER_API_KEY=sk-or-...`
   - Optional: `OPENROUTER_BASE_URL`, `OPENROUTER_MODEL`, `OPENROUTER_APP_NAME`, `OPENROUTER_APP_URL`
2. Ensure `.env` is ignored by git (root `.gitignore` covers this).

## Verify
Run the verifier:

```bash
python3 modules/openRouterAI/verify_openrouter_setup.py
```

It prints whether the key is detected (masked) and shows effective config.

## Use in Code
```python
from modules.openRouterAI.env import get_openrouter_api_key, get_openrouter_config
api_key = get_openrouter_api_key()
config = get_openrouter_config()
```

For making requests, see `client.py` (simple `requests`-free urllib wrapper). This repo avoids network calls in tests; only call it when configured.
