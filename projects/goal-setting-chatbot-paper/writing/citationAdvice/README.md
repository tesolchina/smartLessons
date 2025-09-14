# Citation Enhancement - Streamlined Guide

## 📋 **MASTER_Citation_Guide.md** ⭐ **USE THIS FILE**

**Your single, focused resource for manuscript enhancement**

✅ **What it contains:**
- 12+ specific citation recommendations with exact manuscript text
- Before/After examples showing exactly what to change
- 3-phase priority system (70 total minutes, or 30 minutes minimum)
- Exact locations in your manuscript with search-friendly text
- NEW: Section Echo Map to connect Literature Review → Methods → Results → Discussion → Conclusion

✅ **How to use it:**
1. Open your Word manuscript + this guide side-by-side
2. Start with Priority 1 (3 critical citations - 30 minutes)
3. Use Ctrl+F to find the exact text mentioned in the guide
4. Copy the "After" examples directly into your manuscript

## 📁 Archive Folder
All previous analysis files have been moved to `/archive/` to reduce clutter. The Master Guide contains the most actionable recommendations from all previous analyses.

**Total Enhancement Time:** 30-70 minutes depending on completeness level

---

## 📜 Process & Iterations (based on your feedback)

1) Conversion and First RAG Pass
- Converted the original Word document to Markdown (`manuscript_0902.md`) for structured analysis.
- Ran RAG annotators to produce inline suggestions and a summary (`RAG_Annotated_Manuscript.md`, `RAG_Citation_Summary.md`).

2) Manuscript-Specific Guidance
- Created `Manuscript_Specific_Citation_Guide.md` with explicit insertion points tied to your text.
- Added a broader `Final_RAG_Citation_Guide.md` and plan documents for full coverage.

3) Your Feedback: “Too many files; make it concrete to the manuscript.”
- Action: Archived non-essential files to `/archive/` and kept a single actionable guide.
- Created `MASTER_Citation_Guide.md` with precise Before/After replacements that reference exact manuscript sentences.

4) Your Feedback: “Not enough citations; sections should echo one another.”
- Action: Added 12+ additional targeted citations across Intro, Literature Review, Methods, Results, and Discussion.
- Added a Section Echo Map (Lit Review → Methods → Results → Discussion → Conclusion) with copy‑paste sentences and anchor citations (e.g., TAM, SRL cycles, proximal goals, AI vs rule‑based).

5) Final Streamlining
- Kept only: `MASTER_Citation_Guide.md` and this `README.md` in the root.
- Moved all supporting artifacts (scripts, earlier guides, converted manuscript) to `/archive/` for traceability.

Date of latest update: 2025‑09‑13

---

## 📂 Current Structure

- `MASTER_Citation_Guide.md` — Single source of truth (12+ insertions + Echo Map)
- `README.md` — You are here
- `archive/` — Full history (converted manuscript, RAG outputs, earlier guides, scripts)

### Notable items in `archive/`
- `manuscript_0902.md` — Converted manuscript (source for anchors)
- `Enhanced_RAG_Implementation_Guide.md`, `RAG_Annotated_Manuscript.md`, `RAG_Citation_Summary.md` — First RAG pass artifacts
- `convert_docx_to_md.py`, `rag_citation_annotator.py`, `enhanced_rag_system.py` — Reproducibility scripts

---

## ✅ What changed vs. original draft

- Added foundational SRL anchors (Winne & Hadwin, 1998; Pintrich, 2000; Zimmerman, 2013; Panadero, 2017; Winne, 2022)
- Strengthened SMART section (Doran, 1981; Bjerke & Renger, 2017; Latham & Locke, 2007)
- Reinforced rule‑based limitations and AI advantages (Singh, 2019; Hew, 2021/2022/2025; Ng, 2024; Guan, 2024; Lai, 2024)
- Tied Methods timing to proximal‑goal literature (Schunk, 1990; Bandura & Schunk, 1981; Seijts & Latham, 2001)
- Linked outcomes to SRL and goal‑attainment findings (Kizilcec, 2017; Garavalia & Gredler, 2002)
- Added resource/personalization evidence (Wollny, 2021; Kuhail, 2022; Mohamad, 2021)
- Introduced a Section Echo Map to ensure claims recur coherently across sections

---

## ▶️ Next steps (fast path)

1. Open `MASTER_Citation_Guide.md` and apply Priority 1 (≈30 minutes)
2. Apply Priority 2 and the Echo Map sentences (≈30–40 minutes)
3. Verify all newly cited works appear in your References list
4. Optional: we can auto‑apply changes to the Markdown manuscript in `archive/` and provide a diff for review

---

Generated and maintained on 2025‑09‑13. History retained in `/archive/`.

---

## 🤖 Generate a v2 guide with Grok 4

You can send the relevant files (current guide + RAG outputs + manuscript + RAG literature) to Grok 4 and receive a refined guide.

What gets sent:
- `MASTER_Citation_Guide.md`
- `archive/RAG_Annotated_Manuscript.md`
- `archive/RAG_Citation_Summary.md`
- `archive/manuscript_0902.md`
 - Selected `.md` sources from `projects/ZoteroPDF/LitonGoalChatbot` (prioritized by filename keywords like goal, SRL, chatbot, SMART, TAM)

Files added for this workflow:
- `grok_client.py` — Minimal xAI API client (OpenAI-compatible endpoint).
- `context_builder.py` — Collects and trims the above files into a single prompt context.
- `generate_guide_with_grok.py` — Calls Grok and writes `MASTER_Citation_Guide_v2.md`.

Setup (macOS zsh — OpenRouter recommended):
1) Set your xAI API key and optional overrides:
```
# OpenRouter key (preferred)
export OPENROUTER_API_KEY="<your_openrouter_key>"
export OPENROUTER_API_BASE="https://openrouter.ai/api/v1"  # default
export GROK_MODEL="x-ai/grok-4"                             # default

# or direct xAI (not required if using OpenRouter)
# export XAI_API_KEY="<your_xai_key>"
# export XAI_API_BASE="https://api.x.ai/v1"
```

2) Run the generator from this folder:
```
python3 generate_guide_with_grok.py
```

Result:
- The script writes `MASTER_Citation_Guide_v2.md` with Grok's response and logs usage in `grok_last_call.json`.

Notes:
- The context is trimmed to reasonable character budgets to fit model limits.
- If any of the files are missing, they will simply be skipped.
 - The generator prints verbose logs: provider/base/model, key source, each context file and size, and response usage.

### Include extra RAG sources (optional)

By default, the generator adds up to 12 `.md` literature files from `projects/ZoteroPDF/LitonGoalChatbot` based on filename keywords. Tune with:
```
export RAG_SOURCES_DIR="/absolute/path/to/ZoteroPDF/LitonGoalChatbot"
export RAG_MAX_SOURCES="15"
export RAG_SOURCE_CHAR_LIMIT="10000"
export RAG_FILENAME_KEYWORDS="goal,SRL,chatbot,SMART,TAM,usefulness,ease,proximal,MOOC"
```

### About API key loading

The generator loads the key in this order:
1) `XAI_API_KEY` (environment variable)
2) `XAI_API_KEY_FILE` (path to a file that contains only the key)
3) `.env` files (first match wins):
	- `citationAdvice/.env` (local)
	- `DailyAssistant/tools/.env` and `DailyAssistant/tools/openrouter/.env` (shared), discovered relative to this folder
	- a custom path via `XAI_DOTENV_PATH`

An example is provided in `.env.example` (you can copy to `.env`). If no key is found, the script writes a helpful placeholder and exits gracefully.

### Secrets and git

- `.gitignore` excludes `.env` and `key.txt` in this folder.
- Prefer using `.env` or a key file path via env var; avoid committing secrets.