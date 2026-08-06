from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentOut(BaseModel):
    id: str
    filename: str
    owner_id: str
    page_count: int
    status: str  # "processing" | "ready" | "failed"
    uploaded_at: datetime