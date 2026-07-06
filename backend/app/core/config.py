from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# The .env file lives at the project root (one level above backend/)
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


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
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    default_rate_limit: str = "60/minute"
    query_rate_limit: str = "20/hour"
    openai_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 20
    use_hyde_default: bool = True
    use_query_transform_default: bool = True
    reranker_type: Literal["local", "cohere"] = "local"
    cohere_api_key: str | None = None
    generator_model: str = "gpt-4o-mini"
    openai_chat_input_price_per_1m: float = 0.15
    openai_chat_output_price_per_1m: float = 0.60
    openai_embedding_price_per_1m: float = 0.02
    retriever_top_k: int = 20
    reranker_top_n: int = 5
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = False

    model_config = SettingsConfigDict(
        env_file=str(_ROOT_ENV),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
