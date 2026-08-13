from anthropic import Anthropic
from app.core.config import settings

client = Anthropic(api_key=settings.claude_api_key)

MODEL = "claude-sonnet-4-6"


def generate_answer(question: str, chunks: list[dict]) -> dict:
    """
    Takes the user's question and retrieved chunks (each with
    text, doc_id, page_number), asks Claude to answer using ONLY
    those chunks, and returns which chunk indices it actually used.
    """
    if not chunks:
        return {"answer": "I couldn't find anything relevant in your documents.", "used_indices": []}

    context_blocks = []
    for i, c in enumerate(chunks):
        context_blocks.append(
            f"[Chunk {i}] (Page {c['page_number']})\n{c['text']}"
        )
    context_text = "\n\n".join(context_blocks)

    system_prompt = (
        "You are a document Q&A assistant. Answer the user's question "
        "using ONLY the information in the provided chunks. "
        "If the chunks don't contain enough information to answer, say so clearly. "
        "Do not use outside knowledge.\n\n"
        "Respond with STRICT JSON only, no markdown, no preamble, in this exact shape:\n"
        '{"answer": "...", "used_chunks": [0, 2]}\n'
        "used_chunks should list the indices (integers) of the chunks you actually relied on."
    )

    user_message = f"Chunks:\n{context_text}\n\nQuestion: {question}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = response.content[0].text.strip()

    import json
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback if Claude adds stray formatting
        parsed = {"answer": raw_text, "used_chunks": []}

    return {
        "answer": parsed.get("answer", ""),
        "used_indices": parsed.get("used_chunks", []),
    }