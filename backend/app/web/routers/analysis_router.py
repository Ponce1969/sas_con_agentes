# backend/app/web/routers/analysis_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any

from app.application.analysis_service import AnalysisService, get_analysis_service

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


# Schemas
class AnalysisRequest(BaseModel):
    """Request para análisis de código."""
    codigo: str = Field(..., description="Código Python a analizar", min_length=1, max_length=10000)
    usuario_id: int | None = Field(None, description="ID del usuario (opcional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "codigo": "def suma(a, b):\n    return a + b",
                "usuario_id": 1
            }
        }


class AnalysisResponse(BaseModel):
    """Response del análisis de código."""
    success: bool
    analisis: str | None = None
    error: str | None = None
    codigo: str
    usuario_id: int | None = None
    timestamp: str
    modelo_usado: str | None = None


# Endpoints
@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analizar_codigo(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service)
) -> Dict[str, Any]:
    """
    Analiza código Python y retorna sugerencias de mejora.
    
    - **codigo**: Código Python a analizar (requerido)
    - **usuario_id**: ID del usuario (opcional)
    
    Retorna análisis con:
    - Bugs potenciales
    - Code smells
    - Mejoras de rendimiento
    - Score de calidad (0-100)
    """
    resultado = await service.analizar_codigo(
        codigo=request.codigo,
        usuario_id=request.usuario_id
    )
    
    if not resultado["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado.get("error", "Error desconocido")
        )
    
    return resultado


@router.get("/stats/{usuario_id}", status_code=status.HTTP_200_OK)
async def obtener_estadisticas(
    usuario_id: int,
    service: AnalysisService = Depends(get_analysis_service)
) -> Dict[str, Any]:
    """
    Obtiene estadísticas de análisis para un usuario.
    
    - **usuario_id**: ID del usuario
    
    Retorna:
    - Total de análisis realizados
    - Análisis realizados hoy
    - Score promedio
    """
    return await service.obtener_estadisticas(usuario_id)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Health check del servicio de análisis."""
    return {
        "status": "healthy",
        "service": "analysis",
        "message": "Servicio de análisis operativo"
    }
