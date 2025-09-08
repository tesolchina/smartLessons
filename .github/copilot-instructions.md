# Copilot Instructions for DailyAssistant

## Project Architecture
- **Modular Structure:** Major components are organized under `/operating/` (operational tools), `/modules/` (reusable modules), and `/projects/` (project-specific deliverables).
- **Service Boundaries:** Each subfolder is a self-contained system (e.g., `GoogleSlidesGenerator` for markdown-to-slides, `email_automation` for email workflows, `document_sync` for cloud sync).
- **Data Flow:** Most automation scripts process input files (markdown, email, docs), transform them, and output results to Google Drive, Mail.app, or local folders.
- **Why:** Structure enables rapid onboarding, clear separation of concerns, and easy extension for new automation tasks.

## Developer Workflows
- **Build/Test:** No global build system; run scripts directly (e.g., `python3 email_workflow.py`).
- **Debugging:** Use print/log statements; logs are stored in `logs/` subfolders where present.
- **Google API Setup:** For Google integrations, ensure credentials (`credentials.json`, `token.pickle`) are present in the relevant module.
- **Batch Processing:** Use batch scripts (e.g., `batch_converter.py` in `GoogleSlidesGenerator`) for multi-file operations.

## Project-Specific Conventions
- **Markdown-to-Slides:** Use `---` or `##` as slide delimiters in markdown files. See `GoogleSlidesGenerator/README.md` for details.
- **Email Automation:** Main entry is always `email_workflow.py`. Core tools in `core_tools/`, specialized scripts in `specialized_scripts/`.
- **Document Sync:** Run `gdrive_sync.py` from any location; syncs to `synced_docs/` in project root.
- **Config Files:** Use JSON for templates, authentication, and drive mappings. Example: `templates.json`, `auth_config.json`.

## Integration Points & Dependencies
- **Google APIs:** Used for Slides, Docs, Drive. Credentials must be set up per module.
- **External Libraries:** `google-api-python-client`, `google-auth`, `markdown`, `bs4` (BeautifulSoup), etc. See each module's `requirements.txt`.
- **Cross-Component Communication:** Minimal; most modules operate independently. Shared data via project root or Google Drive.

## Examples
- **Convert Markdown to Slides:**
  ```bash
  python3 operating/GoogleSlidesGenerator/markdown_to_slides.py --input "lecture.md" --template "educational"
  ```
- **Sync Google Drive Docs:**
  ```bash
  python3 modules/document_sync/gdrive_sync.py
  ```
- **Automate Email Workflow:**
  ```bash
  python3 operating/email_automation/email_workflow.py
  ```

## Key Files & Directories
- `operating/GoogleSlidesGenerator/` - Markdown to Slides system
- `operating/email_automation/` - Email workflow automation
- `modules/document_sync/` - Google Drive sync
- `projects/` - Project deliverables and documentation

---

For more details, see each module's README.md. If any section is unclear or missing, please provide feedback for further refinement.
