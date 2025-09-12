#!/usr/bin/env python3
"""Batch annotation script for academic papers using OpenRouter API.

Processes markdown files without existing annotation, extracts metadata using LLM,
and updates files with YAML front matter. Includes rate limiting, checkpointing,
and progress tracking.

Usage:
  python projects/ZoteroPDF/scripts/batch_annotate.py \
    --docs projects/ZoteroPDF/data \
    --manifest projects/ZoteroPDF/annotation_manifest.json \
    --output projects/ZoteroPDF/annotated_data \
    --batch-size 50 \
    --dry-run
"""
import argparse
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
import sys
import frontmatter
from dataclasses import dataclass

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AnnotationResult:
    success: bool
    error: str = ""
    metadata: Dict[str, Any] = None
    confidence: float = 0.0

ANNOTATION_PROMPT = """
You are an expert academic metadata extractor. Analyze this research paper and extract structured metadata.

Return ONLY valid JSON with these fields:
{
  "title": "Paper title (string)",
  "authors": ["Author1", "Author2"] (array of strings),
  "publication_year": 2023 (integer),
  "subject_area": "education|psychology|other" (string),
  "methodology": "quantitative|qualitative|mixed|theoretical|review" (string),
  "document_type": "journal|conference|book_chapter|thesis|report" (string),
  "tags": ["tag1", "tag2"] (array of relevant keywords),
  "abstract": "Brief abstract if available" (string, max 300 chars),
  "confidence": 0.85 (float 0-1, your confidence in this extraction)
}

Paper content:
{content}

JSON:"""

def annotate_document(content: str, model: str = "anthropic/claude-3-haiku") -> AnnotationResult:
    """Annotate a single document using OpenRouter API"""
    try:
        # Truncate content for API efficiency
        truncated = content[:4000] + "..." if len(content) > 4000 else content
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": ANNOTATION_PROMPT.format(content=truncated)}],
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        response = post_chat_completions(payload)
        response_text = response["choices"][0]["message"]["content"].strip()
        
        # Try to parse JSON from response
        try:
            metadata = json.loads(response_text)
            confidence = metadata.pop("confidence", 0.8)
            return AnnotationResult(success=True, metadata=metadata, confidence=confidence)
        except json.JSONDecodeError:
            # Try to extract JSON from response if wrapped in markdown
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                metadata = json.loads(json_match.group(1))
                confidence = metadata.pop("confidence", 0.8)
                return AnnotationResult(success=True, metadata=metadata, confidence=confidence)
            else:
                return AnnotationResult(success=False, error=f"Invalid JSON response: {response_text[:200]}")
                
    except Exception as e:
        return AnnotationResult(success=False, error=str(e))

def update_manifest(manifest_path: Path, file_path: str, annotated: bool, error: str = ""):
    """Update manifest with annotation status"""
    try:
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
        else:
            manifest = {"files": {}, "generated_at": int(time.time())}
        
        if file_path in manifest["files"]:
            manifest["files"][file_path]["annotated"] = annotated
            manifest["files"][file_path]["annotation_error"] = error
            manifest["files"][file_path]["annotation_timestamp"] = int(time.time())
        
        manifest["generated_at"] = int(time.time())
        manifest_path.write_text(json.dumps(manifest, indent=2))
    except Exception as e:
        logger.error(f"Failed to update manifest: {e}")

def main():
    parser = argparse.ArgumentParser(description="Batch annotate academic papers")
    parser.add_argument("--docs", required=True, help="Source documents directory")
    parser.add_argument("--manifest", required=True, help="Annotation manifest file")
    parser.add_argument("--output", required=True, help="Output annotated directory")
    parser.add_argument("--batch-size", type=int, default=50, help="Files per batch")
    parser.add_argument("--rate-limit", type=float, default=1.0, help="Seconds between API calls")
    parser.add_argument("--dry-run", action="store_true", help="Don't make API calls")
    parser.add_argument("--model", default="anthropic/claude-3-haiku", help="OpenRouter model")
    args = parser.parse_args()

    docs_dir = Path(args.docs)
    manifest_path = Path(args.manifest)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest to find unannotated files
    if not manifest_path.exists():
        logger.error(f"Manifest not found: {manifest_path}")
        logger.info("Run build_manifest.py first")
        return
    
    manifest = json.loads(manifest_path.read_text())
    unannotated_files = [
        fp for fp, info in manifest["files"].items() 
        if not info.get("annotated", False) and Path(fp).suffix == ".md"
    ]
    
    logger.info(f"Found {len(unannotated_files)} unannotated files")
    
    if args.dry_run:
        logger.info("DRY RUN - no API calls will be made")
        for i, fp in enumerate(unannotated_files[:10]):
            logger.info(f"Would process: {Path(fp).name}")
        return

    processed = 0
    errors = 0
    
    for file_path in unannotated_files[:args.batch_size]:
        try:
            logger.info(f"Processing {Path(file_path).name} ({processed+1}/{min(len(unannotated_files), args.batch_size)})")
            
            # Read source file
            source_file = Path(file_path)
            if not source_file.exists():
                logger.warning(f"Source file not found: {file_path}")
                continue
                
            content = source_file.read_text(encoding='utf-8', errors='ignore')
            
            # Skip if already has front matter
            if content.strip().startswith('---'):
                logger.info(f"Skipping {source_file.name} - already has front matter")
                continue
            
            # Rate limiting
            if processed > 0:
                time.sleep(args.rate_limit)
            
            # Annotate
            result = annotate_document(content, args.model)
            
            if result.success:
                # Create output file with front matter
                output_file = output_dir / source_file.name
                
                # Create post with front matter
                post = frontmatter.Post(content)
                post.metadata.update(result.metadata)
                
                # Write annotated file
                output_file.write_text(frontmatter.dumps(post), encoding='utf-8')
                
                # Update manifest
                update_manifest(manifest_path, file_path, True)
                
                logger.info(f"✅ Annotated {source_file.name} (confidence: {result.confidence:.2f})")
                processed += 1
                
            else:
                logger.error(f"❌ Failed to annotate {source_file.name}: {result.error}")
                update_manifest(manifest_path, file_path, False, result.error)
                errors += 1
                
        except Exception as e:
            logger.error(f"❌ Exception processing {file_path}: {e}")
            errors += 1
    
    logger.info(f"Batch complete: {processed} annotated, {errors} errors")

if __name__ == "__main__":
    main()
