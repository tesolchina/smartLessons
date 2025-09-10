# OpenRouterAI Module

A comprehensive module for interacting with Large Language Models through the OpenRouter API, including utilities for text analysis, speaker separation, and structured LLM workflows.

## Quick Start

### 1. Setup Environment
Copy `.env.example` at repo root to `.env` and add your API key:
```bash
OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"  # Optional
```

### 2. Test Setup
```bash
python modules/openRouterAI/examples/test_environment.py
```

### 3. Basic Usage
```python
from openRouterAI.client import post_chat_completions

response = post_chat_completions({
    "model": "anthropic/claude-3.5-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
})
print(response["choices"][0]["message"]["content"])
```

## Advanced Features

### 📊 Text Analysis Utilities
- **LLM Text Analyzer**: Chunk large texts, analyze with status reporting
- **Speaker Separation**: Identify speakers in transcripts based on content
- **Custom Analysis Workflows**: Template system for structured analysis

### 🔧 Examples & Templates
All examples include comprehensive status reporting and error handling:

- `examples/test_environment.py` - Verify setup and configuration
- `examples/llm_text_analyzer.py` - Generic text analysis framework
- `examples/speaker_separation_example.py` - Speaker identification system
- `examples/USAGE_GUIDE.md` - Complete usage documentation

### 📈 Status Reporting
All utilities provide detailed progress tracking:
```
🤖 LLM Text Analysis
============================================================
📖 Reading transcript...
📂 Attempting to read transcript from: transcript.txt
✅ Successfully read transcript: 35,788 characters
📊 Split transcript into 4 chunks of ~2000 words each
🔍 Analyzing chunk 1/4... (2000 words)
✅ Chunk 1 analysis complete
📡 Sending synthesis request to OpenRouter API...
✅ Analysis complete!
```

## Core Components

### Environment Management (`env.py`)
- Automatic .env file loading
- Environment variable fallbacks
- Configuration validation

### API Client (`client.py`)
- Simple urllib-based requests
- Error handling and retries
- No external dependencies beyond standard library

### Analysis Framework (`examples/`)
- Chunking for large texts
- Progress tracking and status reporting
- Result compilation and export
- Customizable prompt templates

## Documentation

📚 **[Complete Usage Guide](examples/USAGE_GUIDE.md)** - Comprehensive documentation with examples, troubleshooting, and best practices.

## Security

- ✅ `.env` files automatically ignored by git
- ✅ API keys never committed to version control  
- ✅ Secure environment variable handling
- ✅ Production-ready configuration management
