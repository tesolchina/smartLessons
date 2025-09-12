#!/bin/bash
#
# Google Drive CLI Upload Script
# Upload LANG 2077 slides to Google Drive using rclone
#

echo "🎓 LANG 2077 - Google Drive Upload via rclone"
echo "==============================================="

# Check if rclone is installed
if ! command -v rclone &> /dev/null; then
    echo "❌ rclone not found"
    echo "📦 Installing rclone..."
    
    if command -v brew &> /dev/null; then
        brew install rclone
        echo "✅ rclone installed"
    else
        echo "❌ Homebrew not found. Please install rclone manually:"
        echo "   Visit: https://rclone.org/downloads/"
        exit 1
    fi
fi

# Check if rclone is configured for Google Drive
if ! rclone listremotes | grep -q "gdrive:"; then
    echo "🔧 Setting up rclone for Google Drive..."
    echo "This will open a browser for authentication."
    
    rclone config create gdrive drive
    
    if [ $? -eq 0 ]; then
        echo "✅ rclone configured successfully"
    else
        echo "❌ rclone configuration failed"
        exit 1
    fi
fi

# Find the latest PowerPoint file
SLIDES_DIR="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
LATEST_FILE=$(ls -t "$SLIDES_DIR"/*.pptx 2>/dev/null | head -1)

if [ -z "$LATEST_FILE" ]; then
    echo "❌ No PowerPoint files found in $SLIDES_DIR"
    exit 1
fi

FILENAME=$(basename "$LATEST_FILE")
echo "📤 Uploading: $FILENAME"

# Create folder on Google Drive
rclone mkdir "gdrive:HKBU_LANG2077" 2>/dev/null

# Upload file
if rclone copy "$LATEST_FILE" "gdrive:HKBU_LANG2077/"; then
    echo "✅ Upload successful!"
    
    # Try to get shareable link
    LINK=$(rclone link "gdrive:HKBU_LANG2077/$FILENAME" 2>/dev/null)
    
    if [ -n "$LINK" ]; then
        echo "🔗 Shareable link: $LINK"
        
        # Copy link to clipboard (macOS)
        echo "$LINK" | pbcopy
        echo "📋 Link copied to clipboard!"
        
        # Open in browser
        read -p "🌐 Open in browser? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "$LINK"
        fi
    else
        echo "⚠️  Upload successful, but couldn't get shareable link"
        echo "📁 File location: Google Drive > HKBU_LANG2077 > $FILENAME"
    fi
    
    echo ""
    echo "🎉 Success! Your LANG 2077 slides are on Google Drive!"
    echo ""
    echo "📝 To convert to Google Slides:"
    echo "   1. Open the file in Google Drive"
    echo "   2. Right-click and select 'Open with > Google Slides'"
    echo "   3. File > Save as Google Slides"
    echo ""
    
else
    echo "❌ Upload failed"
    exit 1
fi
