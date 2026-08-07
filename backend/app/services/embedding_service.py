from sentence_transformers import SentenceTransformer

# Loaded once at import time - reused across requests
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Takes a list of chunk texts, returns a list of embedding vectors
    (same order as input).
    """
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()