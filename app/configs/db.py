from functools import lru_cache
from pydantic import BaseSettings


class DataBaseSettings(BaseSettings):
    """
     SQLite: sqlite://:memory:
     MySQL: mysql://root:@127.0.0.1:3306/
     PostgreSQL: postgres://postgres:@127.0.0.1:5432/
    """
    DATABASE_DSN: str = "sqlite://db.sqlite3"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env.sample"


@lru_cache()
def get_db_settings():
    return DataBaseSettings()
