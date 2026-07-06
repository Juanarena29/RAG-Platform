from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.hashing import hash_api_key
from app.db.models import ApiKey, Document, UsageLog, User
from app.rag.pipeline import PipelineResult
from app.rag.usage import PipelineUsage
from app.schemas.query import Source


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


def test_query_requires_auth(client: TestClient) -> None:
    response = client.post("/query", json={"question": "What is attention?"})
    assert response.status_code == 401


def test_query_invalid_body_returns_422(
    client: TestClient,
    test_user_with_key: tuple[User, str],
) -> None:
    _, raw_key = test_user_with_key
    response = client.post(
        "/query",
        headers=_auth_header(raw_key),
        json={"question": "ab"},
    )
    assert response.status_code == 422


def test_query_success_returns_response_and_logs_usage(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    db_session: Session,
    monkeypatch,
) -> None:
    user, raw_key = test_user_with_key
    document = Document(
        user_id=user.id,
        original_filename="paper.pdf",
        filename="paper.pdf",
        file_path="/tmp/paper.pdf",
        file_size=100,
        status="completed",
    )
    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    async def _fake_run_pipeline(**kwargs):  # noqa: ANN003
        assert kwargs["user_id"] == user.id
        return PipelineResult(
            answer="Attention focuses on relevant tokens.",
            sources=[
                Source(
                    document_id=document.id,
                    original_filename=f"document_{document.id}",
                    page_number=1,
                    text="Attention mechanism",
                    score=0.95,
                )
            ],
            query_used="transformed attention query",
            hyde_used=True,
            query_transform_used=True,
            usage=PipelineUsage(
                prompt_tokens=120,
                completion_tokens=45,
                embedding_tokens=10,
                estimated_cost_usd=0.000045,
            ),
        )

    monkeypatch.setattr("app.api.routes.query.run_pipeline", _fake_run_pipeline)

    response = client.post(
        "/query",
        headers=_auth_header(raw_key),
        json={"question": "What is attention?", "use_hyde": True, "max_sources": 3},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Attention focuses on relevant tokens."
    assert body["hyde_used"] is True
    assert body["sources"][0]["original_filename"] == "paper.pdf"
    assert body["usage"]["prompt_tokens"] == 120
    assert body["usage"]["total_tokens"] == 175
    assert body["usage"]["estimated_cost_usd"] == 0.000045

    usage_logs = db_session.query(UsageLog).filter(UsageLog.endpoint == "/query").all()
    assert len(usage_logs) == 1
    assert usage_logs[0].user_id == user.id


def test_query_pipeline_failure_returns_500(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    monkeypatch,
) -> None:
    _, raw_key = test_user_with_key

    async def _failing_pipeline(**kwargs):  # noqa: ANN003
        raise RuntimeError("pipeline exploded")

    monkeypatch.setattr("app.api.routes.query.run_pipeline", _failing_pipeline)

    response = client.post(
        "/query",
        headers=_auth_header(raw_key),
        json={"question": "What is attention?"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to process query"


def test_query_passes_authenticated_user_id_to_pipeline(
    client: TestClient,
    db_session: Session,
    monkeypatch,
) -> None:
    user_a = _create_user_with_key(db_session, "qa@test.com", "rag_query_user_a_key")
    user_b = _create_user_with_key(db_session, "qb@test.com", "rag_query_user_b_key")
    captured_user_ids: list[int] = []

    async def _capture_pipeline(**kwargs):  # noqa: ANN003
        captured_user_ids.append(kwargs["user_id"])
        return PipelineResult(
            answer="ok",
            sources=[],
            query_used="query",
            hyde_used=False,
            query_transform_used=False,
            usage=PipelineUsage.zero(),
        )

    monkeypatch.setattr("app.api.routes.query.run_pipeline", _capture_pipeline)

    client.post(
        "/query",
        headers=_auth_header("rag_query_user_a_key"),
        json={"question": "Question for user A?"},
    )
    client.post(
        "/query",
        headers=_auth_header("rag_query_user_b_key"),
        json={"question": "Question for user B?"},
    )

    assert captured_user_ids == [user_a.id, user_b.id]


def test_query_passes_feature_flags_to_pipeline(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    monkeypatch,
) -> None:
    _, raw_key = test_user_with_key
    captured: dict[str, bool] = {}

    async def _capture_pipeline(**kwargs):  # noqa: ANN003
        captured["use_hyde"] = kwargs["use_hyde"]
        captured["use_query_transform"] = kwargs["use_query_transform"]
        return PipelineResult(
            answer="ok",
            sources=[],
            query_used="What is attention?",
            hyde_used=kwargs["use_hyde"],
            query_transform_used=kwargs["use_query_transform"],
            usage=PipelineUsage.zero(),
        )

    monkeypatch.setattr("app.api.routes.query.run_pipeline", _capture_pipeline)

    response = client.post(
        "/query",
        headers=_auth_header(raw_key),
        json={
            "question": "What is attention?",
            "use_hyde": False,
            "use_query_transform": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["hyde_used"] is False
    assert body["query_transform_used"] is False
    assert captured == {"use_hyde": False, "use_query_transform": False}
