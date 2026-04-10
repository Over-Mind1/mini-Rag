from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    app_name: str
    app_version: str
    app_description: str
    api_key: str
    file_allowed_extensions: list[str]
    file_max_size_mb: int
    file_default_chunk_size: int



@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()