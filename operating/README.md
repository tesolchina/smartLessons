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
