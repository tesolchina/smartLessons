#!/usr/bin/env python3
"""
GCAP 3056 Enhanced Google Docs & Drive Manager
Tool to read, write, and create documents in Google Drive folders

Usage:
    python gcap3056_enhanced_manager.py --create-info-gathering-docs
    python gcap3056_enhanced_manager.py --sync-project "energy_poverty"
    python gcap3056_enhanced_manager.py --read-project "energy_poverty"
"""
import sys
import os
import pickle
import argparse
import re
import json
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google API configuration - Enhanced with Drive API
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_TOOLS_DIR = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api"
TOKEN_PATH = os.path.join(GOOGLE_TOOLS_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(GOOGLE_TOOLS_DIR, 'credentials.json')

# Project documents configuration with folder IDs (to be discovered)
PROJECT_DOCS = {
    "energy_poverty": {
        "url": "https://docs.google.com/document/d/1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk/edit?tab=t.0",
        "doc_id": "1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk",
        "local_dir": "Projects and teams/energy_poverty",
        "folder_id": None  # To be discovered
    },
    "hko_chatbot": {
        "url": "https://docs.google.com/document/d/1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw/edit?tab=t.0",
        "doc_id": "1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw",
        "local_dir": "Projects and teams/hko_chatbot",
        "folder_id": None
    },
    "chronic_disease_co_care": {
        "url": "https://docs.google.com/document/d/1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA/edit?tab=t.0",
        "doc_id": "1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA",
        "local_dir": "Projects and teams/chronic_disease_co_care",
        "folder_id": None
    },
    "anti_scamming_education": {
        "url": "https://docs.google.com/document/d/1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA/edit?tab=t.8lpba9bjqpel#heading=h.s640o2lk1eg6",
        "doc_id": "1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA",
        "local_dir": "Projects and teams/anti_scamming_education",
        "folder_id": None
    },
    "emergency_alert_system": {
        "url": "https://docs.google.com/document/d/19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0/edit?tab=t.0",
        "doc_id": "19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0",
        "local_dir": "Projects and teams/emergency_alert_system",
        "folder_id": None
    }
}

class GCAP3056EnhancedManager:
    def __init__(self):
        self.docs_service = None
        self.drive_service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google API using existing credentials"""
        creds = None
        
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(CREDENTIALS_PATH):
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print(f"❌ Credentials file not found at {CREDENTIALS_PATH}")
                    print("Please set up Google API credentials first.")
                    return False
            
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        
        self.docs_service = build('docs', 'v1', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)
        print("✅ Authenticated with Google Docs and Drive APIs")
        return True
    
    def find_parent_folder_id(self, doc_id):
        """Find the parent folder of a given document"""
        try:
            file_metadata = self.drive_service.files().get(
                fileId=doc_id,
                fields='parents'
            ).execute()
            
            parents = file_metadata.get('parents', [])
            if parents:
                return parents[0]  # Return first parent folder ID
            return None
            
        except Exception as e:
            print(f"❌ Error finding parent folder for {doc_id}: {e}")
            return None
    
    def discover_project_folders(self):
        """Discover and update folder IDs for all projects"""
        print("🔍 Discovering project folder IDs...")
        
        for project_name, info in PROJECT_DOCS.items():
            doc_id = info['doc_id']
            folder_id = self.find_parent_folder_id(doc_id)
            
            if folder_id:
                PROJECT_DOCS[project_name]['folder_id'] = folder_id
                print(f"✅ {project_name}: Found folder ID {folder_id}")
            else:
                print(f"⚠️  {project_name}: Could not find parent folder")
        
        # Save updated configuration
        config_file = Path("project_folders_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(PROJECT_DOCS, f, indent=2)
        
        print(f"💾 Folder configuration saved to {config_file}")
    
    def create_info_gathering_template(self, project_name):
        """Create info gathering template content for a project"""
        templates = {
            "energy_poverty": {
                "title": "Energy Poverty - Info Gathering",
                "content": """# Energy Poverty in Hong Kong - Information Gathering

## Project Overview
**Topic:** Energy Poverty and Social Equity in Hong Kong
**Focus:** How energy affordability affects vulnerable populations

## Key Research Questions
1. What is the current state of energy poverty in Hong Kong?
2. Which demographics are most affected by energy poverty?
3. What are the health and social impacts of energy poverty?
4. What policy interventions exist currently?
5. How do other cities address energy poverty effectively?

## Information Needed
### Quantitative Data
- [ ] Energy expenditure as % of household income by district
- [ ] Electricity tariff trends over past 5 years
- [ ] Number of households in subdivided flats
- [ ] Energy consumption patterns by income level
- [ ] Utility disconnection rates

### Qualitative Information
- [ ] Personal stories from affected families
- [ ] Social worker perspectives
- [ ] NGO reports on energy poverty
- [ ] Government policy statements
- [ ] Academic research findings

## Potential Arguments to Develop
1. **Equity Argument:** Energy poverty exacerbates social inequality
2. **Health Argument:** Inadequate heating/cooling affects public health
3. **Economic Argument:** Energy poverty cycles trap families in poverty
4. **Policy Argument:** Current subsidies are insufficient/misdirected

## Sources to Investigate
- [ ] Census and Statistics Department data
- [ ] CLP and HK Electric reports
- [ ] Society for Community Organization (SoCO) studies
- [ ] Legislative Council papers on energy policy
- [ ] Academic journals on energy poverty

## Action Items
- [ ] Interview families in subdivided flats
- [ ] Review government energy assistance programs
- [ ] Compare Hong Kong with other cities (Singapore, London)
- [ ] Calculate true cost of energy poverty to society

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {timestamp}*
"""
            },
            "hko_chatbot": {
                "title": "HKO Chatbot - Info Gathering",
                "content": """# HKO Chatbot Development - Information Gathering

## Project Overview
**Topic:** Hong Kong Observatory Chatbot for Public Weather Information
**Focus:** Improving public access to weather information through AI

## Key Research Questions
1. What are current limitations of HKO's information delivery?
2. How do citizens currently access weather information?
3. What chatbot features would be most valuable?
4. What are the technical requirements and constraints?
5. How can we ensure accessibility for all users?

## Information Needed
### User Research
- [ ] Survey of current HKO website/app usage
- [ ] Pain points in accessing weather information
- [ ] Preferred communication channels (WhatsApp, Telegram, etc.)
- [ ] Accessibility needs for elderly/disabled users
- [ ] Language preferences (Cantonese, English, Mandarin)

### Technical Requirements
- [ ] HKO's current API capabilities
- [ ] Data formats and update frequencies
- [ ] Integration possibilities with existing systems
- [ ] Chatbot platform options and costs
- [ ] Security and privacy requirements

## Potential Arguments to Develop
1. **Accessibility Argument:** Chatbots improve information access for all citizens
2. **Efficiency Argument:** Automated responses reduce staff workload
3. **Innovation Argument:** Government should lead in digital transformation
4. **Public Safety Argument:** Better weather communication saves lives

## Sources to Investigate
- [ ] HKO current services and user feedback
- [ ] Chatbot best practices from other weather services
- [ ] Digital government initiatives in Hong Kong
- [ ] Accessibility guidelines for government services
- [ ] Cost-benefit analysis of chatbot implementations

## Action Items
- [ ] Interview HKO staff about current challenges
- [ ] Survey public about weather information needs
- [ ] Review international weather chatbot examples
- [ ] Assess technical feasibility and costs

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {timestamp}*
"""
            },
            "chronic_disease_co_care": {
                "title": "Chronic Disease Co-care - Info Gathering",
                "content": """# Chronic Disease Co-care Pilot Scheme - Information Gathering

## Project Overview
**Topic:** Evaluation and Improvement of Hong Kong's Chronic Disease Co-care Model
**Focus:** Assessing effectiveness and scalability of integrated care

## Key Research Questions
1. How effective is the current co-care pilot scheme?
2. What are the barriers to patient participation?
3. How well are public and private sectors coordinating?
4. What are the cost implications of scaling up?
5. How does this compare to international models?

## Information Needed
### Program Performance
- [ ] Patient enrollment and retention rates
- [ ] Health outcome improvements (HbA1c, blood pressure)
- [ ] Patient satisfaction scores
- [ ] Healthcare provider feedback
- [ ] Cost per patient vs. traditional care

### System Analysis
- [ ] Coordination mechanisms between HA and private doctors
- [ ] Information sharing protocols and challenges
- [ ] Training requirements for healthcare providers
- [ ] Quality assurance measures
- [ ] Scaling challenges and opportunities

## Potential Arguments to Develop
1. **Efficiency Argument:** Co-care reduces pressure on public system
2. **Quality Argument:** Integrated care improves patient outcomes
3. **Equity Argument:** Program access should be expanded to more patients
4. **Economic Argument:** Long-term savings justify investment

## Sources to Investigate
- [ ] Hospital Authority performance data
- [ ] Participant feedback surveys
- [ ] Healthcare provider interviews
- [ ] Legislative Council health panel discussions
- [ ] International integrated care studies

## Action Items
- [ ] Interview patients in co-care program
- [ ] Survey private doctors participating
- [ ] Review HA data on program outcomes
- [ ] Compare with integrated care models elsewhere

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {timestamp}*
"""
            },
            "anti_scamming_education": {
                "title": "Anti-Scamming Education - Info Gathering",
                "content": """# Anti-Scamming Education Emergency Alert System - Information Gathering

## Project Overview
**Topic:** Enhanced Public Education and Emergency Alerts for Scam Prevention
**Focus:** Improving Hong Kong's response to evolving scam threats

## Key Research Questions
1. What are the most prevalent scam types affecting Hong Kong?
2. How effective are current anti-scam education efforts?
3. What emergency alert mechanisms exist and how can they be improved?
4. Which demographics are most vulnerable to scams?
5. How quickly do scam tactics evolve and spread?

## Information Needed
### Scam Landscape
- [ ] Police statistics on scam types and financial losses
- [ ] Demographic profiles of scam victims
- [ ] Emerging scam trends and tactics
- [ ] Cross-border scam operations
- [ ] Social media and technology-enabled scams

### Current Response Systems
- [ ] Police anti-scam education programs
- [ ] Media awareness campaigns effectiveness
- [ ] Bank and financial institution alerts
- [ ] Community organization outreach
- [ ] Emergency alert system capabilities

## Potential Arguments to Develop
1. **Prevention Argument:** Education is more cost-effective than enforcement
2. **Technology Argument:** Real-time alerts can prevent losses
3. **Vulnerability Argument:** Elderly and new immigrants need targeted protection
4. **Coordination Argument:** Multi-agency approach is essential

## Sources to Investigate
- [ ] Hong Kong Police scam statistics and reports
- [ ] Monetary Authority warnings and guidelines
- [ ] Senior citizen organizations feedback
- [ ] Banking industry anti-scam measures
- [ ] International best practices in scam prevention

## Action Items
- [ ] Interview police anti-scam unit
- [ ] Survey vulnerable populations about scam awareness
- [ ] Review current alert systems effectiveness
- [ ] Study rapid response models from other jurisdictions

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {timestamp}*
"""
            },
            "emergency_alert_system": {
                "title": "Emergency Alert System - Info Gathering",
                "content": """# Emergency Alert System Enhancement - Information Gathering

## Project Overview
**Topic:** Improving Hong Kong's Emergency Alert System
**Focus:** Enhancing public warning capabilities for natural disasters and emergencies

## Key Research Questions
1. What are the current capabilities and limitations of Hong Kong's alert system?
2. How does it compare to international best practices?
3. What technologies could improve alert reach and effectiveness?
4. How well do different populations receive and respond to alerts?
5. What are the coordination challenges between agencies?

## Information Needed
### Current System Assessment
- [ ] Types of emergencies currently covered
- [ ] Alert delivery channels and reach
- [ ] Response times for different alert types
- [ ] Public awareness and understanding of alerts
- [ ] Technical infrastructure and capabilities

### Gap Analysis
- [ ] Coverage gaps in population or geography
- [ ] Language and accessibility barriers
- [ ] Technology limitations
- [ ] Inter-agency coordination issues
- [ ] Public education and preparedness needs

## Potential Arguments to Develop
1. **Safety Argument:** Enhanced alerts save lives and reduce injuries
2. **Technology Argument:** Modern systems can reach more people faster
3. **Inclusion Argument:** All residents deserve equal access to warnings
4. **Preparedness Argument:** Better alerts improve overall emergency response

## Sources to Investigate
- [ ] Government emergency management policies
- [ ] Observatory and Fire Services alert protocols
- [ ] International emergency alert system studies
- [ ] Public feedback on recent emergency responses
- [ ] Technology industry emergency communication solutions

## Action Items
- [ ] Review recent emergency responses and alert effectiveness
- [ ] Survey public awareness of alert systems
- [ ] Study international emergency alert best practices
- [ ] Interview emergency management officials

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {timestamp}*
"""
            }
        }
        
        template = templates.get(project_name, {
            "title": f"{project_name.replace('_', ' ').title()} - Info Gathering",
            "content": f"""# {project_name.replace('_', ' ').title()} - Information Gathering

## Project Overview
**Topic:** {project_name.replace('_', ' ').title()}
**Focus:** [Define the focus area]

## Key Research Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]

## Information Needed
- [ ] [Information item 1]
- [ ] [Information item 2]

## Potential Arguments to Develop
1. [Argument 1]
2. [Argument 2]

## Sources to Investigate
- [ ] [Source 1]
- [ ] [Source 2]

## Action Items
- [ ] [Action 1]
- [ ] [Action 2]

## Notes and Insights
[Add findings and insights here as research progresses]

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        })
        
        # Replace timestamp placeholder
        content = template["content"].replace("{timestamp}", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        return template["title"], content
    
    def create_info_gathering_doc(self, project_name):
        """Create an info gathering document in the project's Google Drive folder"""
        if project_name not in PROJECT_DOCS:
            print(f"❌ Project '{project_name}' not found")
            return None
        
        folder_id = PROJECT_DOCS[project_name]['folder_id']
        if not folder_id:
            print(f"❌ Folder ID not found for {project_name}. Run --discover-folders first.")
            return None
        
        try:
            title, content = self.create_info_gathering_template(project_name)
            
            print(f"📝 Creating '{title}' in {project_name} folder...")
            
            # Create the document
            doc = self.docs_service.documents().create(
                body={'title': title}
            ).execute()
            
            doc_id = doc.get('documentId')
            
            # Move document to project folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                fields='id,parents'
            ).execute()
            
            # Add content to document
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            
            print(f"✅ Created: {title}")
            print(f"📄 Document ID: {doc_id}")
            print(f"🔗 URL: {doc_url}")
            
            return {
                'title': title,
                'doc_id': doc_id,
                'url': doc_url,
                'content': content
            }
            
        except Exception as e:
            print(f"❌ Error creating document for {project_name}: {e}")
            return None
    
    def create_local_info_gathering_file(self, project_name, doc_data=None):
        """Create local markdown file for info gathering"""
        local_dir = Path(PROJECT_DOCS[project_name]['local_dir'])
        local_dir.mkdir(parents=True, exist_ok=True)
        
        if doc_data:
            title = doc_data['title']
            content = doc_data['content']
            doc_id = doc_data['doc_id']
            doc_url = doc_data['url']
        else:
            title, content = self.create_info_gathering_template(project_name)
            doc_id = "TBD"
            doc_url = "TBD"
        
        # Create local markdown file
        filename = "info_gathering.md"
        file_path = local_dir / filename
        
        # Add sync metadata to content
        sync_header = f"""<!-- SYNC INFO -->
<!-- Google Doc ID: {doc_id} -->
<!-- Google Doc URL: {doc_url} -->
<!-- Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->
<!-- Auto-generated by GCAP 3056 Enhanced Manager -->

"""
        
        full_content = sync_header + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"💾 Local file created: {file_path}")
        return file_path
    
    def create_all_info_gathering_docs(self):
        """Create info gathering documents for all projects"""
        print("🚀 Creating info gathering documents for all projects...")
        
        # First discover folder IDs
        self.discover_project_folders()
        
        results = {}
        for project_name in PROJECT_DOCS.keys():
            print(f"\n📁 Processing {project_name}...")
            
            # Create Google Doc
            doc_data = self.create_info_gathering_doc(project_name)
            
            # Create local file
            local_file = self.create_local_info_gathering_file(project_name, doc_data)
            
            if doc_data:
                results[project_name] = {
                    'google_doc': doc_data,
                    'local_file': str(local_file)
                }
        
        # Save results
        results_file = Path("info_gathering_creation_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Results saved to {results_file}")
        return results

def main():
    parser = argparse.ArgumentParser(description='GCAP 3056 Enhanced Google Docs & Drive Manager')
    
    # Discovery operations
    parser.add_argument('--discover-folders', action='store_true', help='Discover project folder IDs')
    
    # Creation operations
    parser.add_argument('--create-info-gathering-docs', action='store_true', help='Create info gathering docs for all projects')
    parser.add_argument('--create-info-gathering', help='Create info gathering doc for specific project')
    
    # Read operations
    parser.add_argument('--read-project', help='Read specific project document')
    parser.add_argument('--list-projects', action='store_true', help='List all available projects')
    
    args = parser.parse_args()
    
    if not any([args.discover_folders, args.create_info_gathering_docs, args.create_info_gathering,
                args.read_project, args.list_projects]):
        print("❌ Please specify an operation")
        parser.print_help()
        sys.exit(1)
    
    manager = GCAP3056EnhancedManager()
    
    if args.discover_folders:
        manager.discover_project_folders()
    
    elif args.create_info_gathering_docs:
        manager.create_all_info_gathering_docs()
    
    elif args.create_info_gathering:
        doc_data = manager.create_info_gathering_doc(args.create_info_gathering)
        if doc_data:
            manager.create_local_info_gathering_file(args.create_info_gathering, doc_data)
    
    elif args.list_projects:
        print("📁 Available projects:")
        for i, (project_name, info) in enumerate(PROJECT_DOCS.items(), 1):
            print(f"  {i}. {project_name}")
            print(f"     Main Doc: {info['doc_id']}")
            print(f"     Local Dir: {info['local_dir']}")
            print()
    
    elif args.read_project:
        print(f"📖 Reading {args.read_project} (using original functionality)")
        # Could integrate original read functionality here

if __name__ == "__main__":
    main()
