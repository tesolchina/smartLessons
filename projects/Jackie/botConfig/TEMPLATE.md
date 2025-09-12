# Bytewise Educational Chatbot Configuration Template

## Template Structure

Based on the actual Bytewise platform configurations, each bot should follow this JSON structure:

```json
{
  "name": "🎯 Bot Display Name",
  "styleClass": "from-color-500 to-color-500",
  "model": "gpt-4.1 | gpt-4.1-mini",
  "welcomePrompt": "Initial greeting message to users",
  "reportGenerationInstructions": "Instructions for generating session reports",
  "systemPrompt": "Comprehensive system prompt defining bot behavior and role",
  "teacherEmail": ["email1@hkbu.edu.hk", "email2@hkbu.edu.hk"]
}
```

## Required Fields

### Core Configuration
- **name**: Display name with emoji prefix (e.g., "🎯 Bot Name")
- **styleClass**: Tailwind gradient classes for UI styling (e.g., "from-blue-500 to-cyan-500")
- **model**: AI model to use ("gpt-4.1" or "gpt-4.1-mini")
- **welcomePrompt**: Initial message shown to users when they start a session
- **systemPrompt**: Complete behavioral instructions and role definition
- **reportGenerationInstructions**: How to generate session summary reports
- **teacherEmail**: Array of instructor email addresses for notifications

## System Prompt Patterns

### 1. Socratic Method Pattern (discussionPrep.json)
- **Role**: "You are a Socratic Inquirer"
- **Primary Directive**: Stay anchored to user's original topic
- **Behavior**: Only ask questions, never provide answers
- **Key Features**: Few-shot examples, tangent handling, answer refusal

### 2. Menu-Driven Interaction (ielts-writing.json, GCAPanalyst.json)
- **Critical Rule**: Menu interaction logic with numbered options
- **Protocol System**: Different modes for different tasks
- **Evidence-Based Feedback**: Include quoted snippets as evidence
- **Role Switching**: Adopt different expert roles per protocol

### 3. Assessment & Feedback Pattern (feedbackOnOutline.json)
- **Structured Assessment**: Clear evaluation criteria
- **Comparative Analysis**: Side-by-side outline comparison
- **Evidence Requirements**: Quote snippets for all feedback
- **Socratic Follow-up**: Questions to deepen understanding

### 4. Simple Assistant Pattern (fun.json, learning.json)
- **Minimal Configuration**: Basic role and welcome message
- **Straightforward Interaction**: No complex protocols
- **Clear Purpose**: Specific, focused functionality

## Advanced Features

### Menu Systems
```
**Menu Interaction Logic (CRITICAL RULE):**
1. When the user types 'menu', you MUST present the numbered options
2. After presenting menu, WAIT for user's choice
3. Map user input to corresponding protocol
4. Begin protocol immediately, do not revert to welcome
```

### Evidence-Based Feedback
```
**Evidence-Based Feedback RULE:**
- Include quoted snippets for all comments: "Snippet — [Section]: [text]"
- Quote only 1-2 most relevant lines
- State "No supporting snippet found" if point is missing
```

### Protocol System
Each numbered option should have:
- **Role**: Specific expert identity to adopt
- **Goal**: Clear objective for that interaction mode
- **Action**: Immediate next steps and question patterns

## Styling Guide

### Name Format
- Start with relevant emoji
- Use descriptive, professional titles
- Examples: "💡 Socratic Dialogue Partner", "✍️ IELTS Writing Tutor"

### Style Classes
- Use Tailwind gradient classes
- Common patterns:
  - `from-blue-500 to-cyan-500` (blue/cyan)
  - `from-green-500 to-teal-500` (green/teal)
  - `from-indigo-500 to-purple-600` (purple)
  - `from-amber-500 to-rose-500` (warm)

### Model Selection
- **gpt-4.1**: Complex interactions, advanced reasoning
- **gpt-4.1-mini**: Simpler tasks, faster responses

## Validation Checklist

- [ ] All required fields present (name, styleClass, model, welcomePrompt, systemPrompt, reportGenerationInstructions, teacherEmail)
- [ ] Name includes appropriate emoji and clear description
- [ ] styleClass uses valid Tailwind gradient classes
- [ ] Model selection appropriate for complexity level
- [ ] systemPrompt defines clear role and behavioral guidelines
- [ ] Menu system logic included if applicable
- [ ] Evidence-based feedback rules defined if applicable
- [ ] Protocol system clearly structured if applicable
- [ ] JSON syntax is valid
- [ ] Teacher emails are correct HKBU addresses

## Example Configurations

The repository contains these real examples:
- `discussionPrep.json` - Socratic dialogue partner
- `ielts-writing.json` - IELTS writing tutor with menu system
- `GCAPanalyst.json` - Social issues analyst with protocols
- `feedbackOnOutline.json` - Academic writing feedback
- `policy-discourse-analyst.json` - Policy analysis with evidence rules
- `fun.json` - Simple entertainment bot
- `learning.json` - Basic learning assistant

## Best Practices

### System Prompt Writing
1. **Start with clear role definition**: "You are a [specific role]"
2. **Include critical rules**: Use **bold** for emphasis on important behaviors
3. **Provide examples**: Use few-shot examples for complex interactions
4. **Define protocols**: Clear numbered options for menu systems
5. **Specify evidence requirements**: How to quote and reference user content

### Educational Design
1. **Socratic Method**: Ask questions rather than providing direct answers
2. **Academic Integrity**: Guide learning without doing work for students
3. **Evidence-Based**: Always reference specific parts of student work
4. **Structured Feedback**: Use clear criteria and systematic evaluation
5. **Adaptive Teaching**: Adjust to student level and needs

### Technical Considerations
1. **Model Selection**: Balance capability needs with response speed
2. **Menu Logic**: Clear state management for multi-mode interactions
3. **Error Handling**: Define behavior for unexpected inputs
4. **Session Management**: Consider how conversations flow and end
5. **Report Generation**: Meaningful summaries for educators

---
*Template based on Bytewise Frontend Bot Configurations*  
*Repository: Bob8259/new-bytewise-frontend/src/botConfig*  
*Last Updated: September 12, 2025*
