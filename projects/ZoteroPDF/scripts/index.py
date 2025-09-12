#!/usr/bin/env python3
"""
Document Indexer for Academic Papers
Creates a searchable index from annotated documents using FAISS and simple embeddings.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import pickle
import frontmatter
import numpy as np
import faiss
from collections import defaultdict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleEmbedding:
    """Simple text embedding using TF-IDF for fast indexing"""
    
    def __init__(self):
        self.vocabulary = {}
        self.idf_weights = {}
        self.doc_count = 0
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        import re
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        return words
    
    def _build_vocabulary(self, documents: List[str]):
        """Build vocabulary and IDF weights"""
        word_doc_count = defaultdict(int)
        self.doc_count = len(documents)
        
        # Count document frequency for each word
        for doc in documents:
            words = set(self._tokenize(doc))
            for word in words:
                word_doc_count[word] += 1
        
        # Build vocabulary and IDF weights
        self.vocabulary = {word: idx for idx, word in enumerate(word_doc_count.keys())}
        self.idf_weights = {
            word: np.log(self.doc_count / count)
            for word, count in word_doc_count.items()
        }
        
        logger.info(f"Built vocabulary with {len(self.vocabulary)} words")
    
    def fit_transform(self, documents: List[str]) -> np.ndarray:
        """Fit vocabulary and transform documents to embeddings"""
        self._build_vocabulary(documents)
        return self.transform(documents)
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """Transform documents to TF-IDF embeddings"""
        embeddings = []
        
        for doc in documents:
            words = self._tokenize(doc)
            word_counts = defaultdict(int)
            
            # Count term frequency
            for word in words:
                if word in self.vocabulary:
                    word_counts[word] += 1
            
            # Create TF-IDF vector
            vector = np.zeros(len(self.vocabulary))
            for word, count in word_counts.items():
                if word in self.vocabulary:
                    tf = count / len(words) if words else 0
                    idf = self.idf_weights[word]
                    vector[self.vocabulary[word]] = tf * idf
            
            embeddings.append(vector)
        
        return np.array(embeddings, dtype=np.float32)

class AcademicIndexer:
    """Academic document indexer using FAISS"""
    
    def __init__(self):
        self.embeddings_model = SimpleEmbedding()
        self.index = None
        self.documents = []
        self.metadata = []
        
    def load_annotated_documents(self, annotated_dir: Path) -> List[Dict[str, Any]]:
        """Load documents with metadata from annotated directory"""
        documents = []
        
        logger.info(f"Loading documents from {annotated_dir}")
        
        for md_file in annotated_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Combine title, content, and metadata for embedding
                search_text_parts = []
                
                # Add title and metadata
                if post.metadata.get('title'):
                    search_text_parts.append(post.metadata['title'])
                if post.metadata.get('tags'):
                    search_text_parts.extend(post.metadata['tags'])
                if post.metadata.get('subject_area'):
                    search_text_parts.append(post.metadata['subject_area'])
                
                # Add first part of content (for efficiency)
                content_preview = post.content[:2000]  # First 2000 chars
                search_text_parts.append(content_preview)
                
                search_text = " ".join(search_text_parts)
                
                doc_data = {
                    "id": len(documents),
                    "file_path": str(md_file),
                    "filename": md_file.name,
                    "content": post.content,
                    "metadata": post.metadata,
                    "search_text": search_text
                }
                
                documents.append(doc_data)
                
            except Exception as e:
                logger.warning(f"Failed to load {md_file}: {e}")
                continue
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def create_index(self, annotated_dir: Path, index_dir: Path):
        """Create FAISS index from annotated documents"""
        
        # Load documents
        documents = self.load_annotated_documents(annotated_dir)
        if not documents:
            logger.error("No documents loaded!")
            return
        
        # Prepare texts for embedding
        search_texts = [doc["search_text"] for doc in documents]
        
        logger.info("Creating embeddings...")
        embeddings = self.embeddings_model.fit_transform(search_texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        logger.info(f"Creating FAISS index with dimension {dimension}")
        
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        # Store documents and metadata
        self.documents = documents
        
        # Save index and data
        index_dir.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(index_dir / "faiss.index"))
        
        # Save embeddings model
        with open(index_dir / "embeddings_model.pkl", 'wb') as f:
            pickle.dump(self.embeddings_model, f)
        
        # Save document metadata
        with open(index_dir / "documents.json", 'w') as f:
            json.dump(documents, f, indent=2, default=str)
        
        logger.info(f"✅ Index created successfully!")
        logger.info(f"📊 {len(documents)} documents indexed")
        logger.info(f"📁 Saved to {index_dir}")
    
    def load_index(self, index_dir: Path):
        """Load existing FAISS index"""
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(index_dir / "faiss.index"))
            
            # Load embeddings model
            with open(index_dir / "embeddings_model.pkl", 'rb') as f:
                self.embeddings_model = pickle.load(f)
            
            # Load document metadata
            with open(index_dir / "documents.json", 'r') as f:
                self.documents = json.load(f)
            
            logger.info(f"✅ Index loaded: {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            raise
    
    def search(self, query: str, k: int = 5, min_score: float = 0.1) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not self.index:
            raise ValueError("Index not loaded. Call load_index() or create_index() first.")
        
        # Create query embedding
        query_embedding = self.embeddings_model.transform([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= min_score and idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    "score": float(score),
                    "document": doc,
                    "title": doc["metadata"].get("title", "No title"),
                    "authors": doc["metadata"].get("authors", []),
                    "tags": doc["metadata"].get("tags", []),
                    "filename": doc["filename"]
                })
        
        return results

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create or search document index")
    parser.add_argument("--annotated", "-a", default="/workspaces/ZoteroMDsMineru3/annotated_data",
                       help="Directory with annotated documents")
    parser.add_argument("--index", "-i", default="/workspaces/ZoteroMDsMineru3/faiss_index",
                       help="Index directory")
    parser.add_argument("--create", action="store_true", help="Create new index")
    parser.add_argument("--search", "-s", help="Search query")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results")
    
    args = parser.parse_args()
    
    indexer = AcademicIndexer()
    
    if args.create:
        logger.info("Creating new index...")
        annotated_dir = Path(args.annotated)
        index_dir = Path(args.index)
        indexer.create_index(annotated_dir, index_dir)
        
    elif args.search:
        logger.info("Loading index for search...")
        index_dir = Path(args.index)
        indexer.load_index(index_dir)
        
        logger.info(f"Searching for: '{args.search}'")
        results = indexer.search(args.search, k=args.top_k)
        
        print(f"\n🔍 Search Results for: '{args.search}'")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Authors: {', '.join(result['authors'])}")
            print(f"   Tags: {', '.join(result['tags'][:5])}")
            print(f"   File: {result['filename']}")
        
        if not results:
            print("No results found.")
    
    else:
        print("Specify --create to build index or --search to query")

if __name__ == "__main__":
    main()
