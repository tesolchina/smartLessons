#!/bin/bash
# Google Drive Sync Script for GCAP 3226
# Run this script to keep local files synced with Google Drive

DRIVE_PATH="/Users/simonwang/Google Drive/GCAP 3226 - Empowering Citizens through Data"
LOCAL_PATH="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226"

echo "Starting GCAP 3226 sync: $(date)"

# Check if Google Drive is mounted
if [ ! -d "$DRIVE_PATH" ]; then
    echo "Error: Google Drive not found at $DRIVE_PATH"
    echo "Please ensure Google Drive Desktop is installed and running"
    exit 1
fi

# Sync course materials from Drive to local
echo "Syncing course materials..."
rsync -av --delete "$DRIVE_PATH/Course Materials/" "$LOCAL_PATH/course_materials/" 2>/dev/null || echo "Course materials folder not yet created in Drive"

# Sync assignments  
echo "Syncing assignments..."
rsync -av --delete "$DRIVE_PATH/Assignments & Projects/" "$LOCAL_PATH/course_materials/assignments/" 2>/dev/null || echo "Assignments folder not yet created in Drive"

# Upload budget tracking from local to Drive
echo "Uploading budget tracking..."
rsync -av --delete "$LOCAL_PATH/budget_planning/" "$DRIVE_PATH/Budget & Administration/" 2>/dev/null || echo "Creating Budget folder in Drive..."

# Upload chatbot development from local to Drive
echo "Uploading chatbot resources..."
rsync -av --delete "$LOCAL_PATH/chatbots/" "$DRIVE_PATH/Chatbot Resources/" 2>/dev/null || echo "Creating Chatbot folder in Drive..."

echo "Sync completed: $(date)"
echo "Check sync_log.txt for detailed information"
