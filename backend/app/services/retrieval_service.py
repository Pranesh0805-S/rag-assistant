from app.services.embedding_service import embed_texts
from app.core.vectorstore import document_chunks_collection

def retrieve_chunks(query: str, user_id: str, top_k: int = 5) -> list[dict]:
    """
    Embeds the query and returns the top_k most relevant chunks
    belonging to this user only.
    """
    query_embedding = embed_texts([query])[0]

    results = document_chunks_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"user_id": user_id},  # server-side isolation, never trust client
    )

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "doc_id": metadata["doc_id"],
            "page_number": metadata["page_number"],
            "distance": distance,
        })
    return chunks