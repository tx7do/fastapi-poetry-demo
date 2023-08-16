import secrets
from functools import lru_cache
from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    AUTH_SECRET_KEY: str = secrets.token_urlsafe(32)
    AUTH_ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_DAYS: float = 6 * 24 * 8

    class Config:
        env_file = "config/.env"
        case_sensitive = True
        extra = Extra.allow


@lru_cache()
def get_auth_settings():
    return AuthSettings()
