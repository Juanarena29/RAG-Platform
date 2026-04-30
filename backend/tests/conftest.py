from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.hashing import hash_api_key
from app.db.database import Base, get_db
from app.db.models import ApiKey, User
from app.main import app


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield session
    session.close()
    app.dependency_overrides.clear()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def test_user_with_key(db_session: Session) -> tuple[User, str]:
    user = User(email="test@example.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    raw_key = "rag_test_fixture_key_abc123"
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),
            is_active=True,
        )
    )
    db_session.commit()
    return user, raw_key


@pytest.fixture()
def inactive_user(db_session: Session) -> tuple[User, str]:
    """Active key pointing to an inactive user — should never authenticate."""
    user = User(email="inactive_user@example.com", is_active=False)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    raw_key = "rag_inactive_user_key_abc999def"
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),
            is_active=True,
        )
    )
    db_session.commit()
    return user, raw_key


@pytest.fixture()
def inactive_key(db_session: Session) -> tuple[User, str]:
    """Inactive key for an active user — should never authenticate."""
    user = User(email="inactive_key@example.com", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    raw_key = "rag_inactive_key_xyz456defgh"
    db_session.add(
        ApiKey(
            user_id=user.id,
            key_prefix=raw_key[:12],
            key_hash=hash_api_key(raw_key),
            is_active=False,
        )
    )
    db_session.commit()
    return user, raw_key


def _clear_limiter_storage() -> None:
    """Reset in-memory rate limit counters.

    limiter._storage is a MemoryStorage instance (limits 5.x).
    """
    from app.api.middleware import limiter

    storage = getattr(limiter, "_storage", None)
    if storage is None:
        return
    reset_fn = getattr(storage, "reset", None) or getattr(
        getattr(storage, "storage", None), "reset", None
    )
    if reset_fn is not None:
        try:
            reset_fn()
        except Exception:
            pass


@pytest.fixture(autouse=True)
def reset_rate_limiter() -> Generator[None, None, None]:
    _clear_limiter_storage()
    yield
    _clear_limiter_storage()
