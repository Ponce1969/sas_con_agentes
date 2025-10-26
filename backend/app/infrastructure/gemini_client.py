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

    async def analyze_code(self, code: str, model: str = "gemini-1.5-flash") -> str:
        """
        Analiza código Python y retorna sugerencias de mejora.
        
        Args:
            code: Código Python a analizar
            model: Modelo de Gemini a usar
            
        Returns:
            Análisis en formato markdown
        """
        prompt = f"""Eres un experto en Python con 10 años de experiencia. Analiza este código y proporciona:

1. **🐛 Bugs Potenciales**: Errores que podrían causar problemas en producción
2. **👃 Code Smells**: Malas prácticas o código que "huele mal"
3. **⚡ Mejoras de Rendimiento**: Optimizaciones posibles
4. **📊 Score de Calidad**: Calificación de 0-100 con justificación

Código a analizar:
```python
{code}
```

Formato de respuesta en Markdown:
## 🐛 Bugs Potenciales
- [lista de bugs o "No se detectaron bugs"]

## 👃 Code Smells
- [lista de code smells o "Código limpio"]

## ⚡ Mejoras de Rendimiento
- [lista de mejoras o "Rendimiento óptimo"]

## 📊 Score de Calidad: [0-100]
[justificación del score en 2-3 líneas]

Sé específico, constructivo y profesional."""

        url = f"{self.base_url}/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": 0.3,  # Más determinístico
            "max_tokens": 1000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(url, headers=self.headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                analysis = data.get("text", data.get("response", ""))
                if not analysis:
                    logger.warning(f"No se recibió análisis: {data}")
                    return "⚠️ No se pudo generar el análisis"
                return analysis
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error al analizar código: {e.response.text}")
                return f"❌ Error HTTP: {e.response.status_code}"
            except Exception as e:
                logger.error(f"Error inesperado al analizar código: {e}")
                return f"❌ Error: {str(e)}"

# ----------------- USO EJEMPLO -----------------
# async def main():
#     client = GeminiClient()
#     code = "def suma(a, b): return a + b"
#     analysis = await client.analyze_code(code)
#     print(analysis)
# asyncio.run(main())

