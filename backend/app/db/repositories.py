from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Document


def create_document(
    db: Session,
    *,
    user_id: int,
    original_filename: str,
    filename: str,
    file_path: str,
    file_size: int,
    status: str = "pending",
) -> Document:
    document = Document(
        user_id=user_id,
        original_filename=original_filename,
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        status=status,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: Session, document_id: int, user_id: int) -> Document | None:
    return (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == user_id)
        .first()
    )


def get_documents_by_ids(
    db: Session,
    user_id: int,
    document_ids: list[int],
) -> list[Document]:
    if not document_ids:
        return []

    return (
        db.query(Document)
        .filter(Document.user_id == user_id, Document.id.in_(document_ids))
        .all()
    )


def get_documents_by_user(db: Session, user_id: int) -> list[Document]:
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )


def update_document_status(
    db: Session,
    *,
    document_id: int,
    status: str,
    chunk_count: int | None = None,
    error_message: str | None = None,
) -> Document | None:
    document = db.get(Document, document_id)
    if not document:
        return None

    document.status = status
    document.chunk_count = chunk_count
    document.error_message = error_message
    if status == "completed":
        document.processed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(document)
    return document
