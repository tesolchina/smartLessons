# AI Chatbot for English Writing Enhancement - Project Intent and Implementation Plan

## Executive Summary

This document outlines the intent and implementation plan for an AI-powered writing assistant chatbot designed for Traditional Chinese Medicine (TCM) students at HKBU. The chatbot serves dual purposes: **training students in AI literacy** and **assessing their writing improvement capabilities** through AI-assisted essay revision.

## Project Background

### Target Audience
- **Primary Users**: Traditional Chinese Medicine (TCM) students without computer science background
- **Secondary Users**: Faculty members and writing instructors
- **Total Scale**: 800+ students across multiple classes and instructors

### Course Context
- Integration with existing English writing curriculum
- Part of AI literacy training initiative
- Combines writing assessment with AI interaction skills development

## Project Objectives

### 1. AI Literacy Development
Train students to effectively interact with AI tools by teaching:
- **Contextual Communication**: How to provide sufficient background information to AI
- **Strategic Planning**: Making informed decisions about revision priorities
- **One-Shot Prompting**: Using exemplary essays as reference points
- **Critical Evaluation**: Requesting explanations and justifications from AI
- **Human-AI Collaboration**: Maintaining human agency in the revision process

### 2. Writing Assessment Enhancement
- Provide structured writing improvement feedback
- Enable comparative analysis between original and revised drafts
- Generate comprehensive reports for instructor evaluation
- Support both training and assessment modes

### 3. Scalable Implementation
- Handle 800+ students across multiple instructors
- Automated report distribution system
- Efficient token usage optimization
- Seamless integration with existing course structure

## Core System Components

### 1. Dual-Mode Architecture

#### Training Mode
- **Purpose**: Educational experience with AI interaction
- **Features**:
  - Guided prompts and suggestions
  - Pre-loaded context and rubrics
  - Sample essay integration
  - No formal evaluation
  - BCC reports to instructor email only

#### Assessment Mode
- **Purpose**: Formal evaluation of student capabilities
- **Features**:
  - Independent student interaction with AI
  - No guided prompts or hints
  - Report generation with student identification
  - Distribution to assigned instructors
  - Evaluation against AI interaction rubrics

### 2. Technical Architecture

#### Frontend Interface
- **Writing Area**: Side-by-side original and revised draft comparison
- **Chat Interface**: Real-time AI conversation panel
- **Configuration Panel**: API key management and model selection
- **Report Generation**: Automated analysis and feedback compilation

#### Backend Systems
- **AI Integration**: GPT-4.1 model utilization (simplified from multi-model approach)
- **Session Management**: Persistent chat history and draft states
- **Email System**: Automated report distribution with instructor mapping
- **Data Handling**: JSON-based configuration and sample essay management

## Pedagogical Framework

### Learning Objectives for Students

1. **Contextual AI Communication**
   - Provide comprehensive background information
   - Explain assignment requirements and rubrics
   - Articulate personal learning objectives
   - Set clear expectations for AI interaction

2. **Strategic Essay Revision**
   - Analyze essay weaknesses systematically
   - Prioritize revision areas based on time constraints
   - Develop focused improvement plans
   - Make informed decisions about revision scope

3. **Exemplar-Based Learning**
   - Identify high-quality writing samples
   - Use exemplars as revision references
   - Apply comparative analysis techniques
   - Understand quality benchmarks

4. **Critical AI Evaluation**
   - Request detailed explanations for AI suggestions
   - Evaluate suggestions against rubric criteria
   - Challenge and verify AI recommendations
   - Maintain critical thinking throughout the process

5. **Collaborative Revision Process**
   - Implement AI suggestions through personal editing
   - Maintain authorial voice and agency
   - Balance AI assistance with independent judgment
   - Produce genuinely improved writing

### Assessment Criteria

#### In-depth AI Conversation (33% weight)
- Quality of context provision
- Depth of questioning and exploration
- Strategic approach to revision planning
- Effective use of follow-up queries

#### Critical Review of AI Suggestions (33% weight)
- Evaluation of AI recommendations
- Request for explanations and justifications
- Assessment against rubric criteria
- Independent judgment demonstration

#### Essay Improvement Quality (34% weight)
- Measurable improvement between drafts
- Alignment with rubric standards
- Integration of AI suggestions
- Overall writing enhancement

## Implementation Strategy

### Phase 1: UI/UX Development
- **Priority Items**:
  - Move API key input to top of interface
  - Simplify model selection (GPT-4.1 only)
  - Implement session caching
  - Optimize layout for desktop use
  - Enhance chat and editing area sizes

### Phase 2: Core Functionality
- **Draft Management**: Side-by-side comparison interface
- **Chat Integration**: Persistent conversation history
- **Report Generation**: Comprehensive analysis including chat history and draft comparison
- **Email System**: Training mode (BCC to instructor) and Assessment mode (CC to student, forward to assigned instructor)

### Phase 3: Content Integration
- **Sample Essay System**: JSON-based sample essay management
- **Prompt Engineering**: Separate configuration files for instructor modification
- **Rubric Integration**: Embedded assessment criteria
- **Instructor Resources**: Easy content modification system

### Phase 4: Scalability Features
- **Student-Instructor Mapping**: Database for 800+ students
- **Automated Distribution**: Email routing system
- **Token Optimization**: Backend model switching for different tasks
- **Performance Monitoring**: Usage tracking and optimization

## Technical Specifications

### Frontend Requirements
- **Platform**: Web-based application (desktop-optimized)
- **Framework**: Vue.js with responsive design
- **Interface Elements**:
  - Resizable dual-pane editor
  - Real-time chat interface
  - Configuration management panel
  - Report preview and generation

### Backend Requirements
- **AI Integration**: OpenAI GPT-4.1 API
- **Token Management**: Optimized usage with model switching
- **Session Persistence**: Chat history and draft state management
- **Email Service**: SMTP integration for automated reporting
- **Data Storage**: JSON-based configuration and sample management

### Security and Privacy
- **No server-side personal data storage**
- **Email-based data handling only**
- **Student ID mapping for instructor assignment**
- **Secure API key management**

## Success Metrics

### Student Engagement
- Quality of AI interactions based on established criteria
- Improvement in writing quality between drafts
- Demonstration of AI literacy skills
- Effective use of revision strategies

### System Performance
- Successful handling of 800+ concurrent users
- Efficient token usage within institutional limits
- Reliable report generation and distribution
- Minimal technical support requirements

### Educational Outcomes
- Measurable writing improvement
- Enhanced AI literacy skills
- Improved revision strategies
- Greater awareness of writing quality standards

## Timeline and Milestones

### Immediate (Current Week)
- UI/UX improvements implementation
- Basic functionality testing
- Sample essay integration

### Short-term (Next 2 Weeks)
- Core feature completion
- Instructor testing and feedback
- System optimization

### Medium-term (Month 1-2)
- Full system deployment
- Student training sessions
- Performance monitoring

### Long-term (Semester)
- Large-scale implementation
- Continuous improvement based on usage data
- Expansion to additional courses and departments

## Risk Management

### Technical Risks
- **Token Limitations**: Monitor usage and implement model switching
- **System Scalability**: Load testing and optimization
- **API Reliability**: Backup systems and error handling

### Educational Risks
- **Student Preparation**: Comprehensive training in AI interaction
- **Faculty Adoption**: Clear documentation and support
- **Assessment Validity**: Continuous rubric refinement

### Operational Risks
- **Email System Reliability**: Automated monitoring and backup procedures
- **Data Management**: Secure handling of student information
- **Technical Support**: Streamlined troubleshooting procedures

## Conclusion

This AI chatbot system represents a comprehensive approach to integrating AI literacy training with writing assessment. By focusing on both technical functionality and pedagogical effectiveness, the system aims to enhance student writing capabilities while developing essential AI interaction skills for the modern academic and professional environment.

The dual-mode architecture ensures both educational value and assessment validity, while the scalable design accommodates the large student population effectively. Success depends on careful implementation of both technical features and educational strategies, with continuous refinement based on user feedback and performance data.