from app.core.config import Settings, get_settings


# Test de configuración
def test_settings_defaults_load() -> None:
    settings = Settings()

    assert settings.environment == "dev"
    assert settings.app_name == "RAG Platform API"
    assert settings.app_version == "0.1.0"

# Test de caché de configuración
def test_get_settings_is_cached() -> None:
    """Testea que la configuración se cachea correctamente."""
    first = get_settings()
    second = get_settings()

    assert first is second
