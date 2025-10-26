# backend/app/web/routers/health_router.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", summary="Check API health")
async def health_check():
    """
    Endpoint de salud de la API.
    Devuelve estado OK si la API está corriendo.
    """
    return JSONResponse(content={"status": "ok"})

