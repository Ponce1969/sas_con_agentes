# backend/app/application/services.py

from typing import List, Dict, Any
from core.domain.models import TextItem  # Ajusta según tus modelos de dominio
from .embeddings_service import EmbeddingsService

class TextProcessingService:
    """
    Servicio principal de procesamiento de textos:
    - Genera embeddings
    - Prepara datos para almacenamiento o análisis
    """

    def __init__(self, embeddings_service: EmbeddingsService = None):
        # Permite inyección de dependencias (hexagonal)
        self.embeddings_service = embeddings_service or EmbeddingsService()

    def process_text(self, text_item: TextItem) -> Dict[str, Any]:
        """
        Procesa un texto individual: genera embedding y prepara output.
        """
        embedding = self.embeddings_service.generate_embedding(text_item.content)
        return {
            "id": text_item.id,
            "text": text_item.content,
            "embedding": embedding
        }

    def process_texts_batch(self, items: List[TextItem]) -> List[Dict[str, Any]]:
        """
        Procesa un batch de TextItem.
        """
        texts = [item.content for item in items]
        embeddings_dict = self.embeddings_service.batch_generate_embeddings(texts)
        results = []
        for item in items:
            results.append({
                "id": item.id,
                "text": item.content,
                "embedding": embeddings_dict.get(item.content, [])
            })
        return results

# --- Ejemplo mínimo de uso ---
if __name__ == "__main__":
    from core.domain.models import TextItem

    service = TextProcessingService()
    items = [
        TextItem(id="1", content="Hola mundo"),
        TextItem(id="2", content="Esto es una prueba de embedding")
    ]
    results = service.process_texts_batch(items)
    for r in results:
        print(f"{r['id']}: {r['text']} -> embedding len={len(r['embedding'])}")

# backend/app/core/config.py

import os
from pathlib import Path
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Ajusta según estructura

class Settings(BaseSettings):
    """
    Configuración central de la aplicación SaaS.
    Usa variables de entorno (.env) y valores por defecto.
    """

    # --- FastAPI ---
    APP_NAME: str = "ProyectoNeuronalSaaS"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- API Keys ---
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")  # Obligatorio

    # --- Embeddings / Vector DB ---
    VECTOR_DIM: int = 1536
    VECTOR_INDEX_PATH: str = str(BASE_DIR / "data" / "vector_index.pkl")

    # --- Database ---
    DATABASE_URL: str = Field("sqlite:///./db.sqlite3", env="DATABASE_URL")

    # --- Misc ---
    MAX_REQUESTS_PER_MINUTE: int = 60
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

# Instancia global de configuración
settings = Settings()
