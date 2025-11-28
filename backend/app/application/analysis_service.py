# backend/app/application/analysis_service.py

import logging
import re
from datetime import date, datetime
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.models import Analysis, User
from app.infrastructure.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Servicio de aplicación para análisis de código Python.
    Orquesta la lógica de negocio y coordina con la infraestructura.
    """

    def __init__(
        self,
        db: Optional[AsyncSession] = None,
        gemini_client: Optional[GeminiClient] = None,
    ):
        """
        Inicializa el servicio.

        Args:
            db: Sesión de base de datos (opcional)
            gemini_client: Cliente de Gemini (opcional)
        """
        self.db = db
        self.gemini_client = gemini_client or GeminiClient(api_key=settings.GEMINI_API_KEY)

    def _extract_score(self, analisis: str) -> Optional[int]:
        """Extraer score de calidad del análisis."""
        match = re.search(r"Score de Calidad:\s*(\d+)/100", analisis)
        if match:
            return int(match.group(1))
        return None

    def _extract_improved_code(self, analisis: str) -> Optional[str]:
        """Extraer código mejorado del análisis."""
        patterns = [
            r"##\s*✨\s*Código Mejorado.*?```python\s*(.*?)\s*```",
            r"✨\s*Código Mejorado.*?```python\s*(.*?)\s*```",
            r"Código Mejorado.*?```python\s*(.*?)\s*```",
        ]
        for pattern in patterns:
            match = re.search(pattern, analisis, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    async def analizar_codigo(
        self,
        codigo: str,
        usuario_id: Optional[int] = None,
        user_api_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Analiza código Python y retorna sugerencias de mejora.

        Args:
            codigo: Código Python a analizar
            usuario_id: ID del usuario (opcional)
            user_api_key: API key propia del usuario (opcional)

        Returns:
            Diccionario con el análisis y metadatos
        """
        try:
            # Validar código
            if not codigo or not codigo.strip():
                return {
                    "success": False,
                    "error": "El código no puede estar vacío",
                    "codigo": codigo,
                    "timestamp": datetime.now().isoformat(),
                }

            if len(codigo) > 10000:
                return {
                    "success": False,
                    "error": "El código es demasiado largo (máximo 10,000 caracteres)",
                    "codigo": codigo[:100] + "...",
                    "timestamp": datetime.now().isoformat(),
                }

            logger.info(f"Analizando código para usuario_id={usuario_id}")

            # Usar API key del usuario si tiene, sino la del sistema
            if user_api_key:
                client = GeminiClient(api_key=user_api_key)
                logger.info("Usando API key del usuario")
            else:
                client = self.gemini_client

            # Llamar a Gemini
            analisis = await client.analyze_code(code=codigo, model=settings.GEMINI_MODEL)

            # Extraer datos del análisis
            score = self._extract_score(analisis)
            codigo_mejorado = self._extract_improved_code(analisis)

            # Guardar en DB si hay usuario autenticado y DB disponible
            analysis_id = None
            if self.db and usuario_id:
                try:
                    analysis_record = Analysis(
                        user_id=usuario_id,
                        code_original=codigo,
                        code_improved=codigo_mejorado,
                        analysis_result=analisis,
                        quality_score=score,
                        model_used=settings.GEMINI_MODEL,
                    )
                    self.db.add(analysis_record)
                    await self.db.flush()
                    analysis_id = analysis_record.id

                    # Actualizar contadores del usuario
                    await self._update_user_counters(usuario_id)

                    logger.info(f"✅ Análisis guardado con ID={analysis_id}")
                except Exception as e:
                    logger.warning(f"No se pudo guardar análisis en DB: {e}")

            return {
                "success": True,
                "analisis": analisis,
                "codigo": codigo,
                "usuario_id": usuario_id,
                "timestamp": datetime.now().isoformat(),
                "modelo_usado": settings.GEMINI_MODEL,
                "analysis_id": analysis_id,
            }

        except Exception as e:
            logger.error(f"Error en análisis de código: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Error interno: {str(e)}",
                "codigo": codigo[:100] + "..." if len(codigo) > 100 else codigo,
                "timestamp": datetime.now().isoformat(),
            }

    async def _update_user_counters(self, usuario_id: int) -> None:
        """Actualizar contadores de análisis del usuario."""
        if not self.db:
            return

        result = await self.db.execute(select(User).where(User.id == usuario_id))
        user = result.scalars().first()

        if user:
            today = date.today()

            # Resetear contador diario si es nuevo día
            if user.last_analysis_date and user.last_analysis_date.date() != today:
                user.analyses_today = 0

            user.analyses_today += 1
            user.total_analyses += 1
            user.last_analysis_date = datetime.now()

    async def obtener_estadisticas(self, usuario_id: int) -> dict[str, Any]:
        """Obtiene estadísticas de análisis para un usuario."""
        if not self.db:
            return {
                "usuario_id": usuario_id,
                "total_analisis": 0,
                "analisis_hoy": 0,
                "score_promedio": 0,
                "limite_diario": 5,
            }

        # Obtener usuario
        result = await self.db.execute(select(User).where(User.id == usuario_id))
        user = result.scalars().first()

        if not user:
            return {"error": "Usuario no encontrado"}

        # Calcular score promedio
        avg_result = await self.db.execute(
            select(func.avg(Analysis.quality_score)).where(
                Analysis.user_id == usuario_id, Analysis.quality_score.isnot(None)
            )
        )
        avg_score = avg_result.scalar() or 0

        # Obtener límite según rol
        limite_diario = user.role.max_analyses_per_day if user.role else 5

        return {
            "usuario_id": usuario_id,
            "total_analisis": user.total_analyses,
            "analisis_hoy": user.analyses_today,
            "score_promedio": round(avg_score, 1),
            "limite_diario": limite_diario,
            "tiene_api_propia": bool(user.gemini_api_key_encrypted),
        }

    async def obtener_historial(
        self, usuario_id: int, limit: int = 10, offset: int = 0
    ) -> dict[str, Any]:
        """Obtiene historial de análisis de un usuario."""
        if not self.db:
            return {"analyses": [], "total": 0}

        # Contar total
        count_result = await self.db.execute(
            select(func.count(Analysis.id)).where(Analysis.user_id == usuario_id)
        )
        total = count_result.scalar() or 0

        # Obtener análisis paginados
        result = await self.db.execute(
            select(Analysis)
            .where(Analysis.user_id == usuario_id)
            .order_by(Analysis.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        analyses = result.scalars().all()

        return {
            "analyses": [
                {
                    "id": a.id,
                    "code_preview": a.code_original[:100] + "..."
                    if len(a.code_original) > 100
                    else a.code_original,
                    "quality_score": a.quality_score,
                    "model_used": a.model_used,
                    "created_at": a.created_at.isoformat(),
                }
                for a in analyses
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
