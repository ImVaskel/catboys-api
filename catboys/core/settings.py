from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_url: PostgresDsn
    submission_channel_id: int

    token: str
    bot_prefix: str = "$"


settings = Settings()
