from scripts.index import SimpleEmbedding

def test_simple_embedding_vector_shape():
    model = SimpleEmbedding()
    docs = ["alpha beta beta", "beta gamma", "delta alpha"]
    emb = model.fit_transform(docs)
    assert emb.shape[0] == 3
    assert emb.shape[1] > 0
    # Ensure variance (not all zeros / identical)
    assert (emb.sum(axis=1) > 0).all()
