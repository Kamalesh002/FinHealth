# Backend Configuration
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SME Financial Health Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./financial_health.db")
    
    # Groq API (LLM)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")  # 32-byte key for AES-256
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list = ["csv", "xlsx", "pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # Industry Types
    INDUSTRIES: list = [
        "Manufacturing",
        "Retail", 
        "Agriculture",
        "Services",
        "Logistics",
        "E-commerce"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
