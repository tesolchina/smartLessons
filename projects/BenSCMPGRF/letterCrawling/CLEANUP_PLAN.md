# SCMP Letters Crawler - Script Cleanup Plan

## Scripts to Keep (Production Ready)

### 1. `comprehensive_extraction.py` - **MAIN SCRIPT**
- **Purpose**: Complete pipeline for extracting individual letters from all 25 pages
- **Status**: Production ready, uses fetch_webpage methodology
- **Features**: 
  - Loads original dataset (25 pages)
  - Demonstrates proper extraction methodology
  - Uses ### heading pattern for letter separation
  - Author detection and content cleanup
  - Comprehensive corpus creation
- **Usage**: Main script for future weekly crawling and letter extraction

### 2. `enhanced_extraction.py` - **DEMONSTRATION SCRIPT**
- **Purpose**: Enhanced extraction with pre-fetched content from 4 sample pages
- **Status**: Production ready, working demonstration
- **Features**:
  - Processes 4 pages with complete fetch_webpage content
  - Successfully extracts 6 individual letters
  - Shows proper ### heading methodology
  - Author attribution working correctly
- **Usage**: Reference implementation and testing

### 3. `scmp_letters_crawler.py` - **BASIC CRAWLER**
- **Purpose**: Initial crawler for getting letter page listings
- **Status**: Production ready, basic functionality
- **Features**:
  - Crawls SCMP letters main page
  - Extracts letter page URLs and metadata
  - Saves to JSON format
- **Usage**: For getting fresh letter page listings

## Scripts to Archive (Historical/Development)

### 4. `fetch_all_letters.py` - Working but superseded
- Contains working extraction logic but superseded by comprehensive_extraction.py
- Successfully extracted 2 demo letters in testing
- Keep for reference but not main production use

### 5. `demo_proper_extraction.py` - Proof of concept
- Successfully demonstrated correct methodology (4 letters from 2 pages)
- Identified the ### heading approach that solved the problem
- Keep for reference and methodology validation

## Scripts to Remove (Deprecated/Broken)

### Broken/Failed Approaches:
- `split_individual_letters.py` - FAILED approach that created 89 fake letters
- `test_page_extraction.py` - Test script, no longer needed
- `debug_crawler.py` - Debug script, purpose served
- `analyze_page_html.py` - Analysis script, no longer needed

### Superseded Scripts:
- `extract_letter_content.py` - Superseded by comprehensive approach
- `resume_extraction.py` - One-time use script for interruption recovery
- `cleanup_letters.py` - One-time use script for file merging
- `create_research_corpus.py` - Functionality moved to comprehensive script
- `complete_extraction.py` - Superseded by comprehensive_extraction.py
- `manual_letter_extraction.py` - Manual example, no longer needed
- `proper_letter_separator.py` - Development script, superseded

## Recommended File Structure

```
letterCrawling/
├── README.md                     # Usage documentation
├── scmp_crawler.py              # Renamed from scmp_letters_crawler.py
├── comprehensive_extraction.py   # Main production script
├── enhanced_extraction.py       # Demonstration/reference script
├── utils/
│   ├── fetch_all_letters.py    # Archived working script
│   └── demo_proper_extraction.py # Archived proof of concept
└── note.md                      # Keep existing notes
```

## Next Steps

1. Create README.md with usage instructions
2. Remove deprecated scripts
3. Move archive scripts to utils/ folder
4. Rename scmp_letters_crawler.py to scmp_crawler.py for clarity
5. Test that remaining scripts work correctly