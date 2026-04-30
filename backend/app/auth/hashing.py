import hashlib


def hash_api_key(raw_api_key: str) -> str:
    """Return SHA-256 hex digest for a raw API key."""
    return hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
