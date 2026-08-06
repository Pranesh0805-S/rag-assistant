import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 500       # tokens per chunk
CHUNK_OVERLAP = 50     # tokens of overlap between consecutive chunks


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Takes [{'page_number': 1, 'text': '...'}, ...]
    Returns [{'page_number': 1, 'chunk_index': 0, 'text': '...'}, ...]
    """
    all_chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = page["text"].strip()

        if not text:
            continue  # skip blank pages

        tokens = encoding.encode(text)
        start = 0
        chunk_index = 0

        while start < len(tokens):
            end = min(start + CHUNK_SIZE, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens)

            all_chunks.append({
                "page_number": page_number,
                "chunk_index": chunk_index,
                "text": chunk_text,
            })

            chunk_index += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP  # slide window with overlap

    return all_chunks