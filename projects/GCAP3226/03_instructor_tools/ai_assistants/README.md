# Regression Analysis Assessment Chatbot

## Overview
This AI-powered chatbot assesses the quality and reliability of regression analysis documents for the GCAP3226 course. It uses OpenRouter API with Claude 3.5 Sonnet to provide detailed feedback on methodology, policy relevance, technical soundness, and implementation feasibility.

## Setup

1. **Install Dependencies**
```bash
pip install requests
```

2. **Configuration Files**
- Ensure `mathGuru/mathGuru.json` contains assessment prompts
- Ensure `.env` file contains your OpenRouter API key in format: `OpenRouter Key=your_key_here`

## Usage

### Command Line Usage

```bash
# Full assessment of a regression analysis document
python regression_assessor.py TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md

# Quick assessment (methodology + policy relevance only)
python regression_assessor.py TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md --type quick

# Technical assessment (focus on statistical methodology)
python regression_assessor.py TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md --type technical

# Policy assessment (focus on policy applicability)
python regression_assessor.py TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md --type policy

# Save results to file
python regression_assessor.py TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md --output assessment_results.md
```

### Assessment Types

- **full**: Complete assessment using all prompts (default)
- **quick**: Basic methodology and policy relevance assessment
- **technical**: Focus on statistical methodology and technical soundness
- **policy**: Focus on policy applicability and feasibility

### Assessment Categories

1. **Methodology Assessment**: Evaluates statistical approach, model selection, and analytical rigor
2. **Policy Relevance**: Assesses connection to policy goals and real-world applicability
3. **Technical Soundness**: Reviews assumptions, limitations, and statistical validity
4. **Data Feasibility**: Evaluates data requirements and collection practicality
5. **Improvement Suggestions**: Provides specific recommendations for enhancement
6. **Overall Assessment**: Comprehensive evaluation with strengths and weaknesses

## Files Assessment Ready

All regression analysis documents are ready for assessment:

- `TopicSelectionPM/Topic1_BusFrequency/Regression_Applications.md`
- `TopicSelectionPM/Topic2_BusStopMerge/Regression_Applications.md`
- `TopicSelectionPM/Topic3_BusRoutesCoordination/Regression_Applications.md`
- `TopicSelectionPM/Topic4_SolidWasteCharging/Regression_Applications.md`
- `TopicSelectionPM/Topic5_GreenCommunity/Regression_Applications.md`
- `TopicSelectionPM/Topic6_FluShotParticipation/Regression_Applications.md`
- `TopicSelectionPM/Topic7_TyphoonSignal/Regression_Applications.md`

## Example Output

The chatbot provides detailed assessments like:

```
🔍 Assessing document: Regression_Applications.md
📊 Assessment type: full
============================================================

📋 Running assessment: Methodology Assessment

──────────────────────────────────────────────────────────
The regression methodology outlined in this document demonstrates 
a solid understanding of statistical modeling principles...
[Detailed AI assessment continues]
──────────────────────────────────────────────────────────

📋 Running assessment: Policy Relevance
...
```

## Error Handling

The chatbot handles common issues:
- Missing configuration files
- API key authentication problems
- Network connectivity issues
- Invalid document formats
- API rate limiting

## Support

For issues or questions about the assessment tool, refer to the source code comments or check the configuration files.