import chromadb

# Persistent local Chroma client - stores data on disk under storage/chroma
chroma_client = chromadb.PersistentClient(path="storage/chroma")

# Single shared collection for all users.
# Isolation is enforced via "user_id" in metadata on every insert/query -
# never trust a user_id from the frontend, always use the one from the JWT.
document_chunks_collection = chroma_client.get_or_create_collection(
    name="document_chunks"
)