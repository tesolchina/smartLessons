import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).parent.parent / "projects" / "ZoteroPDF"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.extend([str(PROJECT_ROOT), str(SCRIPTS_DIR)])

from scripts.rag import AcademicRAG  # noqa: E402
from scripts.index import AcademicIndexer  # noqa: E402

class DummyIndexer(AcademicIndexer):
    def __init__(self):
        super().__init__()
        self.documents = [
            {"content": "Study on cooperative learning benefits.",
             "metadata": {"title": "Coop Study", "authors": ["Smith"], "publication_year": 2021},
             "filename": "coop.md"},
            {"content": "Paper about metacognitive strategies in self-regulation.",
             "metadata": {"title": "Meta Study", "authors": ["Lee"], "publication_year": 2020},
             "filename": "meta.md"},
        ]
        import numpy as np
        import faiss
        # Minimal embedding model state
        self.embeddings_model.vocabulary = {"cooperative":0, "learning":1, "metacognitive":2}
        self.embeddings_model.idf_weights = {k:1.0 for k in self.embeddings_model.vocabulary}
        self.embeddings_model.doc_count = 2
        self.index = faiss.IndexFlatIP(3)
        vecs = np.array([[0.9,0.9,0.1],[0.1,0.2,0.9]], dtype='float32')
        faiss.normalize_L2(vecs)
        self.index.add(vecs)

    def search(self, query: str, k: int = 3, min_score: float = 0.0):
        # Deterministic order for this test
        return [
            {"score": 0.95, "document": self.documents[0], "title": "Coop Study", "authors": ["Smith"], "tags": [], "filename": "coop.md"},
            {"score": 0.70, "document": self.documents[1], "title": "Meta Study", "authors": ["Lee"], "tags": [], "filename": "meta.md"},
        ][:k]

@pytest.fixture()
def rag_with_mock(monkeypatch):
    # Monkeypatch indexer to avoid disk load
    rag = AcademicRAG.__new__(AcademicRAG)
    rag.model = "mock/model"
    rag.indexer = DummyIndexer()
    rag.rag_prompt_template = "Sources:{sources}\nQ:{question}\nA:"

    # Fake OpenRouter response
    def fake_post_chat(payload):
        return {"choices": [{"message": {"content": "Mock answer referencing sources."}}]}

    # Patch the imported function in module scope
    monkeypatch.setattr("scripts.rag.post_chat_completions", fake_post_chat)
    return rag


def test_rag_query_returns_answer_and_sources(rag_with_mock):
    result = rag_with_mock.query("benefits of cooperative learning", top_k=2)
    assert "answer" in result
    assert result["answer"].startswith("Mock answer")
    assert len(result["sources"]) == 2
    titles = {s['title'] for s in result['sources']}
    assert "Coop Study" in titles and "Meta Study" in titles


def test_rag_query_respects_top_k(rag_with_mock):
    result = rag_with_mock.query("benefits of cooperative learning", top_k=1)
    assert len(result["sources"]) == 1
    assert result['sources'][0]['title'] == "Coop Study"
