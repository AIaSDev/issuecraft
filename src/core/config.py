"""Configuration management."""
import os


class Config:
    """Application configuration."""
    
    # Database configuration
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./issues.db"
    )
    
    # Support PostgreSQL connection string format
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # API configuration
    API_TITLE = "IssueCraft API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "A minimal FastAPI issue tracker demonstrating Clean Architecture"
