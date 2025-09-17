# GCAP 3056 Project Info Gathering Setup

## ✅ Completed Tasks

### 1. Enhanced Google Docs Manager
- **Created:** `gcap3056_enhanced_manager.py` - Enhanced version with Google Drive folder operations
- **Features:** Document creation, folder discovery, local file sync
- **Capabilities:** Both read and write access to Google Docs and Drive

### 2. Local Info Gathering Files Created
All 5 projects now have local `info_gathering.md` files with structured templates:

1. **Projects and teams/energy_poverty/info_gathering.md**
   - Focus: Energy poverty and social equity in Hong Kong
   - Key questions about energy affordability impacts
   - Research framework for vulnerable populations

2. **Projects and teams/hko_chatbot/info_gathering.md**
   - Focus: Hong Kong Observatory chatbot development
   - User research and technical requirements
   - Public service innovation framework

3. **Projects and teams/chronic_disease_co_care/info_gathering.md**
   - Focus: Chronic disease co-care pilot scheme evaluation
   - Public-private healthcare coordination
   - Scalability and effectiveness assessment

4. **Projects and teams/anti_scamming_education/info_gathering.md**
   - Focus: Anti-scamming education and emergency alerts
   - Scam prevention and public education
   - Vulnerable population protection strategies

5. **Projects and teams/emergency_alert_system/info_gathering.md**
   - Focus: Emergency alert system enhancement
   - Public warning capabilities improvement
   - International best practices comparison

### 3. File Structure and Sync Preparation
Each file includes:
- **Sync metadata:** Google Doc ID placeholders for future linking
- **Structured content:** Research questions, information needs, potential arguments
- **Action items:** Specific tasks for information gathering
- **Source tracking:** Academic, government, and industry sources to investigate

## 🔄 Pending Tasks (OAuth Required)

### Google API Authentication
**Status:** OAuth authorization in progress
- Two terminal sessions are waiting for Google account authorization
- URLs provided for browser-based authentication
- Once complete, will enable full Google Docs/Drive access

### Next Steps After OAuth Completion

1. **Discover Project Folders**
   ```bash
   python gcap3056_enhanced_manager.py --discover-folders
   ```
   - Will find Google Drive folder IDs for each project
   - Maps existing Google Docs to their parent folders

2. **Create Google Docs**
   ```bash
   python gcap3056_enhanced_manager.py --create-info-gathering-docs
   ```
   - Creates "Info Gathering" Google Docs in each project folder
   - Syncs content from local markdown files
   - Provides collaboration-ready documents

3. **Update Local Files with Google Doc Links**
   - Replace "TBD" placeholders with actual Google Doc IDs
   - Enable bidirectional sync between local and Google

## 📋 Information Gathering Framework

Each project template includes:

### Research Questions
- **5 key questions** specific to each project topic
- Focus on policy implications and implementation challenges
- Designed to support argumentative research papers

### Information Needed
- **Quantitative data:** Statistics, performance metrics, financial data
- **Qualitative information:** Stakeholder perspectives, case studies
- **Policy analysis:** Current regulations, government positions

### Potential Arguments
- **4 argument frameworks** per project
- Policy, equity, efficiency, and innovation angles
- Foundation for research paper development

### Sources to Investigate
- Government agencies and departments
- Academic institutions and research
- Industry reports and best practices
- International comparisons

### Action Items
- Interview opportunities
- Survey possibilities
- Data collection strategies
- Comparative analysis tasks

## 🎯 Project-Specific Focus Areas

### Energy Poverty
- **Equity focus:** Social justice and vulnerable populations
- **Data needs:** Household energy costs, subsidized housing statistics
- **Policy angle:** Government assistance program effectiveness

### HKO Chatbot
- **Innovation focus:** Digital government transformation
- **User research:** Public accessibility and communication preferences
- **Technical analysis:** API capabilities and platform requirements

### Chronic Disease Co-care
- **Healthcare integration:** Public-private coordination
- **Performance metrics:** Patient outcomes and cost-effectiveness
- **Scaling challenges:** System-wide implementation barriers

### Anti-Scamming Education
- **Prevention focus:** Education vs. enforcement approaches
- **Vulnerability analysis:** Elderly and immigrant populations
- **Technology integration:** Real-time alert systems

### Emergency Alert System
- **Public safety:** Life-saving communication systems
- **Technology gaps:** Modern alerting capabilities
- **Inclusivity:** Equal access for all population groups

## 🔗 Integration with Existing Work

### Teacher's Notes Integration
The info gathering templates complement existing teacher's note summaries:
- Build upon insights from `teachers_notes_summary.md` files
- Extend analysis with structured research framework
- Connect oral feedback to systematic investigation

### Project Workflow
1. **Info Gathering Phase:** Use structured templates to collect information
2. **Analysis Phase:** Process findings using argument frameworks
3. **Writing Phase:** Transform research into argumentative papers
4. **Collaboration:** Share Google Docs for team input and feedback

## 📞 Next Actions Required

### Immediate (User Action)
1. **Complete OAuth authorization** for both running terminal sessions
2. **Authorize Google account** access to Docs and Drive APIs

### After Authorization
1. **Run folder discovery** to map project Google Drive folders
2. **Create Google Docs** for each project's info gathering
3. **Begin information collection** using the structured templates
4. **Update and maintain** both local and Google versions

This setup provides a comprehensive framework for systematic information gathering across all 5 GCAP 3056 projects, with seamless integration between local markdown files and collaborative Google Docs.
