import secrets
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.auth.hashing import hash_api_key
from app.db.models import ApiKey

API_KEY_PREFIX = "rag_"
API_KEY_TOKEN_BYTES = 32
KEY_PREFIX_VISIBLE_CHARS = 12


@dataclass(frozen=True)
class CreatedApiKey:
    raw_key: str
    key_prefix: str
    key_hash: str


def create_api_key() -> CreatedApiKey:
    """Generate a new API key and its persistence-safe artifacts."""
    token = secrets.token_urlsafe(API_KEY_TOKEN_BYTES)
    raw_key = f"{API_KEY_PREFIX}{token}"
    key_prefix = raw_key[:KEY_PREFIX_VISIBLE_CHARS]
    key_hash = hash_api_key(raw_key)

    return CreatedApiKey(raw_key=raw_key, key_prefix=key_prefix, key_hash=key_hash)


def get_active_api_key(db: Session, raw_key: str) -> ApiKey | None:
    """Find an active API key row by hashing the provided raw key."""
    key_hash = hash_api_key(raw_key)
    return (
        db.query(ApiKey)
        .filter(ApiKey.key_hash == key_hash, ApiKey.is_active.is_(True))
        .first()
    )
