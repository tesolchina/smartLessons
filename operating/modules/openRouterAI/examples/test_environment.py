#!/usr/bin/env python3
"""
Test OpenRouter Environment Setup

This script tests the OpenRouter API configuration and environment setup.
It can be run from anywhere in the project to verify the API key is properly configured.

Usage:
    python test_environment.py

This script will:
1. Check if the OpenRouter environment can be imported
2. Verify API key configuration
3. Display configuration status
4. Provide troubleshooting guidance if issues are found
"""

import sys
import os
from pathlib import Path

# Add the modules directory to path to import from openRouterAI
current_file = Path(__file__).resolve()
modules_dir = current_file.parent.parent.parent  # Go up to modules level
sys.path.insert(0, str(modules_dir))

def test_openrouter_environment():
    """Test OpenRouter environment setup and configuration"""
    
    print("🧪 Testing OpenRouter Environment Setup")
    print("=" * 50)
    
    try:
        from openRouterAI.env import get_openrouter_config, get_openrouter_api_key
        print("✅ Successfully imported OpenRouter environment")
        
        # Test configuration
        config = get_openrouter_config()
        print(f"🔧 OpenRouter Config:")
        print(f"   Base URL: {config['base_url']}")
        print(f"   Model: {config['model']}")
        print(f"   Has API Key: {config['has_key']}")
        
        # Test API key
        api_key = get_openrouter_api_key()
        if api_key:
            print(f"🔑 API Key found: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'too_short'}")
            print("✅ Environment setup is complete and ready to use!")
        else:
            print("❌ No API Key found")
            print("💡 To fix this, you need to either:")
            print("   1. Set OPENROUTER_API_KEY environment variable")
            print("   2. Create a .env file in the repo root with:")
            print("      OPENROUTER_API_KEY=\"your-api-key-here\"")
            
            # Show expected .env location
            module_dir = Path(__file__).resolve().parent.parent
            repo_root = module_dir.parent
            env_path = repo_root / ".env"
            print(f"   3. Expected .env location: {env_path}")
            print(f"   4. Copy format from: {repo_root / '.env.example'}")
            
        return api_key is not None
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the correct location")
        print("💡 Expected structure: modules/openRouterAI/examples/")
        return False

if __name__ == "__main__":
    success = test_openrouter_environment()
    sys.exit(0 if success else 1)
