from sentence_transformers import SentenceTransformer

# Not loaded yet - will load on first actual use
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Takes a list of chunk texts, returns a list of embedding vectors
    (same order as input).
    """
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()