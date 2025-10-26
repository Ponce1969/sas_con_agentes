# backend/app/web/routers/embeddings_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from core.config import Settings, get_settings
from application.embeddings_service import EmbeddingsService

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

settings: Settings = get_settings()
service = EmbeddingsService(api_key=settings.GEMINI_API_KEY)

# ----------------- Pydantic Models -----------------
class EmbeddingRequest(BaseModel):
    texts: List[str]

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

# ----------------- Routes -----------------
@router.post("/", response_model=EmbeddingResponse)
async def generate_embeddings(
    request: EmbeddingRequest
):
    """
    Genera embeddings usando el modelo Gemini-texto-004.
    """
    try:
        embeddings = await service.get_embeddings(request.texts)
        return EmbeddingResponse(embeddings=embeddings)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando embeddings: {str(e)}"
        )

