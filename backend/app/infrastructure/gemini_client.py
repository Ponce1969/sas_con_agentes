# backend/app/infrastructure/gemini_client.py

import os
import httpx
from typing import List, Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Cliente para la API de Google Gemini.
    Modelo recomendado: gemini-2.5-flash (el más moderno y potente)
    Compatible con API v1beta.
    Maneja llamadas async y API key desde .env.
    """

    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere GEMINI_API_KEY para usar GeminiClient")
        self.base_url = base_url
        self.headers = {
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

    async def analyze_code(self, code: str, model: str = "gemini-2.5-flash") -> str:
        """
        Analiza código Python y retorna sugerencias de mejora.
        
        Args:
            code: Código Python a analizar
            model: Modelo de Gemini a usar (gemini-2.5-flash - el más moderno y potente)
            
        Returns:
            Análisis en formato markdown
        """
        prompt = f"""Eres un experto en Python con 10 años de experiencia. Analiza este código y proporciona un análisis detallado.

**CÓDIGO A ANALIZAR:**
```python
{code}
```

**INSTRUCCIONES:**
1. Identifica bugs, code smells y mejoras de rendimiento
2. Proporciona el código CORREGIDO completo (no solo fragmentos)
3. Explica cada cambio realizado
4. Asigna un score de calidad (0-100)

**FORMATO DE RESPUESTA (usa exactamente este formato):**

## 🐛 Bugs Potenciales
- [Lista detallada de bugs encontrados, o "✅ No se detectaron bugs"]

## 👃 Code Smells
- [Lista de malas prácticas encontradas, o "✅ Código limpio"]

## ⚡ Mejoras de Rendimiento
- [Lista de optimizaciones posibles, o "✅ Rendimiento óptimo"]

## 📊 Score de Calidad: [0-100]/100

**Justificación:** [Explica el score en 2-3 líneas]

## ✨ Código Mejorado

```python
# Código corregido con todas las mejoras aplicadas
[AQUÍ VA EL CÓDIGO COMPLETO MEJORADO]
```

## 📝 Cambios Realizados
1. **[Tipo de cambio]**: [Explicación breve]
2. **[Tipo de cambio]**: [Explicación breve]
[etc...]

**IMPORTANTE:** 
- Sé específico y constructivo
- Si el código está perfecto, di "✅ Código excelente, no requiere cambios"
- Siempre incluye el código mejorado completo, no fragmentos"""

        # URL de la API oficial de Google Gemini
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 4096,  # Aumentado para incluir código completo
                "topP": 0.8,
                "topK": 10
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                resp = await client.post(url, headers=self.headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                # Extraer texto de la respuesta de Gemini
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            analysis = parts[0]["text"]
                            return analysis
                
                logger.warning(f"No se recibió análisis en formato esperado: {data}")
                return "⚠️ No se pudo generar el análisis"
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error al analizar código: {e.response.text}")
                return f"❌ Error HTTP: {e.response.status_code}\n\nDetalles: {e.response.text[:200]}"
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

