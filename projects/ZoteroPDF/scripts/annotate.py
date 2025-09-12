#!/usr/bin/env python3
"""
Academic Document Annotator using OpenRouter API
Extracts metadata from academic papers using LLM via OpenRouter.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Set
import re
import sys
import time
from datetime import datetime, timedelta
import frontmatter

# Add openRouterAI to path
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions
from metadata_schema import AcademicMetadata

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenRouterAnnotator:
    """Academic document annotator using OpenRouter API"""
    
    def __init__(self, model: str = "anthropic/claude-3-haiku"):
        """
        Initialize the annotator with OpenRouter API
        
        Args:
            model: Model to use for annotation (default: Claude 3 Haiku for cost-effectiveness)
        """
        self.model = model
        
        # Academic-focused prompt template
        self.prompt_template = """
You are an expert academic librarian and research assistant. Analyze this academic document excerpt and extract structured metadata.

Document excerpt (first 2000 characters):
---
{document}
---

Extract the following information and return ONLY a valid JSON object with these fields:

{{
    "title": "Concise academic title (max 15 words, remove extra formatting)",
    "authors": ["Author 1", "Author 2"],
    "publication_year": 2024,
    "category": "research|review|technical|policy|book_chapter",
    "subject_area": "Primary academic discipline (e.g., education, psychology, linguistics)",
    "methodology": "quantitative|qualitative|mixed|theoretical|empirical",
    "document_type": "journal|conference|report|thesis|book_chapter",
    "tags": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "has_abstract": true,
    "has_methodology": true,
    "has_results": true,
    "research_questions": ["Research question 1 if clearly stated"],
    "key_findings": ["Key finding 1 if clearly stated"]
}}

Rules:
- Extract only information clearly present in the text
- Use null for missing information
- Keep titles concise and descriptive
- Focus on academic/research keywords for tags
- Be conservative with research_questions and key_findings - only include if explicitly stated

Return ONLY the JSON object, no explanations.
"""
    
    def extract_clean_text(self, content: str, max_chars: int = 2000) -> str:
        """Extract clean text for LLM processing"""
        # Remove excessive whitespace and formatting artifacts
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\/]', ' ', content)
        
        # Take first part for analysis
        return content[:max_chars].strip()
    
    def annotate_document(self, file_path: Path) -> AcademicMetadata:
        """Annotate a single academic document"""
        try:
            logger.info(f"Annotating: {file_path.name}")
            
            # Read document content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract clean text for processing
            clean_text = self.extract_clean_text(content)
            
            if len(clean_text) < 100:
                logger.warning(f"Document too short: {file_path.name}")
                return AcademicMetadata(source_file=file_path.name, confidence_score=0.1)
            
            # Prepare prompt
            prompt = self.prompt_template.format(document=clean_text)
            
            # Call OpenRouter API using the existing client
            try:
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 1000
                }
                
                response = post_chat_completions(payload)
                response_text = response["choices"][0]["message"]["content"].strip()
                logger.debug(f"LLM response: {response_text[:200]}...")
                
            except Exception as e:
                logger.error(f"API call failed for {file_path.name}: {e}")
                return AcademicMetadata(
                    source_file=file_path.name,
                    confidence_score=0.0
                )
            
            # Parse JSON response
            try:
                # Clean response text (remove code blocks if present)
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]
                
                metadata_dict = json.loads(json_text.strip())
                
                # Clean up null values for list fields
                for field in ["research_questions", "key_findings", "tags", "authors"]:
                    if metadata_dict.get(field) is None:
                        metadata_dict[field] = []
                
                # Add processing metadata
                metadata_dict["source_file"] = file_path.name
                metadata_dict["confidence_score"] = 0.8  # Default high confidence for successful extraction
                
                # Create and validate metadata object
                metadata = AcademicMetadata(**metadata_dict)
                
                logger.info(f"✅ Successfully extracted metadata for {file_path.name}")
                return metadata
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON for {file_path.name}: {e}")
                logger.debug(f"Raw response: {response_text}")
                
                # Fallback: extract basic information manually
                return self._fallback_extraction(content, file_path.name)
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return AcademicMetadata(
                source_file=file_path.name,
                confidence_score=0.0
            )
    
    def _fallback_extraction(self, content: str, filename: str) -> AcademicMetadata:
        """Fallback extraction using simple patterns"""
        logger.info(f"Using fallback extraction for {filename}")
        
        # Simple pattern-based extraction
        title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else None
        
        # Clean title
        if title:
            title = re.sub(r'[^\w\s\-\:\,\.]', '', title)[:100]
        
        has_abstract = bool(re.search(r'#\s*abstract', content, re.IGNORECASE))
        has_methodology = bool(re.search(r'(method|approach|procedure)', content, re.IGNORECASE))
        has_results = bool(re.search(r'(result|finding|conclusion)', content, re.IGNORECASE))
        
        return AcademicMetadata(
            title=title,
            source_file=filename,
            has_abstract=has_abstract,
            has_methodology=has_methodology,
            has_results=has_results,
            confidence_score=0.3  # Low confidence for fallback
        )
    
    def batch_annotate(self, 
                       input_dir: Path, 
                       output_dir: Path, 
                       limit: Optional[int] = None,
                       resume: bool = True,
                       progress_log: Path = Path("/workspaces/ZoteroMDsMineru3/logs/annotation_progress.json"),
                       checkpoint_interval: int = 25,
                       sleep_between: float = 0.0):
        """Batch annotate documents with robust progress tracking & resume capability.

        Args:
            input_dir: Directory containing source markdown files
            output_dir: Directory to write annotated files
            limit: Optional limit for number of files (debug/testing)
            resume: If True, skip already processed files listed in progress log
            progress_log: JSON file tracking progress for resume / monitoring
            checkpoint_interval: How many files between writing progress log
            sleep_between: Optional sleep to throttle API usage (seconds)
        """

        start_time = time.time()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect all markdown files deterministically (sorted for reproducibility)
        md_files: List[Path] = sorted(list(input_dir.rglob("*.md")))
        if limit:
            md_files = md_files[:limit]

        total_files = len(md_files)

        # Load existing progress if resuming
        processed_paths: Set[str] = set()
        success_count = 0
        error_count = 0
        existing_data: Dict[str, Any] = {}
        if resume and progress_log.exists():
            try:
                with open(progress_log, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                processed_paths = set(existing_data.get("processed_file_paths", []))
                success_count = existing_data.get("successful_annotations", 0)
                error_count = existing_data.get("failed_annotations", 0)
                logger.info(f"Resume enabled: {len(processed_paths)} files already processed; skipping them.")
            except Exception as e:
                logger.warning(f"Could not load existing progress log: {e}")

        logger.info(f"Starting batch annotation of {total_files} files (resume={resume})...")

        def write_progress(current_index: int):
            elapsed = time.time() - start_time
            processed_count = len(processed_paths)
            rate = processed_count / elapsed if elapsed > 0 else 0
            remaining = total_files - processed_count
            eta = time.time() + (remaining / rate) if rate > 0 else None
            progress_payload = {
                "total_files": total_files,
                "processed_files": processed_count,
                "successful_annotations": success_count,
                "failed_annotations": error_count,
                "current_index": current_index,
                "start_time": existing_data.get("start_time") or datetime.fromtimestamp(start_time).isoformat(),
                "last_update": datetime.utcnow().isoformat(),
                "estimated_completion": datetime.fromtimestamp(eta).isoformat() if eta else None,
                "processed_file_paths": sorted(list(processed_paths))[-1000:]  # cap to avoid huge file
            }
            try:
                progress_log.parent.mkdir(parents=True, exist_ok=True)
                with open(progress_log, 'w', encoding='utf-8') as pf:
                    json.dump(progress_payload, pf, indent=2)
            except Exception as e:
                logger.error(f"Failed to write progress log: {e}")

        for idx, file_path in enumerate(md_files, 1):
            str_path = str(file_path)
            if resume and str_path in processed_paths:
                if idx % 100 == 0:
                    logger.info(f"Skip checkpoint: {idx}/{total_files} (already processed)")
                continue

            logger.info(f"Processing {idx}/{total_files}: {file_path.name}")
            try:
                metadata = self.annotate_document(file_path)

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    original_content = f.read()

                post = frontmatter.Post(
                    content=original_content,
                    **metadata.model_dump(exclude_unset=True, exclude={'extraction_date'})
                )

                output_file = output_dir / file_path.relative_to(input_dir)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))

                processed_paths.add(str_path)
                if metadata.confidence_score and metadata.confidence_score > 0.5:
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logger.error(f"Failed to process {file_path.name}: {e}")
                error_count += 1
                processed_paths.add(str_path)  # Mark as processed to avoid infinite retry unless separate retry logic

            # Periodic checkpoint
            if idx % checkpoint_interval == 0:
                write_progress(idx)
                logger.info(f"Checkpoint saved ({idx}/{total_files}). Success={success_count} Errors={error_count}")

            if sleep_between > 0:
                time.sleep(sleep_between)

        # Final write
        write_progress(total_files)

        logger.info("Batch annotation complete!")
        logger.info(f"✅ Successful: {success_count}")
        logger.info(f"⚠️  Errors/Low confidence: {error_count}")
        logger.info(f"📁 Output directory: {output_dir}")
        logger.info(f"🕒 Elapsed: {timedelta(seconds=int(time.time()-start_time))}")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Annotate academic documents with metadata")
    parser.add_argument("--input", "-i", default="/workspaces/ZoteroMDsMineru3/data", 
                       help="Input directory with MD files")
    parser.add_argument("--output", "-o", default="/workspaces/ZoteroMDsMineru3/annotated_data",
                       help="Output directory for annotated files")
    parser.add_argument("--limit", "-l", type=int, default=None,
                       help="Limit number of files to process (omit for all)")
    parser.add_argument("--model", "-m", default="anthropic/claude-3-haiku",
                       help="OpenRouter model to use")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume; re-process all files")
    parser.add_argument("--checkpoint", type=int, default=25, help="Checkpoint interval (files)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between files (throttle)")
    parser.add_argument("--progress-log", default="/workspaces/ZoteroMDsMineru3/logs/annotation_progress.json", help="Progress log path")
    
    args = parser.parse_args()
    
    # Initialize annotator
    try:
        annotator = OpenRouterAnnotator(model=args.model)
        
        # Run batch annotation
        input_dir = Path(args.input)
        output_dir = Path(args.output)
        
        annotator.batch_annotate(
            input_dir=input_dir,
            output_dir=output_dir,
            limit=args.limit,
            resume=not args.no_resume,
            progress_log=Path(args.progress_log),
            checkpoint_interval=args.checkpoint,
            sleep_between=args.sleep
        )
        
    except Exception as e:
        logger.error(f"Annotation failed: {e}")

if __name__ == "__main__":
    main()
