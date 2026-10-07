from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PocketSmart AI"
    app_env: str = "development"
    secret_key: str = "change-this-to-a-long-random-secret"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    gemini_enabled: bool = True
    mock_recommendations: bool = False
    max_upload_mb: int = 5


settings = Settings()
