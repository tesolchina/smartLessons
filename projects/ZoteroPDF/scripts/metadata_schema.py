#!/usr/bin/env python3
"""
Academic Metadata Schema for RAG System
Defines the structure for academic paper metadata extraction.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
import yaml
from datetime import datetime

class AcademicMetadata(BaseModel):
    """Schema for academic paper metadata extracted by LLM"""
    
    # Core bibliographic information
    title: Optional[str] = Field(None, description="Main title of the paper (max 15 words)")
    authors: List[str] = Field(default_factory=list, description="List of author names")
    publication_year: Optional[int] = Field(None, description="Year of publication if found")
    
    # Content classification
    category: Optional[str] = Field(None, description="research|review|technical|policy|book_chapter")
    subject_area: Optional[str] = Field(None, description="Primary academic discipline")
    methodology: Optional[str] = Field(None, description="quantitative|qualitative|mixed|theoretical|empirical")
    document_type: Optional[str] = Field(None, description="journal|conference|report|thesis|book_chapter")
    
    # Content analysis
    tags: List[str] = Field(default_factory=list, description="5-7 relevant academic keywords")
    has_abstract: bool = Field(False, description="Whether document contains an abstract")
    has_methodology: bool = Field(False, description="Whether document describes methodology")
    has_results: bool = Field(False, description="Whether document presents results/findings")
    
    # Processing metadata
    confidence_score: float = Field(0.0, description="Confidence in extraction accuracy (0-1)")
    extraction_date: str = Field(default_factory=lambda: datetime.now().isoformat())
    source_file: Optional[str] = Field(None, description="Original filename")
    
    # Academic-specific fields
    research_questions: List[str] = Field(default_factory=list, description="Key research questions if identified")
    key_findings: List[str] = Field(default_factory=list, description="Main findings/conclusions if extractable")
    
    def to_yaml_frontmatter(self) -> str:
        """Convert to YAML front matter format for markdown files"""
        # Convert to dict and remove None values
        data = {k: v for k, v in self.dict().items() if v is not None and v != [] and v != ""}
        
        # Format the YAML
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=True)
        return f"---\n{yaml_str}---\n"
    
    def get_search_text(self) -> str:
        """Generate searchable text representation"""
        search_parts = []
        
        if self.title:
            search_parts.append(self.title)
        if self.authors:
            search_parts.extend(self.authors)
        if self.tags:
            search_parts.extend(self.tags)
        if self.subject_area:
            search_parts.append(self.subject_area)
        if self.methodology:
            search_parts.append(self.methodology)
            
        return " ".join(search_parts)

# Example metadata instances for testing
SAMPLE_METADATA = AcademicMetadata(
    title="Effects of AI on Academic Writing Assessment",
    authors=["Smith, J.", "Johnson, A."],
    publication_year=2024,
    category="research",
    subject_area="education",
    methodology="quantitative",
    document_type="journal",
    tags=["artificial intelligence", "writing assessment", "education technology", "automated scoring"],
    has_abstract=True,
    has_methodology=True,
    has_results=True,
    confidence_score=0.85
)

if __name__ == "__main__":
    # Test the schema
    print("Academic Metadata Schema Test")
    print("=" * 40)
    
    print("\nSample metadata:")
    print(SAMPLE_METADATA.to_yaml_frontmatter())
    
    print("Search text:")
    print(SAMPLE_METADATA.get_search_text())
    
    print("\nValidation test:")
    try:
        # Test with minimal data
        minimal = AcademicMetadata(title="Test Paper")
        print("✅ Minimal metadata valid")
        
        # Test with full data
        full = AcademicMetadata(**SAMPLE_METADATA.dict())
        print("✅ Full metadata valid")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
