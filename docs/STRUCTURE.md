# DailyAssistant - Clean Operational Structure

## Directory Organization

### 📁 `/projects/` - Specific Projects
Individual projects with dedicated timelines and objectives.

```
projects/
└── screening_test/               # Screening Test Development Project
    ├── README.md                # Project overview
    ├── my_updates.md           # Personal progress tracking
    ├── screening_test_project.md # Main project document
    ├── modules/                # Project-specific modules
    ├── test_questions/         # Question bank
    ├── ui_testing/            # UI testing documentation & logs
    ├── ui_testing_templates/  # Reusable testing templates
    └── meeting_notes/         # Meeting minutes
```

### 📁 `/operating/` - Daily Operational Tools
Administrative and operational automation tools used across all projects.

```
operating/
├── README.md                   # Operational tools guide
├── emailRetrieval.md          # Email extraction notes
├── email_automation/          # Email processing and automation
│   ├── email_retrieval_script.py # Extract emails from Outlook
│   ├── email_drafts/          # Draft templates and storage
│   └── README.md              # Email automation guide
├── document_sync/             # Document synchronization tools
│   ├── gdrive_sync.py         # Google Drive sync script
│   └── README.md              # Sync documentation
└── crawlers/                  # Web data extraction utilities
    ├── crawler.py             # Generic web crawler
    ├── parser02.py            # Data parsing tools
    └── sitemap_parser.py      # Sitemap processing
```

### 📁 `/synced_docs/` - Synchronized Documents
Documents pulled from various sources (Google Drive, etc.).

## Key Benefits

### ✅ **Clear Separation**
- **Projects**: Specific, time-bound objectives with their own resources
- **Operating**: Daily operational tools used across all work
- **Root**: Project planning and overall documentation

### ✅ **Operational Focus** 
- Email automation for daily communication
- Document sync for file management
- Web crawlers for data extraction
- All tools work across projects

### ✅ **Simplified Structure**
- No more separate modules - everything is either project-specific or operational
- Easier navigation and maintenance
- Clear purpose for each directory

## Usage Examples

### Using Document Sync Module
```bash
# From any project directory
python3 ../../modules/document_sync/gdrive_sync.py
```

### Using Email Automation
```bash
# Extract project-related emails
python3 ../../modules/email_automation/email_retrieval_script.py
```

### Project Development
```bash
# Work on screening test
cd projects/screening_test/
# All project-specific files are contained here
```

## Quick Navigation

- **Current Project**: `projects/screening_test/`
- **Email Tools**: `modules/email_automation/`
- **Sync Tools**: `modules/document_sync/`
- **Main Docs**: Root directory (README.md, projectNotes.md)

---
*Reorganized: September 6, 2025*
*Structure: Projects + Reusable Modules*
