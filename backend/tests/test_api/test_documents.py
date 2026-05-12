from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.hashing import hash_api_key
from app.db.models import ApiKey, Document, User


def _auth_header(raw_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {raw_key}"}


def _create_user_with_key(db_session: Session, email: str, raw_key: str) -> User:
    user = User(email=email, is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),
            is_active=True,
        )
    )
    db_session.commit()
    return user


def _drop_task(coro):  # noqa: ANN001
    coro.close()
    return None


def test_upload_requires_auth(client: TestClient) -> None:
    response = client.post(
        "/documents/upload",
        files={"file": ("doc.pdf", b"%PDF-1.4\nx", "application/pdf")},
    )
    assert response.status_code == 401


def test_upload_valid_pdf_returns_202_and_persists_document(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    db_session: Session,
    tmp_path: Path,
    monkeypatch,
) -> None:
    user, raw_key = test_user_with_key
    monkeypatch.setattr("app.api.routes.documents.settings.upload_dir", str(tmp_path))
    monkeypatch.setattr(
        "app.api.routes.documents.asyncio.create_task",
        _drop_task,
    )

    response = client.post(
        "/documents/upload",
        headers=_auth_header(raw_key),
        files={"file": ("paper.pdf", b"%PDF-1.4\nhello", "application/pdf")},
    )
    assert response.status_code == 202
    body = response.json()
    assert "document_id" in body
    assert body["status"] == "pending"

    document = db_session.get(Document, body["document_id"])
    assert document is not None
    assert document.user_id == user.id
    assert document.status == "pending"


def test_upload_invalid_pdf_returns_400(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key
    response = client.post(
        "/documents/upload",
        headers=_auth_header(raw_key),
        files={"file": ("bad.txt", b"not-pdf", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_oversized_pdf_returns_400(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key
    oversized = b"%PDF-" + b"a" * (21 * 1024 * 1024)
    response = client.post(
        "/documents/upload",
        headers=_auth_header(raw_key),
        files={"file": ("large.pdf", oversized, "application/pdf")},
    )
    assert response.status_code == 400


def test_list_documents_is_isolated_per_user(
    client: TestClient, db_session: Session, tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr("app.api.routes.documents.settings.upload_dir", str(tmp_path))
    monkeypatch.setattr(
        "app.api.routes.documents.asyncio.create_task",
        _drop_task,
    )
    user_a = _create_user_with_key(db_session, "a@test.com", "rag_user_a_key_123")
    user_b = _create_user_with_key(db_session, "b@test.com", "rag_user_b_key_456")

    for key in ("rag_user_a_key_123", "rag_user_b_key_456"):
        client.post(
            "/documents/upload",
            headers=_auth_header(key),
            files={"file": ("doc.pdf", b"%PDF-1.4\nhello", "application/pdf")},
        )

    unauth_response = client.get("/documents")
    assert unauth_response.status_code == 401

    response_a = client.get("/documents", headers=_auth_header("rag_user_a_key_123"))
    assert response_a.status_code == 200
    docs_a = response_a.json()["documents"]
    assert len(docs_a) == 1
    assert db_session.get(Document, docs_a[0]["id"]).user_id == user_a.id

    response_b = client.get("/documents", headers=_auth_header("rag_user_b_key_456"))
    assert response_b.status_code == 200
    docs_b = response_b.json()["documents"]
    assert len(docs_b) == 1
    assert db_session.get(Document, docs_b[0]["id"]).user_id == user_b.id
