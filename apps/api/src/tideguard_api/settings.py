"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized configuration for the API service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite+aiosqlite:///./tideguard_dev.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000", "https://tideguard.app"]

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    jwt_secret: str = "dev-secret-change-me"

    s3_endpoint: str = ""
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_bucket_data: str = "tideguard-data"
    s3_bucket_photos: str = "tideguard-photos"

    pinn_checkpoint_path: str = "checkpoints/pinn_v1.pt"
    sentry_dsn: str = ""
    rate_limit_per_minute: int = 60


def get_settings() -> Settings:
    return Settings()
