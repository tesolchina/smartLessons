#!/usr/bin/env python3
"""
Test OpenRouter environment setup
"""

import sys
import os
from pathlib import Path

# Add the modules path
modules_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "modules"
sys.path.insert(0, str(modules_path))

try:
    from openRouterAI.env import get_openrouter_config, get_openrouter_api_key
    print("✅ Successfully imported OpenRouter environment")
    
    config = get_openrouter_config()
    print(f"🔧 OpenRouter Config: {config}")
    
    api_key = get_openrouter_api_key()
    if api_key:
        print(f"🔑 API Key found: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'too_short'}")
    else:
        print("❌ No API Key found")
        print("💡 You need to either:")
        print("   1. Set OPENROUTER_API_KEY environment variable")
        print("   2. Create a .env file in the repo root with OPENROUTER_API_KEY")
        
        # Show example
        repo_root = modules_path.parent
        env_path = repo_root / ".env"
        print(f"   3. Expected .env location: {env_path}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
