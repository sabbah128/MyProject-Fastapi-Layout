from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated


class Settings (BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ""
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

if not settings.SQLALCHEMY_DATABASE_URL:
    raise ValueError("❌ Environment variable SQLALCHEMY_DATABASE_URL not set or empty.")
