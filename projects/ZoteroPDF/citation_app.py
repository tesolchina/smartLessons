#!/usr/bin/env python3
"""
Streamlit interface for Citation Review System
Upload manuscript and get AI-powered citation analysis and improvement suggestions.
"""

import streamlit as st
import json
import tempfile
from pathlib import Path
import sys

# Add parent directories to path
sys.path.append(str(Path(__file__).parent))
from scripts.citation_reviewer import CitationReviewer

st.set_page_config(
    page_title="Citation Review Assistant", 
    layout="wide",
    page_icon="📝"
)

st.title("📝 Citation Review Assistant")
st.caption("AI-powered manuscript citation analysis and improvement suggestions")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # Index directory
    index_dir = st.text_input(
        "Reference Corpus Index", 
        value="faiss_index",
        help="Directory containing the FAISS index of your 40 reference papers"
    )
    
    # Model selection
    model = st.selectbox(
        "AI Model",
        ["anthropic/claude-3-haiku", "openai/gpt-4o-mini", "google/gemini-flash-1.5"],
        help="LLM model for citation analysis"
    )
    
    # Analysis options
    st.subheader("Analysis Options")
    analyze_full = st.checkbox("Full manuscript analysis", value=True)
    analyze_section = st.text_input("Specific section (optional)", placeholder="e.g., Literature Review")
    
    st.markdown("---")
    st.subheader("About")
    st.write("""
    This tool helps you:
    - Extract citations from your manuscript
    - Analyze citation appropriateness
    - Suggest improvements
    - Find missing references
    - Identify gaps in literature coverage
    """)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Manuscript")
    
    # File upload with better styling
    uploaded_file = st.file_uploader(
        "Choose your manuscript file",
        type=['md', 'txt', 'docx'],
        help="Upload your manuscript in Markdown, plain text, or Word format",
        accept_multiple_files=False
    )
    
    st.markdown("**OR**")
    
    # Text area for pasting content
    manuscript_text = st.text_area(
        "Paste manuscript text:",
        height=300,
        placeholder="Paste your manuscript text here...\n\nExample:\n# Introduction\nGoal setting has been shown to improve student learning (Smith et al., 2022).\nRecent studies suggest...",
        help="You can paste your manuscript content directly here"
    )
    
    # Show character count for pasted text
    if manuscript_text.strip():
        char_count = len(manuscript_text)
        word_count = len(manuscript_text.split())
        st.caption(f"📊 {char_count:,} characters, ~{word_count:,} words")

with col2:
    st.subheader("⚙️ Analysis Controls")
    
    # Show current status
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        content_available = True
    elif manuscript_text.strip():
        st.success(f"✅ Text pasted: {len(manuscript_text)} characters")
        content_available = True
    else:
        st.info("📝 Upload a file or paste text to begin analysis")
        content_available = False
    
    if content_available:
        st.markdown("**Analysis Options:**")
        
        # Create button with better styling
        analyze_button = st.button(
            "🔍 Analyze Citations", 
            type="primary",
            use_container_width=True,
            help="Click to start citation analysis"
        )
        
        if analyze_button:
            try:
                # Validate content
                if uploaded_file:
                    content = uploaded_file.read().decode('utf-8')
                    st.info(f"📖 Processing uploaded file: {uploaded_file.name}")
                else:
                    content = manuscript_text
                    st.info("📖 Processing pasted text")
                
                if not content.strip():
                    st.error("❌ No content found. Please upload a file or paste text.")
                    st.stop()
                
                # Check index directory
                if not Path(index_dir).exists():
                    st.error(f"❌ Index directory not found: {index_dir}")
                    st.error("Please ensure the FAISS index has been created.")
                    st.stop()
                
                # Initialize reviewer with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔄 Initializing citation reviewer...")
                progress_bar.progress(20)
                
                reviewer = CitationReviewer(Path(index_dir), model)
                
                status_text.text("🔍 Extracting citations...")
                progress_bar.progress(40)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
                    tmp.write(content)
                    tmp_path = Path(tmp.name)
                
                progress_bar.progress(60)
                
                # Perform analysis
                if analyze_section.strip() and not analyze_full:
                    # Section-specific analysis
                    status_text.text(f"🎯 Analyzing section: {analyze_section}")
                    progress_bar.progress(80)
                    results = reviewer.generate_section_suggestions(content, analyze_section)
                    
                    st.session_state['analysis_results'] = results
                    st.session_state['analysis_type'] = 'section'
                    
                else:
                    # Full manuscript analysis  
                    status_text.text("📝 Performing full citation analysis...")
                    progress_bar.progress(80)
                    results = reviewer.review_manuscript(tmp_path)
                    
                    st.session_state['analysis_results'] = results
                    st.session_state['analysis_type'] = 'full'
                
                # Complete analysis
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Clean up temporary file
                tmp_path.unlink()
                
                # Clear progress indicators after a moment
                import time
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                st.success("🎉 Citation analysis completed successfully!")
                st.rerun()  # Refresh to show results
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)  # Show full traceback in expander
    else:
        st.info("Upload a file or paste text to begin analysis")

# Display results
if 'analysis_results' in st.session_state:
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    results = st.session_state['analysis_results']
    analysis_type = st.session_state['analysis_type']
    
    if analysis_type == 'section':
        # Section analysis results
        if 'error' in results:
            st.error(results['error'])
        else:
            st.subheader(f"Section: {results['section']}")
            
            st.markdown("### 💡 Suggestions")
            st.markdown(results['suggestions'])
            
            if 'relevant_papers' in results:
                st.markdown("### 📚 Relevant Papers")
                for paper in results['relevant_papers']:
                    with st.expander(f"{paper['title']} (Score: {paper['score']:.3f})"):
                        st.write(f"**Authors:** {', '.join(paper.get('authors', []))}")
                        st.write(f"**Content preview:** {paper['document']['content'][:300]}...")
    
    else:
        # Full manuscript analysis results
        tab1, tab2, tab3 = st.tabs(["📋 Overview", "🔍 Citation Analysis", "📝 Download Report"])
        
        with tab1:
            # Overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Citations", results['total_citations'])
            
            with col2:
                inappropriate = len([ca for ca in results['citation_analyses'] 
                                   if ca.get('appropriateness') == 'inappropriate'])
                st.metric("Inappropriate Citations", inappropriate)
            
            with col3:
                partial = len([ca for ca in results['citation_analyses'] 
                              if ca.get('appropriateness') == 'partially_appropriate'])
                st.metric("Needs Improvement", partial)
            
            st.markdown("### 🎯 Overall Assessment")
            st.markdown(results['overall_suggestions'])
        
        with tab2:
            # Individual citation analysis
            st.subheader("Individual Citation Analysis")
            
            for i, analysis in enumerate(results['citation_analyses']):
                citation = analysis['citation']
                
                # Status indicator
                status = analysis.get('appropriateness', 'unknown')
                if status == 'appropriate':
                    status_icon = "✅"
                elif status == 'partially_appropriate':
                    status_icon = "⚠️"
                elif status == 'inappropriate':
                    status_icon = "❌"
                else:
                    status_icon = "❓"
                
                with st.expander(f"{status_icon} Citation {i+1}: {citation['citation']}"):
                    # Context
                    st.markdown("**Context:**")
                    st.code(f"...{citation['context']}...")
                    
                    # Analysis
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**Assessment:**")
                        st.write(f"Status: {status}")
                        st.write(f"Reason: {analysis.get('appropriateness_reason', 'No reason provided')}")
                        
                        if analysis.get('missing_aspects'):
                            st.markdown("**Missing Aspects:**")
                            for aspect in analysis['missing_aspects']:
                                st.write(f"• {aspect}")
                    
                    with col2:
                        st.markdown("**Suggestions:**")
                        st.write(analysis.get('suggested_improvements', 'No suggestions'))
                        
                        if analysis.get('additional_citations'):
                            st.markdown("**Additional Citations:**")
                            for citation_suggestion in analysis['additional_citations']:
                                st.write(f"• {citation_suggestion}")
                    
                    # Related papers
                    if analysis.get('related_papers'):
                        st.markdown("**Related Papers from Corpus:**")
                        for paper in analysis['related_papers'][:3]:
                            st.write(f"• {paper['title']} (Score: {paper['score']:.3f})")
        
        with tab3:
            # Download report
            st.subheader("📝 Download Analysis Report")
            
            # Generate markdown report
            report = f"""# Citation Review Report

**Total Citations**: {results['total_citations']}
**Analysis Date**: {st.session_state.get('analysis_date', 'Unknown')}

## Overall Assessment

{results['overall_suggestions']}

## Individual Citation Analysis

"""
            
            for i, analysis in enumerate(results['citation_analyses'], 1):
                citation = analysis['citation']
                report += f"""### Citation {i}: {citation['citation']}

**Context**: ...{citation['context']}...
**Status**: {analysis.get('appropriateness', 'Unknown')}
**Reason**: {analysis.get('appropriateness_reason', 'No reason provided')}

**Suggested Improvements**:
{analysis.get('suggested_improvements', 'No suggestions')}

**Additional Citations**:
{chr(10).join([f"- {paper}" for paper in analysis.get('additional_citations', [])])}

---

"""
            
            st.download_button(
                label="📥 Download Full Report (Markdown)",
                data=report,
                file_name="citation_review_report.md",
                mime="text/markdown"
            )
            
            # JSON download for further processing
            st.download_button(
                label="📥 Download Analysis Data (JSON)",
                data=json.dumps(results, indent=2, default=str),
                file_name="citation_analysis.json",
                mime="application/json"
            )

# Help section
with st.expander("❓ How to Use"):
    st.markdown("""
    ### Getting Started
    
    1. **Setup Reference Corpus**: Ensure your 40 reference papers are indexed in the FAISS index
    2. **Upload Manuscript**: Upload your manuscript file or paste the text
    3. **Choose Analysis Type**: 
       - Full analysis: Reviews all citations in the manuscript
       - Section analysis: Focuses on a specific section (e.g., "Literature Review")
    4. **Review Results**: Check the overview, individual citation analysis, and download reports
    
    ### What the Analysis Provides
    
    - **Citation Extraction**: Automatically finds citations in your text
    - **Appropriateness Assessment**: Evaluates if citations are used correctly
    - **Missing Aspects**: Identifies important points from papers that aren't mentioned
    - **Improvement Suggestions**: Specific recommendations for better citation usage
    - **Additional Citations**: Suggests other relevant papers from your corpus
    - **Gap Analysis**: Identifies areas needing stronger literature support
    
    ### Tips for Best Results
    
    - Ensure your reference corpus is properly indexed with rich metadata
    - Use clear section headings in your manuscript for section-specific analysis
    - Review the "Related Papers" suggestions to discover relevant connections
    - Use the pedagogical filter if your work focuses on teaching applications
    """)
