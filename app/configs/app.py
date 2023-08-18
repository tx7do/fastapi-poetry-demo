from functools import lru_cache
from typing import List, Union
from pydantic import AnyHttpUrl, Field, field_validator, Extra

from ..dependencies.pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    APP_TITLE: str = Field(default="")
    APP_DESCRIPTION: str = Field(default="")
    DEBUG: bool = Field(default=False)

    SERVER_PORT: int = Field(default=1800)

    API_ROOTING_V1: str = Field(default="")

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default=[])

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = "config/.env"
        case_sensitive = True
        extra = Extra.allow


@lru_cache()
def get_app_settings():
    return ApplicationSettings()
