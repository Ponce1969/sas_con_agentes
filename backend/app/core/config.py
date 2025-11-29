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

    # --- Database (TODO: Todas desde .env) ---
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    POSTGRES_USER: str = Field(default="neural_user", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="neural_saas_db", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(default="db", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")

    # --- Seguridad JWT ---
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # --- API Keys ---
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", env="GEMINI_MODEL")

    # --- Redis ---
    REDIS_HOST: str = Field(default="redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_URL: str = Field(default="redis://redis:6379/0", env="REDIS_URL")

    # --- Celery ---
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/0", env="CELERY_RESULT_BACKEND")

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

