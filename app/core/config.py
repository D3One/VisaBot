from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="visa-bot-safe", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    storage_path: str = Field(default="data/status_store.json", alias="STORAGE_PATH")

    # Preferred env var: BOT_TOKEN, per the Telegram-focused API patch.
    telegram_bot_token: str | None = Field(default=None, alias="BOT_TOKEN")

    # Backwards-compatible fallback for earlier scaffold versions.
    telegram_bot_token_legacy: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")

    @property
    def bot_token(self) -> str | None:
        return self.telegram_bot_token or self.telegram_bot_token_legacy


@lru_cache
def get_settings() -> Settings:
    return Settings()
