# DailyAssistant Operating Tools Overview

This document summarizes key Python tools under `operating/`, highlights duplicated code areas, and introduces new reusable utilities under `modules/common_utils/` to reduce duplication.

## What’s here

- Google Docs tooling (`operating/GoogleDocsAPI/`)
  - `doc_roundtrip_update.py`: Read + comment round-trip via LLM; renders Markdown to Google Docs.
  - `md_to_gdoc_append.py`: Append a local Markdown file into a Doc with markers.
  - `assignments_generator.py`: Draft assignment instructions/rubrics and update Docs.
  - `slides_to_md_append_and_ai_comments.py`: Extract slides PDF → Markdown and add AI accessibility comments; append to Doc.
  - `slides_md_cleaner_append.py`: Cleanup/normalize slide Markdown via LLM and append to Doc.

- Email automation (`operating/email_automation/`): Inbound/outbound workflows and helpers.
- Sync and crawlers (`operating/document_sync/`, `operating/crawlers/`): Drive sync, sitemap crawling, etc.
- Content enhancement (`operating/*.py`): Markdown enhancers, document analyzers, and workflow scripts.

## Common utilities (new)

To avoid duplicated code across tools, reusable helpers are added under `modules/common_utils/`:

- `llm.py`
  - `chat(prompt, model, ...)` and `chat_with_fallback(...)` using OpenRouter with optional fallback.
- `pdf_utils.py`
  - `extract_pdf_text_per_page(path)` and `pages_to_slide_markdown(pages)` for PDF → Markdown.
- `gdocs_utils.py`
  - `append_markdown_formatted(docs, document_id, md, build_replace_requests)` to append and format Markdown.

These utilities are already used by the slide-processing scripts to remove duplication.

## Duplicate functions audit

Run: `python3 operating/duplicate_functions_audit.py --output operating/DUPLICATES_REPORT.md`

See `operating/DUPLICATES_REPORT.md` for details. Highlights:

- Many duplicates exist between `operating/` and `operating/PyScripts/` variants (e.g., `markdown_enhancer.py`, `generic_document_analyzer.py`, `lc_ai_document_analyzer.py`, etc.).
- GoogleDocsAPI duplicates between `gcap3226_editor.py` and `document_editor.py` setup blocks.
- New slide tools share similar append/LLM/PDF code; now consolidated via `modules/common_utils/`.

## Suggested refactors (next steps)

1) Import shared helpers
   - Replace inline OpenRouter calls with `common_utils.llm.chat_with_fallback`.
   - Replace ad-hoc PDF parsing with `common_utils.pdf_utils`.
   - Use `common_utils.gdocs_utils.append_markdown_formatted` for consistent Doc writes.

2) Consolidate duplicated scripts
   - For pairs in `operating/` and `operating/PyScripts/`, keep one canonical version under `operating/` and have thin wrappers or symlinks.

3) Update READMEs
   - Document common patterns and parameters to encourage reuse and reduce drift.

## Quick example

Using the common utilities in a new tool:

```python
from common_utils.llm import chat_with_fallback
from common_utils.pdf_utils import extract_pdf_text_per_page, pages_to_slide_markdown
from common_utils.gdocs_utils import append_markdown_formatted

# ... build prompt, get docs service and build_replace_requests ...
md = chat_with_fallback(prompt, model='x-ai/grok-4')
append_markdown_formatted(docs, doc_id, md, build_replace_requests)
```

By centralizing these pieces, maintenance and future enhancements (e.g., retries, rate limiting, richer Markdown rendering) become straightforward.
