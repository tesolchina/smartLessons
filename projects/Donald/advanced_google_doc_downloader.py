#!/usr/bin/env python3
"""
Advanced Google Doc processor with multiple download options.
This script provides several methods to get content from Google Docs.
"""

import os
import requests
import subprocess
import sys
from pathlib import Path

def download_via_export_url(doc_id, format_type='docx', output_path=None):
    """
    Try to download Google Doc using export URL.
    This may require authentication depending on document permissions.
    """
    print(f"🔄 Attempting to download as {format_type}...")
    
    # Google Docs export URLs
    export_urls = {
        'docx': f'https://docs.google.com/document/d/{doc_id}/export?format=docx',
        'pdf': f'https://docs.google.com/document/d/{doc_id}/export?format=pdf',
        'txt': f'https://docs.google.com/document/d/{doc_id}/export?format=txt',
        'odt': f'https://docs.google.com/document/d/{doc_id}/export?format=odt',
        'html': f'https://docs.google.com/document/d/{doc_id}/export?format=html'
    }
    
    if format_type not in export_urls:
        print(f"❌ Unsupported format: {format_type}")
        return None
    
    url = export_urls[format_type]
    
    if not output_path:
        output_path = f"Donald_Wong_IGCSE_Geo_Coursework.{format_type}"
    
    try:
        # Try to download
        response = requests.get(url, allow_redirects=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Successfully downloaded: {output_path}")
            return output_path
        else:
            print(f"❌ Download failed with status code: {response.status_code}")
            print("This likely means the document requires authentication.")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Download error: {e}")
        return None

def try_curl_download(doc_id, format_type='docx', output_path=None):
    """
    Try downloading using curl command (may work if browser is logged in)
    """
    print(f"🔄 Trying curl download as {format_type}...")
    
    export_urls = {
        'docx': f'https://docs.google.com/document/d/{doc_id}/export?format=docx',
        'pdf': f'https://docs.google.com/document/d/{doc_id}/export?format=pdf',
        'txt': f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
    }
    
    if format_type not in export_urls:
        print(f"❌ Unsupported format: {format_type}")
        return None
    
    url = export_urls[format_type]
    
    if not output_path:
        output_path = f"Donald_Wong_IGCSE_Geo_Coursework.{format_type}"
    
    try:
        # Use curl with cookie jar (might use browser cookies)
        cmd = [
            'curl',
            '-L',  # Follow redirects
            '-o', output_path,
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 1000:  # Reasonable file size
                print(f"✅ Successfully downloaded with curl: {output_path} ({file_size} bytes)")
                return output_path
            else:
                print(f"❌ Downloaded file too small ({file_size} bytes), likely an error page")
                os.remove(output_path)
                return None
        else:
            print(f"❌ Curl download failed: {result.stderr}")
            return None
            
    except subprocess.SubprocessError as e:
        print(f"❌ Curl error: {e}")
        return None

def convert_to_markdown(input_file, output_folder):
    """Convert downloaded file to markdown using pandoc"""
    try:
        # Check if pandoc is available
        result = subprocess.run(["which", "pandoc"], capture_output=True, text=True)
        if result.returncode != 0:
            print("📦 Installing pandoc...")
            subprocess.run(["brew", "install", "pandoc"], check=True)
        
        output_path = os.path.join(output_folder, "Donald_Wong_IGCSE_Geo_Coursework_DOWNLOADED.md")
        
        # Convert using pandoc
        cmd = [
            "pandoc",
            input_file,
            "-o", output_path,
            "--extract-media=./media",
            "--wrap=none"  # Don't wrap lines
        ]
        
        subprocess.run(cmd, check=True)
        print(f"✅ Converted to markdown: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e}")
        return None
    except FileNotFoundError as e:
        print(f"❌ Pandoc installation failed: {e}")
        return None

def main():
    doc_id = "16iQJdg6hNmmlG6hLFRueRawOhI5l8JT2n8-ezXbtsSQ"
    output_folder = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo"
    
    print("🚀 Advanced Google Doc Downloader")
    print(f"📄 Document ID: {doc_id}")
    print(f"📁 Output folder: {output_folder}")
    print("-" * 60)
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    os.chdir(output_folder)
    
    # Try different download methods
    downloaded_file = None
    
    # Method 1: Direct HTTP request
    print("\n📥 Method 1: Direct HTTP download")
    downloaded_file = download_via_export_url(doc_id, 'docx')
    
    if not downloaded_file:
        # Method 2: Using curl
        print("\n📥 Method 2: Curl download")
        downloaded_file = try_curl_download(doc_id, 'docx')
    
    if not downloaded_file:
        # Method 3: Try different formats
        print("\n📥 Method 3: Trying alternative formats")
        for fmt in ['txt', 'html', 'pdf']:
            print(f"  Trying {fmt}...")
            downloaded_file = download_via_export_url(doc_id, fmt)
            if downloaded_file:
                break
    
    if downloaded_file:
        print(f"\n✅ Successfully downloaded: {downloaded_file}")
        
        # Convert to markdown if it's a convertible format
        if downloaded_file.endswith(('.docx', '.html', '.txt')):
            markdown_file = convert_to_markdown(downloaded_file, output_folder)
            if markdown_file:
                print(f"📝 Markdown version created: {markdown_file}")
        
        print(f"\n🎉 Process complete! Files saved in: {output_folder}")
        
    else:
        print("\n❌ All download methods failed.")
        print("\n💡 Possible solutions:")
        print("1. Document may be private - check sharing permissions")
        print("2. Download manually from browser using the instructions")
        print("3. Make sure you're logged into the correct Google account")
        print("4. Try using Google Drive Desktop sync")
        
        # Show the manual download link again
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        print(f"\n🔗 Manual download link: {doc_url}")

if __name__ == "__main__":
    # Install required packages
    try:
        import requests
    except ImportError:
        print("📦 Installing requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        import requests
    
    main()