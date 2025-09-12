# Cost and Time Estimates: PDF → Clean Markdown

Purpose: Provide a simple, evidence-based way to forecast the time and cost to clean PDF papers into high-quality Markdown using the routine in `operating/pdf_md_cleaner`.

## TL;DR
- Time: ≈ 7–8 seconds per 1,000 tokens (cleaning step)
- Cost: ≈ $0.006–$0.007 per 1,000 tokens (based on observed runs with the current model/account)
- Rough rule of thumb: academic PDFs ≈ 2.5–3.0k tokens per page after extraction
  - Cost per page: ≈ $0.016–$0.021
  - Time per page: ≈ 18–24 seconds

Note: These are empirical estimates from your recent runs. Actuals vary with layout, figures, tables, and model choice.

## How to measure on each run
The pipeline prints an LLM usage estimate and cleaning time:
- Tokens ≈ (prompt chars + output chars) / 4
- Cleaning time is measured end-to-end for the LLM phase

Example command:
```bash
python3 operating/pdf_md_cleaner/run.py \
  --input "/abs/path/to/file.pdf" \
  --model anthropic/claude-3.2 \
  --chunk-chars 4000 \
  --max-tokens 900
```
What you'll see (example):
- “ℹ️  LLM usage estimate: prompt ~23237 chars, output ~8798 chars, ≈ 8008 tokens total”
- “⏱️  Cleaning time: 62.7s”

## Recent calibration (your data)
- Paper A (3 pages)
  - Tokens: ≈ 8,008 • Time: 62.7s • Cost: $0.05
  - Cost per 1k tokens: $0.0062 • Time per 1k tokens: 7.8s
- Paper B
  - Tokens: ≈ 13,567 • Time: 93.6s • Cost: $0.09
  - Cost per 1k tokens: $0.0066 • Time per 1k tokens: 6.9s
- Paper C
  - Tokens: ≈ 18,374 • Time: 132.0s • Cost: $0.13
  - Cost per 1k tokens: $0.0071 • Time per 1k tokens: 7.2s

From these: use 7.3s per 1k tokens for time, and $0.0068 per 1k tokens for cost (midpoints) as a planning default.

## Quick estimator
Given estimated tokens T (thousands):
- Time (seconds) ≈ 7.3 × T
- Cost (USD) ≈ 0.0068 × T

If you only know pages P, and assume 2.5–3.0k tokens per page:
- Tokens (thousands) T ≈ 2.5–3.0 × P
- Example (5 pages): T ≈ 12.5–15.0 →
  - Time ≈ 91–110 seconds
  - Cost ≈ $0.085–$0.102

## Variables that change estimates
- Model and pricing (per-1k tokens)
- Document layout (dense text vs. figures/tables)
- Chunk sizes and max_tokens settings
- Network latency and transient rate limits

## Tips
- Keep `--chunk-chars` around 4,000–6,000 and `--max-tokens` 800–1200 for stable performance.
- Use the routine’s idempotence: outputs are skipped if up to date; add `--force` to rebuild.
- Delete raw Markdown when you only need the `.clean.md` with `--delete-raw-md`.

## Optional next steps
- Add an `--estimate-only` mode to compute tokens/time/cost without calling the LLM (based on chunk prompts and a configurable output ratio).
- Batch mode: process all PDFs in a folder with a per-file summary and a totals report.
