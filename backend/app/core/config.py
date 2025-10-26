# backend/app/core/config.py

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # project_saas/

class Settings(BaseSettings):
    """
    Configuración central de la aplicación SaaS.
    Usa variables de entorno (.env) y valores por defecto.
    """

    # --- Proyecto ---
    PROJECT_NAME: str = "Neural SaaS Platform"
    PROJECT_DESCRIPTION: str = "Plataforma SaaS de Agentes de IA para Python"
    PROJECT_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # --- FastAPI ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # --- Database ---
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    POSTGRES_USER: str = "neural_user"
    POSTGRES_PASSWORD: str = "neural_password_2024"
    POSTGRES_DB: str = "neural_saas_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # --- Seguridad JWT ---
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- API Keys ---
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Modelo más moderno y potente

    # --- Redis ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # --- CORS ---
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from .env (comma-separated)"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501,http://localhost:8502,http://localhost:3000")
        return [origin.strip() for origin in origins_str.split(",")]

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 60

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    # --- Embeddings / Vector DB ---
    VECTOR_DIM: int = 768  # Gemini embedding dimension
    VECTOR_INDEX_PATH: str = str(BASE_DIR / "data" / "vector_index.pkl")

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorar campos extra del .env

# Instancia global de configuración
settings = Settings()

# Helper function para dependency injection
def get_settings() -> Settings:
    return settings

