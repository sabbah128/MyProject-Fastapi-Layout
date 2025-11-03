from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "test"
    ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

if settings.SQLALCHEMY_DATABASE_URL:
    print("Model config is down.")
else:
    print("❌ Environment variable SQLALCHEMY_DATABASE_URL not set or empty.")
    raise ValueError(
        "❌ Environment variable SQLALCHEMY_DATABASE_URL not set or empty."
    )
