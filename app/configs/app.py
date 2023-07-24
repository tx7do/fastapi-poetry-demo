from functools import lru_cache
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    APP_TITLE: str = "CMS"
    APP_DESCRIPTION: str = "simple cms"
    SERVER_PORT: int = 8000

    class Config:
        env_file = ".env.sample"


@lru_cache()
def get_app_settings():
    return ApplicationSettings()
