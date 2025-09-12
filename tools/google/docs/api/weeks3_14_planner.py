#!/usr/bin/env python3
"""
Weeks 3–14 Planner

Generates a week-by-week plan (Weeks 3–14) for GCAP 3226 using OpenRouter LLM
and can append the result to the Course Planning Google Doc.

Usage examples:
  1) Generate draft only (no Google Doc changes):
     python3 operating/GoogleDocsAPI/weeks3_14_planner.py --generate

  2) Generate draft and append to Google Doc:
     python3 operating/GoogleDocsAPI/weeks3_14_planner.py --generate --apply

Options allow overriding the planning Doc ID, model, and paths.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "projects/GCAP3226"

# Ensure we can import modules/openRouterAI
sys.path.insert(0, str(REPO_ROOT / "modules"))

try:
    from openRouterAI.client import post_chat_completions
    from openRouterAI.env import get_openrouter_api_key
    OPENROUTER_AVAILABLE = True
except Exception as e:  # pragma: no cover
    print(f"⚠️  OpenRouter module not available: {e}")
    OPENROUTER_AVAILABLE = False


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def build_prompt(syllabus_text: str) -> str:
    intro_note = (
        "There is a Course Hub HTML (intro.html) with weekly cards/timeline that will be adjusted. "
        "Please structure output so it can be easily ported into those week cards and a 3-hour class plan."
    )
    week3_assets = (
        "Week 3 local assets available: regression_models_template.ipynb and GCAP3226_week3.csv. "
        "Prefer an intro to regression lab using these."
    )

    instruction = f"""
You are the course planner for GCAP 3226: Empowering Citizens through Data — Participatory Policy Analysis for Hong Kong.

Goal: Produce a week-by-week plan for Weeks 3–14 that aligns with the course structure and assessment. The plan will be appended to the course planning Google Doc and later mirrored in a Course Hub UI (intro.html).

Context (from syllabus analysis):
---
{syllabus_text}
---

Additional constraints:
- {intro_note}
- {week3_assets}
- Cohort is mixed-experience; include optional stretch tasks; keep feasible.
- Favor Hong Kong datasets/examples where possible.

For each week (Week 3 to Week 14), output in clean Markdown with this structure and keep it concise (~8–12 lines per week, no code):

## Week N — Short title
- Learning goals: 2–4 bullets
- 3-hour in-class plan with timestamps (e.g., 0:00–0:15 check-in; 0:15–1:00 demo; 1:00–2:30 team work; 2:30–3:00 share-out)
- Milestones/deliverables (group + individual)
- Required materials/datasets/tools
- Homework/next steps
- Risks & mitigations: 1–2 bullets

Make sure Week 3 leverages the provided notebook and CSV for a regression lab. Align the later weeks with proposal → data collection → analysis → report → presentation phases.
"""
    return instruction


def call_llm(prompt: str, model: str = "openrouter/auto", max_tokens: int = 3500, temperature: float = 0.2) -> str:
    if not OPENROUTER_AVAILABLE:
        raise RuntimeError("OpenRouter client is not available.")
    if not get_openrouter_api_key():
        raise RuntimeError("Missing OPENROUTER_API_KEY. Configure .env or key.txt.")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    print("📡 Calling OpenRouter for Weeks 3–14 draft...", flush=True)
    resp = post_chat_completions(payload)
    content = resp.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError("Empty response from LLM")
    print("✅ Received response (preview below)\n")
    return content


def save_draft(md_text: str, output_dir: Path = PROJECT_ROOT) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "weeks3_14_draft.md"
    out_file.write_text(md_text, encoding="utf-8")
    print(f"💾 Saved draft to: {out_file}")
    return out_file


def get_last_end_index(document: Dict[str, Any]) -> int:
    """Return the endIndex of the last structural element in the doc body.
    This is the safest insertion point at document end.
    """
    body = document.get("body", {})
    content = body.get("content", [])
    if not content:
        # 1 is typically the first valid index to insert at start
        return 1
    last = content[-1]
    return int(last.get("endIndex", 1))


def append_to_google_doc(doc_id: str, md_text: str, section_key: str = "weeks3-14-plan") -> bool:
    """Append the markdown text to the end of the Google Doc with markers."""
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        print(f"❌ Google API libraries not available: {e}")
        return False

    # Import authenticate_google_apis from the same directory as this script
    try:
        import importlib
        import sys as _sys
        this_dir = Path(__file__).parent
        if str(this_dir) not in _sys.path:
            _sys.path.insert(0, str(this_dir))
        auth_setup = importlib.import_module('auth_setup')
        authenticate_google_apis = getattr(auth_setup, 'authenticate_google_apis')
    except Exception as e:
        print(f"❌ Could not import auth_setup.authenticate_google_apis: {e}")
        return False

    print("🧩 Authenticating Google APIs...")
    creds = authenticate_google_apis()
    if not creds:
        print("❌ Authentication failed")
        return False

    docs_service = build('docs', 'v1', credentials=creds)

    print(f"📖 Fetching target document: {doc_id}")
    try:
        document = docs_service.documents().get(documentId=doc_id).execute()
    except Exception as e:
        print(f"❌ Failed to fetch document: {e}")
        return False

    end_index = get_last_end_index(document)

    header = f"\n[LLM:START {section_key}]\n## Weeks 3–14 Plan (Draft)\n"
    footer = f"\n[LLM:END {section_key}]\n"
    insertion_text = header + md_text.strip() + footer

    print("✍️ Appending draft to Google Doc (end of document)...")
    try:
        requests = [{
            'insertText': {
                'location': {'index': max(1, end_index - 1)},
                'text': "\n" + insertion_text + "\n"
            }
        }]
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        print("✅ Successfully appended to Google Doc")
        print(f"🔗 https://docs.google.com/document/d/{doc_id}/edit")
        return True
    except Exception as e:
        print(f"❌ Failed to append to document: {e}")
        return False


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Weeks 3–14 planner for GCAP 3226")
    parser.add_argument("--generate", action="store_true", help="Generate the draft via LLM")
    parser.add_argument("--apply", action="store_true", help="Append the generated draft to the Google Doc")
    parser.add_argument("--doc-id", default="19LYdvuVJLaZ-MMm31jVc4hXo6tCrcWMk-Np4LiDUib8", help="Target Google Doc ID")
    parser.add_argument("--model", default="openrouter/auto", help="OpenRouter model")
    parser.add_argument("--max-tokens", type=int, default=3500)
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args(argv)

    print("🤖 GCAP 3226 Weeks 3–14 Planner")
    print("=" * 45)

    # Load context
    syllabus_path = PROJECT_ROOT / "course_materials/syllabus/syllabus_analysis.md"
    print(f"📂 Loading syllabus analysis: {syllabus_path}")
    syllabus_text = load_text(syllabus_path)
    if not syllabus_text:
        print("⚠️  Syllabus analysis not found or empty. Proceeding with defaults.")

    draft_text = ""
    if args.generate:
        try:
            prompt = build_prompt(syllabus_text)
            draft_text = call_llm(prompt, model=args.model, max_tokens=args.max_tokens, temperature=args.temperature)
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            return 1

        # Save draft locally
        save_draft(draft_text, PROJECT_ROOT)
        # Show a short preview in terminal
        preview = "\n".join(draft_text.splitlines()[:40])
        print("\n=== PREVIEW (first ~40 lines) ===\n")
        print(preview)
        print("\n=== END PREVIEW ===\n")

    if args.apply:
        if not draft_text:
            # If not generated in this run, try loading the last draft
            last_draft = PROJECT_ROOT / "weeks3_14_draft.md"
            print(f"📄 Loading existing draft from: {last_draft}")
            if last_draft.exists():
                draft_text = load_text(last_draft)
            else:
                print("❌ No draft available to apply. Run with --generate first.")
                return 1

        ok = append_to_google_doc(args.doc_id, draft_text, section_key="weeks3-14-plan")
        return 0 if ok else 1

    print("✅ Step complete. Review the draft file and re-run with --apply to write to Google Doc.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
