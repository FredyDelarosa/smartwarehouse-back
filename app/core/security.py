"""
Utilidades de seguridad: hashing de contraseñas y JWT.
Es infraestructura reusable, por eso vive en core (cross-cutting).
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

# ------------------------------------------------------------------
# Workaround para el warning de passlib 1.7.4 con bcrypt >= 4.1
# (passlib intenta leer bcrypt.__about__.__version__, removido en 4.1+)
# ------------------------------------------------------------------
import bcrypt as _bcrypt

if not hasattr(_bcrypt, "__about__"):
    class _About:  # noqa: D401
        __version__ = getattr(_bcrypt, "__version__", "4.0.0")

    _bcrypt.__about__ = _About()  # type: ignore[attr-defined]

# ------------------------------------------------------------------
# Contexto de hashing
# ------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = get_settings()


# ============================================================
# CONTRASEÑAS
# ============================================================
def hash_password(plain_password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, TypeError):
        return False


# ============================================================
# JWT
# ============================================================
def create_access_token(
    subject: str | int,
    extra_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Crea un JWT de acceso.

    Args:
        subject: identificador del usuario (normalmente user.id).
        extra_claims: claims adicionales (ej. {"rol": "Administrador"}).
        expires_delta: expiración personalizada.

    Returns:
        Token JWT firmado como string.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Crea un JWT de refresco (vida más larga, solo para renovar)."""
    if expires_delta is None:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida un JWT.

    Raises:
        JWTError: si el token es inválido o está expirado.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )