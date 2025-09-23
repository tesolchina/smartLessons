# How to Create Chatbot Pages for GCAP3226

**Last Updated**: September 23, 2025  
**Workflow**: Planning → Configuration → Deployment → HTML Creation → Live Testing

---

## 📋 Complete Workflow Overview

Creating a chatbot page involves a systematic process from conceptualization to live deployment. This guide documents the complete workflow used successfully for the GCAP3226 Reflective Essay Tutor.

## 🎯 Phase 1: Planning & Purpose Definition

### Step 1.1: Define Chatbot Purpose
Before creating any code, clearly define:
- **Educational Objective**: What learning outcome should the chatbot support?
- **Target Audience**: Which students and in what context?
- **Interaction Goal**: What should students achieve through the conversation?
- **Integration Point**: How does this fit into the course workflow?

**Example - Reflective Essay Tutor**:
```
Purpose: Help GCAP3226 students write 200-word reflective essays about team projects
Audience: Undergraduate students working on government data analysis projects
Goal: Guide students through structured reflection using mathematical models
Integration: Connects to Moodle forum submission and team project work
```

### Step 1.2: Design Interaction Patterns
Map out the conversation flow:
- **Entry Point**: How students start the conversation
- **Question Sequence**: What questions guide the reflection
- **Collaboration Style**: How the bot helps vs. directs
- **Exit Strategy**: How students complete and submit work

**Example Interaction Pattern**:
```
1. Welcome → Student types 'ok' to begin
2. Government decisions → What decisions is your team analyzing?
3. Data usage → How did government use data for those decisions?
4. Mathematical models → What models could improve decision-making?
5. Data governance → How could government improve data management?
6. Essay compilation → Help organize thoughts into 200-word essay
7. Submission reminder → Direct to Moodle forum posting
```

### Step 1.3: Define Workflow Integration
Specify how the chatbot connects to broader course systems:
- **LMS Integration**: Links to Moodle forums, assignments
- **Assessment Connection**: How chatbot supports grading rubrics
- **Team Coordination**: How individual work connects to team projects
- **Instructor Oversight**: What reports and monitoring are needed

---

## 🤖 Phase 2: Prompt Engineering & Configuration

### Step 2.1: Welcome Prompt Design
Create the first impression that sets expectations:

**Key Elements**:
- Friendly, encouraging tone
- Clear instructions for getting started
- Specific mention of task requirements (word count, topic)
- Connection to course context
- Next steps and submission guidance

**Template Structure**:
```
Greeting + Role Introduction
↓
Task Overview (word count, topic)
↓
Getting Started Instructions
↓
Submission Reminder with Links
```

### Step 2.2: System Prompt Development
Design the comprehensive instruction set that governs bot behavior:

**Core Components**:
1. **Background Context**: Course info, student situation
2. **Persona Definition**: Tone, teaching style, interaction approach
3. **Core Objectives**: Specific learning outcomes to support
4. **Guiding Framework**: Question sequences and methodologies
5. **Process Guidelines**: How to start, progress, and conclude

**Example System Prompt Structure**:
```markdown
# Background
[Course context and student situation]

# Persona & Role Definition
[Teaching style, tone, interaction approach]

# Core Objective
[Specific learning outcomes with measurable elements]

# Guiding Questions Framework
[Structured question sequences for different topics]

# Methodology
[How to ask questions, collaborate, support students]

# Starting Process
[Exact text and sequence for beginning conversations]

# Remember
[Key constraints, reminders, essential elements]
```

### Step 2.3: Report Generation Instructions
Define how the bot should assess and report on student interactions:

**Assessment Framework**:
- Rubric alignment (Content 70%, Presentation 30%)
- Specific criteria for each component
- Word count and formatting considerations
- Quality indicators for AI-assisted work

---

## ⚙️ Phase 3: Configuration & Deployment

### Step 3.1: Create JSON Configuration File
Compile all prompts and settings into the bot configuration format:

**File Structure**: `GCAP3226-[BotName].json`
```json
{
  "name": "Descriptive Bot Name for Course",
  "styleClass": "gradient-class",
  "model": "gpt-4.1",
  "welcomePrompt": "[Welcome message from Step 2.1]",
  "reportGenerationInstructions": "[Assessment framework from Step 2.3]",
  "systemPrompt": "[Complete system prompt from Step 2.2]",
  "bccEmail": ["instructor-email@institution.edu"],
  "ccEmail": ["backup-email@institution.edu"]
}
```

**Location**: `/03_instructor_tools/moodle_management/forum_posts/week##/`

### Step 3.2: GitHub Upload to Bot Configuration
1. **Repository**: https://github.com/Bob8259/new-bytewise-frontend
2. **Target Folder**: `/src/botConfig/`
3. **Process**:
   ```bash
   # Navigate to local repository
   cd /path/to/new-bytewise-frontend
   
   # Copy configuration file
   cp /path/to/GCAP3226-BotName.json src/botConfig/
   
   # Commit and push
   git add src/botConfig/GCAP3226-BotName.json
   git commit -m "Add GCAP3226 [BotName] configuration"
   git push origin main
   ```

### Step 3.3: Railway Deployment Approval
1. Access Railway GUI dashboard
2. Navigate to deployment pending section
3. Review the new bot configuration
4. Approve deployment
5. Monitor deployment logs for successful completion
6. Test bot availability via API endpoint

---

## 🌐 Phase 4: HTML Interface Creation

### Step 4.1: Design HTML Interface
Create the web interface that students will use to access the chatbot:

**Required Elements**:
- Course branding and context
- Clear instructions and expectations
- Integrated chatbot interface
- API key setup instructions for HKBU students
- Responsive design for mobile and desktop use

### Step 4.2: HTML File Structure
Based on successful `reflective-essay-tutor.html` template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags, title, Tailwind CSS -->
</head>
<body>
    <!-- Header with course info -->
    <!-- Two-tab interface: Instructions + Chatbot -->
    <!-- Tab 1: Instructions and rubrics -->
    <!-- Tab 2: Embedded chatbot interface -->
    <!-- API key setup section -->
    <!-- Footer with links and support -->
</body>
</html>
```

**Key Features**:
- **Two-tab design**: Instructions tab + Chatbot tab
- **HKBU API integration**: Instructions for students to get API keys
- **Responsive layout**: Works on mobile and desktop
- **Clear navigation**: Easy switching between instruction and chat
- **Assignment context**: Rubrics, deadlines, submission links

### Step 4.3: Chatbot Integration
Embed the chatbot interface using the deployment endpoint:
```html
<iframe 
    src="https://bot-endpoint.railway.app/chat/[bot-id]" 
    width="100%" 
    height="800px"
    frameborder="0">
</iframe>
```

### Step 4.4: Local Development and Testing
**File Location**: `/03_instructor_tools/chatbots4students/smartLessons/GCAP3226/[bot-name].html`

**Testing Process**:
1. Create HTML file locally
2. Test in browser for layout and functionality
3. Verify chatbot integration works
4. Check responsive design on different screen sizes
5. Validate all links and instructions

---

## 🚀 Phase 5: Live Deployment

### Step 5.1: Upload to smartLessons Repository
1. **Repository**: https://github.com/tesolchina/smartLessons
2. **Target Folder**: `/GCAP3226/`
3. **Process**:
   ```bash
   # Navigate to smartLessons repository
   cd /path/to/smartLessons
   
   # Copy HTML file
   cp /path/to/bot-interface.html GCAP3226/
   
   # Commit and push
   git add GCAP3226/bot-interface.html
   git commit -m "Add [BotName] interface for GCAP3226"
   git push origin main
   ```

### Step 5.2: Verify Live Deployment
**Live URL Pattern**: `https://smartlessons.hkbu.tech/GCAP3226/[filename].html`

**Testing Checklist**:
- [ ] Page loads correctly
- [ ] All tabs function properly
- [ ] Chatbot interface is accessible
- [ ] API key instructions work
- [ ] All links are functional
- [ ] Mobile responsiveness works
- [ ] Content displays properly

---

## 📊 Example Implementation: Reflective Essay Tutor

### Complete Implementation Reference
**Successfully deployed September 2025**

**Configuration File**: 
- Location: `/03_instructor_tools/moodle_management/forum_posts/week04/GCAP3226-reflectEssayTutor.json`
- Deployment: https://github.com/Bob8259/new-bytewise-frontend/tree/main/src/botConfig

**HTML Interface**: 
- Local: `/03_instructor_tools/chatbots4students/smartLessons/GCAP3226/reflective-essay-tutor.html`
- GitHub: https://github.com/tesolchina/smartLessons/blob/main/GCAP3226/reflective-essay-tutor.html

**Live URLs**:
- **Full Interface**: https://smartlessons.hkbu.tech/GCAP3226/reflective-essay-tutor.html
- **Direct Chat**: https://smartlessons.hkbu.tech/GCAP3226/reflective-essay-tutor.html#intro

**Key Features Implemented**:
- Two-tab interface (Instructions + AI Tutor)
- Simplified rubric display (70% Content, 30% Presentation)
- HKBU API key integration instructions
- 200-word essay guidance
- Moodle forum submission links
- Team project context integration

---

## 🔧 Technical Requirements

### Development Environment
- **HTML/CSS/JavaScript**: For interface creation
- **Git**: For version control and deployment
- **GitHub Access**: To both repositories (bytewise-frontend + smartLessons)
- **Railway Access**: For bot deployment approval
- **Text Editor**: For JSON and HTML editing

### API and Integration Points
- **HKBU GenAI API**: For student authentication
- **Railway Deployment**: For bot hosting
- **GitHub Pages**: For HTML interface hosting
- **Moodle Integration**: For assignment submission

### File Organization
```
GCAP3226/
├── 03_instructor_tools/
│   ├── chatbots4students/
│   │   ├── howtoCreateChatbotPages.md (this file)
│   │   └── smartLessons/GCAP3226/
│   │       └── [bot-name].html
│   └── moodle_management/forum_posts/week##/
│       └── GCAP3226-[BotName].json
└── GitHub Repositories:
    ├── tesolchina/smartLessons/GCAP3226/ (HTML interfaces)
    └── Bob8259/new-bytewise-frontend/src/botConfig/ (Bot configs)
```

---

## ⚠️ Best Practices & Troubleshooting

### Planning Phase Best Practices
- Start with clear learning objectives
- Map conversation flow before writing prompts
- Test question sequences with sample students
- Align with existing course rubrics and requirements

### Configuration Best Practices
- Use descriptive, consistent naming conventions
- Include specific word counts and requirements in prompts
- Test prompts with various student input types
- Include clear submission and next-step instructions

### Deployment Best Practices
- Test locally before uploading to GitHub
- Verify bot endpoint is working before HTML creation
- Use staging deployment for testing when possible
- Document all steps for future reference

### Common Issues and Solutions

**Issue**: Bot not responding in live interface
- **Check**: Railway deployment status
- **Verify**: Bot configuration file uploaded correctly
- **Test**: Direct API endpoint functionality

**Issue**: HTML interface layout problems
- **Check**: Tailwind CSS loading properly
- **Verify**: All tab switching JavaScript works
- **Test**: Responsive design on different devices

**Issue**: API key instructions not working
- **Check**: HKBU GenAI service availability
- **Verify**: Instructions match current HKBU interface
- **Update**: Links to current API documentation

---

## 📝 Documentation Templates

### Planning Template
```markdown
## Chatbot: [Name]
**Purpose**: [Learning objective]
**Audience**: [Student description]
**Context**: [Course integration]

### Interaction Flow:
1. [Step 1]: [Description]
2. [Step 2]: [Description]
...

### Success Criteria:
- [Criterion 1]
- [Criterion 2]
...
```

### Testing Checklist Template
```markdown
## Pre-Deployment Testing
- [ ] JSON configuration validated
- [ ] Prompts tested with sample inputs
- [ ] HTML interface displays correctly
- [ ] All links functional
- [ ] Responsive design verified
- [ ] Bot integration working

## Post-Deployment Testing
- [ ] Live URL accessible
- [ ] Chatbot responds correctly
- [ ] Report generation works
- [ ] Email notifications sent
- [ ] Student workflow complete
```

---

## 📞 Support and Resources

### Technical Support
- **smartLessons Repository**: https://github.com/tesolchina/smartLessons
- **Bot Configuration Repository**: https://github.com/Bob8259/new-bytewise-frontend
- **Railway Dashboard**: [Access through provided credentials]

### Documentation Files
- **This Guide**: `/03_instructor_tools/chatbots4students/howtoCreateChatbotPages.md`
- **smartLessons Update Guide**: `/03_instructor_tools/updateWebsiteMoodle/howtoUpdateSmartlessons.md`
- **Example Configuration**: `/03_instructor_tools/moodle_management/forum_posts/week04/GCAP3226-reflectEssayTutor.json`

### Live Examples
- **Reflective Essay Tutor**: https://smartlessons.hkbu.tech/GCAP3226/reflective-essay-tutor.html
- **Course Introduction**: https://smartlessons.hkbu.tech/GCAP3226/intro.html

---

**Next Implementation**: [Date] - [Chatbot Name]  
**Status**: Ready for new bot development following this workflow