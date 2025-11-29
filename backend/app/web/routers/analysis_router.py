# backend/app/web/routers/analysis_router.py

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.analysis_service import AnalysisService
from app.domain.models import User
from app.infrastructure.database import get_db
from app.web.routers.auth_router import get_current_user

router = APIRouter(prefix="/api/analysis", tags=["Análisis de Código"])


# ----------------- SCHEMAS -----------------


class AnalysisRequest(BaseModel):
    """Request para análisis de código."""

    codigo: str = Field(..., description="Código Python a analizar", min_length=1, max_length=50000)

    class Config:
        json_schema_extra = {"example": {"codigo": "def suma(a, b):\n    return a + b"}}


class AnalysisResponse(BaseModel):
    """Response del análisis de código."""

    success: bool
    analisis: Optional[str] = None
    error: Optional[str] = None
    codigo: str
    usuario_id: Optional[int] = None
    timestamp: str
    modelo_usado: Optional[str] = None
    analysis_id: Optional[int] = None  # ID del análisis guardado


# ----------------- ENDPOINTS -----------------


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analizar_codigo(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Analiza código Python y retorna sugerencias de mejora.

    - **Autenticado**: Guarda análisis en historial, usa API key del usuario si tiene
    - **Anónimo**: Análisis sin guardar (limitado)

    Retorna:
    - Bugs potenciales
    - Code smells
    - Mejoras de rendimiento
    - Score de calidad (0-100)
    - Código mejorado
    """
    # Crear servicio con DB para persistencia
    service = AnalysisService(db=db)

    # Obtener user_id si está autenticado
    user_id = current_user.id if current_user else None

    # Obtener API key del usuario si tiene una propia
    user_api_key = None
    if current_user and current_user.gemini_api_key_encrypted:
        user_api_key = current_user.gemini_api_key_encrypted  # TODO: Desencriptar

    resultado = await service.analizar_codigo(
        codigo=request.codigo,
        usuario_id=user_id,
        user_api_key=user_api_key,
    )

    if not resultado["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado.get("error", "Error desconocido"),
        )

    return resultado


@router.get("/stats", status_code=status.HTTP_200_OK)
async def obtener_estadisticas(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Obtiene estadísticas de análisis del usuario autenticado.

    Retorna:
    - Total de análisis realizados
    - Análisis realizados hoy
    - Score promedio
    - Límite diario según plan
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida para ver estadísticas",
        )

    service = AnalysisService(db=db)
    return await service.obtener_estadisticas(current_user.id)


@router.get("/history", status_code=status.HTTP_200_OK)
async def obtener_historial(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Obtiene historial de análisis del usuario autenticado.

    - **limit**: Cantidad de resultados (default: 10, max: 50)
    - **offset**: Desplazamiento para paginación
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida para ver historial",
        )

    # Limitar a máximo 50
    limit = min(limit, 50)

    service = AnalysisService(db=db)
    return await service.obtener_historial(current_user.id, limit, offset)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Health check del servicio de análisis."""
    return {
        "status": "healthy",
        "service": "analysis",
        "message": "Servicio de análisis operativo",
    }
