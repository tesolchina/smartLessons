# Daily Assistant  
[![CI](https://github.com/tesolchina/DailyAssistant/actions/workflows/ci.yml/badge.svg)](https://github.com/tesolchina/DailyAssistant/actions/workflows/ci.yml) ![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey) ![Lint](https://img.shields.io/badge/lint-ruff-informational)

**Purpose**: AI-powered daily task automation with clean operational structure

**Status**: Organized with project-based structure and operational tools

## 🏗️ Structure Overview

### 📁 `/projects/` - Specific Projects
- **`screening_test/`** - Current screening test development project
- Each project contains its own documentation, testing, and deliverables

### 📁 `/operating/` - Daily Operational Tools
- **`email_automation/`** - Email processing and automation tools
- **`document_sync/`** - Google Drive and document synchronization
- **`crawlers/`** - Web data extraction and parsing utilities

### 📁 Root Documentation
- `projectNotes.md` - Master project plans and objectives
- `STRUCTURE.md` - Detailed directory organization guide
- `quick_start_plan.md` - Quick setup instructions  
- `/newWebsitePlanningScripts/` - Planning and organization scripts
- Excel reports and automation utilities

## Export Ready:
✅ **Self-contained**: All dependencies included  
✅ **Portable**: Can be moved to any project context  
✅ **Documented**: Clear usage instructions and examples  
✅ **Modular**: Individual tools can be used separately  

## Key Features:
- Email template generation
- Website crawling and analysis  
- Project note management
- Task automation scripts
- Report generation tools

## Usage:
Copy entire `3_dailyAssistant/` folder to any project for instant AI assistance capabilities.

## 🧪 Testing
This repository now includes initial automated tests (pytest) for the ZoteroPDF RAG components.

Install dependencies (ensure environment active):
```bash
pip install -e .
```

Run all tests:
```bash
pytest -q
```

Run a specific test:
```bash
pytest tests/test_index.py::test_index_creation_and_search -q
```

Notes:
- Tests generate synthetic annotated markdown docs (no external data required).
- FAISS in-memory index built per test session.
- No network calls to OpenRouter (LLM) are performed; generation is mocked where needed.
- Future: add evaluation harness + regression query suite.
