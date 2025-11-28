# backend/app/web/schemas/auth_schemas.py

from typing import Optional

from pydantic import BaseModel, Field, field_validator
import re


# ----------------- REQUEST SCHEMAS -----------------


class UserRegisterRequest(BaseModel):
    """Schema para registro de usuario."""

    email: str = Field(..., max_length=120)
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=100)
    gemini_api_key: Optional[str] = Field(None, description="API Key propia de Gemini (opcional)")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError("Email inválido")
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "MiPassword123",
                "full_name": "Juan Pérez",
                "gemini_api_key": None,
            }
        }


class UserLoginRequest(BaseModel):
    """Schema para login de usuario."""

    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError("Email inválido")
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "MiPassword123",
            }
        }


# ----------------- RESPONSE SCHEMAS -----------------


class UserResponse(BaseModel):
    """Schema de respuesta para usuario."""

    id: int
    email: str
    full_name: Optional[str]
    role: str
    has_own_api_key: bool
    analyses_today: int
    total_analyses: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema de respuesta para token."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """Schema genérico para mensajes."""

    success: bool
    message: str
    data: Optional[dict] = None
