from fastapi.testclient import TestClient

from app.db.models import User


def test_valid_api_key_returns_200(
    client: TestClient, test_user_with_key: tuple[User, str]
) -> None:
    user, raw_key = test_user_with_key

    response = client.get("/me", headers={"Authorization": f"Bearer {raw_key}"})

    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_invalid_api_key_returns_401(client: TestClient) -> None:
    response = client.get("/me", headers={"Authorization": "Bearer rag_invalid_key"})

    assert response.status_code == 401


def test_missing_header_returns_401(client: TestClient) -> None:
    response = client.get("/me")

    assert response.status_code == 401
