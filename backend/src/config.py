from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:3000"]
    jwt_secret: str = "change-me"
    jwt_algorithm: str
    jwt_expires_minutes: int = 8 * 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
