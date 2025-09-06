# Canva CLI Automation System

## Purpose
Comprehensive Canva design creation, collaboration, and management via CLI for academic and professional projects.

## Features
- **Web Automation**: Selenium-based Canva interaction
- **Collaborative Editing**: Team collaboration with automatic invitations
- **Template Management**: Automated template selection and customization
- **Course Materials**: Specialized tools for academic presentations
- **Batch Processing**: Multiple design creation workflows
- **Project Integration**: Compatible with existing email and project tools

## Setup

### Dependencies
```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation
pip3 install -r requirements.txt
```

### Configuration
```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your Canva credentials
```

## Usage

### Basic Design Creation
```bash
python3 canva_cli.py --template "presentation" --project "LANG2077" --slides 3
```

### Course Materials
```bash
python3 course_materials_creator.py --course "LANG2077" --type "introduction"
```

## Available Tools

### Main Automation Scripts
- **`canva_cli.py`** - Core Canva automation with browser control
- **`canva_collaborative_cli.py`** - Enhanced collaboration features with team invitations
- **`canva_collaboration_helper.py`** - No-browser helper for creating collaboration guides

### Course-Specific Tools
- **`lang2077_slides_creator.py`** - LANG 2077 specific slide automation
- **`lang2077_template_generator.py`** - Template generator for course materials
- **`canva_slide_creator.py`** - General slide creation tool (moved from LANG2077)

### Utilities
- **`canva_commands.sh`** - Easy CLI commands for common tasks
- **`CANVA_CLI_SETUP_GUIDE.md`** - Comprehensive setup instructions
- **`MIGRATION_SUMMARY.md`** - File organization history

### Course Materials (LANG2077)
Located in `lang2077_materials/`:
- `lang2077_slides_content.md` - Complete slide content
- `lang2077_slides_data.json` - Structured presentation data
- `canva_creation_guide.md` - Step-by-step Canva instructions
- `powerpoint_creation_guide.md` - Alternative PowerPoint workflow

### Quick Start Commands
```bash
# Create LANG 2077 slides with collaboration
./canva_commands.sh lang2077

# Create collaborative presentation
python3 canva_collaboration_helper.py

# Generate course templates
python3 lang2077_template_generator.py
```

### Batch Creation
```bash
python3 canva_collaborative_cli.py --collaborators user1@hkbu.edu.hk user2@hkbu.edu.hk --template "academic presentation"
```

## Integration
- Works with email automation system
- Saves designs to project folders
- Generates markdown documentation
- Logs all creation activities
- Supports team collaboration workflows

## Supported Design Types
- Academic presentations
- Course announcements
- Event posters
- Social media graphics
- Infographics
- Course materials
- Collaborative team projects
