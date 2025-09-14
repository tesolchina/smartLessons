# Examples

## 1) Strategy plan (Grok-4)
```
python tools/openrouter/sampleLLM.py \
  --plan projects/AItutor/JREtutoring/plan.md \
  --out projects/AItutor/JREtutoring/grok4_response.md \
  --model x-ai/grok-4
```

## 2) Patreon post revision (GPT-5 → Grok-3 fallback)
```
python tools/openrouter/revise_post.py \
  --in projects/AItutor/JREtutoring/draftPost1.md \
  --out projects/AItutor/JREtutoring/draftPost1_revised_gpt.md \
  --model openai/gpt-5 \
  --fallback x-ai/grok-3 \
  --chunked --max-chunks 8 --end-tag "<END_OF_OUTPUT>"
```

## 3) Claude pass
```
python tools/openrouter/sampleLLM.py \
  --plan projects/AItutor/JREtutoring/plan.md \
  --out projects/AItutor/JREtutoring/claude_response.md \
  --model anthropic/claude-3.5-sonnet
```
