import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from app.core.deps import get_current_user
from app.core.database import documents_collection, chunks_collection
from app.services.pdf_service import validate_pdf, extract_text_by_page
from app.services.chunking_service import chunk_pages

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = os.path.join("storage", "uploads")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    file_bytes = await file.read()

    try:
        validate_pdf(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user_id = str(current_user["_id"])
    doc_id = str(uuid.uuid4())

    # Store file on disk, namespaced by user_id to keep isolation clean
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, f"{doc_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    try:
        pages = extract_text_by_page(file_bytes)
    except ValueError as e:
            os.remove(file_path)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    chunks = chunk_pages(pages)

    doc_record = {
        "_id": doc_id,
        "owner_id": user_id,
        "filename": file.filename,
        "file_path": file_path,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "status": "ready",
        "uploaded_at": datetime.now(timezone.utc),
    }
    documents_collection.insert_one(doc_record)

    chunk_docs = [
        {
            "doc_id": doc_id,
            "owner_id": user_id,
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
        }
        for chunk in chunks
    ]
    if chunk_docs:
        chunks_collection.insert_many(chunk_docs)

    return {
        "id": doc_id,
        "filename": file.filename,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "status": "ready",
        "uploaded_at": doc_record["uploaded_at"],
    }