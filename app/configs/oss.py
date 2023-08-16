from functools import lru_cache

from pydantic import Field, Extra

from ..dependencies.pydantic import BaseSettings


class OssSettings(BaseSettings):
    MINIO_ENDPOINT: str = Field(default="127.0.0.1:9000")
    MINIO_UPLOAD_HOST: str = Field(default="127.0.0.1:9000")
    MINIO_DOWNLOAD_HOST: str = Field(default="127.0.0.1:9000")

    MINIO_ACCESS_KEY: str = Field(default="root")
    MINIO_SECRET_KEY: str = Field(default="@Abcd123456")
    MINIO_TOKEN: str = Field(default="")
    MINIO_SECURE: bool = Field(default=False)

    class Config:
        env_file = "config/.env"
        case_sensitive = True
        extra = Extra.allow


@lru_cache()
def get_oss_settings():
    return OssSettings()
