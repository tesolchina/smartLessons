# Quick Use: Call LLMs from any project

Minimal, copy-paste friendly steps.

## One-time setup
1) Add your key to `.env` at repo root:
```
OPENROUTER_API_KEY=sk-or-...
```
2) (Optional) Install helpers:
```
pip install requests python-dotenv
```

## Send a file to a model and save the reply
```
python tools/openrouter/sampleLLM.py \
  --plan projects/<YourProject>/input.md \
  --out projects/<YourProject>/response.md \
  --model x-ai/grok-4
```

## Revise a long draft with pricing suggestion (Patreon)
```
python tools/openrouter/revise_post.py \
  --in projects/<YourProject>/draft.md \
  --out projects/<YourProject>/draft_revised.md \
  --model openai/gpt-5 \
  --fallback x-ai/grok-3 \
  --chunked --max-chunks 8 --end-tag "<END_OF_OUTPUT>"
```

## Tips
- Run from repo root to keep paths consistent.
- Quote special values on zsh (e.g., end tags).
- If a model fails, try `--model x-ai/grok-4` or `--model openrouter/auto`.
