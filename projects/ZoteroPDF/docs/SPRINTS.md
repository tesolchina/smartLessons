# RAG System Implementation Sprints

<!-- Dev Log entry added on 2025-09-13 -->

## Dev Log — 2025-09-13
- Fixed FAISS index loading by changing embeddings pickle format to a stable dict (avoids __main__ class refs)
- Rebuilt index (1975 docs); verified search result structure and metadata access
- Streamlit apps running:
  - Main RAG UI at :8501 (app.py)
  - Citation Review UI at :8502 (citation_app.py)
- Added citation review system (CLI + Streamlit) to analyze manuscript citations and suggest improvements
- Improved docs: project README and `CITATION_REVIEW_GUIDE.md` with usage examples
- Next up: hierarchical chunking, evaluation harness, and UI improvements for upload/paste handling

## Dev Log — 2025-09-13 (evening)
- Addressed Streamlit run-path issues; confirmed both apps launch with explicit paths
- Fixed embeddings pickle compatibility (use dict with vocabulary/idf_weights/doc_count)
- Rebuilt FAISS index and verified metadata structure access in RAG pipeline
- Added `projects/ZoteroPDF/CITATION_REVIEW_GUIDE.md` and updated `projects/ZoteroPDF/README.md`
- Known issue: citation_app upload/paste UX—add clearer state, success/error messages next session

## Overview

Building a RAG system for academic MD files processing using open-source tools.

## Sprint 1A: Environment Setup & Data Analysis

**Duration**: 30-60 minutes
**Status**: 🚀 Starting Now
**Goal**: Setup environment and understand our data structure

### Tasks:

- [X] Create project structure
- [ ] Setup Python environment
- [ ] Install dependencies
- [ ] Install Ollama + Llama3
- [ ] Run data analysis
- [ ] Document findings

### Commands to Execute:

```bash
# 1. Environment Setup
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install langchain faiss-cpu sentence-transformers ollama streamlit pyyaml python-frontmatter

# 3. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3

# 4. Create project structure
mkdir -p scripts annotated_data faiss_index logs
```

### Deliverables:

- Working Python environment
- Data analysis report
- Project structure ready

---

## Sprint 1B: LLM Annotation Pipeline

**Duration**: 2-3 hours
**Status**: ⏳ Pending
**Goal**: Implement automated metadata extraction

### Tasks:

- [ ] Create metadata schema
- [ ] Implement LLM annotation script
- [ ] Test on sample files (5 files)
- [ ] Validate metadata quality
- [ ] Create batch processing capability

### Scripts to Create:

- `scripts/metadata_schema.py`
- `scripts/annotate.py`
- `scripts/analyze_data.py`

### Success Criteria:

- 5 test files successfully annotated
- Metadata extraction >70% accuracy
- YAML front matter properly formatted

---

## Sprint 2: Vector Store & Indexing

**Duration**: 2-3 hours
**Status**: ⏳ Pending
**Goal**: Create searchable document index

### Tasks:

- [ ] Implement document loader with metadata
- [ ] Create FAISS vector store
- [ ] Test document chunking strategy
- [ ] Optimize embedding generation
- [ ] Create index management tools

### Scripts to Create:

- `scripts/index.py`
- `scripts/test_retrieval.py`

### Success Criteria:

- All annotated documents indexed
- Sub-second search response time
- Relevant document retrieval

---

## Sprint 3: Basic RAG Implementation

**Duration**: 2-3 hours
**Status**: ⏳ Pending
**Goal**: Implement query-response system

### Tasks:

- [ ] Create RAG query system
- [ ] Implement academic prompt templates
- [ ] Test with sample queries
- [ ] Add source attribution
- [ ] Optimize response quality

### Scripts to Create:

- `scripts/rag.py`
- `scripts/test_queries.py`

### Success Criteria:

- Working end-to-end RAG system
- Accurate source attribution
- Coherent academic responses

---

## Sprint 4: Streamlit Interface

**Duration**: 1-2 hours
**Status**: ⏳ Pending
**Goal**: Create user-friendly web interface

### Tasks:

- [ ] Create Streamlit app
- [ ] Add search filters (subject, methodology, year)
- [ ] Implement query interface
- [ ] Add document preview
- [ ] Deploy locally

### Files to Create:

- `app.py`
- `requirements.txt`

### Success Criteria:

- Functional web interface
- Advanced search capabilities
- Document preview functionality

---

## Sprint 5: Advanced Features (Optional)

**Duration**: 2-4 hours
**Status**: ⏳ Future
**Goal**: Enhanced capabilities

### Potential Tasks:

- [ ] Pinecone migration for scaling
- [ ] Advanced metadata filtering
- [ ] Citation network analysis
- [ ] Export capabilities
- [ ] Batch query processing

---

## Current Sprint Status

### Sprint 1A - ✅ COMPLETED

**Completed Tasks:**

- [X] Created project structure
- [X] Setup Python environment with LangChain
- [X] Created data analysis script
- [X] Analyzed 1,927 academic MD files (163MB total)

**Key Findings:**

- 55.7% have abstracts, 46.5% have keywords
- Large files (avg 89KB) → need hierarchical chunking
- Rich academic structure with methodology sections
- 2 batches: batch_001 (999 files), batch_002 (928 files)

**Time Completed:** September 11, 2025
**Duration:** 30 minutes

---

### Sprint 1B - ✅ COMPLETED

**Goal:** Implement LLM annotation pipeline for metadata extraction

**Completed Tasks:**

- [X] Used existing OpenRouter API setup (Claude 3 Haiku)
- [X] Created AcademicMetadata schema with Pydantic
- [X] Implemented annotation script with OpenRouter integration
- [X] Tested successfully on 3 sample files (100% success rate)
- [X] Extracted rich metadata: titles, authors, categories, methodologies, findings

**Key Achievements:**

- High-quality metadata extraction with 0.8 confidence scores
- Diverse document types detected: journal, book_chapter
- Academic content analysis: methodology, findings, tags
- YAML front matter integration for git-friendly storage

**Time Completed:** September 11, 2025
**Duration:** 1.5 hours

---

### Sprint 2 - ✅ COMPLETED

**Goal:** Create vector index and implement basic retrieval

**Completed Tasks:**

- [X] Installed FAISS for vector search
- [X] Created custom TF-IDF embedding system (lightweight & efficient)
- [X] Built document indexing pipeline with metadata integration
- [X] Created searchable FAISS index from 3 annotated documents
- [X] Implemented semantic search with relevance scoring
- [X] Built complete RAG system with OpenRouter integration
- [X] Successfully tested end-to-end RAG pipeline

**Key Achievements:**

- ✅ **Search functionality**: Finds relevant papers by query (e.g., "cooperative learning" → Johnson paper)
- ✅ **RAG pipeline**: Retrieves sources + generates scholarly answers via Claude 3 Haiku
- ✅ **Academic responses**: Proper citations, academic language, evidence-based answers
- ✅ **Metadata integration**: Uses titles, tags, authors, content for comprehensive search
- ✅ **Performance**: Fast indexing (361-dimensional vectors) and sub-second search

**Demo Results:**
Query: "What are the benefits of cooperative learning?"

- Retrieved: Johnson & Johnson (2013) paper (0.85 relevance)
- Generated: Comprehensive academic answer with 5 key benefits
- Citations: Proper author attribution and research evidence

**Time Completed:** September 11, 2025
**Duration:** 1.5 hours

---

## 🎯 CURRENT STATUS: CORE RAG SYSTEM COMPLETE!

### Sprint 3 - ✅ COMPLETED

**Goal:** Implement basic RAG (retrieval + generation) capability

**Completed Tasks:**

- [X] Implemented retrieval (semantic + metadata aware)
- [X] Added academic prompt templates
- [X] Integrated OpenRouter (Claude 3 Haiku) for generation
- [X] Implemented source attribution & citation formatting
- [X] Validated responses on representative academic queries

**Key Achievements:**

- End-to-end RAG pipeline operational (query → retrieve → generate → cite)
- Academic style responses with inline/source list citations
- Sub‑second retrieval; 2–3s total response with generation
- Robust metadata leverage (titles, authors, methodology, tags)

**Success Metrics Achieved:**

- 📊 100% annotation success rate (3/3 initial documents)
- 🔍 Accurate semantic search (relevance >0.80 on targeted queries)
- 🤖 Scholarly, citation-backed answers
- ⚡ Fast performance (sub‑second search; low-latency generation)

**Time Completed:** September 11, 2025
**Duration:** ~1 hour (overlapping with Sprint 2 consolidation)

---

## 🎯 CURRENT STATUS (September 12, 2025)

Core foundation (Sprints 1–3) is complete. Transitioning from prototype pipeline to user-facing & scale phase.

### Sprint 4: Streamlit Research UI (In Progress)

**Goal:** Provide an interactive interface for researchers to search, inspect sources, and iterate on queries.

**Planned Duration:** 2–3 hours
**Target Date:** September 12, 2025

**Tasks Progress:**

- [X] Create `app.py` Streamlit skeleton (layout + sidebar)
- [X] Implement query input + retrieval display (scores, metadata)
- [X] Add expandable document preview (truncated + full toggle)
- [X] Add citation block rendering with copy/download
- [X] Integrate generation response panel (sources shown)
- [X] Add basic configuration panel (model, top_k, min_score)
- [X] Logging of queries & latency stats to `logs/usage.log`

**Current Status:** Core functionality working (citation block + in-session caching implemented). Remaining: export answer to Markdown & optional retrieval result caching persistence.

**Success Criteria (unchanged):**

- Single-file Streamlit app runs locally with `streamlit run app.py`
- Query returns: ranked sources (title, authors, relevance score)
- Generated answer cites only displayed sources
- Document preview expandable without re-query
- Adjustable retrieval parameters reflected immediately

**Stretch (if time allows):**

- [ ] Simple caching of retrieval results
- [ ] Export answer + sources to markdown

==========current enquiry========

suppose I have about 40 papers as reference and one manuscript that cite these papers 

how can the current system be used to help the author to review how the 40 papers are cited and to improve 

we can connect to LLM to seek help 

==========please answer below======================

### Backlog for Subsequent Sprint 5 (Scale & Quality)

- Annotate remaining corpus (1,927 → full coverage)
- Improve chunking (hierarchical / section-aware)
- Evaluate alternative embeddings (sentence-transformers) vs TF‑IDF
- Add evaluation harness (precision@k, answer faithfulness)
- Consider vector store migration (Pinecone) if scale demands

---

### Updated Next Steps Summary

1. Implement Streamlit UI (Sprint 4)
2. Scale annotation + full indexing (early Sprint 5)
3. Introduce evaluation metrics & quality dashboard
4. Explore advanced features (citation graph, batch QA)

> Note: Original numbering shifted (previous "Sprint 3" in roadmap is now completed and documented above). Future sprints retain conceptual goals but are renumbered to reflect progress.

---

## 🧪 Testing Guidance

### When to Test

| Phase                            | Trigger                                       | Purpose                                      |
| -------------------------------- | --------------------------------------------- | -------------------------------------------- |
| After indexing (Sprint 2)        | `index.py --create` completes               | Verify index integrity & search quality      |
| Before RAG generation (Sprint 3) | Retrieval returns >=1 result for sample query | Ensure RAG won't fail due to empty context   |
| After any schema/metadata change | Modified front matter fields                  | Confirm search still leverages new fields    |
| Before UI deployment (Sprint 4)  | `streamlit run app.py` launches             | Validate imports, cache, and latency logging |
| Pre-scale (Sprint 5 start)       | >100 docs newly annotated                     | Measure retrieval latency & memory footprint |

### What to Test (Core Functions)

| Component          | File                       | Function / Behavior                                                | Test Method                                              |
| ------------------ | -------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- |
| Embedding build    | `scripts/index.py`       | `SimpleEmbedding.fit_transform` creates non-zero vectors         | Run small list of 3 strings, assert shape & variance     |
| Index load/search  | `scripts/index.py`       | `AcademicIndexer.load_index` + `search` returns ranked results | Search known keyword, check descending scores            |
| RAG formatting     | `scripts/rag.py`         | `AcademicRAG.format_sources` truncates & structures output       | Inspect returned string length & ordering                |
| RAG query pipeline | `scripts/rag.py`         | `AcademicRAG.query` returns answer + sources list                | Mock or real call; assert keys (`answer`,`sources`)  |
| OpenRouter client  | `openRouterAI/client.py` | `post_chat_completions` retry & error surface                    | Temporarily force bad model name; expect error message   |
| Streamlit caching  | `app.py`                 | Session cache reuses prior search                                  | Repeat identical query; confirm no additional index time |
| Citation formatter | `app.py`                 | `format_citations` handles missing authors/year                  | Pass minimal metadata doc; no exception & fallback text  |

### Lightweight Manual Test Script Examples

Run after (a) creating index, (b) adding documents, (c) modifying retrieval logic.

```bash
# 1. Create index (if not built)
python projects/ZoteroPDF/scripts/index.py --create \
	--annotated projects/ZoteroPDF/annotated_data \
	--index projects/ZoteroPDF/faiss_index

# 2. Quick retrieval sanity
python projects/ZoteroPDF/scripts/index.py --index projects/ZoteroPDF/faiss_index \
	--search "cooperative learning"

# 3. Single RAG query
python projects/ZoteroPDF/scripts/rag.py --index projects/ZoteroPDF/faiss_index \
	--query "What are benefits of cooperative learning?" --top-k 3

# 4. Launch UI
streamlit run projects/ZoteroPDF/app.py
```

### Suggested Automated Test Seeds (Future Sprint)

- Add `tests/test_index.py`: build tiny temp index from 2 synthetic docs; assert search returns doc with keyword.
- Add `tests/test_rag_format.py`: feed mock search results; assert formatted source contains all required fields.
- Add `tests/test_citations.py`: ensure citation block lines equal source count; edge-case missing metadata.

### Acceptance Gates Before Scaling (Sprint 5)

| Gate                  | Metric / Condition                             | Target                   |
| --------------------- | ---------------------------------------------- | ------------------------ |
| Retrieval latency     | k=5 search (warm cache)                        | < 0.15s                  |
| Generation latency    | Claude Haiku end-to-end                        | < 3.5s avg (3 trials)    |
| Empty query handling  | Blank or stopword query                        | Returns graceful message |
| Citation integrity    | Each listed source appears in sources expander | 100%                     |
| Deterministic ranking | Same query repeated                            | Score order identical    |

### Troubleshooting Quick Reference

| Symptom             | Likely Cause                   | Rapid Check                   | Fix                                        |
| ------------------- | ------------------------------ | ----------------------------- | ------------------------------------------ |
| No results returned | Index path mismatch            | List files in `faiss_index` | Re-run create with correct path            |
| Generation fails    | Missing `OPENROUTER_API_KEY` | `echo $OPENROUTER_API_KEY`  | Export key / load env file                 |
| Slow retrieval      | Large doc content window       | Log timing from `search`    | Trim `search_text` length / add chunking |
| Duplicate citations | Same doc retrieved twice       | Inspect `indices` array     | Filter duplicates before formatting        |
| Cache not used      | Session reset                  | Check Streamlit reruns        | Persist to disk or memoize externally      |

---

## 🔄 Testing Roadmap Integration

Short-term (Sprint 4): Manual functional tests + add citation & retrieval unit tests.
Medium-term (Sprint 5): Add evaluation harness computing precision@k and answer faithfulness sample set.
Long-term: Continuous regression dataset (fixed queries) tracked in versioned JSON for drift detection.

### ✅ Current Testable Functions (Implemented Now)

| Area                | File                       | Function / Element                | What It Verifies                         | Test Status                                    |
| ------------------- | -------------------------- | --------------------------------- | ---------------------------------------- | ---------------------------------------------- |
| Embeddings          | `scripts/index.py`       | `SimpleEmbedding.fit_transform` | Vocabulary build + non-zero vectors      | Implemented (`test_embeddings.py`)           |
| Indexing            | `scripts/index.py`       | `AcademicIndexer.create_index`  | Generates FAISS index + metadata files   | Covered via fixture                            |
| Index Load          | `scripts/index.py`       | `AcademicIndexer.load_index`    | Loads index & documents count matches    | Fixture assertion (implicit)                   |
| Search              | `scripts/index.py`       | `AcademicIndexer.search`        | Returns ordered results descending score | Implemented (`test_index.py`)                |
| No-Hit Handling     | `scripts/index.py`       | `AcademicIndexer.search`        | Empty list for unrelated query           | Implemented (`test_index.py`)                |
| RAG Formatting      | `scripts/rag.py`         | `AcademicRAG.format_sources`    | Source block contains titles & scores    | Implemented (`test_rag_format.py` via dummy) |
| Citation Formatting | `app.py`                 | `format_citations` logic        | Graceful fallback when metadata missing  | Implemented (`test_citations.py`)            |
| Session Caching     | `app.py`                 | (Session state cache)             | Deterministic reuse (manual)             | Manual (UI)                                    |
| OpenRouter Client   | `openRouterAI/client.py` | `post_chat_completions`         | Retry & error handling                   | Pending (needs mock)                           |

### 🎯 High-Value Next Test Targets

- `AcademicRAG.query` with mock LLM (inject a fake `post_chat_completions`).
- Edge cases: very short query, high `min_score`, `top_k` > doc count.
- Performance budget: timing assertion (<150ms retrieval for synthetic set).
- Citation deduplication (if same doc retrieved multiple times — future scenario).

### 🛠️ Suggested Enhancements for Upcoming Sprint

| Enhancement                    | Benefit                             | Effort |
| ------------------------------ | ----------------------------------- | ------ |
| Mock OpenRouter in unit tests  | Deterministic RAG answer tests      | Low    |
| Coverage threshold (e.g., 70%) | Prevent silent test erosion         | Low    |
| Add mypy type checking         | Earlier type regressions            | Medium |
| Regression query suite JSON    | Track retrieval relevance over time | Medium |
| Timing benchmark test          | Detect performance regressions      | Medium |

---

## 🗺️ Comprehensive Multi-Phase Roadmap

### Phase 0 (DONE) — Prototype Core

Components: Minimal annotation, indexing, retrieval, RAG generation.
Exit Criteria: Query → Answer with sources under 4s.

### Phase 1 (Current) — Research UI & Expanded Corpus

Focus: Streamlit UX, annotation scale-out, stability, logging.
Key Tasks:

- Complete export features (answers + sources to Markdown)
- Add persistent retrieval caching (disk layer)
- Batch annotate remaining ~1,924 docs (parallelizable)
- Add progress tracker (annotated vs total)

### Phase 2 — Quality & Evaluation

Goals: Measure, tune, and trust outputs.
Planned Activities:

- Implement evaluation harness (query set JSON + expected key sources)
- Metrics: precision@k, MRR, citation faithfulness
- Error analysis notebook (false positives / misses)
- Add semantic chunking (section-aware splitting)

### Phase 3 — Advanced Discovery & Enrichment

Goals: Rich scholarly navigation.
Features:

- Citation / co-occurrence graph (authors, tags)
- Topic clustering (e.g., LDA / BERTopic) for thematic maps
- Query expansion suggestions (related concepts, synonyms)
- Paper timeline visualization (publication_year trends)

### Phase 4 — Scaling & Performance

Goals: Robustness for thousands → tens of thousands of docs.
Direction:

- Incremental indexing (append-only + periodic rebuild)
- Optional remote vector store (Pinecone or Qdrant)
- Embedding upgrade evaluation (sentence-transformers baseline vs TF-IDF)
- Caching policy: warm top queries; eviction heuristics

### Phase 5 — Research Assistant Extensions

Goals: Move from retrieval to workflow aid.
Ideas:

- Structured comparative summaries (multi-paper synthesis templates)
- Gap detection (“what’s under-studied about X?”)
- Prompt library for pedagogical, methodological, theoretical queries
- Export to slide outline / academic note format

### Phase 6 — Reliability & Governance

Goals: Trust, reproducibility, maintainability.
Tasks:

- Model/version manifest per answer
- Hash-based provenance (doc content digest recorded with answer)
- Redaction / privacy filters if needed
- Drift monitoring (store periodic retrieval snapshots)

---

## 🎓 Identifying Papers Discussing Pedagogical Implications

### Objective

Enable targeted discovery of papers that explicitly discuss pedagogical implications (e.g., instructional strategies, classroom application, teaching outcomes).

### Signal Sources (Priority → Lower)

1. Metadata fields (tags, subject_area, methodology, findings)
2. Section headings in content ("Implications", "Pedagogical", "Instructional", "Teaching Practice")
3. Key phrase occurrences near conclusion sections
4. LLM-derived classification labels (binary: has_pedagogical_implications)
5. Contextual embeddings of implication paragraphs

### Extraction Strategy

| Step | Method                                                          | Output                        |
| ---- | --------------------------------------------------------------- | ----------------------------- |
| 1    | Regex scan for heading patterns (`^#+ .*implication             | instructional                 |
| 2    | Sliding window phrase scoring (TF-IDF or keyword count)         | Relevance score per doc       |
| 3    | LLM classification on top N candidate docs                      | Binary confidence + rationale |
| 4    | Store flag in front matter (`pedagogical_implications: true`) | Enriched metadata             |
| 5    | Build filtered index view (subset)                              | Fast targeted search          |

### Proposed Keywords / Phrases

Primary: pedagogical, instructional, teaching practice, classroom application, educational practice, learning intervention, curriculum design, instructional strategy, teaching implications.
Secondary (contextual cues): teacher training, learner engagement, classroom implementation, applied in classroom, educational outcome, practical guidance.

### Scoring Heuristic (Pre-LLM)

Score = (Heading Match * 3) + (Primary Keyword Hits * 2) + (Secondary Keyword Hits * 1).
Promote documents with conclusion-like markers ("implications", "conclusion", "recommendations") by +2.
Threshold (initial): 8+ → candidate for LLM confirmation.

### LLM Confirmation Prompt Sketch

"""
You are classifying whether an academic paper explicitly discusses pedagogical or instructional implications (practical teaching applications, strategies, or classroom recommendations).
Return JSON with: {"has_pedagogical_implications": bool, "confidence": 0-1, "evidence": [short quoted snippets]}.
Paper Excerpt:
{text_chunk}
"""

### Index Integration

- Add new metadata field: `pedagogical_implications: true|false`.
- During indexing, boost documents with this flag for queries containing teaching-related terms.
- Provide sidebar toggle: "Only pedagogical implication papers" in Streamlit.

### Retrieval Enhancement

Pseudo-code boost (if using simple re-rank step):

```
if doc.metadata.get('pedagogical_implications'):
	adjusted_score = base_score * 1.15
```

### UI Additions

- Filter checkbox
- Badge in results list (e.g., 🧑🏽‍🏫 Pedagogical) when flag true
- Tooltip showing evidence snippet(s)

### Evaluation Plan

| Metric                       | Definition                   | Target                 |
| ---------------------------- | ---------------------------- | ---------------------- |
| Precision (manual 50 sample) | True pedagogical / predicted | >0.85                  |
| Recall (same sample)         | Predicted / total true       | >0.75 (later optimize) |
| False Positive Review Time   | Avg minutes per 10           | <3                     |

### Phased Rollout

1. Heuristic scoring + manual spot check (10 docs)
2. Add LLM validation for top candidates
3. Backfill metadata for full corpus
4. Integrate flag in UI + retrieval boost
5. Measure precision/recall; tune thresholds

### Future Enhancements

- Multi-label pedagogy taxonomy (assessment, collaboration, motivation, differentiation)
- Implication summary auto-generation
- Cross-linking: implications ↔ methodologies ↔ outcomes

---

### 📝 How to Extend Tests Quickly

1. Create mock function: `def fake_post_chat(payload): return {"choices":[{"message":{"content":"Mock answer"}}]}`.
2. Monkeypatch in pytest: `monkeypatch.setattr('scripts.rag.post_chat_completions', fake_post_chat)`.
3. Assert answer contains expected stub and source count matches requested `top_k`.
