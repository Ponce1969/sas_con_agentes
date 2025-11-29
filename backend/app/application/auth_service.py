# backend/app/application/auth_service.py

import logging
import re
from datetime import datetime, timedelta
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.domain.models import User
from app.infrastructure.encryption import get_encryption_service

logger = logging.getLogger(__name__)

# Hasher Argon2 con configuración segura (OWASP recomendado)
ph = PasswordHasher(
    time_cost=3,        # Iteraciones
    memory_cost=65536,  # 64MB de memoria
    parallelism=4,      # Hilos paralelos
)


class AuthService:
    """Servicio de autenticación con JWT."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ----------------- PASSWORD -----------------

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashear password con Argon2id (más seguro que bcrypt)."""
        return ph.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar password contra hash Argon2."""
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False
        except Exception:
            return False

    # ----------------- JWT -----------------

    @staticmethod
    def create_access_token(user_id: int, email: str, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT."""
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decodificar y validar token JWT."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Error decodificando token: {e}")
            return None

    # ----------------- VALIDACIONES -----------------

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato de email."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validar fortaleza de password.
        Returns: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe tener al menos una mayúscula"
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe tener al menos una minúscula"
        if not re.search(r"\d", password):
            return False, "La contraseña debe tener al menos un número"
        return True, ""

    # ----------------- USER OPERATIONS -----------------

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email con su role cargado."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email.lower())
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID con su role cargado."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        return result.scalars().first()

    async def register_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
    ) -> tuple[Optional[User], str]:
        """
        Registrar nuevo usuario.
        Returns: (user, error_message)
        """
        # Validar email
        if not self.validate_email(email):
            return None, "Formato de email inválido"

        # Validar password
        is_valid, error = self.validate_password(password)
        if not is_valid:
            return None, error

        # Verificar si ya existe
        existing = await self.get_user_by_email(email)
        if existing:
            return None, "El email ya está registrado"

        # Determinar rol (custom si tiene API key propia)
        role_id = 3 if gemini_api_key else 1  # 3=custom, 1=free

        # Encriptar API key si se proporciona
        encrypted_api_key = None
        if gemini_api_key:
            encryption = get_encryption_service()
            encrypted_api_key = encryption.encrypt(gemini_api_key)
            logger.info(f"🔐 API key encriptada para usuario: {email}")

        # Crear usuario
        user = User(
            email=email.lower(),
            hashed_password=self.hash_password(password),
            full_name=full_name,
            gemini_api_key_encrypted=encrypted_api_key,
            role_id=role_id,
            is_active=True,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        logger.info(f"✅ Usuario registrado: {email}")
        return user, ""

    async def authenticate_user(self, email: str, password: str) -> tuple[Optional[User], str]:
        """
        Autenticar usuario.
        Returns: (user, error_message)
        """
        user = await self.get_user_by_email(email)

        if not user:
            return None, "Email o contraseña incorrectos"

        if not self.verify_password(password, user.hashed_password):
            return None, "Email o contraseña incorrectos"

        if not user.is_active:
            return None, "Usuario desactivado"

        logger.info(f"✅ Usuario autenticado: {email}")
        return user, ""

    async def login(self, email: str, password: str) -> tuple[Optional[dict], str]:
        """
        Login completo: autenticar + generar token.
        Returns: (token_data, error_message)
        """
        user, error = await self.authenticate_user(email, password)
        if not user:
            return None, error

        # Generar token
        access_token = self.create_access_token(user.id, user.email)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.name if user.role else "free",
                "has_own_api_key": bool(user.gemini_api_key_encrypted),
            },
        }, ""


# ----------------- DEPENDENCY -----------------


def get_auth_service(db: AsyncSession) -> AuthService:
    """Factory para AuthService."""
    return AuthService(db)
