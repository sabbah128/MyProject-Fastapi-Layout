from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings (BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ""
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

if settings.SQLALCHEMY_DATABASE_URL:
    print("Model config is down.")
else:
    print("❌ Environment variable SQLALCHEMY_DATABASE_URL not set or empty.")
    raise ValueError("❌ Environment variable SQLALCHEMY_DATABASE_URL not set or empty.")
