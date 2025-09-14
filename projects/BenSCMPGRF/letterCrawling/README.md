# SCMP Letters Crawler

A Python toolkit for crawling and extracting individual letters from the South China Morning Post Letters to the Editor section.

## Overview

This project crawls SCMP letters pages (not behind paywall) and extracts individual letters from multi-letter pages for research corpus creation. The system can identify and separate individual letters that are published together on the same webpage.

## Features

- **Weekly Letter Crawling**: Automated collection of letter page URLs and metadata
- **Individual Letter Extraction**: Separates multi-letter pages into individual letters
- **Author Attribution**: Identifies letter authors using pattern recognition
- **Content Cleaning**: Removes advertisements, navigation, and metadata
- **Research Corpus Creation**: Generates structured datasets in JSON and Markdown formats
- **Comprehensive Analysis**: Provides statistics and author analysis

## Scripts

### Production Scripts

#### `comprehensive_extraction.py` - Main Extraction Script
**Primary script for complete letter corpus extraction**

```bash
python comprehensive_extraction.py
```

**Features:**
- Processes all 25 pages from original dataset
- Uses fetch_webpage tool for complete content retrieval
- Extracts individual letters using ### heading methodology
- Creates comprehensive research corpus with ~60-75 letters expected
- Generates detailed statistics and author analysis

#### `scmp_crawler.py` - Basic Page Crawler
**Initial crawler for letter page discovery**

```bash
python scmp_crawler.py
```

**Features:**
- Crawls https://www.scmp.com/comment/letters
- Extracts letter page URLs and metadata
- Saves structured data to JSON format
- Use for weekly letter page discovery

#### `enhanced_extraction.py` - Reference Implementation
**Demonstration script with pre-fetched content**

```bash
python enhanced_extraction.py
```

**Features:**
- Processes 4 sample pages with complete content
- Successfully extracts 6 individual letters
- Demonstrates proper ### heading methodology
- Reference for implementation validation

### Utility Scripts (Archive)

#### `utils/fetch_all_letters.py`
- Working extraction logic, superseded by comprehensive_extraction.py
- Successfully extracted 2 demo letters in testing
- Keep for reference implementation

#### `utils/demo_proper_extraction.py`
- Proof of concept that identified correct methodology
- Successfully demonstrated ### heading approach
- Extracted 4 letters from 2 pages properly
- Keep for methodology validation

## Data Sources

- **Source URL**: https://www.scmp.com/comment/letters
- **Content Type**: Letters to the Editor (not behind paywall)
- **Page Structure**: Each page typically contains 2-3 individual letters
- **Letter Separation**: Individual letters marked with ### headings
- **Author Format**: Names typically include location (e.g., "John Smith, Hong Kong")

## Extraction Methodology

### Letter Identification
1. **### Heading Pattern**: Individual letters separated by ### headings
2. **Content Validation**: Letters must have substantial content (>100 characters)
3. **Author Detection**: Pattern matching for names with location information
4. **Content Cleaning**: Remove ads, navigation, and metadata

### Data Structure
```json
{
  "title": "Letter title from ### heading",
  "content": "Cleaned letter content",
  "author": "Author Name, Location",
  "source_url": "Original page URL",
  "main_page_title": "Main page title",
  "content_length": 1234,
  "word_count": 200,
  "extraction_timestamp": "2024-09-14T..."
}
```

## Output Formats

### Research Corpus Structure
```
output_directory/
├── json/
│   ├── letter_001_author_name.json
│   ├── letter_002_author_name.json
│   └── ...
├── markdown/
│   ├── letter_001_author_name.md
│   ├── letter_002_author_name.md
│   └── ...
├── analysis/
└── corpus_summary_YYYYMMDD_HHMMSS.json
```

### Summary Statistics
- Total letters extracted
- Word counts and content analysis
- Author statistics and top contributors
- Processing information and success rates

## Requirements

- Python 3.11+
- `requests` library for HTTP requests
- `beautifulsoup4` for HTML parsing
- Access to `fetch_webpage` tool for complete content retrieval

## Installation

```bash
# Install required packages
pip install requests beautifulsoup4

# Clone repository and navigate to letterCrawling directory
cd letterCrawling
```

## Usage Examples

### Weekly Letter Discovery
```bash
# Crawl for new letter pages
python scmp_crawler.py

# Extract individual letters from discovered pages
python comprehensive_extraction.py
```

### Research Corpus Creation
```bash
# Run enhanced extraction for demonstration
python enhanced_extraction.py

# Check output in enhanced_research_corpus/ directory
```

## Technical Notes

### Content Extraction Challenges
- **Dynamic Content**: SCMP uses dynamic loading, requires fetch_webpage tool
- **Mixed Content**: Pages contain ads, navigation mixed with letter content
- **Author Attribution**: Authors listed at end of letters with location info
- **Multi-Letter Pages**: Individual letters separated by ### headings

### Validation Results
- **Enhanced Extraction**: 6 letters extracted from 4 pages
- **Content Quality**: 391 words average per letter (enhanced dataset)
- **Author Detection**: 50% success rate for author identification
- **Content Cleaning**: Successfully removes navigation and ads

## Project History

### Problem Resolution
1. **Initial Challenge**: Original splitting created 89 fake letters from page subtitles
2. **Root Cause**: Incomplete webpage content in original dataset
3. **Solution**: Use fetch_webpage tool with ### heading methodology
4. **Validation**: Successfully extracted realistic individual letters

### Methodology Evolution
1. **Basic Crawler**: Letter page URL collection
2. **Content Extraction**: Full page content retrieval
3. **Individual Separation**: ### heading-based letter identification
4. **Content Validation**: Author detection and content cleaning

## Future Use

This toolkit is designed for:
- **Weekly Letter Collection**: Automated discovery and extraction
- **Research Corpus Building**: Structured datasets for analysis
- **Content Analysis**: Author patterns and topic identification
- **Academic Research**: Hong Kong public discourse analysis

## Contact

For questions about implementation or research use, refer to the comprehensive extraction script and demonstration results.