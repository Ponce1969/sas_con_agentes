# backend/app/application/analysis_service.py

from typing import Dict, Any
import logging
from datetime import datetime

from app.infrastructure.gemini_client import GeminiClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Servicio de aplicación para análisis de código Python.
    Orquesta la lógica de negocio y coordina con la infraestructura.
    """

    def __init__(self, gemini_client: GeminiClient | None = None):
        """
        Inicializa el servicio con un cliente de Gemini.
        
        Args:
            gemini_client: Cliente de Gemini (opcional, se crea uno por defecto)
        """
        self.gemini_client = gemini_client or GeminiClient(
            api_key=settings.GEMINI_API_KEY
        )

    async def analizar_codigo(
        self, 
        codigo: str, 
        usuario_id: int | None = None
    ) -> Dict[str, Any]:
        """
        Analiza código Python y retorna sugerencias de mejora.
        
        Args:
            codigo: Código Python a analizar
            usuario_id: ID del usuario que solicita el análisis (opcional)
            
        Returns:
            Diccionario con el análisis y metadatos
        """
        try:
            # Validar que el código no esté vacío
            if not codigo or not codigo.strip():
                return {
                    "success": False,
                    "error": "El código no puede estar vacío",
                    "codigo": codigo,
                    "timestamp": datetime.now().isoformat()
                }

            # Validar longitud del código (máximo 10,000 caracteres para MVP)
            if len(codigo) > 10000:
                return {
                    "success": False,
                    "error": "El código es demasiado largo (máximo 10,000 caracteres)",
                    "codigo": codigo[:100] + "...",
                    "timestamp": datetime.now().isoformat()
                }

            logger.info(f"Analizando código para usuario_id={usuario_id}")
            
            # Llamar a Gemini para análisis
            analisis = await self.gemini_client.analyze_code(
                code=codigo,
                model=settings.GEMINI_MODEL
            )
            
            # TODO: Guardar análisis en base de datos
            # await self.guardar_analisis(codigo, analisis, usuario_id)
            
            return {
                "success": True,
                "analisis": analisis,
                "codigo": codigo,
                "usuario_id": usuario_id,
                "timestamp": datetime.now().isoformat(),
                "modelo_usado": settings.GEMINI_MODEL
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de código: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "codigo": codigo[:100] + "..." if len(codigo) > 100 else codigo,
                "timestamp": datetime.now().isoformat()
            }

    async def obtener_estadisticas(self, usuario_id: int) -> Dict[str, Any]:
        """
        Obtiene estadísticas de análisis para un usuario.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Diccionario con estadísticas
        """
        # TODO: Implementar cuando tengamos base de datos
        return {
            "usuario_id": usuario_id,
            "total_analisis": 0,
            "analisis_hoy": 0,
            "score_promedio": 0
        }


# Factory para Dependency Injection
def get_analysis_service() -> AnalysisService:
    """Factory para crear instancia de AnalysisService."""
    return AnalysisService()
