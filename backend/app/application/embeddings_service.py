# backend/app/application/embeddings_service.py

from typing import List, Dict, Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
import requests

# Configuración centralizada
class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_URL: str = "https://api.gemini.com/v1/embeddings"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../../../../.env")
        env_file_encoding = 'utf-8'

settings = Settings()

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingsService:
    """
    Servicio para generar embeddings usando Gemini-texto-004 vía API externa.
    """

    def __init__(self, api_key: str = settings.GEMINI_API_KEY):
        self.api_key = api_key
        self.api_url = settings.GEMINI_URL

    def generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding para un texto usando Gemini-texto-004
        """
        if not text.strip():
            return []

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gemini-texto-004",
            "input": text
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Dependiendo de la estructura de Gemini, ajustar:
            return data.get("embedding", [])
        except requests.RequestException as e:
            # Manejo profesional de errores
            print(f"[ERROR] Fallo al generar embedding: {e}")
            return []

    def batch_generate_embeddings(self, texts: List[str]) -> Dict[str, List[float]]:
        """
        Genera embeddings para una lista de textos.
        Devuelve un dict {texto: embedding}.
        """
        embeddings = {}
        for t in texts:
            embeddings[t] = self.generate_embedding(t)
        return embeddings

# Ejemplo mínimo de uso
if __name__ == "__main__":
    service = EmbeddingsService()
    test_text = "Hola, esto es una prueba de embedding."
    emb = service.generate_embedding(test_text)
    print(f"Embedding para '{test_text}': {emb[:5]} ... (len={len(emb)})")

