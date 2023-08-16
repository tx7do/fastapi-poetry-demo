from functools import lru_cache
from typing import Union

from pydantic import Extra, RedisDsn, Field, MariaDBDsn, MySQLDsn, PostgresDsn, MongoDsn

from ..dependencies.pydantic import BaseSettings


class DataBaseSettings(BaseSettings):
    """
    SQLite: sqlite://:memory:
    MySQL: mysql://root:@127.0.0.1:3306/
    PostgreSQL: postgres://postgres:@127.0.0.1:5432/
    """

    DATABASE_DSN: Union[MariaDBDsn, MySQLDsn, PostgresDsn, MongoDsn] = Field(default="")

    REDIS_URL: RedisDsn = Field(default="redis://localhost:6379/0")

    class Config:
        env_file = "config/.env"
        case_sensitive = True
        extra = Extra.allow


@lru_cache()
def get_db_settings():
    return DataBaseSettings()
