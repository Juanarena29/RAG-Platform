import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.hashing import hash_api_key
from app.db.models import ApiKey, UsageLog, User

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_user(db: Session, email: str, *, is_active: bool = True) -> User:
    user = User(email=email, is_active=is_active)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_key(db: Session, user_id: int, raw_key: str, *, is_active: bool = True) -> ApiKey:
    key = ApiKey(
        user_id=user_id,
        key_prefix=raw_key[:12],
        key_hash=hash_api_key(raw_key),
        is_active=is_active,
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return key


# ---------------------------------------------------------------------------
# User constraints
# ---------------------------------------------------------------------------


def test_user_email_unique_constraint_raises_on_duplicate(db_session: Session) -> None:
    _make_user(db_session, "dup@test.com")

    db_session.add(User(email="dup@test.com"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_user_email_not_null_constraint_raises_on_null(db_session: Session) -> None:
    db_session.add(User(email=None))  # type: ignore[arg-type]
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


# ---------------------------------------------------------------------------
# User defaults
# ---------------------------------------------------------------------------


def test_user_is_active_defaults_to_true(db_session: Session) -> None:
    user = User(email="defaults@test.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.is_active is True


def test_user_created_at_is_set_automatically(db_session: Session) -> None:
    user = _make_user(db_session, "ts_user@test.com")

    assert user.created_at is not None


# ---------------------------------------------------------------------------
# ApiKey constraints
# ---------------------------------------------------------------------------


def test_api_key_key_hash_unique_constraint_raises_on_duplicate(db_session: Session) -> None:
    user = _make_user(db_session, "hash_unique@test.com")
    raw_key = "rag_hash_unique_test_abc123"
    _make_key(db_session, user.id, raw_key)

    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),  # same hash
            is_active=True,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_api_key_key_hash_not_null_constraint_raises_on_null(db_session: Session) -> None:
    user = _make_user(db_session, "hash_null@test.com")
    db_session.add(ApiKey(user_id=user.id, key_prefix="rag_test", key_hash=None))  # type: ignore[arg-type]
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_api_key_is_active_defaults_to_true(db_session: Session) -> None:
    user = _make_user(db_session, "key_defaults@test.com")
    raw_key = "rag_key_default_active_abc99"

    key = ApiKey(
        user_id=user.id,
        key_prefix=raw_key[:12],
        key_hash=hash_api_key(raw_key),
    )
    db_session.add(key)
    db_session.commit()
    db_session.refresh(key)

    assert key.is_active is True


def test_api_key_created_at_is_set_automatically(db_session: Session) -> None:
    user = _make_user(db_session, "ts_key@test.com")
    key = _make_key(db_session, user.id, "rag_ts_key_test_xyz456abc")

    assert key.created_at is not None


# ---------------------------------------------------------------------------
# Foreign keys (ORM-level relationship integrity)
# ---------------------------------------------------------------------------


def test_api_key_user_id_references_correct_user_via_relationship(
    db_session: Session,
) -> None:
    user = _make_user(db_session, "fk_apikey@test.com")
    key = _make_key(db_session, user.id, "rag_fk_apikey_test_abc123")

    assert key.user_id == user.id
    assert key.user.email == user.email


def test_usage_log_user_id_references_correct_user_via_relationship(
    db_session: Session,
) -> None:
    user = _make_user(db_session, "fk_usagelog@test.com")
    log = UsageLog(user_id=user.id, endpoint="/query")
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    assert log.user_id == user.id
    assert log.user.email == user.email


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------


def test_user_api_keys_relationship_returns_associated_keys(db_session: Session) -> None:
    user = _make_user(db_session, "rel_keys@test.com")
    _make_key(db_session, user.id, "rag_rel_key_one_abc123456")
    _make_key(db_session, user.id, "rag_rel_key_two_def789012")
    db_session.refresh(user)

    assert len(user.api_keys) == 2
    assert all(k.user_id == user.id for k in user.api_keys)


def test_user_usage_logs_relationship_returns_associated_logs(db_session: Session) -> None:
    user = _make_user(db_session, "rel_logs@test.com")
    db_session.add(UsageLog(user_id=user.id, endpoint="/query"))
    db_session.add(UsageLog(user_id=user.id, endpoint="/documents"))
    db_session.commit()
    db_session.refresh(user)

    assert len(user.usage_logs) == 2
    assert all(log.user_id == user.id for log in user.usage_logs)


# ---------------------------------------------------------------------------
# Cascade delete
# ---------------------------------------------------------------------------


def test_deleting_user_cascades_to_api_keys_and_usage_logs(db_session: Session) -> None:
    user = _make_user(db_session, "cascade@test.com")
    key = _make_key(db_session, user.id, "rag_cascade_test_key_xyz789")
    log = UsageLog(user_id=user.id, endpoint="/query")
    db_session.add(log)
    db_session.commit()
    key_id, log_id = key.id, log.id

    db_session.delete(user)
    db_session.commit()

    assert db_session.get(ApiKey, key_id) is None
    assert db_session.get(UsageLog, log_id) is None
