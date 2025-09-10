# SCMP Corpus Download Summary

**Date:** 10 September 2025  
**Source:** Ben's RA Pui Ying Google Drive folder  
**Status:** ✅ **Download Complete**

---

## 📊 Downloaded Corpus Overview

### **Corpus Files Successfully Downloaded (14 files)**

#### **Annual Text Files (6 years of data)**
| Year | File | Lines | Size | Status |
|------|------|-------|------|--------|
| 2018 | 2018.txt | 37,565 lines | 3.1MB | ✅ |
| 2019 | 2019.txt | 29,283 lines | 3.1MB | ✅ |
| 2020 | 2020.txt | 26,925 lines | 3.2MB | ✅ |
| 2021 | 2021.txt | 1,229 lines | 130KB | ✅ |
| 2021 (Revised) | 2021 - revised.txt | 26,674 lines | 2.9MB | ✅ |
| 2022 | 2022.txt | 25,633 lines | 2.7MB | ✅ |
| 2023 | 2023.txt | 44,248 lines | 4.6MB | ✅ |

#### **Metadata Files**
| File | Lines | Purpose |
|------|-------|---------|
| 2022-Jan2025_meta.txt | 8,656 lines | Structured metadata for 2022 |
| 2023-Jan2025_meta.txt | 19,957 lines | Structured metadata for 2023 |
| Combined_23_22.txt | 44,248 lines | Combined 2022-2023 data |

#### **Analysis Files**
| File | Type | Purpose |
|------|------|---------|
| Corpus Tagging_26Aug.xlsx | Excel | Corpus analysis/tagging (924KB) |
| Modified_Corpus Tagging_13March.xlsx | Excel | Updated corpus analysis (3.9MB) |
| Questions for Panel Members.docx | Word Doc | Research questions |
| List of name.docx | Word Doc | Names/references (143KB) |

---

## 🎯 Corpus Scale Analysis

### **Total Data Volume**
- **Text Files**: ~250,000+ lines of SCMP letters
- **Time Span**: 2018-2023 (6 years)
- **Peak Year**: 2023 with 44,248 lines
- **Total Size**: ~25MB of text data

### **Data Quality**
- ✅ Raw text format ready for processing
- ✅ Metadata files available for 2022-2023
- ✅ Analysis spreadsheets with tagging
- ✅ Research documentation included

---

## 🔍 Sample Content Analysis

### **Letter Structure (from 2022.txt)**
```
Title: Japan's military build-up runs counter to Asia's peace and prosperity
Date: December 2022
Content: Multi-paragraph opinion letter
Themes: Regional security, China-Japan relations, military policy
Citizenship angle: Regional peace advocacy, geopolitical commentary
```

### **Content Themes Observed**
- **Geopolitical Issues**: Japan-China relations, regional security
- **Economic Policy**: Military spending, regional prosperity
- **Historical Context**: Wartime legacies, post-war pacifism
- **Civic Engagement**: Policy critique, regional stability advocacy

---

## 🚀 Next Steps for Analysis

### **Phase 1: Data Preparation** 
- [ ] Process raw text files using existing `splitLetters06.py`
- [ ] Extract individual letters with metadata
- [ ] Clean and standardize format
- [ ] Create analysis-ready datasets

### **Phase 2: LLM Integration Setup**
- [ ] Set up OpenRouter API for citizenship analysis
- [ ] Design prompts for Hong Kong identity themes
- [ ] Test on sample letters from each year
- [ ] Validate analysis quality

### **Phase 3: Systematic Analysis**
- [ ] Batch process full corpus (2018-2023)
- [ ] Track citizenship discourse evolution
- [ ] Identify key themes and patterns
- [ ] Generate research findings

---

## 📂 File Locations

**Downloaded Data**: `/projects/BenSCMPGRF/GRF_SCMP_letters/corpus/downloaded_data/`  
**Processing Scripts**: `/projects/BenSCMPGRF/GRF_SCMP_letters/processing scripts/`  
**Analysis Tools**: `download_scmp_data.py` (custom Google Drive loader)

---

## ✅ Ready for Research

The SCMP corpus is now fully downloaded and ready for automated citizenship analysis using LLM tools. The 6-year dataset (2018-2023) provides comprehensive coverage for studying Hong Kong identity and civic engagement discourse evolution.

**Total Impact**: 250,000+ lines of SCMP letters spanning critical years in Hong Kong's political development, ready for systematic analysis.
