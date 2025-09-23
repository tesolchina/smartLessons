# Google Drive Integration for GCAP 3226

*Seamless cloud synchronization for course materials and collaboration*

## 🔗 Google Drive Setup

### Main Course Drive Structure
```
GCAP 3226 - Empowering Citizens through Data/
├── 📁 Course Administration/
│   ├── Syllabus & Schedules/
│   ├── Student Lists & Enrollment/
│   ├── Grade Books/
│   └── Course Policies/
├── 📁 Assignments & Projects/
│   ├── Assignment Instructions/
│   ├── Student Submissions/
│   ├── Rubrics & Grading/
│   └── Sample Projects/
├── 📁 Course Materials/
│   ├── Lecture Slides/
│   ├── Reading Materials/
│   ├── Videos & Multimedia/
│   └── External Resources/
├── 📁 Data & Research/
│   ├── Hong Kong Government Data/
│   ├── Policy Documents/
│   ├── Research Templates/
│   └── Analysis Tools/
├── 📁 Chatbot Resources/
│   ├── Training Data/
│   ├── Conversation Logs/
│   ├── Bot Updates/
│   └── User Feedback/
└── 📁 Budget & Administration/
    ├── Expense Tracking/
    ├── Purchase Orders/
    ├── Receipts/
    └── Financial Reports/
```

## ⚙️ Synchronization Setup

### Local-to-Drive Sync Configuration

1. **Install Google Drive Desktop App**
   ```bash
   # Download from: https://www.google.com/drive/download/
   # Choose "Drive for desktop"
   ```

2. **Configure Sync Folder**
   - Sync Path: `/Users/simonwang/Google Drive/GCAP 3226 - Empowering Citizens through Data/`
   - Local Mirror: `/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/google_drive_sync/`

3. **Selective Sync Settings**
   - ✅ Course Administration (Essential)
   - ✅ Assignments & Projects (Essential) 
   - ✅ Course Materials (Essential)
   - ✅ Data & Research (Large files - Stream only)
   - ✅ Chatbot Resources (Essential)
   - ✅ Budget & Administration (Essential)

## 📋 Sync Automation Script

Create an automated sync script to keep local project files updated with Google Drive:

```bash
#!/bin/bash
# sync_with_drive.sh

DRIVE_PATH="/Users/simonwang/Google Drive/GCAP 3226 - Empowering Citizens through Data"
LOCAL_PATH="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226"

# Sync course materials from Drive to local
rsync -av --delete "$DRIVE_PATH/Course Materials/" "$LOCAL_PATH/course_materials/"

# Sync assignments from Drive to local  
rsync -av --delete "$DRIVE_PATH/Assignments & Projects/" "$LOCAL_PATH/course_materials/assignments/"

# Upload budget tracking from local to Drive
rsync -av --delete "$LOCAL_PATH/budget_planning/" "$DRIVE_PATH/Budget & Administration/"

# Upload chatbot development from local to Drive
rsync -av --delete "$LOCAL_PATH/chatbots/" "$DRIVE_PATH/Chatbot Resources/"

echo "Sync completed: $(date)"
```

## 🔐 Access Permissions

### Drive Folder Sharing Settings

#### Course Administration Folder
- **Simon Wang (Owner)**: Full access
- **Department Admin**: Editor access
- **Course TAs**: Viewer access

#### Student-Facing Folders  
- **Students**: Viewer access to Course Materials
- **Students**: Editor access to designated submission folders
- **Public**: No access (private course materials)

#### Budget & Financial
- **Simon Wang**: Full access
- **Finance Office**: Viewer access
- **Department Head**: Viewer access

## 📊 Drive Usage Monitoring

### Storage Allocation
- **Total Drive Allocation**: 100 GB (Google Workspace for Education)
- **Estimated Course Usage**: 25 GB
- **Breakdown**:
  - Course Materials: 8 GB
  - Student Projects: 10 GB  
  - Chatbot Data: 3 GB
  - Administrative Files: 2 GB
  - Buffer: 2 GB

### Usage Tracking
- **Weekly**: Check storage usage and clean up temporary files
- **Monthly**: Archive old assignments and materials
- **Semester End**: Full backup and archive

## 🔄 Backup Strategy

### Multi-Layer Backup
1. **Primary**: Google Drive (Cloud)
2. **Secondary**: Local sync on development machine
3. **Tertiary**: External drive backup (monthly)
4. **Archive**: University network storage (semester-end)

### Critical Files Priority
- **Tier 1 (Daily Backup)**: Student grades, current assignments
- **Tier 2 (Weekly Backup)**: Course materials, chatbot code
- **Tier 3 (Monthly Backup)**: Archive materials, old projects

## 📱 Mobile Access

### Google Drive Mobile App Setup
- Install Google Drive app on mobile devices
- Enable offline access for critical folders
- Set up document editing permissions
- Configure notification preferences

### Quick Access Shortcuts
- Course schedule and calendar
- Current week's materials
- Student emergency contacts
- Budget tracking spreadsheet

## 🛠️ Integration Tools

### Third-Party Integrations
- **Moodle**: Auto-sync assignment submissions to Drive
- **Calendar**: Sync important course dates
- **Email**: Link Drive files in course communications
- **Chatbots**: Access training materials from Drive

### API Access (Advanced)
```python
# Google Drive API integration example
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def upload_to_drive(file_path, folder_id):
    service = build('drive', 'v3', credentials=creds)
    # Upload implementation here
    pass
```

## 📋 Setup Checklist

### Initial Setup
- [ ] Create main Google Drive folder structure
- [ ] Install Google Drive Desktop app
- [ ] Configure selective sync settings
- [ ] Set up folder sharing permissions
- [ ] Test sync functionality

### Content Migration
- [ ] Upload existing course syllabus
- [ ] Transfer student name lists
- [ ] Import assignment templates
- [ ] Add course reading materials
- [ ] Set up budget tracking sheets

### Access Configuration
- [ ] Share appropriate folders with TAs
- [ ] Create student-accessible material folders
- [ ] Set up submission folders for assignments
- [ ] Configure admin access for finance team
- [ ] Test permissions with different user roles

### Automation Setup
- [ ] Create sync automation script
- [ ] Set up scheduled sync (daily/weekly)
- [ ] Configure backup procedures
- [ ] Set up storage monitoring alerts
- [ ] Test disaster recovery procedures

## 🚨 Troubleshooting

### Common Issues
- **Sync Conflicts**: Use Google Drive's conflict resolution
- **Storage Full**: Clean up old files and archives
- **Permission Denied**: Check sharing settings and user access
- **Slow Sync**: Check internet connection and file sizes

### Emergency Procedures
- **Data Loss**: Restore from backup tiers
- **Access Issues**: Contact Google Workspace admin
- **Corruption**: Use Google Drive's version history
- **Security Breach**: Immediately revoke access and change permissions

## 📞 Support Contacts

- **Primary**: Simon Wang (Project Lead)
- **Google Workspace Admin**: IT Support Team
- **Technical Issues**: University IT Helpdesk
- **Emergency**: Department Admin Office

---

*This Google Drive integration ensures seamless collaboration and secure access to all GCAP 3226 course materials.*
