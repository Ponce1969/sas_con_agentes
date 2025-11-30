# backend/app/domain/models.py
"""
Modelos de dominio SQLAlchemy para la aplicación.

Define las entidades principales:
- Role: Roles de usuario (free, pro, custom, admin)
- User: Usuarios del sistema
- Analysis: Registros de análisis de código
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, declarative_base, relationship

# Type checking para evitar imports circulares
if TYPE_CHECKING:
    from typing import List

Base = declarative_base()


# ----------------- HELPERS -----------------


def utc_now() -> datetime:
    """Retorna datetime actual en UTC (timezone-aware)."""
    return datetime.now(timezone.utc)


# ----------------- MODELS -----------------


class Role(Base, AsyncAttrs):
    """
    Roles de usuario que definen límites y permisos.
    
    Roles predefinidos:
    - free (id=1): 5 análisis/día
    - pro (id=2): 100 análisis/día
    - custom (id=3): Ilimitado (usa su propia API key)
    - admin (id=4): Ilimitado + acceso admin
    """

    __tablename__ = "roles"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = Column(String(255), nullable=True)
    max_analyses_per_day: Mapped[int] = Column(
        Integer, 
        default=5,
        comment="Límite de análisis por día (0 = ilimitado)"
    )

    # Relaciones
    users: Mapped["List[User]"] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name}, limit={self.max_analyses_per_day})>"


class User(Base, AsyncAttrs):
    """
    Usuario del sistema.
    
    Soporta:
    - Autenticación con email/password (Argon2)
    - API key propia de Gemini (encriptada)
    - Contadores de uso
    - Roles con límites
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        Index("ix_users_role_id", "role_id"),
    )

    # Identificación
    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(
        String(120), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="Email único del usuario (lowercase)"
    )
    hashed_password: Mapped[str] = Column(
        String(255), 
        nullable=False,
        comment="Password hasheado con Argon2id"
    )
    full_name: Mapped[Optional[str]] = Column(String(100), nullable=True)

    # Estado
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    # API Key propia del usuario (encriptada con Fernet)
    gemini_api_key_encrypted: Mapped[Optional[str]] = Column(
        String(500), 
        nullable=True,
        comment="API key encriptada con Fernet (AES-128)"
    )

    # Contadores de uso
    analyses_today: Mapped[int] = Column(Integer, default=0, nullable=False)
    total_analyses: Mapped[int] = Column(Integer, default=0, nullable=False)
    last_analysis_date: Mapped[Optional[datetime]] = Column(DateTime(timezone=True), nullable=True)

    # Timestamps (timezone-aware)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), 
        default=utc_now, 
        nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), 
        default=utc_now, 
        onupdate=utc_now,
        nullable=False
    )

    # Relaciones
    role_id: Mapped[Optional[int]] = Column(
        Integer, 
        ForeignKey("roles.id", ondelete="SET NULL"), 
        default=1
    )
    role: Mapped[Optional["Role"]] = relationship("Role", back_populates="users")
    analyses: Mapped["List[Analysis]"] = relationship(
        "Analysis", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role_id={self.role_id})>"

    @property
    def has_own_api_key(self) -> bool:
        """Indica si el usuario tiene su propia API key configurada."""
        return bool(self.gemini_api_key_encrypted)


class Analysis(Base, AsyncAttrs):
    """
    Registro de análisis de código.
    
    Almacena:
    - Código original y mejorado
    - Resultado del análisis (markdown)
    - Score de calidad (0-100)
    - Metadata (modelo, tokens)
    """

    __tablename__ = "analyses"
    __table_args__ = (
        Index("ix_analyses_user_created", "user_id", "created_at"),
        CheckConstraint(
            "quality_score IS NULL OR (quality_score >= 0 AND quality_score <= 100)",
            name="ck_quality_score_range"
        ),
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # Código analizado
    code_original: Mapped[str] = Column(Text, nullable=False)
    code_improved: Mapped[Optional[str]] = Column(Text, nullable=True)

    # Resultados
    analysis_result: Mapped[str] = Column(
        Text, 
        nullable=False,
        comment="Resultado del análisis en formato markdown"
    )
    quality_score: Mapped[Optional[int]] = Column(
        Integer, 
        nullable=True,
        comment="Score de calidad 0-100"
    )

    # Metadata
    model_used: Mapped[str] = Column(
        String(50), 
        default="gemini-2.5-flash",
        nullable=False
    )
    tokens_used: Mapped[Optional[int]] = Column(Integer, nullable=True)

    # Timestamps (timezone-aware)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), 
        default=utc_now,
        nullable=False,
        index=True
    )

    # Relaciones
    user: Mapped["User"] = relationship("User", back_populates="analyses")

    def __repr__(self) -> str:
        return f"<Analysis(id={self.id}, user_id={self.user_id}, score={self.quality_score})>"

    @property
    def code_preview(self) -> str:
        """Retorna preview del código (primeros 100 chars)."""
        if len(self.code_original) > 100:
            return self.code_original[:100] + "..."
        return self.code_original

