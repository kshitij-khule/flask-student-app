import os

class Config:
    # Database — reads from env var, falls back to local SQLite for now
    # We'll change this to PostgreSQL when we add Compose
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/students.db")
    
    # Secret key for JWT auth (we'll use this in Step 3)
    # No fallback — app should refuse to start without this in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # CORS — which frontend is allowed to talk to this API
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5500")