from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define las configuraciones de la aplicación."""

    environment: str = "dev"
    app_name: str = "RAG Platform API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True
    database_url: str = "sqlite:///./rag_platform.db"
    cors_allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    default_rate_limit: str = "60/minute"
    openai_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    inngest_event_key: str = "test"
    inngest_signing_key: str | None = None
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
