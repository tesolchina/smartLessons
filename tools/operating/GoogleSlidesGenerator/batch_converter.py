#!/usr/bin/env python3
"""
Batch Converter - Process Multiple Markdown Files
================================================

Converts multiple markdown files to Google Slides presentations in batch.
Perfect for processing entire course material folders.

Usage:
    python batch_converter.py --course-folder "/path/to/course" --drive-base "GCAP3226"
"""

import os
import argparse
from pathlib import Path
from markdown_to_slides import MarkdownToSlidesConverter


class BatchConverter:
    """Batch processing for multiple markdown files."""
    
    def __init__(self, config_path: str = "config"):
        """Initialize batch converter."""
        self.converter = MarkdownToSlidesConverter(config_path)
        self.results = []
        
    def find_markdown_files(self, folder_path: str, pattern: str = "*.md") -> list:
        """Find all markdown files in a folder and subfolders."""
        folder = Path(folder_path)
        
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        # Find all markdown files
        markdown_files = []
        for file_path in folder.rglob(pattern):
            if file_path.is_file():
                markdown_files.append(file_path)
                
        return sorted(markdown_files)
        
    def determine_drive_path(self, file_path: Path, base_folder: str, course_folder: Path) -> str:
        """Determine appropriate Google Drive folder path for a file."""
        # Get relative path from course folder
        try:
            relative_path = file_path.relative_to(course_folder)
            path_parts = relative_path.parts[:-1]  # Exclude filename
            
            # Build drive folder path
            drive_parts = [base_folder]
            
            for part in path_parts:
                # Map common folder names
                if part.lower().startswith('week'):
                    drive_parts.append(f"Weekly Materials/{part}")
                elif 'lecture' in part.lower():
                    drive_parts.append("Lectures")
                elif 'workshop' in part.lower():
                    drive_parts.append("Workshops")
                elif 'assignment' in part.lower():
                    drive_parts.append("Assignments")
                else:
                    drive_parts.append(part)
                    
            return '/'.join(drive_parts)
            
        except ValueError:
            # File is not under course folder, use base folder
            return base_folder
            
    def determine_output_name(self, file_path: Path) -> str:
        """Generate appropriate output name for presentation."""
        file_stem = file_path.stem
        
        # Clean up common suffixes
        file_stem = file_stem.replace('_Lecture_Slides', '')
        file_stem = file_stem.replace('_Materials_Guide', '')
        file_stem = file_stem.replace('week2LectureNote', 'Week 2 Lecture')
        
        # Add "Slides" suffix if not present
        if not file_stem.lower().endswith('slides'):
            file_stem += " - Slides"
            
        return file_stem
        
    def process_file(self, file_path: Path, drive_base: str, course_folder: Path, template: str = "educational") -> dict:
        """Process a single markdown file."""
        print(f"\n📄 Processing: {file_path.name}")
        
        try:
            # Determine paths and names
            drive_folder = self.determine_drive_path(file_path, drive_base, course_folder)
            output_name = self.determine_output_name(file_path)
            
            print(f"📁 Drive folder: {drive_folder}")
            print(f"📝 Output name: {output_name}")
            
            # Convert file
            result = self.converter.convert(
                input_file=str(file_path),
                template=template,
                drive_folder=drive_folder,
                output_name=output_name
            )
            
            result['source_file'] = str(file_path)
            result['status'] = 'success'
            
            return result
            
        except Exception as e:
            error_result = {
                'source_file': str(file_path),
                'status': 'error',
                'error': str(e),
                'presentation_id': None,
                'file_link': None
            }
            
            print(f"❌ Error processing {file_path.name}: {e}")
            return error_result
            
    def process_course_folder(self, course_folder: str, drive_base: str, 
                             template: str = "educational", file_pattern: str = "*.md") -> list:
        """Process entire course folder."""
        course_path = Path(course_folder)
        print(f"🚀 Processing course folder: {course_path}")
        print(f"📁 Drive base folder: {drive_base}")
        print(f"🎨 Template: {template}")
        
        # Find all markdown files
        markdown_files = self.find_markdown_files(course_folder, file_pattern)
        print(f"📄 Found {len(markdown_files)} markdown files")
        
        if not markdown_files:
            print("⚠️ No markdown files found!")
            return []
            
        # Process each file
        results = []
        for i, file_path in enumerate(markdown_files, 1):
            print(f"\n--- Processing file {i}/{len(markdown_files)} ---")
            
            result = self.process_file(file_path, drive_base, course_path, template)
            results.append(result)
            
        return results
        
    def generate_summary_report(self, results: list) -> str:
        """Generate summary report of batch conversion."""
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']
        
        report = f"""
# Batch Conversion Summary Report
**Generated:** {Path().cwd()}
**Total Files:** {len(results)}

## ✅ Successful Conversions: {len(successful)}
"""
        
        for result in successful:
            file_name = Path(result['source_file']).name
            report += f"- **{file_name}** → [{result['output_name']}]({result['file_link']})\n"
            
        if failed:
            report += f"\n## ❌ Failed Conversions: {len(failed)}\n"
            for result in failed:
                file_name = Path(result['source_file']).name
                report += f"- **{file_name}**: {result['error']}\n"
                
        report += f"\n## 📊 Statistics\n"
        report += f"- Success Rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)\n"
        report += f"- Total Presentations Created: {len(successful)}\n"
        
        if successful:
            report += f"\n## 🔗 All Presentation Links\n"
            for result in successful:
                report += f"- {result['output_name']}: {result['file_link']}\n"
                
        return report


def main():
    """Command line interface for batch processing."""
    parser = argparse.ArgumentParser(description='Batch convert markdown files to Google Slides')
    parser.add_argument('--course-folder', '-f', required=True, help='Course folder path')
    parser.add_argument('--drive-base', '-d', required=True, help='Base Google Drive folder')
    parser.add_argument('--template', '-t', default='educational', help='Slide template')
    parser.add_argument('--pattern', '-p', default='*.md', help='File pattern to match')
    parser.add_argument('--report', '-r', help='Save summary report to file')
    parser.add_argument('--config', '-c', default='config', help='Configuration directory')
    
    args = parser.parse_args()
    
    try:
        # Initialize batch converter
        batch_converter = BatchConverter(args.config)
        
        # Process course folder
        results = batch_converter.process_course_folder(
            course_folder=args.course_folder,
            drive_base=args.drive_base,
            template=args.template,
            file_pattern=args.pattern
        )
        
        # Generate summary report
        report = batch_converter.generate_summary_report(results)
        print("\n" + "="*60)
        print(report)
        
        # Save report to file if requested
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.report}")
            
        # Print final statistics
        successful = len([r for r in results if r['status'] == 'success'])
        total = len(results)
        
        if successful == total:
            print(f"\n🎉 All {total} files converted successfully!")
        else:
            print(f"\n⚠️ {successful}/{total} files converted successfully")
            
        return 0 if successful == total else 1
        
    except Exception as e:
        print(f"\n❌ Batch conversion failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
