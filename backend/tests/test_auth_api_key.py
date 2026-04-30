import pytest
from sqlalchemy.orm import Session

from app.auth.api_key import (
    API_KEY_PREFIX,
    API_KEY_TOKEN_BYTES,
    KEY_PREFIX_VISIBLE_CHARS,
    create_api_key,
    get_active_api_key,
)
from app.auth.hashing import hash_api_key
from app.db.models import ApiKey, User

# ---------------------------------------------------------------------------
# hash_api_key
# ---------------------------------------------------------------------------


def test_hash_api_key_is_sha256_hex() -> None:
    hashed = hash_api_key("rag_test_key")

    assert len(hashed) == 64
    assert all(char in "0123456789abcdef" for char in hashed)


def test_same_input_always_produces_same_hash() -> None:
    assert hash_api_key("rag_test_key") == hash_api_key("rag_test_key")


def test_different_inputs_produce_different_hashes() -> None:
    assert hash_api_key("rag_key_a") != hash_api_key("rag_key_b")


# ---------------------------------------------------------------------------
# create_api_key — artifacts and format
# ---------------------------------------------------------------------------


def test_create_api_key_returns_expected_artifacts() -> None:
    created = create_api_key()

    assert created.raw_key.startswith(API_KEY_PREFIX)
    assert created.key_prefix == created.raw_key[:KEY_PREFIX_VISIBLE_CHARS]
    assert created.key_hash == hash_api_key(created.raw_key)


def test_create_api_key_is_unique_each_call() -> None:
    assert create_api_key().raw_key != create_api_key().raw_key


def test_create_api_key_raw_key_starts_with_rag_prefix() -> None:
    key = create_api_key()

    assert key.raw_key.startswith("rag_")


def test_create_api_key_has_minimum_expected_length() -> None:
    # "rag_" (4 chars) + secrets.token_urlsafe(API_KEY_TOKEN_BYTES)
    # token_urlsafe(n) produces ceil(n * 4/3) URL-safe base64 chars.
    import math

    min_token_chars = math.ceil(API_KEY_TOKEN_BYTES * 4 / 3)
    expected_min = len(API_KEY_PREFIX) + min_token_chars

    assert len(create_api_key().raw_key) >= expected_min


# ---------------------------------------------------------------------------
# get_active_api_key — DB lookups
# ---------------------------------------------------------------------------


def test_get_active_api_key_returns_record_when_hash_matches_and_key_is_active(
    db_session: Session,
) -> None:
    user = User(email="lookup_active@test.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    raw_key = "rag_lookup_active_key_abc123def"
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:KEY_PREFIX_VISIBLE_CHARS],
            key_hash=hash_api_key(raw_key),
            is_active=True,
        )
    )
    db_session.commit()

    result = get_active_api_key(db=db_session, raw_key=raw_key)

    assert result is not None
    assert result.user_id == user.id
    assert result.key_hash == hash_api_key(raw_key)


def test_get_active_api_key_returns_none_when_key_is_inactive(
    db_session: Session,
) -> None:
    user = User(email="lookup_inactive@test.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    raw_key = "rag_lookup_inactive_key_xyz456"
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:KEY_PREFIX_VISIBLE_CHARS],
            key_hash=hash_api_key(raw_key),
            is_active=False,
        )
    )
    db_session.commit()

    result = get_active_api_key(db=db_session, raw_key=raw_key)

    assert result is None


def test_get_active_api_key_returns_none_when_key_does_not_exist(
    db_session: Session,
) -> None:
    result = get_active_api_key(db=db_session, raw_key="rag_completely_unknown_key_000")

    assert result is None
