import os

class Config:
    # No fallback — app must be given a DATABASE_URL explicitly
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable is not set!")

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5500")