#!/usr/bin/env python3
"""
Simple RAG Demo for Academic Papers
A working demonstration of retrieval-augmented generation.
"""

import sys
from pathlib import Path

# Add openRouterAI to path
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions

def simple_rag_demo():
    """Demonstrate RAG with our indexed academic papers"""
    
    print("🎓 Academic RAG Demo")
    print("=" * 50)
    
    # Sample query
    query = "What are the benefits of cooperative learning?"
    print(f"📚 Query: {query}")
    print()
    
    # Mock search results (using our known documents)
    search_results = [
        {
            "title": "The Impact of Cooperative, Competitive, and Individualistic Learning Environments on Academic Achievement",
            "authors": ["David W. Johnson", "Roger T. Johnson"],
            "year": 2013,
            "score": 0.85,
            "content_preview": """Cooperative learning refers to instructional methods in which students work together in small groups to help each other learn academic content. The research shows that cooperative learning experiences, compared with competitive and individualistic ones, promote higher achievement, greater retention, more frequent use of higher-level reasoning strategies, more frequent process gain and collective induction, and greater transfer of what is learned within one situation to another."""
        }
    ]
    
    # Format sources for LLM
    sources_text = ""
    for i, result in enumerate(search_results, 1):
        authors_str = ", ".join(result["authors"])
        sources_text += f"""
Source {i}: {result['title']}
Authors: {authors_str} ({result['year']})
Relevance Score: {result['score']:.3f}
Content: {result['content_preview']}
"""
    
    print("🔍 Retrieved Sources:")
    print(sources_text)
    
    # RAG prompt
    rag_prompt = f"""
You are an expert academic research assistant. Based on the provided academic sources, answer the user's question with scholarly rigor.

Academic Sources:
{sources_text}

Question: {query}

Instructions:
1. Provide a comprehensive answer based on the sources
2. Cite specific papers when referencing findings
3. Use academic language appropriate for research
4. Mention the authors' names when referencing their work

Answer:"""
    
    print("🤖 Generating answer with LLM...")
    print()
    
    try:
        payload = {
            "model": "anthropic/claude-3-haiku",
            "messages": [{"role": "user", "content": rag_prompt}],
            "temperature": 0.3,
            "max_tokens": 800
        }
        
        response = post_chat_completions(payload)
        answer = response["choices"][0]["message"]["content"].strip()
        
        print("💬 RAG Answer:")
        print("-" * 40)
        print(answer)
        print()
        print("✅ RAG Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error generating answer: {e}")

def test_search_integration():
    """Test the search functionality separately"""
    print("\n🔍 Testing Search Integration")
    print("-" * 30)
    
    # Import and test our indexer
    from scripts.index import AcademicIndexer
    
    try:
        indexer = AcademicIndexer()
        
        # Test with a fresh index creation (avoiding pickle)
        annotated_dir = Path("/workspaces/ZoteroMDsMineru3/annotated_data")
        documents = indexer.load_annotated_documents(annotated_dir)
        
        print(f"📊 Loaded {len(documents)} documents:")
        for doc in documents:
            title = doc["metadata"].get("title", "No title")[:60]
            print(f"  - {title}...")
        
        print("\n✅ Document loading works!")
        
    except Exception as e:
        print(f"❌ Search integration error: {e}")

if __name__ == "__main__":
    simple_rag_demo()
    test_search_integration()
