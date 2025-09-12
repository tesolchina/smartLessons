#!/usr/bin/env python3
"""
Direct OpenRouter API integration for chatbot simulation
"""

import json
import urllib.request
import urllib.error
import os
import time
from typing import Any, Dict, Optional

def get_openrouter_api_key() -> Optional[str]:
    """Get OpenRouter API key from environment or .env file"""
    # Check environment variable first
    api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key:
        # Try loading from .env file
        env_paths = [
            '.env',
            '../.env', 
            '../../.env',
            '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/.env'
        ]
        
        for env_path in env_paths:
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('OPENROUTER_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"\'')
                            break
                if api_key:
                    break
            except FileNotFoundError:
                continue
    
    return api_key

def post_chat_completions(payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST to OpenRouter chat completions API"""
    
    api_key = get_openrouter_api_key()
    if not api_key:
        raise ValueError("OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable or create .env file.")
    
    # Prepare request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-app",
        "X-Title": "Educational Chatbot Simulation"
    }
    
    # Convert payload to JSON
    data = json.dumps(payload).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            response_data = response.read()
            return json.loads(response_data.decode('utf-8'))
    
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP {e.code}: {e.reason}"
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            error_msg += f" - {error_data.get('error', {}).get('message', 'Unknown error')}"
        except:
            pass
        raise Exception(error_msg)
    
    except Exception as e:
        raise Exception(f"API request failed: {str(e)}")

def test_openrouter_connection() -> bool:
    """Test if OpenRouter API is accessible"""
    try:
        test_payload = {
            "model": "openai/gpt-4o-mini",  # Use a more accessible model for testing
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        response = post_chat_completions(test_payload)
        return "choices" in response
        
    except Exception as e:
        print(f"OpenRouter test failed: {e}")
        return False
