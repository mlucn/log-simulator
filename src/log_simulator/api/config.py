"""API configuration settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    app_name: str = "Log Simulator API"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8080

    # CORS Settings
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    # Rate Limiting (disabled by default - can be enabled via env var)
    rate_limit_enabled: bool = False
    rate_limit_default: str = "10/minute"  # Default rate limit
    rate_limit_generate: str = "5/minute"  # Stricter for generation

    # Generation Limits
    max_log_count: int = 10000  # Max logs per request
    max_time_spread: int = 86400  # Max time spread in seconds (24 hours)

    # Schema Settings
    schemas_dir: Path = Path(__file__).parent.parent / "schemas"

    class Config:
        """Pydantic config."""

        env_prefix = "LOG_SIM_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
