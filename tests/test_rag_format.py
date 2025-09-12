import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / "projects" / "ZoteroPDF"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(SCRIPTS_DIR))

from scripts.rag import AcademicRAG  # noqa: E402
from scripts.index import AcademicIndexer  # noqa: E402

class DummyIndexer(AcademicIndexer):
    def __init__(self):
        super().__init__()
        # Minimal documents
        self.documents = [
            {"content": "Title A\n\nBody about cooperative learning strategies and benefits.",
             "metadata": {"title": "Doc A", "authors": ["Author1"], "publication_year": 2020},
             "filename": "a.md"}
        ]
        import numpy as np
        import faiss
        self.embeddings_model.vocabulary = {"cooperative":0,"learning":1}
        self.embeddings_model.idf_weights = {"cooperative":1.0,"learning":1.0}
        self.embeddings_model.doc_count = 1
        self.index = faiss.IndexFlatIP(2)
        vec = np.array([[0.7,0.7]], dtype='float32')
        faiss.normalize_L2(vec)
        self.index.add(vec)

    def search(self, query: str, k: int = 3, min_score: float = 0.0):  # override deterministic
        return [{
            "score": 0.9,
            "document": self.documents[0],
            "title": self.documents[0]["metadata"].get("title"),
            "authors": self.documents[0]["metadata"].get("authors"),
            "tags": [],
            "filename": self.documents[0]["filename"]
        }]

class DummyRAG(AcademicRAG):
    def __init__(self):
        # Bypass actual index load
        self.model = "dummy/model"
        self.indexer = DummyIndexer()
        self.rag_prompt_template = "Sources: {sources}\nQ: {question}\nA:"

    def query(self, question: str, top_k: int = 3, min_score: float = 0.0):
        sr = self.indexer.search(question, k=top_k, min_score=min_score)
        formatted_sources = self.format_sources(sr)
        return {"answer": "TEST", "sources": sr, "query": question, "formatted": formatted_sources}


def test_format_sources_contains_title():
    r = DummyRAG()
    out = r.query("benefits of cooperative learning")
    assert "Doc A" in out["formatted"]
    assert "Source 1" in out["formatted"]
