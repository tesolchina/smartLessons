# Operating Tools Directory

## Purpose
Core operational tools for daily administrative tasks, data processing, and automation.

## Directory Structure

```
operating/
├── README.md                   # This file
├── emailRetrieval.md          # Email extraction notes
├── email_automation/          # Email processing tools
│   ├── email_retrieval_script.py
│   ├── email_drafts/
│   └── README.md
├── document_sync/             # Document synchronization
│   ├── gdrive_sync.py
│   └── README.md
└── crawlers/                  # Web data extraction tools
    ├── crawler.py            # Generic web crawler
    ├── parser02.py           # Data parser
    ├── sitemap_parser.py     # Sitemap processing
    └── [other crawler tools]
```

## Tools Overview

### 📧 Email Automation
**Location**: `operating/email_automation/`
- Extract emails from Outlook by keywords
- Manage email drafts and templates
- Cross-platform email sending capabilities

**Usage**: 
```bash
python3 operating/email_automation/email_retrieval_script.py
```

### 📄 Document Sync
**Location**: `operating/document_sync/`
- Sync documents from Google Drive
- Support for multiple file formats (PDF, DOCX, TXT, MD)
- Incremental sync with change detection

**Usage**:
```bash
python3 operating/document_sync/gdrive_sync.py
```

### 🕷️ Web Crawlers
**Location**: `operating/crawlers/`
- Generic web crawling and data extraction
- Sitemap parsing and URL processing  
- Structured data extraction

**Usage**:
```bash
python3 operating/crawlers/crawler.py
```

## Integration with Projects

### From Project Directory
```bash
# From projects/screening_test/
python3 ../../operating/email_automation/email_retrieval_script.py
python3 ../../operating/document_sync/gdrive_sync.py
```

### From Root Directory
```bash
python3 operating/email_automation/email_retrieval_script.py
python3 operating/document_sync/gdrive_sync.py
```

## Operational Philosophy
- **Reusable**: Tools work across multiple projects
- **Efficient**: Automated daily task processing  
- **Administrative**: Focus on operational rather than project-specific tasks
- **Cross-platform**: macOS and Windows compatibility where applicable

---
*Updated: September 6, 2025*  
*Focus: Daily operational automation*

<!-- AUTO_TOOL_INDEX:START -->
Auto-generated tool index for `tools/documents` (UTC 2025-09-12T06:44:46Z).

Regenerate with: `python tools/cli/generate_tool_indexes.py --dirs documents`

| Script | Summary | Run Hint |
|--------|---------|----------|
| `Archives/canva_automation/academic_slide_generator.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.academic_slide_generator` |
| `Archives/canva_automation/canva_api_setup.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_api_setup` |
| `Archives/canva_automation/canva_cli.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_cli` |
| `Archives/canva_automation/canva_collaboration_helper.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.canva_collaboration_helper` |
| `Archives/canva_automation/canva_collaborative_cli.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_collaborative_cli` |
| `Archives/canva_automation/canva_connect_api.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_connect_api` |
| `Archives/canva_automation/canva_connect_cli.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.canva_connect_cli` |
| `Archives/canva_automation/canva_direct_creator.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_direct_creator` |
| `Archives/canva_automation/canva_quick_api.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.canva_quick_api` |
| `Archives/canva_automation/canva_quick_creator.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_quick_creator` |
| `Archives/canva_automation/canva_slide_creator.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.canva_slide_creator` |
| `Archives/canva_automation/create_lang2077_from_content.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.create_lang2077_from_content` |
| `Archives/canva_automation/create_lang2077_html.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.create_lang2077_html` |
| `Archives/canva_automation/lang2077_slides_creator.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.lang2077_slides_creator` |
| `Archives/canva_automation/lang2077_template_generator.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.lang2077_template_generator` |
| `Archives/canva_automation/powerpoint_cli.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.powerpoint_cli` |
| `Archives/canva_automation/slide_creator_cli.py` | !/usr/bin/env python3 | `python -m tools.documents.Archives.canva_automation.slide_creator_cli` |
| `Archives/canva_automation/test_canva_api.py` | !/usr/bin/env python3 | `import tools.documents.Archives.canva_automation.test_canva_api` |
| `afternoon_edit_generator.py` | !/usr/bin/env python3 | `python -m tools.documents.afternoon_edit_generator` |
| `ai_innovation_report_generator.py` | !/usr/bin/env python3 | `python -m tools.documents.ai_innovation_report_generator` |
| `duplicate_functions_audit.py` | !/usr/bin/env python3 | `python -m tools.documents.duplicate_functions_audit` |
| `generic_document_analyzer.py` | !/usr/bin/env python3 | `python -m tools.documents.generic_document_analyzer` |
| `innovation_officer_edit_suggestions.py` | !/usr/bin/env python3 | `python -m tools.documents.innovation_officer_edit_suggestions` |
| `lc_ai_document_analyzer.py` | !/usr/bin/env python3 | `python -m tools.documents.lc_ai_document_analyzer` |
| `lc_markdown_enhancer.py` | !/usr/bin/env python3 | `python -m tools.documents.lc_markdown_enhancer` |
| `markdown_cleanup_via_llm.py` | !/usr/bin/env python3 | `python -m tools.documents.markdown_cleanup_via_llm` |
| `markdown_enhancer.py` | !/usr/bin/env python3 | `python -m tools.documents.markdown_enhancer` |
| `universal_document_enhancer.py` | !/usr/bin/env python3 | `python -m tools.documents.universal_document_enhancer` |
| `word_document_edit_locator.py` | !/usr/bin/env python3 | `python -m tools.documents.word_document_edit_locator` |

<!-- AUTO_TOOL_INDEX:END -->
