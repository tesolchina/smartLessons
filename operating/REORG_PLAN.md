# Operating Folder Reorganization Plan

This plan consolidates duplicate scripts, promotes generic utilities, and organizes the toolbox for consistency and reuse.

## Goals
- One canonical copy per tool (remove `operating/PyScripts` drift)
- Generic, reusable helpers in `modules/common_utils/`
- A simple CLI to run common tasks consistently

## Canonicalization map

Keep scripts under `operating/` as canonical. Archive or remove duplicates under `operating/PyScripts/` after verification.

Examples from the duplicate audit (`operating/DUPLICATES_REPORT.md`):

- Canonical: `operating/markdown_enhancer.py`
  - Duplicates: `operating/PyScripts/markdown_enhancer.py`
- Canonical: `operating/generic_document_analyzer.py`
  - Duplicates: `operating/PyScripts/generic_document_analyzer.py`
- Canonical: `operating/lc_ai_document_analyzer.py`
  - Duplicates: `operating/PyScripts/lc_ai_document_analyzer.py`
- Canonical: `operating/word_document_edit_locator.py`
  - Duplicates: `operating/PyScripts/word_document_edit_locator.py`
- Canonical: `operating/afternoon_edit_generator.py`
  - Duplicates: `operating/PyScripts/afternoon_edit_generator.py`
- Canonical: `operating/universal_document_enhancer.py`
  - Duplicates: `operating/PyScripts/universal_document_enhancer.py`
- Canonical: `operating/innovation_officer_edit_suggestions.py`
  - Duplicates: `operating/PyScripts/innovation_officer_edit_suggestions.py`
- Canonical: `operating/email_automation/generic_email_system.py`
  - Duplicates: `operating/PyScripts/generic_email_system.py`

GoogleDocsAPI consolidation:
- Canonical: `operating/GoogleDocsAPI/document_editor.py` (core helpers) and `gcap3226_editor.py` (project-specific)
- New shared helpers: `modules/common_utils/` already added (LLM, PDF, Docs)

## Steps
1) Freeze `operating/PyScripts/` (no new edits here)
2) Migrate shared logic to `modules/common_utils/` (LLM, PDF, Google Docs) — initial set done
3) Update canonical scripts to import common utils (slides tools done)
4) Add a generic CLI wrapper (`operating/toolbox_cli.py`) — added
5) After a smoke pass, move duplicates in `operating/PyScripts/` to `operating/Archives/` with a pointer back to canonical scripts

## Compatibility
- For any external automation calling `operating/PyScripts/...`, create thin wrappers that import and call the canonical module until callers are updated.

## Timeline
- Phase 1 (now): docs + CLI + utilities + update most-used scripts
- Phase 2: consolidate email and analyzer tools
- Phase 3: archive `operating/PyScripts/`
