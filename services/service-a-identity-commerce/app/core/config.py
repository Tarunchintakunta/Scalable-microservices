"""Configuration settings for Service A - Identity & Commerce"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MIN: int = 60
    
    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # External Services
    NOTIFICATIONS_URL: str
    FRONTEND_URL: str
    SERVICE_B_URL: str
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
