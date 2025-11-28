# backend/app/web/routers/auth_router.py

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth_service import AuthService
from app.domain.models import User
from app.infrastructure.database import get_db
from app.web.schemas import (
    MessageResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

# Security scheme para JWT
security = HTTPBearer(auto_error=False)


# ----------------- DEPENDENCIES -----------------


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Dependency para obtener usuario actual desde JWT.
    Retorna None si no hay token (permite acceso anónimo).
    """
    if not credentials:
        return None

    token = credentials.credentials
    auth_service = AuthService(db)

    # Decodificar token
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener usuario
    user_id = int(payload.get("sub", 0))
    user = await auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )

    return user


async def require_auth(
    user: Optional[User] = Depends(get_current_user),
) -> User:
    """Dependency que REQUIERE autenticación."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticación requerida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# ----------------- ENDPOINTS -----------------


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Registrar nuevo usuario.

    - **email**: Email único del usuario
    - **password**: Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número
    - **full_name**: Nombre completo (opcional)
    - **gemini_api_key**: API Key propia de Gemini (opcional, da acceso ilimitado)
    """
    auth_service = AuthService(db)

    user, error = await auth_service.register_user(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        gemini_api_key=request.gemini_api_key,
    )

    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return MessageResponse(
        success=True,
        message="Usuario registrado exitosamente",
        data={"user_id": user.id, "email": user.email},
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Iniciar sesión y obtener token JWT.

    El token debe enviarse en el header `Authorization: Bearer <token>`
    """
    auth_service = AuthService(db)

    token_data, error = await auth_service.login(
        email=request.email,
        password=request.password,
    )

    if error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)

    # Construir respuesta
    return TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        user=UserResponse(
            id=token_data["user"]["id"],
            email=token_data["user"]["email"],
            full_name=token_data["user"]["full_name"],
            role=token_data["user"]["role"],
            has_own_api_key=token_data["user"]["has_own_api_key"],
            analyses_today=0,
            total_analyses=0,
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: User = Depends(require_auth),
):
    """Obtener información del usuario autenticado."""
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name if user.role else "free",
        has_own_api_key=bool(user.gemini_api_key_encrypted),
        analyses_today=user.analyses_today,
        total_analyses=user.total_analyses,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    user: User = Depends(require_auth),
):
    """
    Cerrar sesión.

    Nota: Con JWT stateless, el logout es del lado del cliente
    (eliminar el token). Este endpoint es para logging/auditoría.
    """
    logger.info(f"Usuario {user.email} cerró sesión")
    return MessageResponse(success=True, message="Sesión cerrada exitosamente")
