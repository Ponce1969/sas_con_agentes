# backend/app/infrastructure/encryption.py
"""
Servicio de encriptación para datos sensibles (API keys).
Usa Fernet (AES-128-CBC con HMAC) para encriptación simétrica reversible.
"""

import os
import base64
import logging
import secrets
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

# --- Constantes de Configuración ---
FERNET_HEADER_PREFIX = "gAAAAA"
PBKDF2_ITERATIONS = 310_000  # Recomendación actual de seguridad
SALT_LENGTH_BYTES = 16


class EncryptionService:
    """
    Servicio para encriptar/desencriptar datos sensibles.

    Usa una clave base y un salt derivados de ENCRYPTION_KEY y ENCRYPTION_SALT
    del entorno. En entornos de desarrollo, si no se proporcionan, se generan
    automáticamente claves y salts aleatorios (NO SEGURO PARA PRODUCCIÓN).
    En producción, la ausencia de estas variables resultará en un error.
    """

    def __init__(self, encryption_key: Optional[str] = None, encryption_salt: Optional[str] = None):
        """
        Inicializa el servicio de encriptación.

        Args:
            encryption_key: Clave base para derivar la clave Fernet.
            encryption_salt: Salt para la derivación de la clave Fernet.
        """
        self.is_production = os.getenv("APP_ENV", "development").lower() == "production"

        # --- Manejo de la Clave de Encriptación ---
        key_source = encryption_key or os.getenv("ENCRYPTION_KEY")
        if not key_source:
            if self.is_production:
                logger.critical("❌ ENCRYPTION_KEY no configurada. Es OBLIGATORIA en producción.")
                raise ValueError("ENCRYPTION_KEY es obligatoria en producción.")
            else:
                key_source = secrets.token_urlsafe(32)
                logger.warning(
                    "⚠️ ENCRYPTION_KEY no configurada. Generando clave aleatoria (SOLO DESARROLLO)."
                )
        self.base_key = key_source

        # --- Manejo del Salt de Encriptación ---
        salt_source = encryption_salt or os.getenv("ENCRYPTION_SALT")
        if not salt_source:
            if self.is_production:
                logger.critical("❌ ENCRYPTION_SALT no configurada. Es OBLIGATORIA en producción.")
                raise ValueError("ENCRYPTION_SALT es obligatoria en producción.")
            else:
                salt_source = secrets.token_hex(SALT_LENGTH_BYTES)
                logger.warning(
                    "⚠️ ENCRYPTION_SALT no configurada. Generando salt aleatorio (SOLO DESARROLLO)."
                )
        self.salt = salt_source.encode('utf-8')

        # Derivar clave Fernet
        self.fernet = self._create_fernet(self.base_key, self.salt)

    def _create_fernet(self, base_key: str, salt: bytes) -> Fernet:
        """Crea instancia Fernet con clave derivada usando PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        derived_key = base64.urlsafe_b64encode(kdf.derive(base_key.encode('utf-8')))
        return Fernet(derived_key)

    def encrypt(self, plaintext: str) -> str:
        """
        Encripta un texto plano.

        Args:
            plaintext: Texto a encriptar (ej: API key)

        Returns:
            Texto encriptado en base64
        """
        if not plaintext:
            return ""

        try:
            encrypted = self.fernet.encrypt(plaintext.encode('utf-8'))
            return encrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Error inesperado al encriptar datos: {e}", exc_info=True)
            raise ValueError("Error de encriptación")

    def decrypt(self, ciphertext: str) -> str:
        """
        Desencripta un texto cifrado.

        Args:
            ciphertext: Texto encriptado en base64

        Returns:
            Texto plano original
        """
        if not ciphertext:
            return ""

        try:
            decrypted = self.fernet.decrypt(ciphertext.encode('utf-8'))
            return decrypted.decode('utf-8')
        except InvalidToken:
            logger.error("Token de encriptación inválido o clave incorrecta.")
            raise ValueError("Error de desencriptación: clave o token inválido")
        except Exception as e:
            logger.error(f"Error inesperado al desencriptar datos: {e}", exc_info=True)
            raise ValueError("Error de desencriptación")

    def is_encrypted(self, text: str) -> bool:
        """
        Verifica si un texto parece estar encriptado con Fernet.

        Args:
            text: Texto a verificar

        Returns:
            True si parece encriptado, False si no
        """
        if not text:
            return False

        return text.startswith(FERNET_HEADER_PREFIX) and len(text) > 100


# Instancia global (singleton)
_encryption_service: Optional[EncryptionService] = None


def get_encryption_service() -> EncryptionService:
    """Obtiene la instancia global del servicio de encriptación (singleton)."""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service
