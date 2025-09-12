#!/usr/bin/env python3
"""
Basic RAG (Retrieval-Augmented Generation) System for Academic Papers
Combines document retrieval with LLM generation using OpenRouter.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import sys

# Add openRouterAI to path
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions
from scripts.index import AcademicIndexer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AcademicRAG:
    """Basic RAG system for academic papers"""
    
    def __init__(self, index_dir: Path, model: str = "anthropic/claude-3-haiku"):
        """
        Initialize RAG system
        
        Args:
            index_dir: Directory containing FAISS index
            model: OpenRouter model to use for generation
        """
        self.model = model
        self.indexer = AcademicIndexer()
        self.indexer.load_index(index_dir)
        
        # Academic RAG prompt template
        self.rag_prompt_template = """
You are an expert academic research assistant. Based on the provided academic sources, answer the user's question with scholarly rigor.

Academic Sources:
{sources}

Question: {question}

Instructions:
1. Provide a comprehensive answer based on the sources
2. Cite specific papers when referencing findings
3. If multiple perspectives exist, present them fairly
4. Mention if the sources are insufficient to fully answer the question
5. Use academic language appropriate for research

Answer:"""
    
    def format_sources(self, search_results: List[Dict[str, Any]]) -> str:
        """Format search results as academic sources"""
        sources = []
        
        for i, result in enumerate(search_results, 1):
            doc = result["document"]
            metadata = doc["metadata"]
            
            # Extract key information
            title = metadata.get("title", "No title")
            authors = ", ".join(metadata.get("authors", ["Unknown authors"]))
            year = metadata.get("publication_year", "Unknown year")
            
            # Get content preview (first 500 chars after title)
            content = doc["content"]
            # Skip title/header lines and get substantial content
            content_lines = content.split('\n')
            content_preview = ""
            for line in content_lines[3:]:  # Skip first few lines (usually title/metadata)
                if line.strip() and not line.startswith('#'):
                    content_preview += line + " "
                if len(content_preview) > 500:
                    break
            
            content_preview = content_preview[:500] + "..." if len(content_preview) > 500 else content_preview
            
            source_text = f"""
Source {i}: {title}
Authors: {authors} ({year})
Relevance Score: {result['score']:.3f}
Content: {content_preview}
"""
            sources.append(source_text)
        
        return "\n".join(sources)
    
    def query(self, question: str, top_k: int = 3, min_score: float = 0.1) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            min_score: Minimum relevance score
            
        Returns:
            Dict with answer, sources, and metadata
        """
        logger.info(f"Processing query: {question}")
        
        # Step 1: Retrieve relevant documents
        search_results = self.indexer.search(question, k=top_k, min_score=min_score)
        
        if not search_results:
            return {
                "answer": "I couldn't find relevant academic sources to answer your question. Please try rephrasing your query or using different keywords.",
                "sources": [],
                "query": question,
                "model_used": self.model
            }
        
        logger.info(f"Found {len(search_results)} relevant documents")
        
        # Step 2: Format sources
        formatted_sources = self.format_sources(search_results)
        
        # Step 3: Generate answer using LLM
        prompt = self.rag_prompt_template.format(
            sources=formatted_sources,
            question=question
        )
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,  # Slightly creative but focused
                "max_tokens": 1000
            }
            
            response = post_chat_completions(payload)
            answer = response["choices"][0]["message"]["content"].strip()
            
            logger.info("✅ Generated response successfully")
            
            return {
                "answer": answer,
                "sources": search_results,
                "query": question,
                "model_used": self.model,
                "source_count": len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            return {
                "answer": f"I found relevant sources but encountered an error generating the response: {e}",
                "sources": search_results,
                "query": question,
                "model_used": self.model
            }
    
    def interactive_query(self):
        """Interactive query session"""
        print("🎓 Academic RAG System")
        print("=" * 50)
        print("Ask questions about the academic papers in the collection.")
        print("Type 'quit' to exit.")
        print()
        
        while True:
            try:
                question = input("📚 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                print("\n🔍 Searching and generating response...")
                result = self.query(question)
                
                print(f"\n💬 Answer:")
                print("-" * 40)
                print(result["answer"])
                
                print(f"\n📖 Sources ({result.get('source_count', 0)}):")
                print("-" * 40)
                for i, source in enumerate(result["sources"], 1):
                    print(f"{i}. {source['title']}")
                    print(f"   Authors: {', '.join(source['document']['metadata'].get('authors', []))}")
                    print(f"   Score: {source['score']:.3f}")
                
                print("\n" + "=" * 50)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Academic RAG System")
    parser.add_argument("--index", "-i", default="/workspaces/ZoteroMDsMineru3/faiss_index",
                       help="Index directory")
    parser.add_argument("--query", "-q", help="Single query (non-interactive)")
    parser.add_argument("--model", "-m", default="anthropic/claude-3-haiku",
                       help="OpenRouter model to use")
    parser.add_argument("--top-k", "-k", type=int, default=3,
                       help="Number of sources to retrieve")
    
    args = parser.parse_args()
    
    try:
        # Initialize RAG system
        rag = AcademicRAG(Path(args.index), model=args.model)
        
        if args.query:
            # Single query mode
            result = rag.query(args.query, top_k=args.top_k)
            
            print(f"Query: {result['query']}")
            print(f"Model: {result['model_used']}")
            print("\nAnswer:")
            print(result['answer'])
            
            print(f"\nSources ({len(result['sources'])}):")
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. {source['title']} (Score: {source['score']:.3f})")
        else:
            # Interactive mode
            rag.interactive_query()
            
    except Exception as e:
        logger.error(f"RAG system failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
