import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

API_TITLE = "IssueCraft API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "A minimal FastAPI issue tracker demonstrating Clean Architecture"