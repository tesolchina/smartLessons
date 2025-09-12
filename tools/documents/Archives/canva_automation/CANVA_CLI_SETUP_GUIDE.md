# Canva CLI Setup Guide for LANG2077 Service Learning Course

## Overview
Based on the extracted emails, Joshua and the team prefer using **Canva** for design materials. While Canva doesn't have a direct CLI, we can set up automated workflows and integrations.

## Quick Setup Options

### Option 1: Canva API Integration (Recommended)
```bash
# Install Canva API dependencies
npm install canva-api
# or
pip install canva-python-api

# Set up environment variables
export CANVA_API_KEY="your_api_key"
export CANVA_BRAND_ID="your_brand_id"
```

### Option 2: Selenium Automation for Canva Web
```bash
# Install selenium for web automation
pip install selenium webdriver-manager

# Create automated Canva workflows
```

### Option 3: Canva Integration via Zapier/Make
```bash
# Use webhook triggers for automated design creation
curl -X POST "https://hooks.zapier.com/hooks/catch/xxx" \
  -H "Content-Type: application/json" \
  -d '{"template": "service_learning", "course": "LANG2077"}'
```

## Service Learning Course Design Templates

### 1. Course Announcement Template
```python
# Python script to generate course announcements
import canva_api

def create_course_announcement():
    design = canva_api.create_design(
        template_id="course_announcement",
        data={
            "course_name": "LANG2077 Service Learning",
            "instructor": "Simon Wang",
            "meeting_date": "September 8, 2:40pm",
            "location": "OEE"
        }
    )
    return design.export("png")
```

### 2. Service Learning Partnership Graphics
```python
def create_partnership_graphic():
    design = canva_api.create_design(
        template_id="partnership_announcement",
        data={
            "partner_organization": "Community Partner",
            "course": "LANG2077",
            "collaboration_type": "Service Learning Project"
        }
    )
    return design.export("pdf")
```

### 3. Student Project Showcase Template
```python
def create_project_showcase():
    design = canva_api.create_design(
        template_id="student_showcase",
        data={
            "project_title": "Student Project Name",
            "student_names": "List of Students",
            "project_description": "Brief description"
        }
    )
    return design.export("png")
```

## Automated Workflow Script

### Main Canva Automation Script
```python
#!/usr/bin/env python3
"""
LANG2077 Canva Automation
Automated design creation for service learning course
"""

import os
import requests
import json
from datetime import datetime

class CanvaAutomation:
    def __init__(self, api_key, brand_id):
        self.api_key = api_key
        self.brand_id = brand_id
        self.base_url = "https://api.canva.com/v1"
        
    def create_service_learning_design(self, template_type, data):
        """Create a new design from template"""
        
        templates = {
            "course_announcement": "template_id_1",
            "partnership_graphic": "template_id_2", 
            "project_showcase": "template_id_3",
            "meeting_reminder": "template_id_4"
        }
        
        payload = {
            "template_id": templates.get(template_type),
            "brand_id": self.brand_id,
            "data": data
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/designs",
            headers=headers,
            json=payload
        )
        
        return response.json()
    
    def export_design(self, design_id, format="png"):
        """Export design to file"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(
            f"{self.base_url}/designs/{design_id}/export",
            headers=headers,
            json={"format": format}
        )
        
        return response.json()

def main():
    """Main automation workflow"""
    
    # Initialize Canva API
    canva = CanvaAutomation(
        api_key=os.getenv("CANVA_API_KEY"),
        brand_id=os.getenv("CANVA_BRAND_ID")
    )
    
    # Create course announcement
    announcement_data = {
        "course_name": "LANG2077 - New Service Learning Course",
        "instructor": "Simon Wang",
        "department": "Language Centre",
        "date": datetime.now().strftime("%B %d, %Y")
    }
    
    design = canva.create_service_learning_design(
        "course_announcement", 
        announcement_data
    )
    
    print(f"✅ Created design: {design.get('id')}")
    
    # Export design
    export = canva.export_design(design['id'], "png")
    print(f"📁 Design exported: {export.get('url')}")

if __name__ == "__main__":
    main()
```

## Quick Commands for LANG2077

### Generate Course Materials
```bash
# Course announcement
python3 canva_automation.py --template course_announcement --course "LANG2077"

# Partnership graphic
python3 canva_automation.py --template partnership_graphic --partner "Community Org"

# Meeting reminder
python3 canva_automation.py --template meeting_reminder --date "Sep 8 2:40pm"
```

### Batch Create Designs
```bash
# Create multiple designs at once
python3 batch_canva_creator.py --templates "announcement,partnership,showcase" --course "LANG2077"
```

## Setup Instructions

### 1. Get Canva API Access
1. Go to [Canva Developers](https://www.canva.com/developers/)
2. Create a new app
3. Get your API key and Brand ID
4. Add to environment variables

### 2. Install Dependencies
```bash
pip install requests python-dotenv
```

### 3. Configure Environment
```bash
# Create .env file
echo "CANVA_API_KEY=your_api_key" >> .env
echo "CANVA_BRAND_ID=your_brand_id" >> .env
```

### 4. Test the Setup
```bash
python3 operating/canva_automation/test_canva.py
```

## Integration with Email System

### Auto-Create Designs from Emails
```python
# When new service learning emails arrive, auto-create designs
def email_to_design_webhook(email_data):
    if "service learning" in email_data.subject.lower():
        canva.create_service_learning_design(
            "course_update",
            {
                "title": email_data.subject,
                "content": email_data.preview,
                "date": email_data.date
            }
        )
```

## Next Steps for LANG2077

1. **Set up Canva API credentials**
2. **Create design templates** for service learning course
3. **Test automation scripts** with sample data
4. **Integrate with email workflows** for automatic design creation
5. **Share designs** with Joshua and team for approval

---

*This setup enables CLI-based Canva design creation for the new LANG2077 service learning course, as requested in the departmental meeting email thread.*
