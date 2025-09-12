#!/usr/bin/env python3
"""Streamlit UI for Academic RAG System (Sprint 4)

Features (initial skeleton):
- Sidebar configuration for model & retrieval parameters
- Query input box
- Retrieval results with metadata chips
- Document preview expanders
- Optional generation panel (triggered after retrieval)
- Basic usage logging

Assumptions:
- Existing FAISS index in ./faiss_index
- Annotated documents already processed
- OpenRouter API environment variables configured (OPENROUTER_API_KEY)

To run:
  streamlit run app.py
"""
from __future__ import annotations
import os
from pathlib import Path
import json
import time
import logging
from typing import List, Dict, Any

import streamlit as st
from io import StringIO
import json

# Local imports
from scripts.index import AcademicIndexer, SimpleEmbedding  # Import SimpleEmbedding for pickle loading
from scripts.rag import AcademicRAG

# Constants
DEFAULT_INDEX_DIR = Path(__file__).parent / "faiss_index"
LOG_FILE = Path(__file__).parent / "logs" / "usage.log"
MANIFEST_PATH = Path(__file__).parent / "annotation_manifest.json"
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

def evict_old_cache(cache_dir: Path, max_files: int = 200):
    """Remove oldest cache files if count exceeds limit"""
    cache_files = list(cache_dir.glob("q_*.json"))
    if len(cache_files) <= max_files:
        return
    
    # Sort by modification time (oldest first)
    cache_files.sort(key=lambda f: f.stat().st_mtime)
    to_remove = cache_files[:len(cache_files) - max_files]
    
    for f in to_remove:
        try:
            f.unlink()
        except Exception:
            pass

LOG_FILE.parent.mkdir(exist_ok=True, parents=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("app")

@st.cache_resource(show_spinner=False)
def load_indexer(index_path: str | Path) -> AcademicIndexer:
    idx = AcademicIndexer()
    idx.load_index(Path(index_path))
    return idx

@st.cache_resource(show_spinner=False)
def load_rag(index_path: str | Path, model: str) -> AcademicRAG:
    return AcademicRAG(Path(index_path), model=model)

def format_citations(results: List[Dict[str, Any]], style: str = "simple") -> str:
    """Format citations from search/generation sources.

    style 'simple': Author(s) (Year). Title.
    Falls back gracefully if fields missing.
    """
    lines = []
    for r in results:
        meta = r["document"]["metadata"]
        authors = meta.get("authors") or []
        year = meta.get("publication_year") or meta.get("year") or "n.d."
        title = meta.get("title") or r.get("title") or r['filename']
        if authors:
            if len(authors) > 2:
                auth_str = f"{authors[0]} et al."
            else:
                auth_str = ", ".join(authors)
        else:
            auth_str = "Unknown"
        lines.append(f"{auth_str} ({year}). {title}.")
    return "\n".join(lines)

def build_citation_block(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "No sources to cite."
    return format_citations(results)

def log_event(event: str, payload: Dict[str, Any]):
    try:
        logging.info(json.dumps({"event": event, **payload}))
    except Exception:
        pass

# --- UI ---
st.set_page_config(page_title="Academic RAG Explorer", layout="wide")
st.title("📚 Academic RAG Explorer")
st.caption("Streamlit interface for exploring academic papers with retrieval & generation")

with st.sidebar:
    st.header("Configuration")
    index_dir = st.text_input("Index Directory", value=str(DEFAULT_INDEX_DIR))
    model = st.selectbox("Model", ["anthropic/claude-3-haiku", "google/gemini-flash-1.5", "openai/gpt-4o-mini"], index=0)
    top_k = st.slider("Top K Results", 1, 10, 5)
    min_score = st.slider("Min Score", 0.0, 1.0, 0.1, 0.05)
    show_generation = st.checkbox("Generate Answer", value=True)
    st.markdown("---")
    st.subheader("Corpus Progress")
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text())
            total = manifest.get("total_files", 0)
            annotated = manifest.get("annotated_files", 0)
            pct = (annotated / total * 100) if total else 0
            st.progress(min(int(pct), 100))
            st.caption(f"Annotated {annotated} / {total} ({pct:.1f}%)")
        except Exception as e:
            st.caption(f"Manifest load error: {e}")
    else:
        st.caption("Manifest not found. Run build_manifest.py")
    st.markdown("---")
    st.subheader("Filters")
    annotated_only = st.checkbox("Annotated only", value=False, help="Show only docs with annotation status != none")
    pedagogical_only = st.checkbox("Pedagogical only", value=False, help="Show only docs tagged as pedagogical implications")
    boost_pedagogical = st.slider("Pedagogical boost", 0.0, 2.0, 0.0, 0.1, help="Additive score boost for pedagogical docs (scaled by their pedagogical_score)")
    st.markdown("---")
    st.subheader("About")
    st.write("Uses lightweight TF-IDF + FAISS for retrieval. Generation via OpenRouter API.")

# Load index (lazy)
indexer = None
rag_system = None
index_error = None
if Path(index_dir).exists():
    try:
        indexer = load_indexer(index_dir)
        if show_generation:
            rag_system = load_rag(index_dir, model)
    except Exception as e:
        index_error = str(e)
else:
    index_error = f"Index directory not found: {index_dir}"

if index_error:
    st.error(index_error)
    st.stop()

# Query Section
st.subheader("🔍 Query")

# Query options
col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("Enter your research question or keywords", 
                         placeholder="e.g., cooperative learning benefits")

with col2:
    st.write("")  # Spacing
    filter_pedagogical = st.checkbox("🎓 Focus on pedagogical implications", 
                                   help="Only include papers with identified teaching applications")

col_run, col_clear = st.columns([1,1])
run_search = col_run.button("Search", type="primary")
if col_clear.button("Clear"):
    st.experimental_rerun()

if 'cache' not in st.session_state:
    st.session_state.cache = {}
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'results' not in st.session_state:
    st.session_state.results = []
if 'generation' not in st.session_state:
    st.session_state.generation = None

if run_search and query:
    cache_key = (query, top_k, round(min_score, 3), filter_pedagogical)
    disk_cache_file = CACHE_DIR / f"q_{abs(hash(cache_key))}.json"
    st.session_state.last_query = query
    if cache_key in st.session_state.cache:
        st.session_state.results = st.session_state.cache[cache_key]
        st.info("Loaded results from cache")
    elif disk_cache_file.exists():
        try:
            cached_payload = json.loads(disk_cache_file.read_text())
            st.session_state.results = cached_payload.get("results", [])
            st.session_state.cache[cache_key] = st.session_state.results
            st.info("Loaded results from disk cache")
        except Exception:
            pass
    else:
        if indexer is None:
            st.error("Indexer not loaded.")
        else:
            t0 = time.time()
            # Apply pedagogical filter if requested
            if filter_pedagogical:
                # Pre-filter with manifest data
                manifest_data = {}
                if MANIFEST_PATH.exists():
                    try:
                        manifest_data = json.loads(MANIFEST_PATH.read_text())
                    except Exception:
                        pass
                
                files_meta = manifest_data.get("files", {}) if isinstance(manifest_data, dict) else {}
                # Get more results initially to account for filtering
                fresh = indexer.search(query, k=top_k*3, min_score=min_score)
                
                # Filter for pedagogical implications
                pedagogical_results = []
                for r in fresh:
                    file_path = r.get("document", {}).get("file_path")
                    meta = files_meta.get(file_path, {})
                    if meta.get("pedagogical_implications"):
                        pedagogical_results.append(r)
                
                # Take top k from filtered results, or fall back to all if insufficient
                if len(pedagogical_results) >= 2:
                    fresh = pedagogical_results[:top_k]
                else:
                    fresh = fresh[:top_k]
            else:
                fresh = indexer.search(query, k=top_k, min_score=min_score)
            
            dt = time.time() - t0
            st.session_state.results = fresh
            st.session_state.cache[cache_key] = fresh
            # Write disk cache
            try:
                evict_old_cache(CACHE_DIR)
                disk_cache_file.write_text(json.dumps({
                    "query": query,
                    "top_k": top_k,
                    "min_score": min_score,
                    "filter_pedagogical": filter_pedagogical,
                    "results": fresh,
                    "created_at": time.time()
                }))
            except Exception:
                pass
            log_event("search", {"query": query, "time": dt, "result_count": len(fresh)})
            st.write(f"Retrieved {len(fresh)} documents in {dt:.3f}s (cached for session)")

results: List[Dict[str, Any]] = st.session_state.results

# Optional filtering & boosting (applied after retrieval / cache load)
if results:
    manifest_data = {}
    if MANIFEST_PATH.exists():
        try:
            manifest_data = json.loads(MANIFEST_PATH.read_text())
        except Exception:
            manifest_data = {}
    files_meta = manifest_data.get("files", {}) if isinstance(manifest_data, dict) else {}

    if annotated_only or pedagogical_only or boost_pedagogical > 0:
        filtered = []
        for r in results:
            file_path = r.get("document", {}).get("file_path")
            meta = files_meta.get(file_path, {})
            # Filter logic
            if annotated_only and not meta.get("annotation_status"):
                continue
            if pedagogical_only and not meta.get("pedagogical_implications"):
                continue
            # Boosting
            adjusted = r["score"]
            if boost_pedagogical > 0 and meta.get("pedagogical_implications"):
                ped_score = meta.get("pedagogical_score", 0)
                norm = min(ped_score / 15.0, 1.0)
                adjusted += boost_pedagogical * norm
            r["adjusted_score"] = adjusted
            r["pedagogical"] = meta.get("pedagogical_implications")
            filtered.append(r)
        if filtered:
            # Re-rank by adjusted score
            filtered.sort(key=lambda x: x.get("adjusted_score", x["score"]), reverse=True)
            results = filtered
            st.session_state.results = results
            if boost_pedagogical > 0:
                st.info("Applied pedagogical boosting to ranking")

# Display Results
if results:
    st.subheader("📄 Retrieved Documents")
    for i, res in enumerate(results, 1):
        meta = res["document"]["metadata"]
        display_score = res.get("adjusted_score", res['score'])
        ped_flag = " 🟢 Pedagogical" if res.get("pedagogical") else ""
        with st.expander(f"{i}. {res['title']} (score={display_score:.3f}){ped_flag}"):
            authors = ", ".join(meta.get("authors", [])) or "Unknown authors"
            tags = meta.get("tags", [])
            st.markdown(f"**Authors:** {authors}")
            if tags:
                st.markdown("**Tags:** " + ", ".join(tags[:12]))
            st.caption(res['filename'])
            content = res["document"]["content"]
            st.markdown("---")
            st.markdown(content[:1500] + ("..." if len(content) > 1500 else ""))
            if len(content) > 1500:
                if st.button(f"Show Full Document {i}"):
                    st.markdown(content)

# Generation Panel
if show_generation and results and query:
    st.subheader("🧠 Generated Answer")
    gen_cols = st.columns([1,1,1,1])
    run_gen = gen_cols[0].button("Run RAG Answer")
    clear_gen = gen_cols[1].button("Clear Answer")
    copy_cite = gen_cols[2].button("Copy Citations")
    export_btn_placeholder = gen_cols[3]

    if clear_gen:
        st.session_state.generation = None

    if run_gen:
        cache_key = ("gen", query, top_k, model, filter_pedagogical)
        if cache_key in st.session_state.cache:
            st.session_state.generation = st.session_state.cache[cache_key]
            st.info("Loaded generation from cache")
        else:
            if rag_system is None:
                st.error("RAG system not initialized.")
            else:
                t0 = time.time()
                rag_res = rag_system.query(query, top_k=top_k, filter_pedagogical=filter_pedagogical)
                dt = time.time() - t0
                st.session_state.generation = rag_res
                st.session_state.cache[cache_key] = rag_res
                log_event("generation", {"query": query, "time": dt, "model": model, "sources": len(rag_res['sources']), "latency": dt, "pedagogical_filtered": filter_pedagogical})

    gen_data = st.session_state.generation
    if gen_data:
        st.markdown(gen_data["answer"])
        with st.expander("Sources Used"):
            for j, src in enumerate(gen_data["sources"], 1):
                st.markdown(f"**{j}. {src['title']}**  (score={src['score']:.3f})")
                st.caption(src['filename'])
        citation_block = build_citation_block(gen_data["sources"])
        st.markdown("**Citations (simple style):**")
        st.code(citation_block, language="text")
        if copy_cite:
            st.session_state.clipboard = citation_block  # Placeholder (Streamlit can't copy directly)
            st.success("Citations prepared for copy (select manually).")
        st.download_button("Download Citations", data=citation_block, file_name="citations.txt")
        # Export markdown (answer + sources) button
        export_md = ["# RAG Answer", "", gen_data["answer"], "", "## Sources", ""]
        for j, src in enumerate(gen_data["sources"], 1):
            export_md.append(f"{j}. {src['title']} (score={src['score']:.3f})")
        export_md.append("\n## Citations\n")
        export_md.append(citation_block)
        export_content = "\n".join(export_md)
        export_btn_placeholder.download_button("Export Markdown", data=export_content, file_name="rag_answer.md")

st.markdown("---")
st.caption("Sprint 4 initial UI - further enhancements (caching, export, parameter tuning) planned.")
