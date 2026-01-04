from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    database_url: PostgresDsn
    openai_api_key: SecretStr
    cache_url: RedisDsn

    class Config:
        env_file = ".env"


def get_app_settings() -> AppSettings:
    return AppSettings()  # type: ignore[call-arg]
