# backend/app/domain/models.py

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# ----------------- MODELOS -----------------


class Role(Base, AsyncAttrs):
    """Roles de usuario: free, pro, admin"""

    __tablename__ = "roles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)
    description: Optional[str] = Column(String(255), nullable=True)
    max_analyses_per_day: int = Column(Integer, default=5)  # Límite por plan

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"


class User(Base, AsyncAttrs):
    """Usuario del sistema con soporte para API key propia"""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password: str = Column(String(255), nullable=False)
    full_name: Optional[str] = Column(String(100), nullable=True)

    # Estado
    is_active: bool = Column(Boolean, default=True)
    is_verified: bool = Column(Boolean, default=False)

    # API Key propia del usuario (encriptada)
    gemini_api_key_encrypted: Optional[str] = Column(String(500), nullable=True)

    # Contadores
    analyses_today: int = Column(Integer, default=0)
    total_analyses: int = Column(Integer, default=0)
    last_analysis_date: Optional[datetime] = Column(DateTime, nullable=True)

    # Timestamps
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    role_id: Optional[int] = Column(Integer, ForeignKey("roles.id"), default=1)
    role = relationship("Role", back_populates="users")
    analyses = relationship("Analysis", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Analysis(Base, AsyncAttrs):
    """Registro de análisis de código"""

    __tablename__ = "analyses"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Código analizado
    code_original: str = Column(Text, nullable=False)
    code_improved: Optional[str] = Column(Text, nullable=True)

    # Resultados
    analysis_result: str = Column(Text, nullable=False)
    quality_score: Optional[int] = Column(Integer, nullable=True)

    # Metadata
    model_used: str = Column(String(50), default="gemini-2.5-flash")
    tokens_used: Optional[int] = Column(Integer, nullable=True)

    # Timestamps
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="analyses")

    def __repr__(self) -> str:
        return f"<Analysis(id={self.id}, user_id={self.user_id}, score={self.quality_score})>"

