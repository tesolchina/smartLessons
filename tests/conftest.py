import os
import tempfile
from pathlib import Path
import pytest
import textwrap
import json

# Adjust import path for project modules (ZoteroPDF project area)
PROJECT_ROOT = Path(__file__).parent.parent / "projects" / "ZoteroPDF"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
import sys
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(SCRIPTS_DIR))

from scripts.index import AcademicIndexer  # noqa: E402

@pytest.fixture(scope="session")
def synthetic_docs(tmp_path_factory):
    """Create a tiny synthetic annotated_data folder with front matter YAML.
    Returns path to directory.
    """
    base = tmp_path_factory.mktemp("annotated")
    docs_dir = base / "batch_000"
    docs_dir.mkdir()
    # Minimal front matter + content
    samples = [
        ("doc1.md", textwrap.dedent("""---\ntitle: Cooperative Learning Strategies\nauthors: ["Johnson", "Johnson"]\npublication_year: 2013\ntags: [education, collaboration]\n---\nCooperative learning improves group outcomes and social interdependence.\n""")),
        ("doc2.md", textwrap.dedent("""---\ntitle: Metacognitive Regulation in Study\nauthors: ["Zimmerman"]\npublication_year: 2011\ntags: [metacognition, self-regulation]\n---\nMetacognitive strategies enhance self-regulated learning performance.\n""")),
        ("doc3.md", textwrap.dedent("""---\ntitle: Null Effects of Surface Processing\nauthors: ["Doe"]\npublication_year: 2020\ntags: [memory]\n---\nShallow processing yields limited long-term retention improvements.\n""")),
    ]
    for name, content in samples:
        (docs_dir / name).write_text(content, encoding='utf-8')
    return docs_dir

@pytest.fixture()
def built_index(tmp_path, synthetic_docs):
    index_dir = tmp_path / "faiss_index"
    indexer = AcademicIndexer()
    indexer.create_index(Path(synthetic_docs), index_dir)
    return index_dir

@pytest.fixture()
def loaded_indexer(built_index):
    indexer = AcademicIndexer()
    indexer.load_index(built_index)
    return indexer
