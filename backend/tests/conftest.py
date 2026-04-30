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
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()

    def override_get_db():
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
