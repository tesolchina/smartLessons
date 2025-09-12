# ZoteroMDsMineru3 Workflow Documentation

## Overview
This document describes the technical workflow for processing Zotero PDFs into organized Markdown files and managing them through GitHub.

## Processing Pipeline

### 1. PDF to Markdown Conversion (MinERU)
The project uses **MinERU** (likely a PDF-to-Markdown conversion tool) to process academic PDFs from Zotero into structured Markdown format.

**Input**: PDF files from Zotero library
**Output**: Markdown (.md) files with extracted text, structure, and metadata
**Location**: Originally processed in `D:\minerU_outputs\` (Windows environment)

### 2. File Organization (`mdMove.py`)

**Purpose**: Organizes scattered Markdown files from MinERU output into a consolidated structure

**Functionality**:
- Traverses the MinERU output directory structure
- Finds all `.md` files recursively 
- Renames files by prepending the parent folder name (Zotero item ID)
- Copies all files to a single output directory
- Pattern: `{zotero_folder}_{original_filename}.md`

**Example transformation**:
```
D:\minerU_outputs\ABC123\paper.md → D:\mineru_mds_sorted_by_script\ABC123_paper.md
D:\minerU_outputs\XYZ789\document.md → D:\mineru_mds_sorted_by_script\XYZ789_document.md
```

### 3. GitHub Upload Management (`GitUpMD5.py`)

**Purpose**: Bulk upload organized Markdown files to GitHub repository with intelligent organization and error handling

**Key Features**:

#### Automatic Directory Organization
- **Problem**: GitHub truncates directory listings at 1,000 files
- **Solution**: Automatically splits large file collections into subdirectories (`batch_001`, `batch_002`, etc.)
- **Limit**: 999 files per subdirectory to stay under GitHub's limits

#### Robust Upload Management
- **Rate Limiting**: Respects GitHub API rate limits (5,000 requests/hour)
- **Error Recovery**: Saves failed uploads to `upload_state.json` for retry
- **Duplicate Detection**: Compares file content using base64 encoding to avoid duplicate uploads
- **Concurrent Processing**: Uses ThreadPoolExecutor for parallel uploads (configurable workers)

#### Upload States
- **Success**: File uploaded successfully
- **Skipped**: File already exists with identical content
- **Failed**: Upload failed due to API errors (saved for retry)
- **Error**: Exception occurred during processing

#### Configuration
- Target repository: `ahmad-rev0/ZoteroMDsMineru3`
- Source directory: `D:\mineru_mds_sorted_by_script`
- Default workers: 2 (to respect rate limits)
- Force update: Enabled (overwrites existing files)

## Current Data Organization

### Repository Structure
```
data/
├── batch_001/    # ~1,000 processed MD files
└── batch_002/    # ~930 processed MD files
```

### File Naming Convention
Files follow the pattern: `out_{ZOTERO_ID}_{PAPER_INFO}.md`

Examples:
- `out_22MV5CS2_The_influences_of_international.md`
- `out_24AE7ZXZ_2020_HKDSE_ENG_P2.md`
- `out_2EVEAMNB_Ekin_-_2023_-_Prompt_Engineerin.md`

## Quality Control Needs

### PDF Source Retrieval
**Issue**: Need to access original PDF files to verify conversion quality
**Required**: 
- Mapping between Zotero IDs and original PDF locations
- Sample-based quality assessment of MinERU conversion
- Identification of conversion errors or missed content

### Conversion Quality Assessment
**Metrics to evaluate**:
- Text extraction accuracy
- Table/figure preservation
- Mathematical notation handling
- Citation format retention
- Document structure maintenance

## Deployment Planning

### Online Tool Requirements

#### Web Interface Components
1. **File Upload Portal**
   - Drag-and-drop PDF upload
   - Batch processing capabilities
   - Progress tracking

2. **Processing Dashboard**
   - Real-time conversion status
   - Quality metrics display
   - Error reporting

3. **Output Management**
   - Markdown preview
   - Download options (individual/batch)
   - GitHub integration for direct repository commits

#### Technical Infrastructure
- **Backend**: Python-based API (FastAPI/Flask)
- **Processing**: MinERU integration
- **Storage**: Cloud storage for temporary files
- **Database**: Metadata and processing history
- **Authentication**: GitHub OAuth for repository access

#### Deployment Options
1. **Cloud Platforms**: 
   - AWS (EC2, Lambda, S3)
   - Google Cloud Platform
   - Microsoft Azure

2. **Containerization**: Docker for consistent deployment
3. **CI/CD**: GitHub Actions for automated deployment

## Next Steps

### Immediate Actions
1. **Script Documentation**: ✅ Completed
2. **PDF Source Mapping**: Create inventory of original PDF locations
3. **Quality Assessment**: Design evaluation framework
4. **Web Interface Design**: Create mockups and user flow

### Development Priorities
1. Quality control automation
2. Web interface development
3. Cloud deployment setup
4. User authentication system
5. Batch processing optimization

---
*Last updated: September 6, 2025*
