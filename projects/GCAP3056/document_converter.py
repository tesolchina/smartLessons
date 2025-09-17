#!/usr/bin/env python3
"""
Generic Document Converter
Converts documents between various formats without using AI.
Supports: DOCX, PDF, HTML, TXT to Markdown and other formats.

Usage:
    python document_converter.py input_file [output_file] [--format output_format]
    python document_converter.py --batch directory
    python document_converter.py --list-formats
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentConverter:
    """Generic document converter using pandoc and other tools."""
    
    SUPPORTED_INPUT_FORMATS = {
        '.docx': 'docx',
        '.doc': 'doc',
        '.pdf': 'pdf',
        '.html': 'html',
        '.htm': 'html',
        '.txt': 'plain-text',
        '.rtf': 'rtf',
        '.odt': 'odt',
        '.epub': 'epub',
        '.tex': 'latex',
        '.md': 'markdown',
        '.rst': 'rst'
    }
    
    SUPPORTED_OUTPUT_FORMATS = {
        'markdown': '.md',
        'md': '.md',
        'pdf': '.pdf',
        'html': '.html',
        'docx': '.docx',
        'txt': '.txt',
        'rtf': '.rtf',
        'tex': '.tex',
        'epub': '.epub',
        'rst': '.rst'
    }
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if required tools are available."""
        self.has_pandoc = shutil.which('pandoc') is not None
        self.has_libreoffice = shutil.which('libreoffice') is not None
        self.has_pdftotext = shutil.which('pdftotext') is not None
        self.has_pdf2txt = shutil.which('pdf2txt.py') is not None
        
        if not self.has_pandoc:
            logger.warning("Pandoc not found. Install with: brew install pandoc")
        
        logger.info(f"Available tools: pandoc={self.has_pandoc}, "
                   f"libreoffice={self.has_libreoffice}, "
                   f"pdftotext={self.has_pdftotext}")
    
    def get_file_format(self, file_path: str) -> Optional[str]:
        """Get the format of a file based on its extension."""
        ext = Path(file_path).suffix.lower()
        return self.SUPPORTED_INPUT_FORMATS.get(ext)
    
    def create_safe_filename(self, input_path: str, output_format: str = 'md') -> str:
        """Create a safe output filename."""
        input_path_obj = Path(input_path)
        base_name = input_path_obj.stem.replace(' ', '_').replace('(', '').replace(')', '')
        output_ext = self.SUPPORTED_OUTPUT_FORMATS.get(output_format, '.md')
        
        output_path = input_path_obj.parent / f"{base_name}_converted{output_ext}"
        return str(output_path)
    
    def convert_with_pandoc(self, input_path: str, output_path: str, 
                           input_format: Optional[str] = None,
                           extract_media: bool = True) -> bool:
        """Convert document using pandoc."""
        if not self.has_pandoc:
            logger.error("Pandoc is required but not available")
            return False
        
        try:
            cmd = ['pandoc', input_path, '-o', output_path]
            
            if input_format:
                cmd.extend(['-f', input_format])
            
            # Extract media if converting to markdown
            if extract_media and output_path.endswith('.md'):
                media_dir = Path(output_path).parent / 'media'
                cmd.extend(['--extract-media', str(media_dir)])
            
            # Add useful pandoc options
            cmd.extend([
                '--wrap=auto',  # Auto-wrap text
                '--standalone',  # Produce standalone document
            ])
            
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully converted {input_path} to {output_path}")
                return True
            else:
                logger.error(f"Pandoc error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error during pandoc conversion: {e}")
            return False
    
    def convert_pdf_to_text(self, input_path: str, output_path: str) -> bool:
        """Convert PDF to text using available tools."""
        # Try pdftotext first (better formatting)
        if self.has_pdftotext:
            try:
                cmd = ['pdftotext', '-layout', input_path, output_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"PDF converted to text using pdftotext")
                    return True
            except Exception as e:
                logger.warning(f"pdftotext failed: {e}")
        
        # Try pdf2txt as fallback
        if self.has_pdf2txt:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    cmd = ['pdf2txt.py', input_path]
                    result = subprocess.run(cmd, stdout=f, capture_output=False, text=True)
                    if result.returncode == 0:
                        logger.info(f"PDF converted to text using pdf2txt")
                        return True
            except Exception as e:
                logger.warning(f"pdf2txt failed: {e}")
        
        # Try pandoc as last resort
        if self.has_pandoc:
            try:
                return self.convert_with_pandoc(input_path, output_path, 'pdf', extract_media=False)
            except Exception as e:
                logger.warning(f"pandoc pdf conversion failed: {e}")
        
        logger.error("No suitable PDF conversion tool available")
        return False
    
    def convert_to_pdf(self, input_path: str, output_path: str) -> bool:
        """Convert document to PDF using available tools."""
        if self.has_libreoffice:
            try:
                # Use LibreOffice for best results
                output_dir = Path(output_path).parent
                cmd = ['libreoffice', '--headless', '--convert-to', 'pdf', 
                       '--outdir', str(output_dir), input_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # LibreOffice creates file with same name but .pdf extension
                    temp_pdf = output_dir / (Path(input_path).stem + '.pdf')
                    if temp_pdf.exists() and str(temp_pdf) != output_path:
                        shutil.move(str(temp_pdf), output_path)
                    logger.info(f"Document converted to PDF using LibreOffice")
                    return True
            except Exception as e:
                logger.warning(f"LibreOffice conversion failed: {e}")
        
        # Try pandoc as fallback
        if self.has_pandoc:
            try:
                return self.convert_with_pandoc(input_path, output_path, extract_media=False)
            except Exception as e:
                logger.warning(f"pandoc PDF conversion failed: {e}")
        
        logger.error("No suitable PDF creation tool available")
        return False
    
    def convert_document(self, input_path: str, output_path: Optional[str] = None, 
                        output_format: str = 'markdown') -> bool:
        """Convert a document to the specified format."""
        if not os.path.exists(input_path):
            logger.error(f"Input file does not exist: {input_path}")
            return False
        
        input_format = self.get_file_format(input_path)
        if not input_format:
            logger.error(f"Unsupported input format: {Path(input_path).suffix}")
            return False
        
        if not output_path:
            output_path = self.create_safe_filename(input_path, output_format)
        
        logger.info(f"Converting {input_path} ({input_format}) to {output_path} ({output_format})")
        
        # Special handling for different conversion types
        if input_format == 'pdf' and output_format in ['markdown', 'md', 'txt']:
            # PDF to text/markdown
            if output_format in ['markdown', 'md']:
                # Convert to text first, then to markdown
                temp_txt = output_path.replace('.md', '.txt')
                if self.convert_pdf_to_text(input_path, temp_txt):
                    if self.convert_with_pandoc(temp_txt, output_path, None):  # Let pandoc auto-detect
                        os.remove(temp_txt)  # Clean up temp file
                        return True
                return False
            else:
                return self.convert_pdf_to_text(input_path, output_path)
        
        elif output_format == 'pdf':
            # Convert to PDF
            return self.convert_to_pdf(input_path, output_path)
        
        else:
            # Use pandoc for most conversions
            return self.convert_with_pandoc(input_path, output_path, input_format)
    
    def batch_convert(self, directory: str, output_format: str = 'markdown',
                     recursive: bool = False) -> List[Dict]:
        """Convert all supported documents in a directory."""
        directory_path = Path(directory)
        if not directory_path.exists():
            logger.error(f"Directory does not exist: {directory}")
            return []
        
        pattern = '**/*' if recursive else '*'
        results = []
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and self.get_file_format(str(file_path)):
                output_path = self.create_safe_filename(str(file_path), output_format)
                success = self.convert_document(str(file_path), output_path, output_format)
                results.append({
                    'input': str(file_path),
                    'output': output_path,
                    'success': success
                })
        
        return results
    
    def list_formats(self):
        """List all supported input and output formats."""
        print("\nSupported Input Formats:")
        for ext, fmt in self.SUPPORTED_INPUT_FORMATS.items():
            print(f"  {ext:<8} -> {fmt}")
        
        print("\nSupported Output Formats:")
        for fmt, ext in self.SUPPORTED_OUTPUT_FORMATS.items():
            print(f"  {fmt:<12} -> {ext}")
        
        print("\nAvailable Tools:")
        print(f"  pandoc: {'✓' if self.has_pandoc else '✗'}")
        print(f"  libreoffice: {'✓' if self.has_libreoffice else '✗'}")
        print(f"  pdftotext: {'✓' if self.has_pdftotext else '✗'}")

def main():
    parser = argparse.ArgumentParser(description='Generic Document Converter')
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path (optional)')
    parser.add_argument('--format', '-f', default='markdown', 
                       help='Output format (default: markdown)')
    parser.add_argument('--batch', '-b', help='Convert all files in directory')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Recursive batch conversion')
    parser.add_argument('--list-formats', '-l', action='store_true',
                       help='List supported formats')
    
    args = parser.parse_args()
    
    converter = DocumentConverter()
    
    if args.list_formats:
        converter.list_formats()
        return
    
    if args.batch:
        results = converter.batch_convert(args.batch, args.format, args.recursive)
        successful = sum(1 for r in results if r['success'])
        print(f"\nBatch conversion complete: {successful}/{len(results)} files converted successfully")
        return
    
    if not args.input:
        parser.print_help()
        return
    
    success = converter.convert_document(args.input, args.output, args.format)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
