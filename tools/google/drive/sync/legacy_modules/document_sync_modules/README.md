# Document Sync Module

## Purpose
Synchronize documents between various cloud storage services and local project directories.

## Features
- **Google Drive Integration**: Sync documents from Google Drive to local folders
- **File Format Support**: PDF, DOCX, TXT, MD, DOC
- **Automatic Organization**: Preserves folder structure
- **Incremental Sync**: Only updates changed files

## Usage

### Google Drive Sync
```bash
# Run from any location
python3 /path/to/modules/document_sync/gdrive_sync.py

# The script will:
# 1. Check Google Drive DailyAssistant folder
# 2. Sync supported files to synced_docs/
# 3. Report sync status
```

### Configuration
- **Google Drive Path**: Automatically detected via CloudStorage
- **Local Sync Path**: `synced_docs/` in project root
- **Supported Extensions**: `.pdf`, `.docx`, `.txt`, `.md`, `.doc`

### Integration with Projects
```bash
# From project directory
cd projects/screening_test/
python3 ../../modules/document_sync/gdrive_sync.py
```

## Files
- `gdrive_sync.py` - Main synchronization script
- `README.md` - This documentation

## Future Enhancements
- [ ] OneDrive integration
- [ ] Dropbox support  
- [ ] Real-time sync monitoring
- [ ] Conflict resolution
- [ ] Selective folder sync

---
*Module: Document Sync | Updated: September 6, 2025*
