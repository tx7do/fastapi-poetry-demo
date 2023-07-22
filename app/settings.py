import os

from dotenv import load_dotenv

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "CMS")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "simple cms")
SERVER_PORT = os.getenv("APP_TITLE", 8000)

DATABASE_DSN = os.getenv("DATABASE_DSN", "sqlite://db.sqlite3")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
