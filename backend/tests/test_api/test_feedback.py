from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import UsageLog, User
from app.rag.pipeline import PipelineResult
from app.rag.usage import PipelineUsage


def _auth_header(raw_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {raw_key}"}


def test_feedback_requires_auth(client: TestClient) -> None:
    response = client.post(
        "/feedback",
        json={"trace_id": "trace-123", "value": "positive"},
    )
    assert response.status_code == 401


def test_feedback_records_usage_log(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    db_session: Session,
    monkeypatch,
) -> None:
    _, raw_key = test_user_with_key
    captured: dict[str, object] = {}

    class _FakeLangfuse:
        def create_score(self, **kwargs: object) -> None:
            captured.update(kwargs)

        def flush(self) -> None:
            captured["flushed"] = True

    monkeypatch.setattr("app.api.routes.feedback.get_langfuse", lambda: _FakeLangfuse())

    response = client.post(
        "/feedback",
        headers=_auth_header(raw_key),
        json={
            "trace_id": "trace-abc-123",
            "value": "negative",
            "comment": "Missing citation",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "recorded"
    assert captured["trace_id"] == "trace-abc-123"
    assert captured["name"] == "user_feedback"
    assert captured["value"] == 0.0
    assert captured["flushed"] is True

    usage_logs = db_session.query(UsageLog).filter(UsageLog.endpoint == "/feedback").all()
    assert len(usage_logs) == 1
    assert "trace-abc-123" in usage_logs[0].detail


def test_query_returns_trace_id(
    client: TestClient,
    test_user_with_key: tuple[User, str],
    monkeypatch,
) -> None:
    _, raw_key = test_user_with_key

    async def _fake_run_pipeline(**kwargs):  # noqa: ANN003
        return PipelineResult(
            answer="ok",
            sources=[],
            query_used="query",
            hyde_used=False,
            query_transform_used=True,
            usage=PipelineUsage.zero(),
        )

    monkeypatch.setattr("app.api.routes.query.run_pipeline", _fake_run_pipeline)

    response = client.post(
        "/query",
        headers=_auth_header(raw_key),
        json={"question": "What is attention?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["trace_id"] is not None
    assert response.headers.get("X-Request-ID") == body["trace_id"]
