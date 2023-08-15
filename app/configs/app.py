from functools import lru_cache
from typing import List, Union
from pydantic import BaseSettings, AnyHttpUrl, validator


class ApplicationSettings(BaseSettings):
    APP_TITLE: str = "CMS"
    APP_DESCRIPTION: str = "simple cms"
    SERVER_PORT: int = 8000

    API_ROOTING_V1: str = "/test_api/v1"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = "config/.env"
        case_sensitive = True


@lru_cache()
def get_app_settings():
    return ApplicationSettings()
