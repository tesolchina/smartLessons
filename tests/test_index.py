from pathlib import Path

def test_index_creation_and_search(loaded_indexer):
    results = loaded_indexer.search("cooperative learning", k=3)
    # Expect at least the cooperative learning doc
    titles = [r['title'].lower() for r in results]
    assert any("cooperative" in t for t in titles)
    # Scores should be in non-increasing order
    scores = [r['score'] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_query_no_results(loaded_indexer):
    results = loaded_indexer.search("quantum entanglement", k=3)
    assert len(results) == 0  # should not match synthetic docs
