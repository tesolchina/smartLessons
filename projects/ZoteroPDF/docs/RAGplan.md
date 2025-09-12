# RAG System Development Plan for Academic MD Files Processing
*Updated based on open-source best practices and LLM annotation capabilities*

## Project Overview
Building an efficient RAG system for processing Zotero-generated markdown files from MinER-u3, leveraging open-source tools and LLM-based automated annotation for enhanced metadata-driven retrieval.

## Technology Stack Selection
- **Vector Database**: FAISS (local development) → Pinecone (production scaling)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **LLM**: Ollama with Llama 3 (local, open-source)
- **Framework**: LangChain for orchestration
- **File Formats**: Markdown with YAML front matter, JSON for structured metadata
- **UI**: Streamlit for web interface

## Sprint 1: Foundation & Data Analysis (Week 1-2)
**Goal**: Establish infrastructure and analyze existing academic content

### Tasks:
- **Environment Setup**:
  ```bash
  python -m venv venv
  pip install langchain faiss-cpu sentence-transformers ollama streamlit pyyaml
  ollama pull llama3
  ```

- **Data Analysis**: 
  - Analyze structure of existing MD files in `/workspaces/ZoteroMDsMineru3/data/`
  - Document academic paper patterns (abstracts, citations, sections)
  - Identify metadata extraction opportunities from academic content

- **Project Structure**:
  ```
  /workspaces/ZoteroMDsMineru3/
  ├── data/                    # Original Zotero MD files
  ├── annotated_data/          # LLM-annotated files with metadata
  ├── faiss_index/            # Vector store
  ├── scripts/
  │   ├── annotate.py         # LLM annotation pipeline
  │   ├── index.py            # Document indexing
  │   └── rag.py              # RAG query system
  └── app.py                  # Streamlit interface
  ```

## Sprint 2: LLM-Based Annotation Pipeline (Week 3-4)
**Goal**: Implement automated metadata annotation using Ollama/Llama3

### Tasks:
- **Metadata Schema Design** for academic papers:
  ```yaml
  ---
  title: "Document title (max 10 words)"
  authors: ["Author 1", "Author 2"]
  category: "research|technical|review|policy"
  tags: ["AI", "machine learning", "education"]
  subject_area: "education|psychology|technology"
  methodology: "quantitative|qualitative|mixed|theoretical"
  publication_year: 2024
  citation_count: 0
  priority: "high|medium|low"
  language: "en"
  document_type: "journal|conference|report|thesis"
  ---
  ```

- **LLM Annotation Script**:
  ```python
  # annotate.py - Enhanced for academic content
  from langchain.document_loaders import DirectoryLoader, TextLoader
  from langchain.llms import Ollama
  from langchain.prompts import PromptTemplate
  
  # Academic-specific prompt template
  prompt_template = """
  Analyze this academic document and extract metadata:
  - Title: Concise academic title (max 10 words)
  - Authors: List of author names if mentioned
  - Category: research|technical|review|policy
  - Subject_area: Primary academic discipline
  - Methodology: research approach if applicable
  - Tags: 5 relevant academic keywords
  - Document_type: journal|conference|report|thesis
  
  Document: {document}
  
  Output as valid JSON only.
  """
  ```

- **Validation & Error Handling**:
  - JSON parsing validation
  - Fallback metadata for parsing failures
  - Batch processing with progress tracking

## Sprint 3: Enhanced Document Processing (Week 5-6)
**Goal**: Optimize for academic content structure and implement vector storage

### Tasks:
- **Academic-Aware Text Splitting**:
  - Respect section boundaries (Abstract, Introduction, Methods, etc.)
  - Preserve citation context
  - Handle academic formatting (tables, equations)

- **FAISS Implementation**:
  ```python
  # index.py - Process annotated academic documents
  from langchain.document_loaders import DirectoryLoader, TextLoader
  from langchain.text_splitter import RecursiveCharacterTextSplitter
  from langchain.vectorstores import FAISS
  from langchain.embeddings import HuggingFaceEmbeddings
  
  # Load annotated documents with metadata
  loader = DirectoryLoader('./annotated_data', glob="**/*.md", loader_cls=TextLoader)
  documents = loader.load()
  
  # Academic-aware chunking
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=200,
      separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
  )
  ```

- **Metadata Integration**:
  - Store academic metadata with embeddings
  - Enable filtering by subject area, methodology, publication year

## Sprint 4: RAG Implementation with Academic Focus (Week 7-8)
**Goal**: Build RAG system optimized for academic queries

### Tasks:
- **Academic Query Processing**:
  - Handle research questions, methodology queries
  - Support comparative analysis requests
  - Enable citation-based searches

- **Context Assembly for Academic Content**:
  ```python
  # Enhanced RAG with academic context
  prompt_template = """
  Use the following academic sources to answer the question.
  
  Context: {context}
  Metadata: {metadata}
  
  Question: {question}
  
  Provide a scholarly response with:
  1. Direct answer based on the sources
  2. Methodology considerations if relevant
  3. Source attribution
  
  Answer: """
  ```

- **Academic-Specific Features**:
  - Citation tracking and source attribution
  - Methodology-aware responses
  - Cross-reference capabilities between papers

## Sprint 5: Advanced Retrieval & Pinecone Migration (Week 9-10)
**Goal**: Scale with cloud infrastructure and advanced features

### Tasks:
- **Pinecone Migration**:
  ```python
  # Migrate to Pinecone for production scaling
  import pinecone
  from langchain.vectorstores import Pinecone
  
  pinecone.init(api_key="your-key", environment="your-env")
  
  # Create index with metadata filtering
  vector_store = Pinecone.from_documents(
      documents, 
      embeddings, 
      index_name="academic-rag-index"
  )
  
  # Query with academic filters
  results = vector_store.similarity_search(
      query, 
      k=5,
      filter={
          "subject_area": "education",
          "methodology": "quantitative",
          "publication_year": {"$gte": 2020}
      }
  )
  ```

- **Advanced Academic Features**:
  - Multi-hop reasoning for literature reviews
  - Author network analysis
  - Methodology comparison capabilities
  - Temporal analysis of research trends

## Sprint 6: Streamlit Interface & Production Setup (Week 11-12)
**Goal**: Deploy user-friendly interface with academic workflows

### Tasks:
- **Academic-Focused UI**:
  ```python
  # app.py - Academic research interface
  import streamlit as st
  
  st.title("Academic Literature RAG System")
  
  # Advanced search filters
  col1, col2, col3 = st.columns(3)
  with col1:
      subject_filter = st.selectbox("Subject Area", ["All", "education", "psychology", "technology"])
  with col2:
      method_filter = st.selectbox("Methodology", ["All", "quantitative", "qualitative", "mixed"])
  with col3:
      year_filter = st.slider("Publication Year", 2000, 2025, (2020, 2025))
  
  # Research query input
  query = st.text_area("Research Question:", placeholder="What are the latest findings on...")
  ```

- **Academic Workflows**:
  - Literature review assistance
  - Methodology comparison
  - Citation network exploration
  - Research gap identification

- **Production Deployment**:
  ```dockerfile
  FROM python:3.9-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD ["streamlit", "run", "app.py", "--server.port=8501"]
  ```

## Key Academic Enhancements

### Metadata Schema for Academic Papers:
- **Bibliographic**: title, authors, publication_year, journal
- **Content**: abstract, keywords, methodology, subject_area
- **Quality**: citation_count, impact_factor, peer_reviewed
- **Processing**: confidence_score, extraction_date

### Academic Query Types:
1. **Literature Review**: "What research exists on X methodology in Y field?"
2. **Methodology**: "What quantitative methods are used for Z?"
3. **Comparative**: "How do findings from A compare to B?"
4. **Temporal**: "How has research on X evolved since 2020?"
5. **Gap Analysis**: "What research gaps exist in Y area?"

### Integration Benefits:
- **FAISS → Pinecone**: Seamless scaling from local development to cloud production
- **LLM Annotation**: Automated, consistent metadata extraction
- **Academic Metadata**: Enables sophisticated filtering and contextualization
- **Markdown + YAML**: Git-friendly, version-controlled, human-readable

## Implementation Priority:
1. **Core RAG** (Sprints 1-4): Basic functionality with academic metadata
2. **Production Scaling** (Sprint 5): Pinecone migration and advanced features  
3. **User Interface** (Sprint 6): Streamlit deployment with academic workflows

This plan leverages the best practices from the Grok notes while focusing specifically on academic content processing and metadata-driven retrieval for