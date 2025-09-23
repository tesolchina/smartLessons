# GCAP3226 Instructor Collaboration System - Usage Guide

## Overview
This system allows Simon and Talia to collaborate on team project notes in a shared Google Doc, then automatically sync those notes to individual team folders.

## System Components

### 1. Main Instructor Collaboration Document
**URL:** https://docs.google.com/document/d/1Vd98A1bFDgJrMj8UiKLrOYdIauP0rr-Ca7kz4A6Hu80

This is your shared workspace where both instructors can:
- Add notes and observations for each team
- Track progress and concerns
- Plan interventions and feedback
- Share private instructor observations

### 2. Automatic Sync System
Updates individual team folders with relevant notes from the collaboration document.

## How to Use

### Step 1: Add Notes to Collaboration Document
1. Open the instructor collaboration document (link above)
2. Navigate to the appropriate team section
3. Add your notes in the designated areas:
   - **PROGRESS NOTES**: Observable progress and achievements
   - **FEEDBACK TO SHARE**: Comments that should be shared with students
   - **PRIVATE INSTRUCTOR NOTES**: Internal observations and concerns
   - **ACTION ITEMS**: Specific follow-up actions needed

### Step 2: Sync Notes to Team Folders
Run the sync command to update all team folders:

```bash
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/98_technical/google_api_reusable
python sync_instructor_notes.py
```

Or sync a specific team only:
```bash
python sync_instructor_notes.py --team Team_1
```

### Step 3: Review Updated Team Folders
After syncing, each team folder will contain:
- `Instructor_Notes_for_Team_X.docx` - Dedicated instructor notes document
- Updated `README.md` with instructor notes section

## Team Structure

| Team | Topic | Folder Link |
|------|-------|-------------|
| Team_1 | Flu Shot Participation Analysis | [Folder](https://drive.google.com/drive/folders/1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo) |
| Team_2 | Inter-Company Bus Route Coordination | [Folder](https://drive.google.com/drive/folders/1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C) |
| Team_3 | Typhoon Signal Data Analysis | [Folder](https://drive.google.com/drive/folders/1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD) |
| Team_4 | Municipal Solid Waste Charging Scheme | [Folder](https://drive.google.com/drive/folders/1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f) |
| Team_5 | Green@Community Recycling Network Analysis | [Folder](https://drive.google.com/drive/folders/1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw) |
| Team_6 | Bus Stop Merger Optimization | [Folder](https://drive.google.com/drive/folders/1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo) |

## Document Structure in Collaboration Doc

For each team, use this structure:

```
TEAM_X - [Topic Name]
Members: [Student names]
Folder: [Google Drive link]

PROGRESS NOTES:
[Add team progress observations here]

FEEDBACK TO SHARE:
[Add feedback that should be shared with the team]

PRIVATE INSTRUCTOR NOTES:
[Add internal notes, concerns, or observations]

ACTION ITEMS:
[Add specific follow-up actions needed]

LAST UPDATED: [Date] by: [Instructor name]

---
```

## Best Practices

### For Collaboration
1. **Date stamp your entries** - Always include dates and your name
2. **Use clear sections** - Separate shareable vs. private notes
3. **Be specific** - Include actionable observations and feedback
4. **Color code** - Use different colors for different types of notes (optional)
5. **Comment system** - Use Google Docs comments for discussions between instructors

### For Syncing
1. **Regular syncing** - Run sync after major note updates
2. **Review before syncing** - Ensure notes are appropriate for student view
3. **Check results** - Verify that notes appear correctly in team folders
4. **Backup important notes** - The system maintains version history

## Troubleshooting

### If sync fails:
1. Check your internet connection
2. Verify Google API credentials are valid
3. Ensure you have access to all team folders
4. Run with specific team to isolate issues

### If notes don't appear:
1. Check that you're using the correct team section headers
2. Verify the team name format (Team_1, Team_2, etc.)
3. Ensure the sync completed without errors

### If permissions issues:
1. Verify that both instructors have edit access to the collaboration document
2. Check that the Google API service account has proper permissions

## File Locations

- **Collaboration system script**: `98_technical/google_api_reusable/instructor_collaboration_system.py`
- **Sync script**: `98_technical/google_api_reusable/sync_instructor_notes.py`
- **This guide**: `98_technical/google_api_reusable/instructor_collaboration_guide.md`
- **Reports**: Generated in `98_technical/google_api_reusable/` with timestamps

## Advanced Features

### Selective Syncing
You can sync specific teams or exclude certain content by modifying the sync script parameters.

### Automated Scheduling
Consider setting up automated syncing on a schedule using cron jobs or similar scheduling systems.

### Integration with Other Tools
The system can be extended to integrate with:
- Email notifications
- Calendar reminders
- Grade book systems
- Student feedback platforms

## Support

For technical issues or feature requests, contact the course technical support or modify the scripts as needed.

---

*System created on: September 23, 2025*
*Last updated: September 23, 2025*