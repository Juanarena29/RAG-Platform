import asyncio
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.middleware import limiter
from app.core.config import get_settings
from app.db.database import SessionLocal, get_db
from app.db.models import UsageLog, User
from app.db.repositories import create_document, get_documents_by_user
from app.ingestion.ingestion_worker import process_document_event
from app.ingestion.validator import DocumentValidationError, validate_pdf
from app.schemas.documents import DocumentListResponse, DocumentStatus, UploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])
settings = get_settings()
MAX_SIZE_BYTES = settings.max_upload_size_mb * 1024 * 1024


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/hour")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UploadResponse:
    content = await file.read()
    filename = file.filename or "document.pdf"

    try:
        validate_pdf(content, filename=filename, max_size_bytes=MAX_SIZE_BYTES)
    except DocumentValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc

    user_dir = Path(settings.upload_dir) / f"user_{current_user.id}"
    user_dir.mkdir(parents=True, exist_ok=True)
    safe_filename = f"{uuid4()}.pdf"
    file_path = user_dir / safe_filename
    file_path.write_bytes(content)

    document = create_document(
        db,
        user_id=current_user.id,
        original_filename=filename,
        filename=safe_filename,
        file_path=str(file_path.resolve()),
        file_size=len(content),
    )
    db.add(
        UsageLog(
            user_id=current_user.id,
            endpoint="/documents/upload",
            status_code=status.HTTP_202_ACCEPTED,
            detail=f"document_id={document.id}",
        )
    )
    db.commit()

    asyncio.create_task(
        process_document_event(
            data={
                "document_id": document.id,
                "user_id": current_user.id,
                "file_path": str(file_path.resolve()),
            },
            session_factory=SessionLocal,
            settings=settings,
        )
    )

    return UploadResponse(
        document_id=document.id,
        original_filename=document.original_filename,
        status=document.status,
        message="Document accepted for asynchronous processing",
    )


@router.get("", response_model=DocumentListResponse)
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentListResponse:
    documents = get_documents_by_user(db, current_user.id)
    return DocumentListResponse(
        documents=[
            DocumentStatus(
                id=document.id,
                original_filename=document.original_filename,
                status=document.status,
                chunk_count=document.chunk_count,
                created_at=document.created_at,
                processed_at=document.processed_at,
            )
            for document in documents
        ]
    )
