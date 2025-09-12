#!/usr/bin/env python3
"""Pedagogical implications detection for academic papers.

Implements heuristic scoring + LLM confirmation to identify papers that discuss
practical teaching applications, classroom strategies, or instructional guidance.

Usage:
  python projects/ZoteroPDF/scripts/detect_pedagogical.py \
    --annotated projects/ZoteroPDF/annotated_data \
    --manifest projects/ZoteroPDF/annotation_manifest.json \
    --threshold 8 \
    --confirm-top 20
"""
import argparse
import json
import logging
import re
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import sys
import frontmatter

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Keywords and phrases for pedagogical implications
PRIMARY_KEYWORDS = [
    "pedagogical", "instructional", "teaching practice", "classroom application",
    "educational practice", "learning intervention", "curriculum design",
    "instructional strategy", "teaching implications", "classroom implementation",
    "educational design", "learning design", "course design", "learning support",
    "student support", "learning experience", "educational experience",
    "teaching strategy", "learning strategy", "educational strategy"
]

SECONDARY_KEYWORDS = [
    "teacher training", "learner engagement", "applied in classroom",
    "educational outcome", "practical guidance", "student learning",
    "instructional design", "teaching method", "classroom management",
    "learning activities", "educational activities", "course activities",
    "student performance", "learning performance", "academic performance",
    "learning process", "educational process", "teaching process",
    "online learning", "distance learning", "e-learning", "blended learning",
    "learning environment", "educational environment", "classroom environment",
    "learning goals", "educational goals", "learning objectives", "course objectives",
    "self-regulated learning", "autonomous learning", "independent learning",
    "chatbot", "educational technology", "learning technology", "digital learning"
]

HEADING_PATTERNS = [
    r"^#+\s*.*implications?\b",
    r"^#+\s*.*instructional\b",
    r"^#+\s*.*pedagogical\b",
    r"^#+\s*.*teaching\s+practice\b",
    r"^#+\s*.*classroom\s+application\b",
    r"^#+\s*.*practical\s+implications?\b",
    r"^#+\s*.*educational\s+implications?\b"
]

CONCLUSION_MARKERS = ["implications", "conclusion", "recommendations", "discussion"]

LLM_CONFIRMATION_PROMPT = """
Does this academic paper contain explicit pedagogical implications or practical teaching recommendations?

Analyze the content and return ONLY valid JSON with this exact format:
{"has_pedagogical_implications": true, "confidence": 0.85, "evidence": ["quote1"], "reasoning": "brief explanation"}

Paper content:
{content}

JSON response:"""

def calculate_heuristic_score(content: str) -> Tuple[int, Dict[str, Any]]:
    """Calculate heuristic score for pedagogical implications"""
    score = 0
    details = {
        "heading_matches": 0,
        "primary_hits": 0,
        "secondary_hits": 0,
        "conclusion_boost": 0
    }
    
    content_lower = content.lower()
    
    # Check for heading patterns (weight: 3)
    for pattern in HEADING_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        if matches:
            details["heading_matches"] += len(matches)
            score += len(matches) * 3
    
    # Primary keyword hits (weight: 2)
    for keyword in PRIMARY_KEYWORDS:
        count = content_lower.count(keyword.lower())
        details["primary_hits"] += count
        score += count * 2
    
    # Secondary keyword hits (weight: 1)
    for keyword in SECONDARY_KEYWORDS:
        count = content_lower.count(keyword.lower())
        details["secondary_hits"] += count
        score += count * 1
    
    # Conclusion section boost (weight: 2)
    for marker in CONCLUSION_MARKERS:
        if re.search(rf"^#+\s*.*{marker}\b", content, re.IGNORECASE | re.MULTILINE):
            details["conclusion_boost"] = 2
            score += 2
            break
    
    return score, details

def llm_confirm_pedagogical(content: str, model: str = "anthropic/claude-3-haiku") -> Dict[str, Any]:
    """Use LLM to confirm pedagogical implications"""
    try:
        # Use relevant sections (first 1500 + last 500 chars for conclusion)
        if len(content) > 2000:
            excerpt = content[:1500] + "\n...\n" + content[-500:]
        else:
            excerpt = content
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": LLM_CONFIRMATION_PROMPT.format(content=excerpt)}],
            "temperature": 0.1,
            "max_tokens": 300
        }
        
        response = post_chat_completions(payload)
        response_text = response["choices"][0]["message"]["content"].strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            logger.warning(f"Response text: {response_text}")
            # Try to extract JSON if wrapped
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(1))
                    return result
                except json.JSONDecodeError as e2:
                    logger.warning(f"JSON parse error on extracted content: {e2}")
                    return {"has_pedagogical_implications": False, "confidence": 0.0, "error": "Invalid JSON", "raw_response": response_text}
            else:
                logger.warning(f"LLM response not parseable as JSON: {response_text}")
                return {"has_pedagogical_implications": False, "confidence": 0.0, "error": "Invalid JSON", "raw_response": response_text}
                
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        return {"has_pedagogical_implications": False, "confidence": 0.0, "error": str(e)}

def update_file_with_flag(file_path: Path, has_implications: bool, confidence: float, evidence: List[str]):
    """Update file front matter with pedagogical implications flag"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        post.metadata['pedagogical_implications'] = has_implications
        post.metadata['pedagogical_confidence'] = confidence
        if evidence:
            post.metadata['pedagogical_evidence'] = evidence[:3]  # Keep top 3 snippets
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
            
        return True
    except Exception as e:
        logger.error(f"Failed to update {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Detect pedagogical implications in papers")
    parser.add_argument("--annotated", required=True, help="Annotated documents directory")
    parser.add_argument("--manifest", required=True, help="Annotation manifest file")
    parser.add_argument("--threshold", type=int, default=8, help="Heuristic score threshold")
    parser.add_argument("--confirm-top", type=int, default=20, help="LLM confirm top N candidates")
    parser.add_argument("--model", default="anthropic/claude-3-haiku", help="LLM model for confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Don't update files")
    args = parser.parse_args()

    annotated_dir = Path(args.annotated)
    manifest_path = Path(args.manifest)
    
    if not manifest_path.exists():
        logger.error(f"Manifest not found: {manifest_path}")
        return
    
    # Get annotated files from manifest
    manifest = json.loads(manifest_path.read_text())
    annotated_files = [
        fp for fp, info in manifest["files"].items()
        if info.get("annotated", False) and Path(fp).suffix == ".md"
    ]
    
    logger.info(f"Analyzing {len(annotated_files)} annotated files")
    
    candidates = []
    
    # Phase 1: Heuristic scoring
    for file_path in annotated_files:
        try:
            # Use the full path from manifest
            annotated_file = Path(file_path)
            if not annotated_file.exists():
                continue
            
            content = annotated_file.read_text(encoding='utf-8', errors='ignore')
            score, details = calculate_heuristic_score(content)
            
            if score >= args.threshold:
                candidates.append({
                    "file_path": str(annotated_file),
                    "score": score,
                    "details": details,
                    "content": content
                })
                
        except Exception as e:
            logger.warning(f"Error processing {file_path}: {e}")
    
    # Sort by score (highest first)
    candidates.sort(key=lambda x: x["score"], reverse=True)
    logger.info(f"Found {len(candidates)} candidates above threshold {args.threshold}")
    
    # Phase 2: Apply results (heuristic-only or LLM-confirmed)
    confirmed = 0
    rejected = 0
    
    if args.confirm_top > 0:
        # LLM confirmation mode
        for i, candidate in enumerate(candidates[:args.confirm_top]):
            logger.info(f"LLM confirmation {i+1}/{min(len(candidates), args.confirm_top)}: {Path(candidate['file_path']).name}")
            
            if not args.dry_run:
                time.sleep(1.0)  # Rate limiting
            
            if args.dry_run:
                logger.info(f"DRY RUN: Would confirm {candidate['file_path']} (score: {candidate['score']})")
                continue
            
            llm_result = llm_confirm_pedagogical(candidate["content"], args.model)
            
            # Debug LLM response
            logger.info(f"LLM result: {llm_result}")
            
            has_implications = llm_result.get("has_pedagogical_implications", False)
            confidence = llm_result.get("confidence", 0.0)
            evidence = llm_result.get("evidence", [])
            
            if has_implications and confidence > 0.6:
                if update_file_with_flag(Path(candidate["file_path"]), True, confidence, evidence):
                    confirmed += 1
                    logger.info(f"✅ Confirmed pedagogical implications: {Path(candidate['file_path']).name} (conf: {confidence:.2f})")
                else:
                    logger.error(f"Failed to update file: {candidate['file_path']}")
            else:
                rejected += 1
                logger.info(f"❌ Rejected: {Path(candidate['file_path']).name} (conf: {confidence:.2f})")
    else:
        # Heuristic-only mode
        logger.info("Running in heuristic-only mode (no LLM confirmation)")
        for candidate in candidates:
            if args.dry_run:
                logger.info(f"DRY RUN: Would mark as pedagogical {candidate['file_path']} (score: {candidate['score']})")
                continue
            
            # Use heuristic score as confidence (normalized to 0-1)
            heuristic_confidence = min(candidate['score'] / 100.0, 1.0)
            
            if update_file_with_flag(Path(candidate["file_path"]), True, heuristic_confidence, []):
                confirmed += 1
            else:
                logger.error(f"Failed to update file: {candidate['file_path']}")
    
    logger.info(f"Pedagogical implications detection complete:")
    logger.info(f"  Candidates identified: {len(candidates)}")
    logger.info(f"  LLM confirmed: {confirmed}")
    logger.info(f"  LLM rejected: {rejected}")

if __name__ == "__main__":
    main()
