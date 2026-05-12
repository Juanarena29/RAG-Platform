import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy.orm import Session, sessionmaker

import app.ingestion.inngest_functions as workflow_module
from app.db.models import Document, User
from app.ingestion.embedder import EmbeddedChunk


class _FakeQdrantClient:
    def __init__(self, url: str, api_key: str | None = None) -> None:
        self.url = url
        self.api_key = api_key
        self.collections: set[str] = set()
        self.points_written = 0

    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in self.collections

    def create_collection(self, collection_name: str, vectors_config) -> None:  # noqa: ANN001
        self.collections.add(collection_name)

    def upsert(self, collection_name: str, points) -> None:  # noqa: ANN001
        self.collections.add(collection_name)
        self.points_written += len(points)


def _settings(upload_dir: Path) -> SimpleNamespace:
    return SimpleNamespace(
        max_upload_size_mb=20,
        openai_api_key="test-openai-key",
        qdrant_url="http://localhost:6333",
        qdrant_api_key=None,
        upload_dir=str(upload_dir),
    )


def _session_factory(db_session: Session) -> sessionmaker:
    return sessionmaker(bind=db_session.get_bind(), autoflush=False, autocommit=False)


def test_process_document_event_completes_document(
    monkeypatch, tmp_path: Path, db_session: Session
) -> None:
    user = User(email="workflow_ok@test.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    file_path = tmp_path / "doc.pdf"
    file_path.write_bytes(b"%PDF-1.4\ncontent")
    document = Document(
        user_id=user.id,
        original_filename="doc.pdf",
        filename="doc.pdf",
        file_path=str(file_path),
        file_size=file_path.stat().st_size,
        status="pending",
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    monkeypatch.setattr(
        workflow_module,
        "parse_pdf",
        lambda _content: [SimpleNamespace(page_number=0, text="parsed text")],
    )
    monkeypatch.setattr(
        workflow_module,
        "embed_chunks",
        lambda chunks, api_key: asyncio.sleep(
            0,
            result=[
                EmbeddedChunk(
                    document_id=chunks[0].document_id,
                    chunk_index=chunks[0].chunk_index,
                    page_number=chunks[0].page_number,
                    text=chunks[0].text,
                    vector=[0.2] * 1536,
                )
            ],
        ),
    )
    monkeypatch.setattr(workflow_module, "QdrantClient", _FakeQdrantClient)

    asyncio.run(
        workflow_module.process_document_event(
            data={"document_id": document.id, "user_id": user.id, "file_path": str(file_path)},
            session_factory=_session_factory(db_session),
            settings=_settings(tmp_path),
        )
    )

    db_session.expire_all()
    refreshed = db_session.get(Document, document.id)
    assert refreshed is not None
    assert refreshed.status == "completed"
    assert refreshed.chunk_count == 1
    assert refreshed.error_message is None


def test_process_document_event_marks_failed_on_error(
    monkeypatch, tmp_path: Path, db_session: Session
) -> None:
    user = User(email="workflow_fail@test.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    file_path = tmp_path / "doc-fail.pdf"
    file_path.write_bytes(b"%PDF-1.4\ncontent")
    document = Document(
        user_id=user.id,
        original_filename="doc-fail.pdf",
        filename="doc-fail.pdf",
        file_path=str(file_path),
        file_size=file_path.stat().st_size,
        status="pending",
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    monkeypatch.setattr(
        workflow_module,
        "parse_pdf",
        lambda _content: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    with pytest.raises(RuntimeError):
        asyncio.run(
            workflow_module.process_document_event(
                data={"document_id": document.id, "user_id": user.id, "file_path": str(file_path)},
                session_factory=_session_factory(db_session),
                settings=_settings(tmp_path),
            )
        )

    db_session.expire_all()
    refreshed = db_session.get(Document, document.id)
    assert refreshed is not None
    assert refreshed.status == "failed"
    assert refreshed.error_message is not None
