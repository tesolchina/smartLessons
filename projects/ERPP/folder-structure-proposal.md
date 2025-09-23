# ERPP Project Folder Structure Proposal

## Current State Analysis
- **Root level**: General project files (context, plan, emails)
- **Students folder**: Individual student research projects
- **Ruobin's work**: Research plan on L2 poetry writing with LLMs

## Proposed Overall Structure

```
ERPP/
├── README.md                           # Project overview and navigation
├── context.md                          # Current context (existing)
├── plan.md                            # Strategic plan for AY 2025-26 (existing)
├── .venv/                             # Python environment (existing)
├── scripts/                           # Utility scripts
│   ├── convert_docx_to_md.py         # Document conversion tools
│   └── data_collection/               # Data gathering scripts
├── admin/                             # Administrative documents
│   ├── emails/                        # Email correspondence (existing)
│   ├── meetings/                      # Meeting notes and records
│   ├── budget/                        # Financial planning documents
│   └── reports/                       # Program reports and assessments
├── programme/                         # Core programme materials
│   ├── curriculum/                    # Course materials and syllabi
│   ├── workshops/                     # Workshop designs and materials
│   ├── gen-ai-integration/            # AI tools and guidelines
│   ├── website/                       # Web presence materials
│   └── promotional/                   # Marketing and outreach materials
├── research/                          # Research activities and publications
│   ├── historical-data/               # Programme data from 2017-2018 onwards
│   ├── current-analysis/              # Current challenges and assessment
│   ├── literature-review/             # Academic research compilation
│   └── publications/                  # Papers and research outputs
├── students/                          # Individual student projects (existing)
│   ├── current/                       # Active students
│   │   ├── Ruobin/                    # Individual student folders
│   │   └── [other-students]/
│   ├── alumni/                        # Graduated students' work
│   └── peer-tutors/                   # Peer tutor materials and training
├── technology/                        # Technical implementation
│   ├── chatbot/                       # LLM chatbot development
│   ├── platforms/                     # HKBU Bytewise and other platforms
│   ├── apis/                          # API configurations and logging
│   └── data-collection/               # Technical data gathering tools
└── resources/                         # Reference materials
    ├── templates/                     # Document and activity templates
    ├── guidelines/                    # Best practices and policies
    └── external/                      # External resources and links
```

## Detailed Breakdown for Ruobin's Research Project

Based on her research plan on "What Is the 'Temperature' of a Poem? Classroom Interactions in L2 Poetry Writing with LLMs as Co-creation Partners", here's a proposed structure:

```
students/current/Ruobin/
├── README.md                          # Project overview and timeline
├── notes.md                           # Working notes (existing)
├── Research_Plan_9_12.md             # Main research plan (existing)
├── 01-literature-review/              # Academic background research
│   ├── ddl-research/                  # Data-driven learning studies
│   ├── ai-creative-writing/           # AI in creative writing research
│   ├── l2-poetry/                     # L2 poetry pedagogy research
│   ├── parameter-studies/             # Temperature/top-p research
│   └── bibliography.md                # Comprehensive reference list
├── 02-research-design/                # Methodology and experimental design
│   ├── methodology.md                 # Research methods overview
│   ├── participants/                  # Participant recruitment and consent
│   ├── ethics/                        # IRB and ethics documentation
│   ├── validity-reliability/          # Measurement and validation
│   └── timeline/                      # Detailed project schedule
├── 03-chatbot-design/                 # AI system development
│   ├── prompt-engineering/            # Chatbot prompt designs
│   ├── parameter-testing/             # Temperature/top-p experiments
│   ├── ui-design/                     # User interface specifications
│   ├── logging-system/                # Data collection mechanisms
│   └── pilot-testing/                 # Pre-study validation
├── 04-data-collection/                # Experimental data
│   ├── pilot-study/                   # Initial testing results
│   ├── main-study/                    # Primary data collection
│   ├── transcripts/                   # Chat logs and recordings
│   ├── artifacts/                     # Student poems and revisions
│   └── surveys/                       # Participant feedback
├── 05-analysis/                       # Data analysis and results
│   ├── interaction-coding/            # Move type classification
│   ├── statistical-analysis/          # Quantitative results
│   ├── qualitative-analysis/          # Thematic analysis
│   ├── comparative-analysis/          # Parameter condition comparisons
│   └── findings/                      # Key results and insights
├── 06-outputs/                        # Research products
│   ├── papers/                        # Academic papers and drafts
│   ├── presentations/                 # Conference presentations
│   ├── tutorial-materials/            # Practitioner resources
│   └── open-resources/                # Shareable materials
└── 07-admin/                          # Project management
    ├── meetings/                      # Supervisor meeting notes
    ├── progress-reports/              # Regular updates
    ├── deadlines/                     # Important dates
    └── correspondence/                # Email and communication logs
```

## Rationale for This Structure

### Programme-Level Organization
1. **Separation of concerns**: Admin, programme delivery, research, and technology
2. **Scalability**: Can accommodate multiple students and research projects
3. **Collaboration**: Clear spaces for shared resources and individual work
4. **Historical continuity**: Proper archiving of programme evolution

### Research Project Organization
1. **Linear workflow**: Follows typical research progression
2. **Parallel tracks**: Literature review can proceed alongside design work
3. **Data integrity**: Clear separation of collection, analysis, and outputs
4. **Reproducibility**: Well-documented methodology and materials
5. **Collaboration**: Easy for supervisors and peers to navigate

### Benefits
- **Clear navigation**: Anyone can quickly find relevant materials
- **Version control**: Easy to track progress and changes
- **Backup and sharing**: Organized structure for cloud storage
- **Future expansion**: Room for additional students and research streams
- **Documentation**: Built-in organization for academic requirements

## Next Steps

1. **Validate structure** with supervisors and stakeholders
2. **Create folder hierarchy** systematically
3. **Migrate existing files** to appropriate locations
4. **Establish naming conventions** for consistency
5. **Set up templates** for common document types
6. **Create README files** for navigation guidance

Would you like me to proceed with creating this folder structure, or would you prefer to modify any aspects first?