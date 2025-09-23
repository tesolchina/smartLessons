# How to Update smartLessons Website

**Last Updated**: September 23, 2025  
**Repository**: https://github.com/tesolchina/smartLessons  
**Live Site**: https://smartlessons.hkbu.tech/

---

## 📋 Overview

This guide explains how to upload and update content on the smartLessons website, which is hosted on GitHub Pages and accessible at `https://smartlessons.hkbu.tech/`.

## 🔧 Prerequisites

- Access to the `tesolchina/smartLessons` GitHub repository
- Git installed and configured on your local machine
- Local clone of the smartLessons repository

## 📁 Repository Structure

```
smartLessons/
├── GCAP3226/           # Course-specific folder
│   ├── intro.html
│   ├── reflective-essay-tutor.html
│   ├── simulationBus56.html    # ← New file added
│   └── week1/
├── GCAP3056/           # Other courses
├── LANG0036/
└── index.html          # Main site index
```

## 🚀 Step-by-Step Upload Process

### Step 1: Navigate to Local Repository
```bash
cd /path/to/smartLessons/repository
# Example:
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/03_instructor_tools/chatbots4students/smartLessons
```

### Step 2: Check Repository Status
```bash
git status
git remote -v
```
**Expected output:**
```
origin  https://github.com/tesolchina/smartLessons.git (fetch)
origin  https://github.com/tesolchina/smartLessons.git (push)
```

### Step 3: Add Your File to Appropriate Folder
```bash
# Copy file to the correct course folder
cp /path/to/your/file.html GCAP3226/

# Example:
cp /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/resources/simulationBus56.html GCAP3226/
```

### Step 4: Stage the Changes
```bash
git add GCAP3226/yourfile.html
# Example:
git add GCAP3226/simulationBus56.html
```

### Step 5: Commit the Changes
```bash
git commit -m "Descriptive commit message"
# Example:
git commit -m "Add Route 56 Bus Simulation Visualization for GCAP3226"
```

### Step 6: Push to GitHub
```bash
git push origin main
```

### Step 7: Verify Upload
- **GitHub**: Check https://github.com/tesolchina/smartLessons/tree/main/GCAP3226
- **Live Site**: Access https://smartlessons.hkbu.tech/GCAP3226/yourfile.html

---

## 📝 Example: Uploading simulationBus56.html

### Complete Process Used (September 23, 2025)

**Source File**: `/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/resources/simulationBus56.html`

**Commands Executed**:
```bash
# 1. Navigate to repository
cd /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/03_instructor_tools/chatbots4students/smartLessons

# 2. Check repository status
git remote -v
ls -la GCAP3226/

# 3. Copy file to GCAP3226 folder
cp /Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/resources/simulationBus56.html GCAP3226/

# 4. Add to git
git add GCAP3226/simulationBus56.html

# 5. Commit changes
git commit -m "Add Route 56 Bus Simulation Visualization for GCAP3226"

# 6. Push to GitHub
git push origin main
```

**Result**:
- **GitHub URL**: https://github.com/tesolchina/smartLessons/blob/main/GCAP3226/simulationBus56.html
- **Live URL**: https://smartlessons.hkbu.tech/GCAP3226/simulationBus56.html
- **Commit**: `a8e34b7` - 777 lines added, 7.30 KiB

---

## 🌐 URL Structure

### GitHub Repository URLs
- **Main Repository**: `https://github.com/tesolchina/smartLessons`
- **GCAP3226 Folder**: `https://github.com/tesolchina/smartLessons/tree/main/GCAP3226`
- **Specific File**: `https://github.com/tesolchina/smartLessons/blob/main/GCAP3226/filename.html`
- **Raw File**: `https://raw.githubusercontent.com/tesolchina/smartLessons/main/GCAP3226/filename.html`

### Live Website URLs
- **Main Site**: `https://smartlessons.hkbu.tech/`
- **GCAP3226 Content**: `https://smartlessons.hkbu.tech/GCAP3226/`
- **Specific File**: `https://smartlessons.hkbu.tech/GCAP3226/filename.html`

---

## 📂 Folder Organization

### Current GCAP3226 Contents
```
GCAP3226/
├── intro_temp.html                     # Template introduction
├── intro.html                          # Course introduction
├── reflective-essay-tutor.html         # AI tutor interface
├── simulationBus56.html                # Bus route simulation (NEW)
├── sample-student-conversation.md      # Example conversations
└── week1/                               # Week 1 materials
    ├── assignment.html
    ├── intro.html
    ├── lesson.html
    └── resources/
```

### Recommended File Naming
- Use descriptive names: `simulationBus56.html` instead of `sim.html`
- Include course context: `GCAP3226-assignment1.html`
- Use hyphens for spaces: `reflective-essay-tutor.html`
- Include version if needed: `intro-v2.html`

---

## ⚠️ Important Notes

### File Requirements
- **HTML files**: Must be complete, self-contained files
- **Dependencies**: Include all CSS/JS inline or use CDN links
- **Size**: Keep files reasonable (< 10MB recommended)
- **Encoding**: Use UTF-8 encoding

### GitHub Pages Considerations
- **Deployment Time**: Changes may take 1-10 minutes to appear live
- **Caching**: Browsers may cache files; use hard refresh (Ctrl+F5)
- **HTTPS**: All content is served over HTTPS automatically
- **Custom Domain**: Site uses `smartlessons.hkbu.tech` domain

### Best Practices
1. **Test Locally**: Verify HTML works before uploading
2. **Descriptive Commits**: Use clear commit messages
3. **Check Status**: Always run `git status` before committing
4. **Verify Live**: Test the live URL after pushing
5. **Documentation**: Update this guide when adding new processes

---

## 🔍 Troubleshooting

### Common Issues

**Issue**: File not appearing on live site
- **Solution**: Wait 5-10 minutes for GitHub Pages deployment
- **Check**: Verify file was committed and pushed successfully

**Issue**: Permission denied when pushing
- **Solution**: Ensure you have write access to the repository
- **Alternative**: Create a pull request if you don't have direct access

**Issue**: File shows but content is wrong
- **Solution**: Check browser cache, use hard refresh
- **Verify**: Compare GitHub file with local file

**Issue**: Repository not found
- **Solution**: Verify you're in the correct directory
- **Check**: Run `git remote -v` to confirm repository URL

### Verification Checklist
- [ ] File successfully added to local repository
- [ ] Changes committed with descriptive message
- [ ] Changes pushed to GitHub successfully
- [ ] File visible in GitHub repository
- [ ] File accessible on live website
- [ ] Content displays correctly in browser

---

## 📞 Support

For technical issues or questions about the smartLessons website:
- **Repository**: https://github.com/tesolchina/smartLessons
- **Documentation**: This file
- **Live Site**: https://smartlessons.hkbu.tech/

---

**Last Successful Upload**: September 23, 2025 - `simulationBus56.html`  
**Next Update**: [Date] - [Description]
