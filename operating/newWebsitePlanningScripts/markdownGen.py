import os

# Base directory where the folders are located
base_dir = "/workspaces/lcwebsiteAnalytics/newWebsitePlanning"

# Markdown template for planning.md
markdown_template = """# {page_title}

## Overview
- **Purpose**: [What is the purpose of this page?]
- **Audience**: [Who is the primary audience for this page?]

## Links to Older Web Pages
- **Old Web Page URL**: [Provide links to the older version of this page, if available]
  - Example: [Old Page](https://example.com/old-page)

## Structure of the Page
- **Main Heading**: {page_title}
- **Sub-sections**:
  1. [Sub-section 1 title]
  2. [Sub-section 2 title]
  3. [Etc.]

## Features and Content
- **Key Features**:
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]
- **Content Details**:
  - [Brief description of content for this page or section]

## Links to Resources
- **HTML File**: [{html_file_name}]({html_file_name})
- **Other Assets**:
  - [Images]
  - [Documents]
  - [External links]

## Planned Updates
- [Any updates or changes planned for this page in the new website structure]

## Notes
- [Any additional notes or considerations for this page]
"""

# Function to create planning.md files
def create_markdown_files(base_dir):
    # Walk through the directory structure
    for root, dirs, files in os.walk(base_dir):
        # Get the current folder name
        folder_name = os.path.basename(root)
        
        # Skip the base directory itself (only process sub-folders)
        if root == base_dir:
            continue
        
        # Determine the HTML file name for this folder
        html_file_name = f"{folder_name}_template.html"
        
        # Check if the HTML file exists in this folder
        if html_file_name in files:
            # Prepare the content for planning.md
            planning_md_content = markdown_template.format(
                page_title=folder_name.replace("_", " "),  # Convert underscores to spaces for readability
                html_file_name=html_file_name
            )
            
            # Path for the planning.md file
            planning_md_path = os.path.join(root, "planning.md")
            
            # Write the planning.md file
            with open(planning_md_path, "w") as md_file:
                md_file.write(planning_md_content)
            
            print(f"Created: {planning_md_path}")
        else:
            print(f"Skipped: {root} (No HTML template found)")

# Run the function to generate planning.md files
create_markdown_files(base_dir)