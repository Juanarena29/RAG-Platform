from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.hashing import hash_api_key
from app.db.models import ApiKey, User


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


# --- scheme / format edge cases ---


def test_non_bearer_auth_scheme_returns_401_with_detail(client: TestClient) -> None:
    response = client.get("/me", headers={"Authorization": "Token rag_some_key_abc"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization scheme"


def test_bearer_prefix_with_only_spaces_returns_401_with_detail(
    client: TestClient,
) -> None:
    response = client.get("/me", headers={"Authorization": "Bearer    "})

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing API key"


def test_bearer_prefix_without_any_value_returns_401_with_detail(
    client: TestClient,
) -> None:
    response = client.get("/me", headers={"Authorization": "Bearer"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization scheme"


# --- credential state edge cases ---


def test_inactive_api_key_returns_401(
    client: TestClient, inactive_key: tuple[User, str]
) -> None:
    _, raw_key = inactive_key

    response = client.get("/me", headers={"Authorization": f"Bearer {raw_key}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_inactive_user_returns_401(
    client: TestClient, inactive_user: tuple[User, str]
) -> None:
    _, raw_key = inactive_user

    response = client.get("/me", headers={"Authorization": f"Bearer {raw_key}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid user"


def test_valid_key_pointing_to_nonexistent_user_returns_401(
    client: TestClient, db_session: Session
) -> None:
    raw_key = "rag_orphan_key_for_ghost_user_xyz"
    # SQLite does not enforce FK by default — insert a key referencing a
    # user_id that does not exist so we can test the user-lookup guard.
    db_session.add(
        ApiKey(
            user_id=99999,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),
            is_active=True,
        )
    )
    db_session.commit()

    response = client.get("/me", headers={"Authorization": f"Bearer {raw_key}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid user"
