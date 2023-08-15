from functools import lru_cache
from ..dependencies.pydantic import BaseSettings


class DataBaseSettings(BaseSettings):
    """
    SQLite: sqlite://:memory:
    MySQL: mysql://root:@127.0.0.1:3306/
    PostgreSQL: postgres://postgres:@127.0.0.1:5432/
    """

    DATABASE_DSN: str = "mysql://root:123456@localhost:3306/cms"

    REDIS_URL: str = "redis://localhost:6379/0"

    MONGO_INITDB_ROOT_USERNAME: str = "username"
    MONGO_INITDB_ROOT_PASSWORD: str = "password"
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str = None

    class Config:
        env_file = "config/.env"
        case_sensitive = True


@lru_cache()
def get_db_settings():
    return DataBaseSettings()
