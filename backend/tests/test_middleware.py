from fastapi.testclient import TestClient

from app.db.models import User
from app.main import app


def test_cors_allows_localhost_origin() -> None:
    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_rate_limit_returns_429_after_limit(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key

    status_codes: list[int] = []
    for _ in range(61):
        response = client.get("/me", headers={"Authorization": f"Bearer {raw_key}"})
        status_codes.append(response.status_code)

    assert 429 in status_codes
