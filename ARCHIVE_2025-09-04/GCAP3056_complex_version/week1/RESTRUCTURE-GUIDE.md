# Week 1 Restructured: Topic-Based Content with Markdown

## Overview
Week 1 content has been restructured into 4 topics, each with 3 activity types. Content is stored in editable markdown files and dynamically rendered in HTML.

## New Folder Structure

```
week1/
├── index.html                          # Original structure (maintained for compatibility)
├── index-topics.html                   # New topic-based structure
├── css/                                # Shared stylesheets
│   └── styles.css
├── js/                                 # JavaScript functionality
│   └── course-app.js
├── topics/                             # NEW: Topic-based organization
│   ├── template.html                   # Base template for content pages
│   ├── topic1-government-framework/    # Topic 1: Government & Accountability
│   │   ├── interactive-lecture.html    # HTML page that loads markdown
│   │   ├── practice-discussion.html    # HTML page that loads markdown
│   │   ├── reflect-assess.html         # HTML page that loads markdown
│   │   └── content/                    # Markdown content files
│   │       ├── interactive-lecture.md  # Editable content
│   │       ├── practice-discussion.md  # Editable content
│   │       └── reflect-assess.md       # Editable content
│   ├── topic2-transparency-access/     # Topic 2: Transparency & Information
│   │   └── content/                    # (To be created)
│   ├── topic3-public-participation/    # Topic 3: Public Participation
│   │   └── content/                    # (To be created)
│   └── topic4-advocacy-skills/         # Topic 4: Practical Skills
│       └── content/                    # (To be created)
├── interactive-lecture/                # OLD: Original structure (kept for reference)
├── practice-discussion/                # OLD: Original structure (kept for reference)
└── reflect-assess/                     # OLD: Original structure (kept for reference)
```

## Content Organization by Topic

### Topic 1: Government Framework & Accountability ✅ COMPLETE
**Learning Focus**: Understanding government as "necessary evil" and accountability mechanisms

**Content Files**:
- `interactive-lecture.md`: Government roles, social contract, democratic accountability
- `practice-discussion.md`: Scenario analysis, position writing, peer review activities
- `reflect-assess.md`: Self-assessment quiz, reflection questions, goal setting

### Topic 2: Transparency & Access to Information 🔄 PLANNED
**Learning Focus**: Information rights, transparency laws, and government openness

**Content to Include**:
- Access to Information laws in Hong Kong
- How to request government information
- Analyzing transparency reports
- Case studies of successful information requests

### Topic 3: Public Participation & Letters to Editor 🔄 PLANNED
**Learning Focus**: Engaging in public discourse and advocacy through media

**Content to Include**:
- Role of letters to editor in democracy
- Writing effective advocacy letters
- Understanding editorial guidelines
- Analyzing successful advocacy campaigns

### Topic 4: Practical Advocacy Skills 🔄 PLANNED
**Learning Focus**: Putting knowledge into practice with real advocacy strategies

**Content to Include**:
- Research and issue analysis methods
- Building coalitions and partnerships
- Meeting with officials and representatives
- Measuring advocacy impact

## Technical Implementation

### Markdown-to-HTML System
Each HTML page dynamically loads and renders its corresponding markdown file:

1. **Fetch**: JavaScript fetches the markdown file from the `content/` folder
2. **Parse**: Custom `parseMarkdown()` function converts markdown to styled HTML
3. **Render**: Content is inserted into the page with Tailwind CSS styling
4. **Progress**: Local storage tracks completion of each activity

### Benefits of This Structure

#### For Content Creators
- **Easy Editing**: Content is in simple markdown format
- **Version Control**: Markdown files can be tracked in git
- **Collaborative**: Multiple people can edit content simultaneously
- **Flexible**: Easy to add, remove, or reorganize content

#### For Students
- **Clear Navigation**: Topic-based organization matches learning progression
- **Progress Tracking**: Visual indicators show completion status
- **Consistent Experience**: Same interface across all content types
- **Offline Capable**: Content cached for better performance

#### For Developers
- **Maintainable**: Separation of content and presentation
- **Scalable**: Easy to add new topics or activities
- **Reusable**: Template system for consistent page structure
- **Modern**: Uses current web standards and best practices

## Testing the New Structure

### Access Points
1. **Original Structure**: `http://localhost:8081/GCAP3056/week1/index.html`
2. **New Topic Structure**: `http://localhost:8081/GCAP3056/week1/index-topics.html`

### Test Topic 1 Activities
- **Interactive Lecture**: `topics/topic1-government-framework/interactive-lecture.html`
- **Practice & Discussion**: `topics/topic1-government-framework/practice-discussion.html`
- **Reflect & Assess**: `topics/topic1-government-framework/reflect-assess.html`

## Migration Plan

### Phase 1: Complete Topic 1 ✅
- [x] Create folder structure
- [x] Write Topic 1 markdown content
- [x] Build HTML templates with markdown loading
- [x] Test all three activity types

### Phase 2: Expand to All Topics 🔄
- [ ] Create content for Topics 2-4
- [ ] Build topic overview navigation
- [ ] Implement progress tracking across topics

### Phase 3: Integration 🔄
- [ ] Update main course navigation
- [ ] Migrate existing content to new structure
- [ ] Remove old files after migration
- [ ] Update documentation and links

## Content Creation Guidelines

### Markdown Format Standards
- Use `#` for main titles, `##` for sections, `###` for subsections
- Use `**bold**` for emphasis, `*italic*` for subtle emphasis
- Use bullet points (`-`) for lists
- Include interactive elements as markdown with clear instructions
- Add assessment criteria and learning objectives

### Activity Type Guidelines

#### Interactive Lecture
- Include learning objectives
- Provide clear explanations with examples
- Add interactive questions or polls
- Include discussion points for engagement

#### Practice & Discussion
- Provide hands-on exercises
- Include peer collaboration activities
- Offer scenarios for analysis
- Give clear instructions for submissions

#### Reflect & Assess
- Include self-assessment questions
- Provide reflection prompts
- Set clear assessment criteria
- Include goal-setting activities

This restructured approach provides a more organized, maintainable, and scalable foundation for the course content while maintaining the dynamic, interactive learning experience.
