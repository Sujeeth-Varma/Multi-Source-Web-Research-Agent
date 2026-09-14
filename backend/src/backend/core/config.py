from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys & Model
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    SERPER_API_KEY: str = ""



    
    # Observability
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    LANGFUSE_BASE_URL: Optional[str] = None

    def get_langfuse_host(self) -> str:
        return self.LANGFUSE_BASE_URL or self.LANGFUSE_HOST or "https://cloud.langfuse.com"

    
    # Research & Retrieval Limits
    MAX_PLANNING_QUERIES: int = 4
    MAX_SEARCH_RESULTS_PER_QUERY: int = 5
    MAX_SOURCES_TO_FETCH: int = 8
    HTTP_TIMEOUT_SECONDS: float = 10.0
    MAX_CONTENT_BYTES: int = 500_000  # 500 KB limit per fetched page
    
    # Log level
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
