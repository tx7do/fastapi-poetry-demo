from functools import lru_cache

from ..dependencies.pydantic import BaseSettings


class OssSettings(BaseSettings):
    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_UPLOAD_HOST: str = "127.0.0.1:9000"
    MINIO_DOWNLOAD_HOST: str = "127.0.0.1:9000"

    MINIO_ACCESS_KEY: str = "root"
    MINIO_SECRET_KEY: str = "123456"
    MINIO_TOKEN: str = ""
    MINIO_SECURE: bool = False

    class Config:
        env_file = "config/.env"
        case_sensitive = True


@lru_cache()
def get_oss_settings():
    return OssSettings()
