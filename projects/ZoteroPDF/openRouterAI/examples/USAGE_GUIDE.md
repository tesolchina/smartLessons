# OpenRouter AI Module - Usage Guide

## Overview

The OpenRouter AI module provides a simple interface to interact with various Large Language Models (LLMs) through the OpenRouter API. This module handles authentication, API calls, and provides utilities for common LLM tasks like text analysis.

## Quick Start

### 1. Environment Setup

First, ensure you have an OpenRouter API key. You can obtain one from [OpenRouter.ai](https://openrouter.ai/).

**Option A: Using .env file (Recommended)**
```bash
# Create a .env file in the repository root
# File: DailyAssistant/.env
OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
OPENROUTER_APP_NAME="YourAppName"
OPENROUTER_APP_URL="https://your-app-url.com"
```

**Option B: Environment Variables**
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
```

### 2. Install Dependencies

```bash
pip install python-dotenv requests
```

### 3. Test Your Setup

```python
# Run from anywhere in the project
python modules/openRouterAI/examples/test_environment.py
```

Expected output:
```
🧪 Testing OpenRouter Environment Setup
==================================================
✅ Successfully imported OpenRouter environment
🔧 OpenRouter Config:
   Base URL: https://openrouter.ai/api/v1
   Model: anthropic/claude-3.5-sonnet
   Has API Key: True
🔑 API Key found: sk-or-v1-4...7d8c
✅ Environment setup is complete and ready to use!
```

## Basic Usage

### Simple API Call

```python
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "modules"))

from openRouterAI.client import post_chat_completions

# Basic chat completion
payload = {
    "model": "anthropic/claude-3.5-sonnet",
    "messages": [
        {"role": "user", "content": "Explain quantum physics in simple terms"}
    ],
    "max_tokens": 500,
    "temperature": 0.7
}

response = post_chat_completions(payload)
print(response["choices"][0]["message"]["content"])
```

### Environment Configuration

```python
from openRouterAI.env import get_openrouter_config, get_openrouter_api_key

# Check configuration
config = get_openrouter_config()
print(f"Using model: {config['model']}")
print(f"API available: {config['has_key']}")

# Get API key (for debugging)
api_key = get_openrouter_api_key()
if api_key:
    print(f"API key configured: {api_key[:10]}...")
```

## Advanced Usage Examples

### 1. Text Analysis with LLM Text Analyzer

```python
from openRouterAI.examples.llm_text_analyzer import LLMTextAnalyzer, example_content_analysis

# Initialize analyzer
analyzer = LLMTextAnalyzer(
    model="anthropic/claude-3.5-sonnet",
    chunk_size=2000  # words per chunk
)

# Get example prompts
analysis_prompt, synthesis_prompt = example_content_analysis()

# Analyze a large text file
results = analyzer.analyze_file(
    file_path="path/to/large_document.txt",
    analysis_prompt=analysis_prompt,
    synthesis_prompt=synthesis_prompt,
    output_dir="analysis_results"
)

# Check results
if results["success"]:
    print(f"Analysis complete! Results in: {results['output_dir']}")
    print(f"Processed {results['statistics']['total_words']:,} words")
```

### 2. Speaker Separation Analysis

```python
from openRouterAI.examples.speaker_separation_example import analyze_transcript_for_speakers

# Define expected speakers
expected_speakers = [
    "Speaker 1 - Main presenter (technical content)",
    "Speaker 2 - Guest expert (methodology discussion)"
]

# Analyze transcript for speaker separation
results = analyze_transcript_for_speakers(
    transcript_path="transcript.txt",
    output_dir="speaker_analysis",
    expected_speakers=expected_speakers
)

# Results include detailed speaker attribution recommendations
```

### 3. Custom Analysis Workflow

```python
from openRouterAI.examples.llm_text_analyzer import LLMTextAnalyzer

def custom_analysis_workflow():
    analyzer = LLMTextAnalyzer()
    
    # Custom analysis prompt
    analysis_prompt = """
    Analyze this text for:
    1. Main arguments presented
    2. Evidence quality
    3. Logical structure
    4. Potential biases
    
    Text chunk {chunk_num}:
    {chunk_text}
    
    Provide structured analysis.
    """
    
    # Custom synthesis prompt  
    synthesis_prompt = """
    Based on {total_chunks} analyzed chunks, provide:
    1. Overall argument summary
    2. Evidence strength assessment
    3. Structural analysis
    4. Bias evaluation
    
    Analyses: {analyses}
    """
    
    return analyzer.analyze_file(
        "document.txt", 
        analysis_prompt, 
        synthesis_prompt
    )
```

## Available Models

Common models available through OpenRouter:

- `anthropic/claude-3.5-sonnet` - Excellent for analysis and reasoning
- `openai/gpt-4o` - Strong general-purpose model
- `openai/gpt-4o-mini` - Faster, more economical option
- `meta-llama/llama-3.1-405b-instruct` - Open source alternative
- `google/gemini-pro` - Google's competitive model

Check [OpenRouter Models](https://openrouter.ai/models) for the latest options.

## Best Practices

### 1. Prompt Engineering

```python
# Good: Specific, structured prompts
prompt = """
Analyze this text for sentiment and themes.

Text: {text}

Please provide:
1. Overall sentiment: [Positive/Negative/Neutral]
2. Confidence: [High/Medium/Low] 
3. Main themes: [List top 3]
4. Key phrases: [Quote relevant phrases]

Format as structured output.
"""

# Avoid: Vague or overly broad prompts
prompt = "What do you think about this text?"
```

### 2. Error Handling

```python
from openRouterAI.client import post_chat_completions

def safe_llm_call(payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = post_chat_completions(payload)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Token Management

```python
# Monitor token usage
payload = {
    "model": "anthropic/claude-3.5-sonnet", 
    "messages": [{"role": "user", "content": text}],
    "max_tokens": 1500,  # Adjust based on expected response length
    "temperature": 0.1   # Lower for consistent analysis
}

response = post_chat_completions(payload)

# Check usage if available
if "usage" in response:
    print(f"Tokens used: {response['usage']['total_tokens']}")
```

### 4. Status Reporting

```python
def analyze_with_progress(texts, prompt_template):
    results = []
    
    for i, text in enumerate(texts, 1):
        print(f"🔍 Processing {i}/{len(texts)}...")
        
        try:
            result = analyze_text(text, prompt_template)
            print(f"✅ Completed {i}/{len(texts)}")
            results.append(result)
        except Exception as e:
            print(f"❌ Failed {i}/{len(texts)}: {e}")
            results.append(None)
    
    success_count = sum(1 for r in results if r is not None)
    print(f"📊 Analysis complete: {success_count}/{len(texts)} successful")
    
    return results
```

## Troubleshooting

### Common Issues

**1. "No API Key Found"**
```bash
# Check if .env file exists and is in the right location
ls -la DailyAssistant/.env

# Verify content format
cat DailyAssistant/.env | grep OPENROUTER
```

**2. "Import Error: No module named 'openRouterAI'"**
```python
# Ensure correct path setup
import sys
from pathlib import Path

# Add modules directory
modules_path = Path(__file__).resolve().parent.parent / "modules"
sys.path.insert(0, str(modules_path))

# Now import should work
from openRouterAI.client import post_chat_completions
```

**3. "HTTP 401 Unauthorized"**
```python
# Test API key validity
from openRouterAI.env import get_openrouter_api_key
key = get_openrouter_api_key()
print(f"Key starts with: {key[:10] if key else 'No key found'}")

# Regenerate key at openrouter.ai if needed
```

**4. "HTTP 429 Rate Limited"**
```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                raise
```

## File Structure Reference

```
modules/openRouterAI/
├── __init__.py              # Module initialization
├── client.py                # Core API client
├── env.py                   # Environment configuration
├── requirements.txt         # Dependencies
├── README.md               # Basic module info
├── examples/               # Example scripts and utilities
│   ├── test_environment.py        # Environment testing
│   ├── llm_text_analyzer.py       # Generic text analysis
│   ├── speaker_separation_example.py  # Speaker analysis example
│   └── USAGE_GUIDE.md             # This file
└── key.txt                 # API key storage (not committed to git)
```

## Security Notes

- ✅ `.env` files are automatically ignored by git (see `.gitignore`)
- ✅ `key.txt` is in `.gitignore` 
- ❌ Never commit API keys to version control
- ✅ Use environment variables in production
- ✅ Rotate API keys periodically

## Support and Contribution

- **Issues**: Report in the main repository issue tracker
- **Examples**: Add new examples to the `examples/` directory
- **Documentation**: Update this guide for new features
- **Testing**: Use `test_environment.py` to validate setup

---

*Last updated: September 9, 2025*
