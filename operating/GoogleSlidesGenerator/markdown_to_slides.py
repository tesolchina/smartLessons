#!/usr/bin/env python3
"""
Google Slides Generator - Main Conversion Engine
===============================================

Converts markdown files to Google Slides presentations with professional formatting.
Designed for educational content like GCAP 3226 course materials.

Usage:
    python markdown_to_slides.py --input "lecture.md" --template "educational" --drive-folder "Course/Lectures"
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Google API imports
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Text processing imports
import markdown
from bs4 import BeautifulSoup


class MarkdownToSlidesConverter:
    """Main converter class for markdown to Google Slides."""
    
    def __init__(self, config_path: str = "config"):
        """Initialize converter with configuration."""
        self.config_path = Path(config_path)
        self.load_configuration()
        self.setup_google_apis()
        
    def load_configuration(self):
        """Load configuration files."""
        # Load templates
        templates_file = self.config_path / "templates.json"
        if templates_file.exists():
            with open(templates_file, 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        else:
            self.templates = self.get_default_templates()
            
        # Load drive configuration
        drive_config_file = self.config_path / "drive_config.json" 
        if drive_config_file.exists():
            with open(drive_config_file, 'r', encoding='utf-8') as f:
                self.drive_config = json.load(f)
        else:
            self.drive_config = {"default_folder": "Presentations"}
            
    def setup_google_apis(self):
        """Set up Google Slides and Drive API clients."""
        try:
            # Load service account credentials
            creds_file = self.config_path / "service_account_key.json"
            if not creds_file.exists():
                raise FileNotFoundError("Service account key file not found. Run setup_auth.py first.")
                
            scopes = [
                'https://www.googleapis.com/auth/presentations',
                'https://www.googleapis.com/auth/drive'
            ]
            
            self.credentials = Credentials.from_service_account_file(
                str(creds_file), scopes=scopes
            )
            
            self.slides_service = build('slides', 'v1', credentials=self.credentials)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            
            print("✅ Google APIs initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Google APIs: {e}")
            raise
            
    def parse_markdown_file(self, file_path: str) -> Dict[str, Any]:
        """Parse markdown file and extract slide structure."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract metadata from file
        metadata = self.extract_metadata(content)
        
        # Split into slides
        slides_data = self.split_into_slides(content)
        
        return {
            'metadata': metadata,
            'slides': slides_data,
            'total_slides': len(slides_data)
        }
        
    def extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract presentation metadata from markdown."""
        metadata = {}
        
        # Look for title (first # heading)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Look for subtitle (second # heading or first ## heading)
        subtitle_match = re.search(r'^## (.+)$', content, re.MULTILINE)
        if subtitle_match:
            metadata['subtitle'] = subtitle_match.group(1).strip()
            
        # Extract other metadata from markdown frontmatter or comments
        date_match = re.search(r'\*\*Date:\*\* (.+)', content)
        if date_match:
            metadata['date'] = date_match.group(1).strip()
            
        course_match = re.search(r'\*\*Course:\*\* (.+)', content)
        if course_match:
            metadata['course'] = course_match.group(1).strip()
            
        instructors_match = re.search(r'\*\*Instructors:\*\* (.+)', content)
        if instructors_match:
            metadata['instructors'] = instructors_match.group(1).strip()
            
        return metadata
        
    def split_into_slides(self, content: str) -> List[Dict[str, Any]]:
        """Split markdown content into individual slides."""
        # Remove metadata section
        content = re.sub(r'^---.*?^---', '', content, flags=re.MULTILINE | re.DOTALL)
        
        # Split by slide delimiters
        slide_delimiters = [
            r'^---$',  # Horizontal rule
            r'^## Slide \d+:',  # Explicit slide markers
            r'^## \d+\.',  # Numbered slides
        ]
        
        # Use horizontal rules as primary delimiter
        slide_sections = re.split(r'^---+$', content, flags=re.MULTILINE)
        
        slides = []
        for i, section in enumerate(slide_sections):
            section = section.strip()
            if not section:
                continue
                
            slide_data = self.parse_slide_content(section, i + 1)
            if slide_data:
                slides.append(slide_data)
                
        return slides
        
    def parse_slide_content(self, section: str, slide_number: int) -> Dict[str, Any]:
        """Parse individual slide content."""
        lines = section.split('\n')
        slide_data = {
            'number': slide_number,
            'type': 'content',  # default type
            'title': '',
            'content': [],
            'notes': []
        }
        
        # Extract title (first ## heading)
        title_match = re.search(r'^## (.+)$', section, re.MULTILINE)
        if title_match:
            slide_data['title'] = title_match.group(1).strip()
            
        # Process content line by line
        current_section = 'content'
        content_buffer = []
        
        for line in lines:
            line = line.strip()
            
            # Skip title line (already extracted)
            if line.startswith('## ') and slide_data['title'] in line:
                continue
                
            # Handle different content types
            if line.startswith('### '):
                # Subsection
                content_buffer.append({
                    'type': 'subsection',
                    'text': line[4:].strip()
                })
            elif line.startswith('#### '):
                # Sub-subsection
                content_buffer.append({
                    'type': 'subheading',
                    'text': line[5:].strip()
                })
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet point
                content_buffer.append({
                    'type': 'bullet',
                    'text': line[2:].strip(),
                    'level': 1
                })
            elif re.match(r'^\d+\.', line):
                # Numbered list
                content_buffer.append({
                    'type': 'numbered',
                    'text': re.sub(r'^\d+\.\s*', '', line),
                    'number': len([c for c in content_buffer if c.get('type') == 'numbered']) + 1
                })
            elif line.startswith('  - ') or line.startswith('  * '):
                # Sub-bullet point
                content_buffer.append({
                    'type': 'bullet',
                    'text': line[4:].strip(),
                    'level': 2
                })
            elif line:
                # Regular text
                content_buffer.append({
                    'type': 'text',
                    'text': line
                })
                
        slide_data['content'] = content_buffer
        return slide_data
        
    def create_google_slides_presentation(self, parsed_data: Dict[str, Any], template: str = "educational") -> str:
        """Create Google Slides presentation from parsed data."""
        try:
            # Create new presentation
            presentation_title = parsed_data['metadata'].get('title', 'Untitled Presentation')
            
            presentation = {
                'title': presentation_title
            }
            
            presentation_response = self.slides_service.presentations().create(
                body=presentation
            ).execute()
            
            presentation_id = presentation_response['presentationId']
            print(f"✅ Created presentation: {presentation_title} (ID: {presentation_id})")
            
            # Get template configuration
            template_config = self.templates.get(template, self.templates['default'])
            
            # Delete default slide and create custom slides
            self.clear_default_slide(presentation_id)
            
            # Create title slide
            self.create_title_slide(presentation_id, parsed_data['metadata'], template_config)
            
            # Create content slides
            for slide_data in parsed_data['slides']:
                self.create_content_slide(presentation_id, slide_data, template_config)
                
            print(f"✅ Generated {len(parsed_data['slides']) + 1} slides")
            return presentation_id
            
        except HttpError as e:
            print(f"❌ Error creating presentation: {e}")
            raise
            
    def clear_default_slide(self, presentation_id: str):
        """Remove the default empty slide."""
        try:
            # Get presentation to find default slide ID
            presentation = self.slides_service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            if presentation['slides']:
                default_slide_id = presentation['slides'][0]['objectId']
                
                requests = [{
                    'deleteObject': {
                        'objectId': default_slide_id
                    }
                }]
                
                self.slides_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
                
        except Exception as e:
            print(f"⚠️ Could not remove default slide: {e}")
            
    def create_title_slide(self, presentation_id: str, metadata: Dict[str, str], template_config: Dict[str, Any]):
        """Create title slide."""
        slide_id = f"title_slide_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        requests = [
            {
                'createSlide': {
                    'objectId': slide_id,
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE'
                    }
                }
            }
        ]
        
        # Execute slide creation
        self.slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
        
        # Add title and subtitle text
        text_requests = []
        
        if metadata.get('title'):
            text_requests.append({
                'insertText': {
                    'objectId': f"{slide_id}_title",
                    'text': metadata['title']
                }
            })
            
        if metadata.get('subtitle'):
            text_requests.append({
                'insertText': {
                    'objectId': f"{slide_id}_subtitle", 
                    'text': metadata['subtitle']
                }
            })
            
        # Add additional metadata
        if metadata.get('date') or metadata.get('instructors'):
            footer_text = []
            if metadata.get('date'):
                footer_text.append(metadata['date'])
            if metadata.get('instructors'):
                footer_text.append(metadata['instructors'])
                
            text_requests.append({
                'insertText': {
                    'objectId': f"{slide_id}_body",
                    'text': ' | '.join(footer_text)
                }
            })
            
        if text_requests:
            self.slides_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': text_requests}
            ).execute()
            
    def create_content_slide(self, presentation_id: str, slide_data: Dict[str, Any], template_config: Dict[str, Any]):
        """Create content slide."""
        slide_id = f"slide_{slide_data['number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        requests = [
            {
                'createSlide': {
                    'objectId': slide_id,
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_BODY'
                    }
                }
            }
        ]
        
        # Execute slide creation
        self.slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
        
        # Add content
        text_requests = []
        
        # Add title
        if slide_data['title']:
            text_requests.append({
                'insertText': {
                    'objectId': f"{slide_id}_title",
                    'text': slide_data['title']
                }
            })
            
        # Add body content
        body_text = self.format_slide_content(slide_data['content'])
        if body_text:
            text_requests.append({
                'insertText': {
                    'objectId': f"{slide_id}_body",
                    'text': body_text
                }
            })
            
        if text_requests:
            self.slides_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': text_requests}
            ).execute()
            
    def format_slide_content(self, content_items: List[Dict[str, Any]]) -> str:
        """Format slide content items into text."""
        formatted_lines = []
        
        for item in content_items:
            item_type = item.get('type', 'text')
            text = item.get('text', '')
            
            if item_type == 'subsection':
                formatted_lines.append(f"\n{text}")
            elif item_type == 'subheading':
                formatted_lines.append(f"  {text}")
            elif item_type == 'bullet':
                level = item.get('level', 1)
                indent = '  ' * (level - 1)
                formatted_lines.append(f"{indent}• {text}")
            elif item_type == 'numbered':
                number = item.get('number', 1)
                formatted_lines.append(f"{number}. {text}")
            elif item_type == 'text':
                if formatted_lines and not formatted_lines[-1].endswith('\n'):
                    formatted_lines.append(f"\n{text}")
                else:
                    formatted_lines.append(text)
                    
        return '\n'.join(formatted_lines)
        
    def upload_to_drive(self, presentation_id: str, folder_name: str, file_name: str) -> str:
        """Upload presentation to Google Drive folder."""
        try:
            # Find or create folder
            folder_id = self.find_or_create_drive_folder(folder_name)
            
            # Move presentation to folder
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            
            # Update file metadata
            updated_file = self.drive_service.files().update(
                fileId=presentation_id,
                body=file_metadata
            ).execute()
            
            # Get shareable link
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            
            self.drive_service.permissions().create(
                fileId=presentation_id,
                body=permission
            ).execute()
            
            file_link = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
            print(f"✅ Uploaded to Drive: {file_name}")
            print(f"🔗 Link: {file_link}")
            
            return file_link
            
        except HttpError as e:
            print(f"❌ Error uploading to Drive: {e}")
            raise
            
    def find_or_create_drive_folder(self, folder_path: str) -> str:
        """Find or create folder in Google Drive."""
        folder_parts = folder_path.split('/')
        current_folder_id = 'root'
        
        for folder_name in folder_parts:
            if not folder_name.strip():
                continue
                
            # Search for existing folder
            query = f"name='{folder_name}' and '{current_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
            
            results = self.drive_service.files().list(q=query).execute()
            folders = results.get('files', [])
            
            if folders:
                current_folder_id = folders[0]['id']
            else:
                # Create new folder
                folder_metadata = {
                    'name': folder_name,
                    'parents': [current_folder_id],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.drive_service.files().create(
                    body=folder_metadata
                ).execute()
                
                current_folder_id = folder['id']
                print(f"📁 Created folder: {folder_name}")
                
        return current_folder_id
        
    def get_default_templates(self) -> Dict[str, Any]:
        """Get default slide templates."""
        return {
            "default": {
                "name": "Default",
                "colors": {
                    "primary": "#1a73e8",
                    "secondary": "#34a853",
                    "text": "#202124",
                    "background": "#ffffff"
                },
                "fonts": {
                    "title": "Arial",
                    "body": "Arial"
                }
            },
            "educational": {
                "name": "Educational",
                "colors": {
                    "primary": "#5D5CDE",
                    "secondary": "#7B7AE8", 
                    "text": "#202124",
                    "background": "#ffffff"
                },
                "fonts": {
                    "title": "Roboto",
                    "body": "Roboto"
                }
            },
            "hkbu": {
                "name": "HKBU Theme",
                "colors": {
                    "primary": "#8B4513",
                    "secondary": "#D2691E",
                    "text": "#000000",
                    "background": "#ffffff"
                },
                "fonts": {
                    "title": "Arial",
                    "body": "Arial"
                }
            }
        }
        
    def convert(self, input_file: str, template: str = "educational", 
                drive_folder: str = None, output_name: str = None) -> Dict[str, str]:
        """Main conversion method."""
        print(f"🚀 Converting {input_file} to Google Slides...")
        
        # Parse markdown file
        parsed_data = self.parse_markdown_file(input_file)
        print(f"📄 Parsed {parsed_data['total_slides']} slides")
        
        # Create Google Slides presentation
        presentation_id = self.create_google_slides_presentation(parsed_data, template)
        
        # Determine output name and folder
        if not output_name:
            output_name = Path(input_file).stem + "_Slides"
        if not drive_folder:
            drive_folder = self.drive_config.get('default_folder', 'Presentations')
            
        # Upload to Drive
        file_link = self.upload_to_drive(presentation_id, drive_folder, output_name)
        
        return {
            'presentation_id': presentation_id,
            'file_link': file_link,
            'output_name': output_name,
            'folder': drive_folder
        }


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Convert Markdown to Google Slides')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file')
    parser.add_argument('--template', '-t', default='educational', help='Slide template to use')
    parser.add_argument('--drive-folder', '-f', help='Google Drive folder path')
    parser.add_argument('--output-name', '-o', help='Output presentation name')
    parser.add_argument('--config', '-c', default='config', help='Configuration directory')
    
    args = parser.parse_args()
    
    try:
        # Initialize converter
        converter = MarkdownToSlidesConverter(args.config)
        
        # Convert file
        result = converter.convert(
            input_file=args.input,
            template=args.template,
            drive_folder=args.drive_folder,
            output_name=args.output_name
        )
        
        print(f"\n🎉 Conversion successful!")
        print(f"📊 Presentation: {result['output_name']}")
        print(f"📁 Folder: {result['folder']}")
        print(f"🔗 Link: {result['file_link']}")
        
    except Exception as e:
        print(f"\n❌ Conversion failed: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())
