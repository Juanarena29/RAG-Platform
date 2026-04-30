import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------


def test_settings_defaults_load() -> None:
    settings = Settings()

    assert settings.environment == "dev"
    assert settings.app_name == "RAG Platform API"
    assert settings.app_version == "0.1.0"


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------


def test_get_settings_is_cached() -> None:
    first = get_settings()
    second = get_settings()

    assert first is second


# ---------------------------------------------------------------------------
# Precedence: env vars override .env file defaults
# ---------------------------------------------------------------------------


def test_env_variable_overrides_default_for_environment_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")

    settings = Settings()

    assert settings.environment == "production"


def test_env_variable_overrides_default_for_debug_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEBUG", "false")

    settings = Settings()

    assert settings.debug is False


# ---------------------------------------------------------------------------
# Invalid types
# ---------------------------------------------------------------------------


def test_settings_raises_validation_error_on_invalid_debug_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEBUG", "not_a_bool")

    with pytest.raises(ValidationError):
        Settings()


# ---------------------------------------------------------------------------
# List parsing from env
# ---------------------------------------------------------------------------


def test_settings_parses_cors_allowed_origins_from_json_array_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        '["http://example.com", "http://custom.test"]',
    )

    settings = Settings()

    assert "http://example.com" in settings.cors_allowed_origins
    assert "http://custom.test" in settings.cors_allowed_origins
    # default origins must not bleed in when env var is set
    assert "http://localhost:3000" not in settings.cors_allowed_origins
