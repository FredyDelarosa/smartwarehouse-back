"""
Puertos de seguridad.

Definen los contratos que la capa de aplicación necesita para
hashear contraseñas y emitir/validar tokens JWT.
Las implementaciones concretas viven en `app.infrastructure.security`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class PasswordHasherPort(ABC):
    """Contrato para el hashing de contraseñas."""

    @abstractmethod
    def hash(self, plain_password: str) -> str:
        """Devuelve el hash de una contraseña en texto plano."""
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash almacenado."""
        ...


class TokenProviderPort(ABC):
    """Contrato para emisión y validación de tokens JWT."""

    @abstractmethod
    def create_access_token(
        self,
        subject: str | int,
        extra_claims: Optional[dict[str, Any]] = None,
        expires_minutes: Optional[int] = None,
    ) -> str:
        """Crea un token de acceso."""
        ...

    @abstractmethod
    def create_refresh_token(
        self,
        subject: str | int,
        expires_days: Optional[int] = None,
    ) -> str:
        """Crea un token de refresco."""
        ...

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]:
        """
        Decodifica y valida un token.
        Lanza `jose.JWTError` si el token es inválido o está expirado.
        """
        ...