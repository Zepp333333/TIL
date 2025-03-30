import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_TOKEN: str | None = os.environ.get("SECRET_TOKEN")


def get_settings() -> Settings:
    return Settings()
