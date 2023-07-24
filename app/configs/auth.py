from functools import lru_cache
from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    AUTH_SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 720

    class Config:
        env_file = ".env.sample"


@lru_cache()
def get_auth_settings():
    return AuthSettings()
