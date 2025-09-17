# Generic Document Converter

A powerful, AI-free document conversion tool that converts documents between various formats using pandoc and other system tools.

## 🚀 Quick Start

```bash
# Convert DOCX to Markdown
python document_converter.py document.docx

# Convert with custom output name
python document_converter.py document.docx output.md

# Convert to specific format
python document_converter.py document.docx --format html

# Batch convert all documents in a directory
python document_converter.py --batch /path/to/documents

# List all supported formats
python document_converter.py --list-formats
```

## 📋 Features

- **AI-Free Conversion**: Uses pandoc and system tools without AI dependencies
- **Multiple Formats**: Supports DOCX, PDF, HTML, TXT, RTF, ODT, EPUB, LaTeX, Markdown, RST
- **Media Extraction**: Automatically extracts images and media from documents
- **Batch Processing**: Convert multiple documents at once
- **Smart Naming**: Automatically generates safe output filenames
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Logging**: Detailed progress and error reporting

## 📦 Installation

### Prerequisites

The tool requires **pandoc** as the primary conversion engine:

#### macOS (using Homebrew)
```bash
brew install pandoc
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install pandoc
```

#### Windows (using Chocolatey)
```bash
choco install pandoc
```

### Optional Tools (for enhanced functionality)

#### LibreOffice (for better PDF creation)
```bash
# macOS
brew install --cask libreoffice

# Ubuntu/Debian
sudo apt install libreoffice

# Windows
# Download from https://www.libreoffice.org/
```

#### PDF Tools (for better PDF to text conversion)
```bash
# macOS
brew install poppler  # provides pdftotext

# Ubuntu/Debian
sudo apt install poppler-utils

# Windows
# Download from http://blog.alivate.com.au/poppler-windows/
```

## 🛠 Usage

### Basic Conversion

```bash
# Convert DOCX to Markdown (default)
python document_converter.py report.docx

# Convert with specific output name
python document_converter.py report.docx report_converted.md

# Convert to HTML
python document_converter.py report.docx --format html

# Convert to PDF
python document_converter.py report.md --format pdf
```

### Batch Conversion

```bash
# Convert all documents in current directory
python document_converter.py --batch .

# Convert all documents in specific directory
python document_converter.py --batch /path/to/documents

# Recursive batch conversion
python document_converter.py --batch /path/to/documents --recursive

# Batch convert to specific format
python document_converter.py --batch /path/to/documents --format html
```

### Advanced Usage

```bash
# Convert PDF to Markdown (requires pdftotext or similar)
python document_converter.py document.pdf

# Convert multiple formats in pipeline
python document_converter.py document.docx temp.html --format html
python document_converter.py temp.html final.pdf --format pdf
```

## 📄 Supported Formats

### Input Formats
| Extension | Format | Description |
|-----------|--------|-------------|
| `.docx` | Microsoft Word | Modern Word documents |
| `.doc` | Microsoft Word | Legacy Word documents |
| `.pdf` | PDF | Portable Document Format |
| `.html` | HTML | Web pages |
| `.htm` | HTML | Web pages |
| `.txt` | Plain Text | Simple text files |
| `.rtf` | Rich Text | Rich Text Format |
| `.odt` | OpenDocument | LibreOffice/OpenOffice |
| `.epub` | EPUB | E-book format |
| `.tex` | LaTeX | LaTeX documents |
| `.md` | Markdown | Markdown files |
| `.rst` | reStructuredText | Documentation format |

### Output Formats
| Format | Extension | Description |
|--------|-----------|-------------|
| `markdown` | `.md` | Markdown format |
| `html` | `.html` | Web page format |
| `pdf` | `.pdf` | PDF format |
| `docx` | `.docx` | Microsoft Word |
| `txt` | `.txt` | Plain text |
| `rtf` | `.rtf` | Rich Text Format |
| `tex` | `.tex` | LaTeX format |
| `epub` | `.epub` | E-book format |
| `rst` | `.rst` | reStructuredText |

## 🔧 Configuration

### Tool Detection

The converter automatically detects available tools:

```bash
python document_converter.py --list-formats
```

This shows:
- Supported input/output formats
- Available conversion tools
- Missing optional tools

### Conversion Quality

For best results:

1. **DOCX to Markdown**: Excellent with pandoc
2. **PDF to Text**: Requires `pdftotext` for best formatting
3. **Any to PDF**: Requires LibreOffice for best results
4. **HTML/Web**: Excellent with pandoc
5. **LaTeX**: Excellent with pandoc

## 🚨 Troubleshooting

### Common Issues

#### "Pandoc not found"
```bash
# Install pandoc first
brew install pandoc  # macOS
sudo apt install pandoc  # Ubuntu/Debian
```

#### "No suitable PDF conversion tool available"
```bash
# For PDF to text conversion
brew install poppler  # macOS
sudo apt install poppler-utils  # Ubuntu/Debian

# For creating PDFs
brew install --cask libreoffice  # macOS
sudo apt install libreoffice  # Ubuntu/Debian
```

#### "Permission denied" errors
```bash
# Make sure the file is readable
chmod +r input_file.docx

# Make sure output directory is writable
chmod +w output_directory/
```

### Error Logs

The tool provides detailed logging. For debugging:

```bash
# Run with Python to see full error traces
python document_converter.py document.docx --format pdf
```

## 📚 Examples

### Example 1: Research Paper Workflow
```bash
# Convert research paper from Word to Markdown for editing
python document_converter.py research_paper.docx research_paper.md

# Convert to HTML for web publication
python document_converter.py research_paper.md research_paper.html

# Convert to PDF for final submission
python document_converter.py research_paper.md research_paper.pdf
```

### Example 2: Batch Document Processing
```bash
# Convert all Word documents in a directory to Markdown
python document_converter.py --batch documents/ --format markdown

# Recursively convert all documents in project structure
python document_converter.py --batch . --recursive --format html
```

### Example 3: PDF Text Extraction
```bash
# Extract text from PDF for analysis
python document_converter.py report.pdf report.txt

# Convert PDF to Markdown for editing
python document_converter.py report.pdf report.md
```

## 🔗 Integration

### Use in Scripts

```python
from document_converter import DocumentConverter

converter = DocumentConverter()

# Convert single document
success = converter.convert_document('input.docx', 'output.md', 'markdown')

# Batch convert
results = converter.batch_convert('/path/to/docs', 'html')
```

### Use in Workflows

```bash
#!/bin/bash
# Convert all DOCX files to Markdown for Git versioning
for file in *.docx; do
    python document_converter.py "$file" "${file%.docx}.md"
done
```

## 🆘 Support

### Getting Help

1. **Check tool availability**: `python document_converter.py --list-formats`
2. **Verify input file**: Make sure the file exists and is readable
3. **Check logs**: Look for detailed error messages in the output
4. **Try different format**: Some conversions work better than others

### Reporting Issues

When reporting issues, include:
- Input file format and size
- Desired output format
- Error messages
- Operating system
- Available tools (from `--list-formats`)

## 📝 License

This tool is free to use and modify. It leverages open-source tools:
- **Pandoc**: Universal document converter
- **LibreOffice**: Office suite for document processing
- **Poppler**: PDF rendering library

## ✨ Pro Tips

1. **Best Markdown Quality**: DOCX → Markdown works excellently
2. **Best PDF Creation**: Use LibreOffice when available
3. **Preserve Formatting**: Some complex formatting may be lost in conversion
4. **Media Files**: Images are automatically extracted to `media/` folder
5. **Batch Processing**: Use `--recursive` for complex directory structures
6. **File Names**: Tool automatically creates safe filenames with underscores

---

**Created for GCAP 3056 Project - Document conversion without AI dependencies**
