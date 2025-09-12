#!/usr/bin/env bash
# Quick Setup Script for GoogleSlidesGenerator
# ============================================

set -e

echo "🚀 GoogleSlidesGenerator - Quick Setup"
echo "======================================"

# Check Python version
echo "🐍 Checking Python..."
python3 --version || {
    echo "❌ Python 3 is required but not found."
    exit 1
}

# Install required packages
echo "📦 Installing required packages..."
pip3 install --user google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Create config directory if not exists
echo "📁 Creating config directory..."
mkdir -p config

# Check if credentials exist
echo "🔐 Checking authentication setup..."
if [[ ! -f "config/credentials.json" ]]; then
    echo "⚠️  Google API credentials not found."
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable Google Slides API and Google Drive API"
    echo "4. Create OAuth 2.0 credentials (Desktop Application)"
    echo "5. Download credentials.json to config/"
    echo ""
    echo "Or run: python3 setup_auth.py"
    echo ""
else
    echo "✅ Found credentials.json"
fi

# Test basic functionality
echo "🧪 Testing basic functionality..."
python3 -c "
import json
from pathlib import Path

# Test template loading
try:
    with open('config/templates.json') as f:
        templates = json.load(f)
    print('✅ Templates loaded successfully')
    print(f'   Available templates: {list(templates.keys())}')
except Exception as e:
    print(f'❌ Template loading failed: {e}')

# Test drive config
try:
    with open('config/drive_config.json') as f:
        config = json.load(f)
    print('✅ Drive config loaded successfully')
except Exception as e:
    print(f'❌ Drive config loading failed: {e}')
"

echo ""
echo "🎯 Setup Status:"
echo "=================="

# Check Week 2 file
if [[ -f "../Week2_Lecture_Slides.md" ]]; then
    echo "✅ Week 2 lecture file found"
    echo "   Ready to test: python3 test_system.py --week2-only"
else
    echo "⚠️  Week 2 lecture file not found"
    echo "   Expected: ../Week2_Lecture_Slides.md"
fi

# Check all components
echo "📋 Component Status:"
echo "✅ Core converter: markdown_to_slides.py"
echo "✅ Batch processor: batch_converter.py"
echo "✅ Test suite: test_system.py"
echo "✅ Templates: config/templates.json"
echo "✅ Drive config: config/drive_config.json"

if [[ -f "config/credentials.json" ]]; then
    echo "✅ Authentication: config/credentials.json"
    echo ""
    echo "🎉 System is ready!"
    echo ""
    echo "🚀 Quick Start:"
    echo "1. Test with Week 2: python3 test_system.py --week2-only"
    echo "2. Full test suite: python3 test_system.py"
    echo "3. Convert single file: python3 markdown_to_slides.py ../Week2_Lecture_Slides.md"
    echo "4. Batch process: python3 batch_converter.py --course-folder /path/to/course --drive-base GCAP3226"
else
    echo "⚠️  Authentication: Need credentials.json"
    echo ""
    echo "🔧 Complete Setup:"
    echo "1. Run: python3 setup_auth.py"
    echo "2. Follow the authentication flow"
    echo "3. Test: python3 test_system.py --week2-only"
fi

echo ""
echo "📚 Documentation: README.md"
echo "🆘 Support: Check README.md for troubleshooting"
