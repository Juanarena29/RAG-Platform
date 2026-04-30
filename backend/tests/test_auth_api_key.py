from app.auth.api_key import (
    API_KEY_PREFIX,
    KEY_PREFIX_VISIBLE_CHARS,
    create_api_key,
)
from app.auth.hashing import hash_api_key


def test_hash_api_key_is_sha256_hex() -> None:
    hashed = hash_api_key("rag_test_key")

    assert len(hashed) == 64
    assert all(char in "0123456789abcdef" for char in hashed)


def test_same_input_always_produces_same_hash() -> None:
    assert hash_api_key("rag_test_key") == hash_api_key("rag_test_key")


def test_different_inputs_produce_different_hashes() -> None:
    assert hash_api_key("rag_key_a") != hash_api_key("rag_key_b")


def test_create_api_key_returns_expected_artifacts() -> None:
    created = create_api_key()

    assert created.raw_key.startswith(API_KEY_PREFIX)
    assert created.key_prefix == created.raw_key[:KEY_PREFIX_VISIBLE_CHARS]
    assert created.key_hash == hash_api_key(created.raw_key)


def test_create_api_key_is_unique_each_call() -> None:
    assert create_api_key().raw_key != create_api_key().raw_key
