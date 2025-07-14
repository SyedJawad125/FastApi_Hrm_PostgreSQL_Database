from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # Database configuration
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./hrms.db"
    
    # Authentication
    # SECRET_KEY: str = "your-secret-key-here"
    SECRET_KEY: str = "super-secret-fastapi-key-1255"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()