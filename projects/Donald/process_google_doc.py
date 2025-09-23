#!/usr/bin/env python3
"""
Script to process Google Doc file and create a local copy.

Google .gdoc files are pointers to online documents and cannot be directly read.
This script provides multiple approaches to handle the Google Doc.
"""

import os
import shutil
import subprocess
import sys
import json
from pathlib import Path
import urllib.parse

def check_file_exists(file_path):
    """Check if the Google Doc file exists"""
    if os.path.exists(file_path):
        print(f"✓ Found file: {file_path}")
        return True
    else:
        print(f"✗ File not found: {file_path}")
        return False

def get_file_info(file_path):
    """Get information about the .gdoc file"""
    try:
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")
        
        # Try to read the content (it's usually a small text file with URL)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"File content preview:\n{content[:500]}...")
            return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_google_doc_url(content):
    """Extract the actual Google Doc URL from .gdoc file content"""
    try:
        # .gdoc files contain JSON with doc_id
        data = json.loads(content)
        doc_id = data.get('doc_id')
        if doc_id:
            url = f"https://docs.google.com/document/d/{doc_id}/edit"
            print(f"✓ Extracted doc_id: {doc_id}")
            return url
        
        # Fallback: check for direct URL in content
        lines = content.split('\n')
        for line in lines:
            if 'docs.google.com' in line:
                return line.strip()
        return None
    except json.JSONDecodeError:
        # Try the old method for non-JSON .gdoc files
        lines = content.split('\n')
        for line in lines:
            if 'docs.google.com' in line:
                return line.strip()
        return None
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None

def create_download_instructions(google_doc_url, local_folder):
    """Create instructions for manually downloading the document"""
    instructions_file = os.path.join(local_folder, "DOWNLOAD_INSTRUCTIONS.md")
    
    instructions = f"""# Google Doc Download Instructions

## Original File Location:
{google_doc_url}

## Manual Download Steps:

1. **Open the Google Doc in browser:**
   - Click this link: {google_doc_url}
   - Make sure you're logged into the correct Google account

2. **Download as different formats:**
   
   ### Option 1: Download as Microsoft Word (.docx)
   - File → Download → Microsoft Word (.docx)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.docx`
   
   ### Option 2: Download as PDF
   - File → Download → PDF Document (.pdf)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.pdf`
   
   ### Option 3: Download as Plain Text
   - File → Download → Plain Text (.txt)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.txt`

3. **Copy downloaded file to this folder:**
   ```
   {local_folder}
   ```

## Automated Conversion:
After downloading, run this script again with the downloaded file to convert to markdown:
```bash
python process_google_doc.py --convert downloaded_file.docx
```

## Alternative: Use Google Drive Desktop
1. Install Google Drive Desktop app
2. Sync the folder containing the document
3. Access the file through the local Google Drive folder
"""
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✓ Created download instructions: {instructions_file}")
    return instructions_file

def try_open_in_browser(url):
    """Try to open the Google Doc URL in default browser"""
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", url])
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", url])
        elif sys.platform == "win32":
            subprocess.run(["start", url], shell=True)
        print(f"✓ Opened Google Doc in browser: {url}")
        return True
    except Exception as e:
        print(f"✗ Could not open browser: {e}")
        return False

def convert_docx_to_markdown(docx_path, output_folder):
    """Convert downloaded .docx file to markdown using pandoc"""
    try:
        output_path = os.path.join(output_folder, "Donald_Wong_IGCSE_Geo_Coursework.md")
        
        # Check if pandoc is available
        result = subprocess.run(["which", "pandoc"], capture_output=True, text=True)
        if result.returncode != 0:
            print("✗ Pandoc not found. Install with: brew install pandoc")
            return None
        
        # Convert using pandoc
        subprocess.run([
            "pandoc",
            docx_path,
            "-o", output_path,
            "--extract-media=./media"
        ], check=True)
        
        print(f"✓ Converted to markdown: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"✗ Conversion failed: {e}")
        return None
    except FileNotFoundError:
        print("✗ Pandoc not found. Install with: brew install pandoc")
        return None

def main():
    # File paths
    google_doc_path = "/Users/simonwang/Library/CloudStorage/GoogleDrive-simonwanghkteacher@gmail.com/My Drive/DonaldStudies2025/Copy of Donald Wong IGCSE Geo Coursework.gdoc"
    local_folder = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo"
    
    print("🔄 Processing Google Doc file...")
    print(f"Source: {google_doc_path}")
    print(f"Target folder: {local_folder}")
    print("-" * 60)
    
    # Ensure target folder exists
    os.makedirs(local_folder, exist_ok=True)
    
    # Check if file exists
    if not check_file_exists(google_doc_path):
        print("\n❌ Cannot proceed: Google Doc file not found")
        print("\nPossible solutions:")
        print("1. Make sure Google Drive is synced")
        print("2. Check the file path is correct")
        print("3. Ensure you have access to the document")
        return
    
    # Read the .gdoc file content
    content = get_file_info(google_doc_path)
    if not content:
        return
    
    # Try to extract Google Doc URL
    google_doc_url = extract_google_doc_url(content)
    if google_doc_url:
        print(f"\n📄 Found Google Doc URL: {google_doc_url}")
        
        # Create download instructions
        instructions_file = create_download_instructions(google_doc_url, local_folder)
        
        # Try to open in browser
        print("\n🌐 Attempting to open Google Doc in browser...")
        try_open_in_browser(google_doc_url)
        
        print(f"\n✅ Process complete!")
        print(f"📋 Follow instructions in: {instructions_file}")
        print("🔄 After downloading, run this script again to convert to markdown")
        
    else:
        print("❌ Could not extract Google Doc URL from file")
        
        # Copy the .gdoc file anyway for examination
        local_gdoc_path = os.path.join(local_folder, "Donald_Wong_IGCSE_Geo_Coursework.gdoc")
        shutil.copy2(google_doc_path, local_gdoc_path)
        print(f"📁 Copied .gdoc file to: {local_gdoc_path}")

if __name__ == "__main__":
    # Check for command line arguments for conversion mode
    if len(sys.argv) > 1 and sys.argv[1] == "--convert":
        if len(sys.argv) > 2:
            docx_file = sys.argv[2]
            local_folder = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo"
            convert_docx_to_markdown(docx_file, local_folder)
        else:
            print("Usage: python process_google_doc.py --convert <docx_file>")
    else:
        main()