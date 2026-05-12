import hashlib
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.db.repositories import update_document_status
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import embed_chunks
from app.ingestion.parser import parse_pdf
from app.ingestion.validator import validate_pdf


def _collection_name_for_user(user_id: int) -> str:
    return f"user_{user_id}"


def _point_id(document_id: int, chunk_index: int) -> int:
    digest = hashlib.sha256(f"{document_id}:{chunk_index}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


async def process_document_event(
    *,
    data: dict[str, Any],
    session_factory: sessionmaker[Session],
    settings: Settings,
) -> None:
    document_id = int(data["document_id"])
    user_id = int(data["user_id"])
    file_path = Path(data["file_path"])

    with session_factory() as db:
        update_document_status(db, document_id=document_id, status="processing")

    try:
        content = file_path.read_bytes()
        validate_pdf(
            content,
            filename=file_path.name,
            max_size_bytes=settings.max_upload_size_mb * 1024 * 1024,
        )

        pages = parse_pdf(content)
        chunks = chunk_pages(document_id=document_id, pages=pages)
        embedded_chunks = await embed_chunks(chunks, api_key=settings.openai_api_key)

        client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
        collection_name = _collection_name_for_user(user_id)
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

        points = [
            PointStruct(
                id=_point_id(chunk.document_id, chunk.chunk_index),
                vector=chunk.vector,
                payload={
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "page_number": chunk.page_number,
                    "text": chunk.text,
                    "user_id": user_id,
                },
            )
            for chunk in embedded_chunks
        ]
        if points:
            client.upsert(collection_name=collection_name, points=points)

        with session_factory() as db:
            update_document_status(
                db,
                document_id=document_id,
                status="completed",
                chunk_count=len(embedded_chunks),
                error_message=None,
            )
    except Exception as exc:
        with session_factory() as db:
            update_document_status(
                db,
                document_id=document_id,
                status="failed",
                chunk_count=None,
                error_message=str(exc),
            )
        raise
