import magic
import fitz  # PyMuPDF

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_MIME_TYPES = {"application/pdf"}


def validate_pdf(file_bytes: bytes, filename: str) -> None:
    """Raises ValueError if the file is not a valid, safe PDF."""
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only .pdf files are allowed")

    if len(file_bytes) == 0:
        raise ValueError("Uploaded file is empty")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds max size of {MAX_FILE_SIZE // (1024*1024)}MB")

    mime_type = magic.from_buffer(file_bytes, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Invalid file type detected: {mime_type}")


def extract_text_by_page(file_bytes: bytes) -> list[dict]:
    """Returns [{'page_number': 1, 'text': '...'}, ...]. Raises ValueError on corrupt PDFs."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Could not parse PDF: {e}")

    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        pages.append({"page_number": i, "text": text})
    doc.close()
    return pages