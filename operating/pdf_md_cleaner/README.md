# PDF → Clean Markdown Pipeline

This routine module converts a PDF to Markdown and then cleans the Markdown via an LLM, emitting a `.clean.md` alongside the original file.

## Usage

Quick run (single PDF):

```bash
python3 operating/pdf_md_cleaner/run.py --input "/abs/path/to/file.pdf" --model anthropic/claude-3.2
```

Options:
- `--max-pages` (int): Limit pages for pdfminer fallback (default: 200)
- `--chunk-chars` (int): Approximate max characters per LLM chunk (default: 6000)
- `--max-tokens` (int): LLM max_tokens per chunk (default: 1200)
- `--output-md`: Explicit path for the intermediate `.md` (optional)
- `--output-clean`: Explicit path for the final `.clean.md` (optional)

## How it works
- Tries PyMuPDF for Markdown extraction; falls back to pdfminer.
- Splits Markdown on headings, cleans each chunk via OpenRouter LLM (Claude 3.2 default) with retries and local fallback.
- Writes both `.md` and `.clean.md` by default next to the input PDF.

## Requirements
- Python 3.10+
- Either PyMuPDF (`fitz`) or `pdfminer.six` installed
- OpenRouter API key available (env `OPENROUTER_API_KEY` or `modules/openRouterAI/key.txt`)

