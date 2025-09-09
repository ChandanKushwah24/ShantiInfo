import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://postgres:root@localhost:5432/hotelDB"
    # database_url: str = "sqlite:///./hotelDB.db"
    
    # API settings
    api_title: str = "Hotel Management API"
    api_description: str = "Professional REST API for hotel management with smart booking system"
    api_version: str = "1.0.0"
    
    # Security
    secret_key: str = "hotel-management-secret-key-2024"
    
    class Config:
        env_file = ".env"

settings = Settings()
