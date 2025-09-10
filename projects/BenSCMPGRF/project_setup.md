# Ben SCMP GRF Project - Setup and Analysis Framework

**Date:** 10 September 2025  
**Project:** SCMP Letters Corpus Analysis for Citizenship Practices in Hong Kong  
**Collaborator:** Ben  
**Repository:** https://github.com/tesolchina/GRF_SCMP_letters.git

---

## 🎯 Project Overview

### Research Objective
Develop a corpus of SCMP letters to explore how writers practice their citizenship in the Hong Kong context, using LLM automation via OpenRouter API for analysis.

### Repository Structure (Cloned)
```
GRF_SCMP_letters/
├── README.md
├── Save_Matched_letter/
├── corpus/
│   ├── input letters/
│   │   ├── 2022/
│   │   ├── 2022-Jan2025.txt
│   │   ├── 2022-Jan2025_meta.txt
│   │   ├── 2023-Jan2025.txt
│   │   ├── 2023-Jan2025_meta.txt
│   │   ├── simple_input.txt
│   │   └── simple_input_meta*.txt
│   └── output report/
└── processing scripts/
    ├── splitLetters06.py
    ├── addMeta17-20.py
    └── count_letter_author.py
```

---

## 📊 Current Corpus Status

### Available Data
- **2022 Letters**: Main corpus file with metadata
- **2023 Letters**: Extended corpus with metadata
- **Sample Data**: `simple_input.txt` with processed examples

### Data Structure
Each letter includes:
- Title
- Publication date (month)
- Word count
- Full text content
- Metadata extraction

### Sample Letter Analysis
```
Letter 1: "Rethinking what it means to be literate in the age of AI"
- Date: December (2022)
- Word Count: 514 words
- Theme: Education, AI, literacy in digital age
- Citizenship angle: Civic engagement with technology policy
```

---

## 🔧 Current Processing Pipeline

### Existing Scripts
1. **`splitLetters06.py`**: Main text processing script
   - Splits combined text files into individual letters
   - Adds metadata (title, date, word count)
   - Creates structured output with letter numbering

2. **`addMeta17-20.py`**: Metadata enhancement scripts
   - Various versions for different metadata requirements

3. **`count_letter_author.py`**: Author analysis
   - Counts and analyzes letter authorship patterns

---

## 🤖 LLM Integration Plan

### OpenRouter API Setup
- **Available**: OpenRouter API configuration from existing modules
- **Location**: `modules/openRouterAI/` (already configured)
- **Model Selection**: Non-OpenAI models for HK compliance

### Proposed Analysis Framework

#### 1. **Citizenship Theme Analysis**
```python
# Analyze how letters demonstrate citizenship practices
themes = [
    "civic_engagement",
    "policy_advocacy", 
    "community_concerns",
    "rights_discourse",
    "democratic_participation",
    "local_vs_national_identity"
]
```

#### 2. **Automated Content Analysis**
- **Sentiment Analysis**: Tone toward government, policies
- **Topic Modeling**: Key issues and concerns
- **Rhetorical Strategies**: How writers construct arguments
- **Identity Markers**: Hong Kong vs. broader Chinese identity

#### 3. **Corpus-level Insights**
- Temporal trends in citizenship discourse
- Issue prioritization over time
- Language patterns and civic vocabulary

---

## 🚀 Next Steps

### Phase 1: Environment Setup
- [x] Clone repository
- [ ] Set up OpenRouter API integration
- [ ] Create analysis pipeline structure
- [ ] Test with sample data

### Phase 2: Data Preparation  
- [ ] Process full 2022-2023 corpus
- [ ] Clean and standardize metadata
- [ ] Create analysis-ready datasets
- [ ] Validate data quality

### Phase 3: LLM Analysis Implementation
- [ ] Develop citizenship analysis prompts
- [ ] Implement automated processing pipeline
- [ ] Run batch analysis on full corpus
- [ ] Generate preliminary findings

### Phase 4: Results and Validation
- [ ] Analyze patterns and trends
- [ ] Validate findings with manual review
- [ ] Prepare research outputs
- [ ] Document methodology

---

## 💡 Research Questions

### Primary Questions
1. How do SCMP letter writers construct and express their Hong Kong identity?
2. What civic engagement strategies appear most frequently?
3. How has citizenship discourse evolved from 2022-2023?

### Secondary Questions
1. What linguistic patterns characterize different types of civic participation?
2. How do writers balance local vs. national identity claims?
3. What issues mobilize the most citizen response?

---

## 🔗 Integration with Existing Tools

### Available Resources
- **OpenRouter API**: Pre-configured LLM access
- **Processing Scripts**: Text splitting and metadata extraction
- **Corpus Data**: 2022-2023 SCMP letters with metadata

### Technical Setup
- Python environment ready
- API keys configured
- Repository cloned and accessible

---

## 📝 Notes

- Repository includes Google Drive link for additional data
- Existing processing scripts provide good foundation
- Ready to begin LLM integration for automated analysis
- Focus on Hong Kong citizenship practices and identity construction

**Next Action**: Set up OpenRouter integration for citizenship theme analysis
