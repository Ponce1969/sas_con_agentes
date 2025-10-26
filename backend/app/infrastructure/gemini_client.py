# backend/app/infrastructure/gemini_client.py

import os
import httpx
from typing import List, Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Cliente para la API de Gemini (ej: Gemini-text-004) para obtener embeddings.
    Maneja llamadas async y API key desde .env.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.gemini.com/v1"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere GEMINI_API_KEY para usar GeminiClient")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def create_embedding(self, text: str, model: str = "gemini-text-004") -> List[float]:
        """
        Solicita un embedding para un texto dado.
        """
        url = f"{self.base_url}/embeddings"
        payload = {
            "model": model,
            "input": text
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(url, headers=self.headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                embedding = data.get("embedding")
                if embedding is None:
                    logger.warning(f"No se recibió embedding: {data}")
                    return []
                return embedding
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error al generar embedding: {e.response.text}")
                return []
            except Exception as e:
                logger.error(f"Error inesperado al generar embedding: {e}")
                return []

    async def create_embeddings_batch(self, texts: List[str], model: str = "gemini-text-004") -> Dict[str, List[float]]:
        """
        Solicita embeddings para un batch de textos de forma concurrente.
        """
        tasks = [self.create_embedding(text, model=model) for text in texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        embeddings = {}
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"Error embedding para '{texts[i]}': {res}")
                embeddings[texts[i]] = []
            else:
                embeddings[texts[i]] = res
        return embeddings

# ----------------- USO EJEMPLO -----------------
# async def main():
#     client = GeminiClient()
#     emb = await client.create_embedding("Hola mundo")
#     print(emb)
# asyncio.run(main())

