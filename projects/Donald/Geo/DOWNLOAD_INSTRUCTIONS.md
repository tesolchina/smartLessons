# Google Doc Download Instructions

## Original File Location:
https://docs.google.com/document/d/16iQJdg6hNmmlG6hLFRueRawOhI5l8JT2n8-ezXbtsSQ/edit

## Manual Download Steps:

1. **Open the Google Doc in browser:**
   - Click this link: https://docs.google.com/document/d/16iQJdg6hNmmlG6hLFRueRawOhI5l8JT2n8-ezXbtsSQ/edit
   - Make sure you're logged into the correct Google account

2. **Download as different formats:**
   
   ### Option 1: Download as Microsoft Word (.docx)
   - File → Download → Microsoft Word (.docx)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.docx`
   
   ### Option 2: Download as PDF
   - File → Download → PDF Document (.pdf)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.pdf`
   
   ### Option 3: Download as Plain Text
   - File → Download → Plain Text (.txt)
   - Save as: `Donald_Wong_IGCSE_Geo_Coursework.txt`

3. **Copy downloaded file to this folder:**
   ```
   /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo
   ```

## Automated Conversion:
After downloading, run this script again with the downloaded file to convert to markdown:
```bash
python process_google_doc.py --convert downloaded_file.docx
```

## Alternative: Use Google Drive Desktop
1. Install Google Drive Desktop app
2. Sync the folder containing the document
3. Access the file through the local Google Drive folder
