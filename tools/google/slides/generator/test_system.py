#!/usr/bin/env python3
"""
Quick Test Script for GoogleSlidesGenerator
==========================================

Tests the system with Week 2 lecture slides for immediate validation.
"""

import os
import sys
from pathlib import Path
from markdown_to_slides import MarkdownToSlidesConverter


def test_week2_conversion():
    """Test conversion with Week 2 lecture slides."""
    print("🧪 Testing GoogleSlidesGenerator with Week 2 Lecture Slides")
    print("=" * 60)
    
    # Check for Week 2 lecture file
    week2_file = Path("../Week2_Lecture_Slides.md")
    
    if not week2_file.exists():
        print("❌ Week 2 lecture file not found!")
        print(f"Expected: {week2_file.absolute()}")
        return False
        
    print(f"✅ Found Week 2 file: {week2_file}")
    
    try:
        # Initialize converter
        print("\n📤 Initializing converter...")
        converter = MarkdownToSlidesConverter("config")
        
        # Test conversion
        print("🎨 Converting with educational template...")
        result = converter.convert(
            input_file=str(week2_file),
            template="educational",
            drive_folder="GCAP3226/Weekly Materials/Week 2",
            output_name="Week 2 - AI-Assisted Programming Lecture"
        )
        
        if result['success']:
            print("\n🎉 Conversion successful!")
            print(f"📝 Presentation: {result['output_name']}")
            print(f"🔗 Link: {result['file_link']}")
            print(f"📁 Drive folder: GCAP3226/Weekly Materials/Week 2")
            return True
        else:
            print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_configuration():
    """Test configuration files."""
    print("\n🔧 Testing configuration files...")
    
    config_files = [
        "config/templates.json",
        "config/drive_config.json"
    ]
    
    all_good = True
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file}")
        else:
            print(f"❌ Missing: {config_file}")
            all_good = False
            
    return all_good


def test_authentication():
    """Test Google API authentication."""
    print("\n🔐 Testing authentication...")
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
        # Check for credentials file
        if Path("config/credentials.json").exists():
            print("✅ Found credentials.json")
        else:
            print("⚠️ No credentials.json found")
            print("   Run: python setup_auth.py")
            
        if Path("config/token.json").exists():
            print("✅ Found token.json")
        else:
            print("⚠️ No token.json found")
            print("   Will be created on first run")
            
        return True
        
    except ImportError as e:
        print(f"❌ Missing Google API libraries: {e}")
        print("   Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        return False


def run_full_test():
    """Run complete test suite."""
    print("🚀 GoogleSlidesGenerator - Full Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration Files", test_configuration),
        ("Authentication Setup", test_authentication),
        ("Week 2 Conversion", test_week2_conversion)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️ Some tests failed. Check setup requirements.")
        
    return passed == total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--week2-only":
        # Quick test with Week 2 only
        success = test_week2_conversion()
        exit(0 if success else 1)
    else:
        # Full test suite
        success = run_full_test()
        exit(0 if success else 1)
