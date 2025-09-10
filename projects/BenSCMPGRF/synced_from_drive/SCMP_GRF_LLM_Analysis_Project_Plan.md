# SCMP Letters Citizenship Discourse Analysis: LLM-Enhanced Research Plan

## Project Overview

Based on Ben's 2022/23 GRF application "Communicating Citizenship" and the complete 6-year SCMP letters corpus (2018-2023), this project combines traditional critical discourse analysis with modern LLM automation to analyze citizenship practices in Hong Kong's political discourse.

## Original Research Framework (Ben's GRF Application)

### Core Research Questions
1. **RQ1:** What subjects/issues are foregrounded across letters and how do they link to broader Hong Kong socio-political discourses?
2. **RQ2:** What linguistic/discursive resources do writers use to communicate citizenship positions, claims, goals, and values?  
3. **RQ3:** What epistemologies inform citizenship communication through letter writing?
4. **RQ4:** How can findings validate argumentative letter writing as participatory citizenship?

### Theoretical Framework
- **Critical Discourse Analysis (CDA):** Three-dimensional approach examining discourses, genre, and voice
- **Corpus-Assisted Analysis:** Pattern identification across time periods and linguistic features
- **Citizenship as Practice:** Focus on "communicating citizenship" rather than static definitions
- **Dialectical Approach:** Tension between citizenship as "social location" vs "social positioning"

### Historical Context (2014-2020 in Original Application)
- **Occupy Movement (2014):** Democratic participation demands
- **Extradition Bill Protests (2019):** Opposition to mainland legal jurisdiction  
- **National Security Law (2020):** "Patriots governing Hong Kong" discourse
- **COVID-19 Pandemic:** Civic duty vs individual rights debates

## Enhanced Framework: LLM Integration for 2018-2023 Corpus

### Available Data Assets
- **Complete SCMP Letters Corpus:** 6 years (2018-2023), ~250,000 lines, 14 files
- **Processing Infrastructure:** Existing tools (splitLetters06.py, metadata extraction)
- **LLM Access:** OpenRouter API configured for non-OpenAI models
- **Research Questions Document:** Panel member interview questions for validation

### LLM Analysis Architecture

#### Phase 1: Corpus Preparation and Segmentation
```
Input: 6-year SCMP letters corpus (2018-2023)
Tools: splitLetters06.py, metadata extraction scripts
Output: Individual letters with metadata (date, author, topic, word count)
```

#### Phase 2: Automated Discourse Analysis via LLM
```
Model Selection: Claude-3/GPT-4 via OpenRouter
Prompt Engineering: Based on CDA framework and research questions
Analysis Categories:
- Citizenship positioning (patriot/democrat/civic duty/protest)  
- Argumentation strategies (evidence citation, problem-solution, emotional appeal)
- Temporal discourse shifts (2019 protests, 2020 NSL, 2021-2023 post-NSL)
- Issue classification (politics, pandemic, economy, education, environment)
```

#### Phase 3: Quantitative Pattern Detection
```
Corpus Linguistics Automation:
- Keyword frequency analysis by time period
- Co-occurrence networks for citizenship terms
- Sentiment analysis progression across political events
- Argument structure classification (claim-evidence-warrant)
```

#### Phase 4: Qualitative Deep Analysis
```
Selected Letter Analysis:
- Representative examples per citizenship type
- Micro-linguistic feature analysis (modal verbs, pronoun use, metaphors)
- Intertextual references to government discourse
- Evolution of "patriot" vs "citizen" terminology
```

## Implementation Plan

### Stage 1: Data Processing (Week 1-2)
- [ ] Run existing corpus processing scripts on 2018-2023 data
- [ ] Extract metadata and create structured database
- [ ] Validate data completeness and identify temporal gaps
- [ ] Create sample datasets for LLM testing

### Stage 2: LLM Prompt Development (Week 3-4)  
- [ ] Design prompt templates for each research question
- [ ] Test prompt effectiveness on sample letters
- [ ] Develop classification schemas for citizenship discourse
- [ ] Create automated validation workflows

### Stage 3: Batch Analysis Execution (Week 5-6)
- [ ] Process full corpus through LLM analysis pipeline  
- [ ] Generate quantitative summaries and visualizations
- [ ] Identify high-interest letters for qualitative analysis
- [ ] Cross-reference with major Hong Kong political events

### Stage 4: Research Synthesis (Week 7-8)
- [ ] Compile findings addressing original research questions
- [ ] Compare LLM findings with traditional CDA approaches
- [ ] Document evolution of citizenship discourse 2018-2023
- [ ] Prepare academic paper draft and conference presentations

## Technical Specifications

### LLM Analysis Prompts (Draft Examples)

#### RQ1 Analysis Prompt:
```
Analyze this SCMP letter from [DATE] for public debate topics:

1. Identify main issues discussed (politics, economy, social, etc.)
2. Connect to broader Hong Kong socio-political context
3. Note references to government policies or social movements
4. Classify urgency level and proposed solutions

Letter text: [LETTER_CONTENT]
```

#### RQ2 Citizenship Communication Prompt:
```
Examine linguistic resources used to communicate citizenship:

1. Identify positioning statements (I am, we should, citizens must)
2. Analyze argumentation structure (claims, evidence, warrants)  
3. Note identity markers (Hong Kong people, patriots, residents)
4. Classify citizenship type (civic duty, democratic participation, cultural belonging)

Letter text: [LETTER_CONTENT]
```

### Validation Framework
- **Human-LLM Comparison:** Manual analysis of 100 sample letters to validate LLM accuracy
- **Inter-rater Reliability:** Compare LLM outputs across different models/prompts
- **Historical Validation:** Cross-reference findings with documented political events
- **Expert Review:** Consultation with Hong Kong political discourse scholars

## Expected Outcomes

### Academic Deliverables
- **Research Paper:** "Communicating Citizenship in Crisis: LLM-Enhanced Analysis of SCMP Letters 2018-2023"
- **Conference Presentations:** Hong Kong Studies, Critical Discourse Analysis, Digital Humanities
- **Data Repository:** Processed corpus with LLM annotations for future research

### Educational Applications (Original GRF Goal)
- **Student Letter Writing Guide:** Evidence-based argumentative strategies from successful letters
- **Citizenship Communication Toolkit:** Templates and examples for public discourse participation  
- **Historical Discourse Archive:** Interactive timeline of citizenship debates 2018-2023

### Policy Applications
- **Government Insight:** Citizen concern patterns and communication preferences
- **NGO Resources:** Data-driven understanding of public opinion evolution
- **Media Analysis:** Letters page effectiveness as public discourse forum

## Resource Requirements

### Technical Infrastructure
- **OpenRouter API Credits:** ~$200-500 for full corpus analysis
- **Computing Resources:** Local processing for data preparation and visualization
- **Storage:** ~2GB for processed corpus and analysis outputs

### Timeline: 8-week sprint (expandable to full semester project)

### Success Metrics
- **Corpus Coverage:** >95% of letters successfully analyzed
- **Research Questions:** Comprehensive answers with quantitative and qualitative evidence
- **Academic Impact:** Paper acceptance at peer-reviewed conference
- **Educational Value:** Student-usable resources for citizenship communication

## Next Steps
1. **Immediate:** Begin corpus processing with existing tools
2. **Week 2:** Develop and test LLM analysis prompts  
3. **Week 4:** Launch full corpus analysis pipeline
4. **Week 6:** Generate preliminary findings and visualizations
5. **Week 8:** Complete draft research paper and educational resources

---

*This plan builds on Ben Rowlett and Simon Wang's original GRF application "Communicating Citizenship" while leveraging modern LLM capabilities to analyze the complete 6-year SCMP letters corpus covering Hong Kong's critical political transition period (2018-2023).*
