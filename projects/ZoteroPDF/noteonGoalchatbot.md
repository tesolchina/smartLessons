I'll have a set of md files of research literature - laa already clearned but not yet annoated I am going to create a folder and place them in a the folder then I've got a manuscript in word - should convert to md first and then we need to add more literature 
update the plan tohere on what to do 

---

# Updated Plan: Ingestion, Conversion, Annotation & Expansion

## 1. Folder Structure Strategy
Create (or confirm) these folders:
```
raw_incoming/            # Newly added raw markdown (not yet annotated)
raw_manuscripts/         # Original Word or other format sources (versioned)
converted_manuscripts/   # Markdown conversions of manuscripts (pre-annotation)
annotated_data/          # Output with YAML front matter (current pipeline)
index_artifacts/         # FAISS, embeddings, manifest files
logs/                    # Process + progress logs
```

## 2. Workflow Overview (Lifecycle)
1. Acquire new sources (MD or Word/PDF) → place in `raw_incoming/` or `raw_manuscripts/`
2. Convert non-MD (Word) to Markdown → store in `converted_manuscripts/`
3. Pre-clean (optional normalization) → move to `raw_incoming/`
4. Run annotation (resume-capable) → writes to parallel structure in `annotated_data/`
5. Incrementally update vector index (append mode) → artifacts in `index_artifacts/`
6. Run validation / spot-check
7. Rebuild or merge FAISS index if threshold reached (e.g., >200 new docs)

## 3. Immediate Actions (Today)
| Priority | Action | Owner | Tooling |
|----------|--------|-------|---------|
| High | Create new folder skeleton | You / script | manual mkdir or helper script |
| High | Move unannotated cleaned MDs → `raw_incoming/` | You | file ops |
| High | Place Word manuscript in `raw_manuscripts/` | You | drag/drop |
| High | Convert Word → Markdown (Pandoc) | You / script | pandoc |
| High | Run annotation with new `--resume` once implemented | Pipeline | annotate.py |
| Medium | Add processed manifest + resume logic | Me (next step) | code edit |
| Medium | Append new documents to FAISS index | Pipeline | index script |
| Low | Add quality audit script (random sample diff) | Me | new script |

## 4. Word Manuscript Conversion
Recommended using Pandoc:
```
pandoc "MyManuscript.docx" -t gfm -o converted_manuscripts/MyManuscript.md 
```
Then cleanup steps:
- Remove embedded references if already in Zotero export
- Normalize heading levels (#, ##, ###)
- Ensure paragraphs are separated by single blank line
- Remove page numbers / running headers
- Keep tables as markdown (Pandoc handles basic ones)

## 5. Pre-Annotation Normalization (Optional Script Later)
Target transforms:
- Strip excessive blank lines (>2)
- Unify bullet markers to '-'
- Convert smart quotes to straight quotes
- Ensure final newline

## 6. Enhanced Annotation Plan (Upcoming Code Changes)
Add to `scripts/annotate.py`:
- `--resume` flag: skip files already existing in `annotated_data/` with valid front matter
- Processed manifest: `logs/annotation_manifest.json` with per-file status {file, started_at, completed_at, success, confidence}
- Batch size option: `--batch-size` for periodic checkpoint flush
- Graceful interrupt handling (SIGINT) writing checkpoint
- Retry logic (up to 2 tries) for transient API failures

## 7. Index Update Strategy
Two modes:
- Fast append: Embed + add vectors for new docs only (default)
- Periodic rebuild: After fragmentation >20% or >200 new docs
Artifacts to track:
```
index_artifacts/
  faiss.index
  documents.json
  embeddings_model.pkl
  index_meta.json   # {version, doc_count, last_update, added_since_rebuild}
```

## 8. Quality Control
Spot-check every N=50 new annotations:
- Title sanity (length/clarity)
- Authors parsed correctly (<=10)
- Methodology classification consistent
- Key findings not hallucinated (compare raw file)
Maintain `logs/annotation_qc.md` with sampled validations.

## 9. Adding More Literature Sources
Sources accepted:
- Clean MD exports from Zotero
- DOCX (convert → MD)
- PDF (only if high-quality OCR, otherwise postpone)
Future extension:
- Auto-detect duplicates via normalized title + first author + year

## 10. Backlog / Future Enhancements
- Section-level semantic chunk annotation
- Citation extraction + graph
- Concept taxonomy mapping (embedding cluster labeling)
- Research gap heuristic report
- Streamlit UI for interactive ingestion + search

## 11. KPIs
- Coverage: (# annotated / total) → goal 100%
- Avg annotation time per file
- Confidence score distribution (want >0.7 median)
- QC discrepancy rate (<5%)

## 12. Next Dev Steps (My Side)
1. Implement resume + manifest in annotator
2. Add incremental index updater script (`scripts/update_index.py`)
3. Provide QC sampling script

---
(End of plan update)