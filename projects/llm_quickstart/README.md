# LLM Quickstart via OpenRouter

This folder is your one-stop guide to calling LLMs (Grok, GPT, Claude, etc.) across any project in this repo using the shared `tools/openrouter` utilities.

## Where things live

- Tools (shared clients, examples): `tools/openrouter/`
  - `sampleLLM.py` — Simple end-to-end example that reads a file, calls a model, saves Markdown
  - `revise_post.py` — Robust long-output handler with chunking + model fallbacks
  - `sdk/` — (if present) Env helpers and shared wrappers
  - `llm_common.py` — (if present) Common chat wrappers
- Secrets: `.env` in repo root (NOT committed)
  - `OPENROUTER_API_KEY=sk-or-...`
  - Optional: `OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`)
  - Optional: `OPENROUTER_APP_NAME`, `OPENROUTER_APP_URL` for metadata

## Prerequisites

- Python 3.10+
- Install deps (requests, python-dotenv optional):
```bash
pip install requests python-dotenv
```
- Ensure `.env` exists at repo root with your key:
```bash
OPENROUTER_API_KEY=sk-or-...
```

## Common Tasks

### 1) Send a planning brief to Grok-4
- Edit your brief at: `projects/AItutor/JREtutoring/plan.md`
- Run:
```bash
python tools/openrouter/sampleLLM.py \
  --plan projects/AItutor/JREtutoring/plan.md \
  --out projects/AItutor/JREtutoring/grok4_response.md \
  --model x-ai/grok-4
```

### 2) Revise a long draft and get a Patreon price (with fallbacks)
- Put draft at: `projects/AItutor/JREtutoring/draftPost1.md`
- Run with chunking and explicit end tag:
```bash
python tools/openrouter/revise_post.py \
  --in projects/AItutor/JREtutoring/draftPost1.md \
  --out projects/AItutor/JREtutoring/draftPost1_revised_gpt.md \
  --model openai/gpt-5 \
  --fallback x-ai/grok-3 \
  --chunked --max-chunks 8 --end-tag "<END_OF_OUTPUT>"
```

### 3) Use another model quickly
```bash
python tools/openrouter/sampleLLM.py --model anthropic/claude-3.5-sonnet
```

## Patterns for reliability

- Always load secrets from `.env` (already in `.gitignore`).
- For long outputs, prefer `revise_post.py` with `--chunked` and an explicit end tag.
- If a model name is experimental (e.g., `gpt-5`), provide a realistic fallback (`x-ai/grok-3`, `x-ai/grok-4`, or `openrouter/auto`).
- Quote your end tag on zsh shells: `"<END_OF_OUTPUT>"`.

## Adapting to any project

- Keep your input files under your project folder (e.g., `projects/<YourProject>/input.md`).
- Point the tools to those paths with `--plan` or `--in` and `--out`.
- You can copy `revise_post.py` as a template for any long-form task: change the `build_prompt` body only.

## Troubleshooting

- `File does not exist`: run the command from repo root or fix the paths.
- `OPENROUTER_API_KEY not found`: create `.env` at repo root with your key.
- Truncated output: use `--chunked` and an explicit `--end-tag`, increase `--max-chunks`.
- zsh parse error: quote special values, e.g., `"<END_OF_OUTPUT>"`.

## Security

- `.env` is ignored by git; never commit keys.
- Scripts do not print secrets; headers only include optional metadata.

---

If you want a one-command helper for your project, we can add a tiny wrapper script inside your project that calls these tools with your default paths.