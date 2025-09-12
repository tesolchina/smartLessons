# Generic Document Enhancement Tools - Usage Guide

## Overview
This suite provides reusable tools for analyzing Word documents and enhancing markdown files with supporting evidence and excerpts from multiple sources.

## Tools Available

### 1. Universal Document Enhancer (`universal_document_enhancer.py`)
**Primary tool for most use cases**

#### Basic Usage:
```bash
python3 universal_document_enhancer.py report.md --sources document1.docx document2.docx --output enhanced_report.md
```

#### Advanced Usage with Configuration:
```bash
# Create template configuration
python3 universal_document_enhancer.py --create-config my_config.json

# Edit my_config.json to customize topics and keywords

# Use custom configuration
python3 universal_document_enhancer.py report.md --config my_config.json --output enhanced_report.md
```

#### Configuration File Format:
```json
{
  "topic_mappings": {
    "AI_Technology": ["AI", "artificial intelligence", "machine learning"],
    "Assessment": ["assessment", "evaluation", "rubric", "testing"],
    "Curriculum": ["curriculum", "course design", "learning outcomes"]
  },
  "max_excerpts_per_topic": 3,
  "excerpt_max_length": 250,
  "source_documents": ["doc1.docx", "doc2.docx"],
  "cross_reference_analysis": true
}
```

### 2. Generic Document Analyzer (`generic_document_analyzer.py`)
**For detailed analysis and keyword extraction**

#### Usage:
```bash
python3 generic_document_analyzer.py document1.docx document2.docx --format json --output analysis_results
```

#### Features:
- Keyword frequency analysis across categories
- Document structure extraction
- Cross-document connection identification
- JSON and markdown output formats

### 3. Markdown Enhancer (`markdown_enhancer.py`)
**For lightweight enhancement with auto-detection**

#### Usage:
```bash
python3 markdown_enhancer.py existing_report.md source1.docx source2.docx --auto-detect --output enhanced_report.md
```

#### Features:
- Auto-detects topics from markdown headings
- Finds relevant excerpts based on topic keywords
- Adds supporting evidence sections

### 4. LC-Specific Enhancer (`lc_markdown_enhancer.py`)
**Optimized for Language Center documents**

#### Usage:
```bash
python3 lc_markdown_enhancer.py
```
*Automatically processes all LC markdown files in the PMC directory*

## Customization Examples

### Academic Research Papers:
```json
{
  "topic_mappings": {
    "Methodology": ["methodology", "method", "approach", "framework"],
    "Results": ["results", "findings", "outcomes", "data"],
    "Literature": ["literature review", "previous work", "related studies"],
    "Innovation": ["novel", "innovative", "contribution", "breakthrough"]
  }
}
```

### Business Reports:
```json
{
  "topic_mappings": {
    "Strategy": ["strategy", "planning", "objectives", "goals"],
    "Performance": ["performance", "metrics", "KPI", "results"],
    "Technology": ["technology", "digital", "automation", "systems"],
    "Operations": ["operations", "processes", "workflow", "efficiency"]
  }
}
```

### Education Documents:
```json
{
  "topic_mappings": {
    "Pedagogy": ["teaching", "learning", "pedagogy", "instruction"],
    "Assessment": ["assessment", "evaluation", "grading", "testing"],
    "Curriculum": ["curriculum", "syllabus", "course design", "learning outcomes"],
    "Technology": ["EdTech", "digital tools", "online learning", "AI"]
  }
}
```

## Output Examples

### Generated Evidence Section:
```markdown
## Supporting Evidence and Documentation

### From Policy Document
**Strategy Planning:**
1. *"The institution will implement a comprehensive strategic framework focusing on digital transformation and student-centered learning approaches..."*

**Assessment Innovation:**  
1. *"New assessment methodologies will incorporate both formative and summative evaluation techniques with technology-enhanced feedback systems..."*

### From Implementation Guide
**Technology Integration:**
1. *"Digital tools and AI-assisted learning platforms will be gradually introduced across all academic programs with appropriate faculty training..."*

### Cross-Document Analysis
**Strategic Alignment:** This topic appears across 2 documents (Policy Document: 15, Implementation Guide: 12 mentions), indicating strong institutional commitment.
```

## Best Practices

### 1. Topic Mapping Strategy:
- Use specific, domain-relevant keywords
- Include synonyms and variations
- Balance broad and narrow terms

### 2. Excerpt Quality:
- Adjust `excerpt_max_length` based on document density
- Use `max_excerpts_per_topic` to control information volume
- Enable `cross_reference_analysis` for multi-document insights

### 3. File Organization:
- Keep source documents in consistent locations
- Use descriptive output filenames
- Save configurations for reuse across similar projects

### 4. Iterative Refinement:
- Start with default configurations
- Review generated excerpts for relevance
- Refine topic mappings based on results
- Create project-specific configuration templates

## Integration with Other Tools

### With Git Version Control:
```bash
# Enhance documents and commit changes
python3 universal_document_enhancer.py report.md --sources *.docx
git add enhanced_report.md
git commit -m "Enhanced report with supporting evidence"
```

### With Batch Processing:
```bash
# Process multiple markdown files
for md_file in *.md; do
    python3 universal_document_enhancer.py "$md_file" --sources source1.docx source2.docx
done
```

### With Automation Scripts:
```python
from universal_document_enhancer import UniversalDocumentEnhancer, EnhancementConfig

# Programmatic usage
config = EnhancementConfig.from_json('my_config.json')
enhancer = UniversalDocumentEnhancer(config)
enhanced_content = enhancer.enhance_markdown_file('report.md')
```

## Troubleshooting

### Common Issues:
1. **Import errors**: Ensure `python-docx` is installed: `pip install python-docx`
2. **File not found**: Use absolute paths or check working directory
3. **Empty excerpts**: Verify keywords match document content
4. **Long processing time**: Reduce `max_excerpts_per_topic` for large documents

### Performance Optimization:
- Limit source documents to most relevant ones
- Use specific topic mappings rather than broad keyword lists
- Process documents in batches for large projects

## Future Extensions

These tools can be extended for:
- PDF document support
- Real-time document monitoring
- Web-based interface
- Integration with document management systems
- Multi-language support
- Advanced NLP analysis
