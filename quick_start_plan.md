# Quick Start Plan - DailyAssistant

## Immediate Next Steps (Start Small)

### 1. Google Drive Sync Setup

```bash
# Install Google Drive client for macOS
brew install --cask google-drive

# Alternative: Use rclone for command-line sync
brew install rclone
rclone config  # Configure Google Drive
```

### 2. Document Loading Script

Create a simple Python script to:

- Monitor Google Drive folder
- Load documents automatically
- Parse common formats (PDF, DOCX, TXT)

### 3. Screening Test Project Focus

Priority: Set up basic document processing for screening test materials

## Quick Commands

```bash
# Create Google Drive sync folder
mkdir -p ~/GoogleDrive/DailyAssistant
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install google-api-python-client python-docx PyPDF2
```

## Files to Create Next

1. `gdrive_sync.py` - Google Drive integration
2. `document_loader.py` - Document processing
3. `screening_test/` - Project-specific folder

## Goal

Get basic document sync working → Focus on screening test project
