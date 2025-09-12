# Citation Review System Usage Example

## Scenario
You have a manuscript that cites 40 reference papers, and you want to ensure your citations are appropriate and comprehensive.

## Quick Start

### 1. Command Line Usage

```bash
# Full manuscript review
python scripts/citation_reviewer.py \
    --manuscript my_paper.md \
    --references faiss_index \
    --output citation_review.md

# Analyze specific section
python scripts/citation_reviewer.py \
    --manuscript my_paper.md \
    --references faiss_index \
    --section "Literature Review" \
    --output literature_review_analysis.md
```

### 2. Streamlit Web Interface

```bash
# Launch the citation review interface
streamlit run citation_app.py
```

Then:
1. Upload your manuscript file or paste text
2. Configure the reference corpus path
3. Choose analysis type (full or section-specific)
4. Review results and download reports

## What You Get

### Citation Analysis Report
```markdown
# Citation Review Report

**Total Citations**: 15
**Analysis Date**: 2025-09-13

## Overall Assessment
Your manuscript shows good citation coverage but could benefit from:
- Adding more recent studies (2023-2024)
- Strengthening methodological references
- Including pedagogical implications from Johnson et al. (2023)

## Individual Citation Analysis

### Citation 1: (Smith et al., 2022)
**Context**: ...cooperative learning has been shown to improve student engagement (Smith et al., 2022)...
**Status**: partially_appropriate
**Reason**: Citation is relevant but misses key methodological details

**Suggested Improvements**:
Consider mentioning Smith et al.'s specific finding about peer interaction duration (15-20 minutes optimal) and their sample size (N=240 students across 12 classrooms).

**Additional Citations**:
- Johnson & Johnson (2023) - Recent meta-analysis on cooperative learning
- Brown et al. (2024) - Pedagogical implications for online environments
```

### Key Features

#### 🔍 Citation Extraction
- Automatically detects various citation formats: (Author, 2023), Author et al., 2023, etc.
- Captures citation context for analysis
- Handles multiple citation styles

#### 📊 Appropriateness Assessment
- **Appropriate**: Citation is well-used and contextually correct
- **Partially Appropriate**: Citation is relevant but could be improved
- **Inappropriate**: Citation doesn't fit the context or is misused

#### 💡 Improvement Suggestions
- Missing aspects from the cited paper
- Better ways to integrate the citation
- Specific details to add from the source

#### 📚 Related Paper Discovery
- Finds similar papers from your 40-paper corpus
- Suggests additional citations to strengthen arguments
- Identifies gaps in literature coverage

#### 🎯 Section-Specific Analysis
Perfect for targeted improvements:
- Literature Review section enhancement
- Methodology section citation strengthening
- Discussion section gap analysis

## Example Workflow

### Step 1: Prepare Your Reference Corpus
```bash
# Index your 40 reference papers
python scripts/index.py --create \
    --annotated reference_papers/ \
    --index faiss_index
```

### Step 2: Analyze Your Manuscript
```bash
# Get comprehensive citation review
python scripts/citation_reviewer.py \
    --manuscript dissertation_chapter3.md \
    --references faiss_index \
    --output chapter3_citation_review.md
```

### Step 3: Review and Improve
1. Check overall assessment for systematic issues
2. Review each citation's appropriateness
3. Add suggested additional citations
4. Strengthen weak sections identified in the analysis
5. Re-run analysis to track improvements

## Integration with Existing RAG System

The citation reviewer leverages your existing RAG infrastructure:

- **Uses the same FAISS index** from your 40 reference papers
- **Leverages pedagogical filtering** for education-focused manuscripts
- **Integrates with OpenRouter API** for consistent LLM responses
- **Builds on search capabilities** for finding related papers

## Advanced Features

### Batch Processing
```bash
# Review multiple chapters
for chapter in chapter*.md; do
    python scripts/citation_reviewer.py \
        --manuscript "$chapter" \
        --references faiss_index \
        --output "${chapter%.md}_review.md"
done
```

### Section-Specific Deep Dive
```bash
# Focus on specific sections needing improvement
python scripts/citation_reviewer.py \
    --manuscript paper.md \
    --references faiss_index \
    --section "Theoretical Framework" \
    --output theory_section_analysis.md
```

### Export Integration
The system generates reports compatible with:
- Academic writing tools (Markdown format)
- Reference managers (structured JSON output)
- Collaborative review (shareable HTML reports)

## Benefits for Academic Writing

1. **Comprehensive Coverage**: Ensures you're not missing relevant citations from your corpus
2. **Appropriate Usage**: Verifies citations are used correctly in context
3. **Gap Identification**: Finds areas needing stronger literature support
4. **Quality Improvement**: Specific suggestions for better citation integration
5. **Efficiency**: Automated analysis saves manual review time
6. **Consistency**: Systematic approach to citation quality across sections
