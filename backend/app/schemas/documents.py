from datetime import datetime
from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: int
    original_filename: str
    status: str
    message: str


class DocumentStatus(BaseModel):
    id: int
    original_filename: str
    status: str
    chunk_count: int | None = None
    created_at: datetime
    processed_at: datetime | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentStatus]
