# Generic Forum Analysis System

A flexible, configuration-driven system for analyzing Moodle forum submissions.

## Overview

This system processes JSON exports from Moodle forums and generates comprehensive analysis reports based on configurable instruction files. It can handle any forum structure and assignment type by defining appropriate configuration files.

## Files

### Core Analysis Tools
- **`generic_forum_analyzer.py`** - Main analysis engine that processes any JSON forum export based on configuration files
- **`config_generator.py`** - Interactive tool to create new configuration files for different forum types
- **`csv_student_viewer.py`** - Utility to view and explore student enrollment data

### Configuration Files
- **`config_video_transcript.json`** - Configuration for video transcript submission analysis
- **`config_revise_outline.json`** - Configuration for essay outline revision analysis

### Legacy Tools (Deprecated)
- **`dual_forum_analyzer.py`** - Original hardcoded dual-forum analyzer (superseded by generic system)

## Quick Start

### 1. Validate Configuration
```bash
python3 generic_forum_analyzer.py --validate config_video_transcript.json
```

### 2. Run Analysis
```bash
python3 generic_forum_analyzer.py config_video_transcript.json
```

### 3. List Available Configurations
```bash
python3 generic_forum_analyzer.py --list-configs
```

## Creating New Configurations

### Option 1: Interactive Generator (Recommended)
```bash
python3 config_generator.py
```

The generator will walk you through:
- Basic configuration setup
- Data source paths
- JSON structure mapping
- Assignment component definitions
- Content classification rules
- Analysis criteria
- Report generation settings

### Option 2: Manual Configuration

Create a JSON file following this structure:

```json
{
  "analysis_config": {
    "name": "Your Analysis Name",
    "description": "Description of the forum analysis",
    "version": "1.0"
  },
  "data_sources": {
    "forum_json": "../path/to/forum.json",
    "student_csv": "../path/to/students.csv",
    "output_directory": "../OutputFolder"
  },
  "json_structure": {
    "posts_path": "[0]",
    "post_fields": {
      "id": "id",
      "user": "userfullname",
      "parent": "parent",
      "subject": "subject",
      "message": "message",
      "created": "created",
      "wordcount": "wordcount"
    },
    "instructor_names": ["Instructor Name"]
  },
  "content_classification": {
    "assignment_components": [
      {
        "name": "Component Name",
        "emoji": "📄",
        "indicators": ["keyword1", "keyword2"],
        "min_length": 50,
        "required": true
      }
    ],
    "exclusion_patterns": ["template", "example"]
  },
  "analysis_criteria": {
    "completion_threshold": {
      "complete": 3,
      "partial": 1
    },
    "quality_metrics": [
      "content_completeness",
      "language_quality",
      "assignment_adherence"
    ]
  },
  "report_generation": {
    "individual_report": {
      "filename": "individual_reports.md",
      "title": "Individual Student Reports",
      "include_full_content": true,
      "content_preview_length": 1000
    },
    "overall_report": {
      "filename": "comprehensive_overall_report.md",
      "title": "Comprehensive Analysis Report",
      "include_section_breakdown": true,
      "include_participation_stats": true
    }
  }
}
```

## Configuration Sections Explained

### `analysis_config`
Basic metadata about the analysis type.

### `data_sources`
- **`forum_json`**: Path to Moodle forum JSON export
- **`student_csv`**: Path to student enrollment CSV (optional)
- **`output_directory`**: Where to save analysis reports

### `json_structure`
Maps your JSON structure to the analyzer:
- **`posts_path`**: JSONPath to posts array (usually `"[0]"` for nested exports)
- **`post_fields`**: Field name mappings for post data
- **`instructor_names`**: List of instructor names to exclude from student analysis

### `content_classification`
Defines how to identify assignment components:
- **`assignment_components`**: List of assignment parts with:
  - `name`: Component name
  - `emoji`: Display emoji
  - `indicators`: Keywords/phrases that indicate this component
  - `min_length`: Minimum text length
  - `required`: Whether component is required for completion
- **`exclusion_patterns`**: Patterns that indicate template/example content

### `analysis_criteria`
- **`completion_threshold`**: Number of components needed for complete/partial classification
- **`quality_metrics`**: Types of quality assessment performed

### `report_generation`
Output format configuration for individual and overall reports.

## Output Reports

The system generates two types of reports:

### Individual Student Reports
- Detailed analysis for each student
- Component-by-component breakdown
- Content quality assessment
- Full submission content (configurable)

### Comprehensive Overall Report
- Participation statistics
- Section-based breakdown (if student CSV provided)
- Completion rate analysis
- Missing student identification

## Data Requirements

### Forum JSON Structure
The system expects Moodle forum JSON exports with nested reply structure. Each post should have:
- Unique ID
- User name
- Parent post reference (for replies)
- Subject and message content
- Creation timestamp
- Word count

### Student CSV Structure (Optional)
If provided, should include:
- Student names (for cross-referencing)
- Section codes (for section-based reporting)
- Student IDs (for identification)

## Examples

### Video Transcript Analysis
Analyzes 3-component video transcript submissions:
1. Raw Transcript
2. Error Analysis  
3. Self-Assessment

### Essay Outline Revision
Analyzes 4-component outline revision process:
1. Original Outline
2. Revision Planning
3. Revised Outline
4. Self-Reflection

## Migration from Legacy System

If you have existing `dual_forum_analyzer.py` usage, the new system provides:
- Same analysis quality with improved flexibility
- Configuration-based setup instead of hardcoded rules
- Better extensibility for new forum types
- Maintained compatibility with existing data sources

## Troubleshooting

### Configuration Validation Errors
- Use `--validate` flag to check configuration syntax
- Ensure all file paths are correct and relative to tools directory
- Verify JSON structure matches your actual forum export

### Missing Data
- Check that JSON file contains expected structure
- Verify student CSV encoding (UTF-8 recommended)
- Ensure instructor names match exactly in configuration

### Analysis Issues
- Review content classification indicators
- Adjust minimum length thresholds
- Check exclusion patterns for false positives

## Command Reference

```bash
# List available configurations
python3 generic_forum_analyzer.py --list-configs

# Validate configuration
python3 generic_forum_analyzer.py --validate CONFIG_FILE

# Run analysis
python3 generic_forum_analyzer.py CONFIG_FILE

# Create new configuration
python3 config_generator.py

# View student data
python3 csv_student_viewer.py
```