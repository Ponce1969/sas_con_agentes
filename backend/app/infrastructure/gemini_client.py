# backend/app/infrastructure/gemini_client.py
"""
Cliente asíncrono para la API de Google Gemini.

Características:
- Reutilización de conexiones HTTP (connection pooling)
- Context manager async para manejo de recursos
- Soporte para análisis de código y embeddings
- Timeouts configurables por operación
"""

import asyncio
import logging
from types import TracebackType
from typing import Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


# ----------------- CONSTANTS -----------------


# Modelos por defecto
DEFAULT_ANALYSIS_MODEL = "gemini-2.5-flash"
DEFAULT_EMBEDDING_MODEL = "text-embedding-004"

# URLs base
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Timeouts (segundos)
DEFAULT_TIMEOUT = 30.0
ANALYSIS_TIMEOUT = httpx.Timeout(
    connect=10.0,
    read=180.0,  # 3 min - Gemini 2.5 Flash con thinking puede tardar
    write=30.0,
    pool=10.0,
)
EMBEDDING_TIMEOUT = 30.0

# Configuración de generación
ANALYSIS_GENERATION_CONFIG = {
    "temperature": 0.3,
    "maxOutputTokens": 16384,
    "topP": 0.8,
    "topK": 10,
}


# ----------------- EXCEPTIONS -----------------


class GeminiError(Exception):
    """Error base para operaciones de Gemini."""
    pass


class GeminiAPIError(GeminiError):
    """Error de la API de Gemini (HTTP 4xx/5xx)."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class GeminiTimeoutError(GeminiError):
    """Timeout en llamada a Gemini."""
    pass


class GeminiConfigError(GeminiError):
    """Error de configuración (API key faltante)."""
    pass


# ----------------- PROMPT -----------------


ANALYSIS_PROMPT_TEMPLATE = """Eres un experto en Python con 10 años de experiencia. Analiza este código y proporciona un análisis detallado.

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


# ----------------- CLIENT -----------------


class GeminiClient:
    """
    Cliente asíncrono para la API de Google Gemini.
    
    Uso como context manager (recomendado para múltiples llamadas):
        async with GeminiClient() as client:
            analysis = await client.analyze_code(code)
            embedding = await client.create_embedding(text)
    
    Uso directo (para llamadas únicas):
        client = GeminiClient()
        analysis = await client.analyze_code(code)
        await client.close()
    """

    __slots__ = ("_api_key", "_base_url", "_client", "_owns_client")

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = GEMINI_API_BASE_URL,
    ) -> None:
        """
        Inicializa el cliente de Gemini.
        
        Args:
            api_key: API key de Gemini (o usa GEMINI_API_KEY del entorno)
            base_url: URL base de la API
            
        Raises:
            GeminiConfigError: Si no hay API key configurada
        """
        self._api_key = api_key or getattr(settings, "GEMINI_API_KEY", None)
        if not self._api_key:
            raise GeminiConfigError("GEMINI_API_KEY es requerida")
        
        self._base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None
        self._owns_client = False

    async def __aenter__(self) -> "GeminiClient":
        """Inicia el context manager y crea el cliente HTTP."""
        self._client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
        self._owns_client = True
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Cierra el cliente HTTP al salir del context manager."""
        await self.close()

    async def close(self) -> None:
        """Cierra el cliente HTTP si es propio."""
        if self._client and self._owns_client:
            await self._client.aclose()
            self._client = None

    def _get_client(self, timeout: Optional[httpx.Timeout] = None) -> httpx.AsyncClient:
        """Obtiene o crea un cliente HTTP."""
        if self._client:
            return self._client
        # Cliente temporal para llamadas únicas
        return httpx.AsyncClient(timeout=timeout or DEFAULT_TIMEOUT)

    async def analyze_code(
        self,
        code: str,
        model: str = DEFAULT_ANALYSIS_MODEL,
    ) -> str:
        """
        Analiza código Python y retorna sugerencias de mejora.
        
        Args:
            code: Código Python a analizar
            model: Modelo de Gemini a usar
            
        Returns:
            Análisis en formato markdown
            
        Raises:
            GeminiTimeoutError: Si la operación excede el timeout
            GeminiAPIError: Si la API retorna error
        """
        url = f"{self._base_url}/models/{model}:generateContent?key={self._api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": ANALYSIS_PROMPT_TEMPLATE.format(code=code)}]}],
            "generationConfig": ANALYSIS_GENERATION_CONFIG,
        }
        
        client = self._get_client(ANALYSIS_TIMEOUT)
        should_close = not self._owns_client
        
        try:
            logger.info(f"Enviando código a Gemini ({len(code)} chars)")
            resp = await client.post(url, json=payload, timeout=ANALYSIS_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            
            return self._extract_analysis_text(data)
            
        except httpx.TimeoutException as e:
            logger.error(f"Timeout al analizar código: {e}")
            raise GeminiTimeoutError(
                "⏱️ **Timeout**: El análisis está tomando más tiempo del esperado.\n\n"
                "**Sugerencias:**\n"
                "- Intenta de nuevo (a veces Gemini tarda más)\n"
                "- Divide el código en partes más pequeñas"
            ) from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text[:200]}")
            raise GeminiAPIError(e.response.status_code, e.response.text[:200]) from e
        except Exception as e:
            logger.error(f"Error inesperado: {type(e).__name__}: {e}", exc_info=True)
            raise GeminiError(f"Error inesperado: {e}") from e
        finally:
            if should_close:
                await client.aclose()

    def _extract_analysis_text(self, data: dict) -> str:
        """Extrae el texto del análisis de la respuesta de Gemini."""
        candidates = data.get("candidates", [])
        if not candidates:
            logger.warning(f"Sin candidates en respuesta: {data}")
            return "⚠️ No se pudo generar el análisis"
        
        candidate = candidates[0]
        
        # Verificar truncamiento
        finish_reason = candidate.get("finishReason", "")
        if finish_reason == "MAX_TOKENS":
            logger.warning("Respuesta truncada por MAX_TOKENS")
        
        # Extraer texto
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        
        if parts and "text" in parts[0]:
            analysis = parts[0]["text"]
            logger.info(f"Análisis recibido ({len(analysis)} chars)")
            return analysis
        
        logger.warning(f"Formato inesperado: {data}")
        return "⚠️ No se pudo generar el análisis"

    async def create_embedding(
        self,
        text: str,
        model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> list[float]:
        """
        Genera embedding para un texto.
        
        Args:
            text: Texto para generar embedding
            model: Modelo de embeddings a usar
            
        Returns:
            Vector de embedding (lista de floats)
            
        Raises:
            GeminiAPIError: Si la API retorna error
        """
        # Endpoint correcto para embeddings de Gemini
        url = f"{self._base_url}/models/{model}:embedContent?key={self._api_key}"
        
        # Payload correcto para la API de Gemini
        payload = {
            "content": {"parts": [{"text": text}]},
        }
        
        client = self._get_client()
        should_close = not self._owns_client
        
        try:
            resp = await client.post(url, json=payload, timeout=EMBEDDING_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            
            # Extracción correcta: embedding.values
            embedding = data.get("embedding", {}).get("values", [])
            if not embedding:
                logger.warning(f"No se recibió embedding: {data}")
            return embedding
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error embedding: {e.response.status_code}")
            raise GeminiAPIError(e.response.status_code, e.response.text[:200]) from e
        except Exception as e:
            logger.error(f"Error embedding: {type(e).__name__}: {e}")
            raise GeminiError(f"Error al generar embedding: {e}") from e
        finally:
            if should_close:
                await client.aclose()

    async def create_embeddings_batch(
        self,
        texts: list[str],
        model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> dict[str, list[float]]:
        """
        Genera embeddings para múltiples textos concurrentemente.
        
        Args:
            texts: Lista de textos
            model: Modelo de embeddings
            
        Returns:
            Dict {texto: embedding}
        """
        tasks = [self.create_embedding(text, model=model) for text in texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        embeddings: dict[str, list[float]] = {}
        for text, result in zip(texts, results):
            if isinstance(result, Exception):
                logger.error(f"Error embedding para texto: {type(result).__name__}")
                embeddings[text] = []
            else:
                embeddings[text] = result
        
        return embeddings

