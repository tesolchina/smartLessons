"""
Quick Test Script for Google API Setup

This script provides a simple way to test your Google API configuration
and verify that everything is working correctly.

Usage:
    python test_setup.py
"""

import os
import json
from pathlib import Path

def test_credentials_file():
    """Test if credentials file exists"""
    print("🔍 Testing credentials file...")
    
    config_file = "config.json"
    if not os.path.exists(config_file):
        print("❌ config.json not found")
        return False
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    creds_file = config.get('SERVICE_ACCOUNT_FILE')
    if not creds_file:
        print("❌ SERVICE_ACCOUNT_FILE not specified in config")
        return False
    
    if not os.path.exists(creds_file):
        print(f"❌ Credentials file not found: {creds_file}")
        print("   Please make sure you've downloaded the service account JSON file")
        return False
    
    print(f"✅ Credentials file found: {creds_file}")
    return True

def test_config_values():
    """Test if required config values are set"""
    print("🔍 Testing configuration values...")
    
    with open("config.json", 'r') as f:
        config = json.load(f)
    
    spreadsheet_id = config.get('SPREADSHEET_ID')
    if spreadsheet_id == 'your_spreadsheet_id_here':
        print("❌ SPREADSHEET_ID not updated in config.json")
        print("   Please replace with your actual Google Sheets ID")
        return False
    
    print(f"✅ Spreadsheet ID configured: {spreadsheet_id[:20]}...")
    return True

def test_imports():
    """Test if required packages are installed"""
    print("🔍 Testing package imports...")
    
    required_packages = [
        'google.oauth2.service_account',
        'googleapiclient.discovery',
        'pandas'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            print(f"   Run: pip install -r requirements.txt")
            return False
    
    return True

def test_api_connection():
    """Test actual API connection"""
    print("🔍 Testing Google API connection...")
    
    try:
        from google_api_helper import test_api_connection
        
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        if test_api_connection(config):
            print("✅ Google API connection successful!")
            return True
        else:
            print("❌ Google API connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API connection: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 GCAP3226 Google API Setup Test")
    print("=" * 40)
    
    tests = [
        ("Credentials File", test_credentials_file),
        ("Configuration Values", test_config_values),
        ("Package Imports", test_imports),
        ("API Connection", test_api_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your Google API setup is ready.")
        print("\nNext steps:")
        print("1. Run: python team_setup.py --test-only")
        print("2. If successful, run: python team_setup.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above before proceeding.")

if __name__ == "__main__":
    main()