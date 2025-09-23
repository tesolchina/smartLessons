"""
Team Setup Automation Script for GCAP3226

This script automates the creation of team folders and template files
for the GCAP3226 course using Google APIs.

Usage:
    python team_setup.py --config config.json [--test-only]
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from google_api_helper import GoogleAPIHelper, test_api_connection


def load_config(config_file: str) -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ['SERVICE_ACCOUNT_FILE', 'SPREADSHEET_ID', 'SCOPES']
        missing_fields = [field for field in required_fields if field not in config]
        
        if missing_fields:
            raise ValueError(f"Missing required config fields: {missing_fields}")
        
        return config
        
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        sys.exit(1)


def create_default_templates() -> dict:
    """Create default template configuration"""
    return {
        'project_plan': {
            'name': 'Team Project Plan',
            'type': 'document'
        },
        'data_analysis': {
            'name': 'Data Analysis Worksheet',
            'type': 'spreadsheet'
        },
        'presentation': {
            'name': 'Final Presentation',
            'type': 'presentation'
        },
        'meeting_notes': {
            'name': 'Team Meeting Notes',
            'type': 'document'
        }
    }


def save_results(results: list, output_file: str) -> None:
    """Save setup results to JSON file"""
    try:
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'total_teams': len(results),
            'successful_setups': len([r for r in results if r['status'] == 'success']),
            'failed_setups': len([r for r in results if r['status'] == 'failed']),
            'results': results
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"📄 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")


def print_summary(results: list) -> None:
    """Print setup summary"""
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    
    print("\n" + "="*60)
    print("📊 TEAM SETUP SUMMARY")
    print("="*60)
    print(f"Total teams: {len(results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print("\n✅ Successfully created teams:")
        for result in successful:
            print(f"   • {result['team_name']}: {result['folder_link']}")
    
    if failed:
        print("\n❌ Failed teams:")
        for result in failed:
            print(f"   • {result['team_name']}: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Automate team folder setup for GCAP3226")
    parser.add_argument('--config', '-c', default='config.json', 
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--test-only', '-t', action='store_true',
                       help='Test API connection only, do not create folders')
    parser.add_argument('--output', '-o', default='team_setup_results.json',
                       help='Output file for results (default: team_setup_results.json)')
    
    args = parser.parse_args()
    
    print("🚀 GCAP3226 Team Setup Automation")
    print("="*50)
    
    # Load configuration
    print(f"📋 Loading configuration from: {args.config}")
    config = load_config(args.config)
    
    # Test API connection
    print("🔍 Testing Google API connection...")
    if not test_api_connection(config):
        print("❌ API connection failed. Please check your credentials and configuration.")
        sys.exit(1)
    
    if args.test_only:
        print("✅ Test completed successfully. Use without --test-only to create team folders.")
        return
    
    try:
        # Initialize API helper
        api_helper = GoogleAPIHelper(config)
        
        # Read team assignments
        print("📊 Reading team assignments from spreadsheet...")
        team_data = api_helper.read_team_assignments()
        
        if team_data.empty:
            print("❌ No team data found in spreadsheet")
            return
        
        print(f"📋 Found {len(team_data)} student assignments in {team_data['Team'].nunique()} teams")
        
        # Get template configuration
        templates = config.get('TEMPLATES', create_default_templates())
        print(f"📄 Using {len(templates)} template files per team")
        
        # Setup all teams
        print("\n🚀 Starting team setup process...")
        results = api_helper.setup_all_teams(team_data, templates)
        
        # Update spreadsheet with folder links
        print("\n📊 Updating spreadsheet with folder links...")
        api_helper.update_team_folders_in_sheet(results)
        
        # Save results
        save_results(results, args.output)
        
        # Print summary
        print_summary(results)
        
        print("\n🎉 Team setup automation completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()