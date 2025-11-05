"""Configuration settings for Service A - Identity & Commerce"""
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database - can be provided as full URL or individual parameters
    DATABASE_URL: str
    DB_HOST: str | None = None
    DB_PORT: int = 5432
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str = "ecom_identity_commerce"
    
    @model_validator(mode='before')
    @classmethod
    def build_database_url(cls, data):
        """Construct DATABASE_URL from individual parameters if not provided"""
        if isinstance(data, dict):
            database_url = data.get('DATABASE_URL', '').strip()
            if not database_url:
                if all([data.get('DB_HOST'), data.get('DB_USER'), data.get('DB_PASSWORD')]):
                    password = quote_plus(str(data['DB_PASSWORD']))
                    db_name = data.get('DB_NAME', 'ecom_identity_commerce')
                    db_port = data.get('DB_PORT', 5432)
                    data['DATABASE_URL'] = f"postgresql+psycopg://{data['DB_USER']}:{password}@{data['DB_HOST']}:{db_port}/{db_name}"
        return data
    
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
