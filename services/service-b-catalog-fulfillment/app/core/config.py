"""Configuration settings for Service B - Catalog & Fulfillment"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # Search
    SEARCH_MIN_SCORE: float = 0.3
    
    # External Services
    NOTIFICATIONS_URL: str
    SERVICE_A_URL: str
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
