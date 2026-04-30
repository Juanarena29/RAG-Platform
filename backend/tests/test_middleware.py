from fastapi.testclient import TestClient

from app.db.models import User
from app.main import app

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------


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


def test_cors_does_not_set_allow_origin_header_for_unknown_origin() -> None:
    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    # Starlette CORSMiddleware returns 400 and omits the header for
    # origins that are not in the allow-list.
    assert response.headers.get("access-control-allow-origin") is None


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------


def test_rate_limit_first_sixty_requests_all_return_200(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key
    headers = {"Authorization": f"Bearer {raw_key}"}

    for i in range(60):
        response = client.get("/me", headers=headers)
        assert response.status_code == 200, (
            f"Request {i + 1}/60 should be 200, got {response.status_code}"
        )


def test_rate_limit_sixty_first_request_returns_429(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key
    headers = {"Authorization": f"Bearer {raw_key}"}

    for _ in range(60):
        client.get("/me", headers=headers)

    response = client.get("/me", headers=headers)

    assert response.status_code == 429


def test_rate_limit_429_response_is_valid_json_with_error_field(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    _, raw_key = test_user_with_key
    headers = {"Authorization": f"Bearer {raw_key}"}

    for _ in range(61):
        response = client.get("/me", headers=headers)

    assert response.status_code == 429
    body = response.json()
    assert isinstance(body, dict)
    # slowapi's default handler returns {"error": "Rate limit exceeded: ..."}
    assert "error" in body or "detail" in body
