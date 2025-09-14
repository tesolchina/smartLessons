# SCMP Letters Research Corpus

**Generated:** 2025-09-14 19:36:51

## Corpus Overview

This corpus contains individual letters extracted from the South China Morning Post's 'Letters to the Editor' section. Each letter represents a unique viewpoint from readers on various topics affecting Hong Kong, China, and the region.

## Statistics

| Metric | Value |
|--------|-------|
| Total Letters | 2 |
| Total Words | 288 |
| Average Letter Length | 144 words |
| Unique Authors | 1 |
| Letters with Known Authors | 1 |
| Content Length Range | 359-1416 characters |

## Directory Structure

```
final_research_corpus/
├── json/                    # Individual letters in JSON format
├── markdown/                # Individual letters in Markdown format
├── corpus_summary_20250914_193651.json # Complete corpus metadata
└── README.md               # This documentation
```

## Usage for Research

### Loading Individual Letters
```python
import json
import os

# Load all letters
letters = []
json_dir = 'json/'
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        with open(os.path.join(json_dir, filename), 'r') as f:
            letters.append(json.load(f))
```

### Corpus Summary
```python
# Load corpus metadata
with open('corpus_summary_20250914_193651.json', 'r') as f:
    corpus = json.load(f)
    print(f"Total letters: {corpus['statistics']['total_letters']}")
```

## Data Quality

- **Content Extraction:** Complete webpage content using fetch_webpage approach
- **Letter Separation:** Individual letters identified by ### headings
- **Author Attribution:** Names and locations extracted from letter endings
- **Content Filtering:** Advertisements and navigation content removed
- **Minimum Length:** Letters must have >150 characters of substantive content

## Source

- **Website:** South China Morning Post
- **Section:** Letters to the Editor
- **URL:** https://www.scmp.com/comment/letters
- **Extraction Date:** 2025-09-14
- **Methodology:** Automated extraction with manual validation
