"""
Configuración del engine y la fábrica de sesiones asíncronas.
Usa `asyncmy` como driver, configurado a través de `Settings.database_url_async`.
Soporta conexiones TLS cuando `DB_SSL=True`.
"""

import ssl
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()


# ============================================================
# Contexto SSL (solo si DB_SSL=True)
# ============================================================
def _build_ssl_context() -> ssl.SSLContext:
    """
    Construye el SSLContext para la conexión.
    Si DB_SSL_CA está definido, se usa para verificar el certificado
    del servidor. Si no, se usa el bundle por defecto del sistema.
    """
    if settings.DB_SSL_CA:
        ctx = ssl.create_default_context(cafile=settings.DB_SSL_CA)
    else:
        ctx = ssl.create_default_context()
    return ctx


_connect_args: dict = {}
if settings.DB_SSL:
    _connect_args["ssl"] = _build_ssl_context()


# ============================================================
# Engine asíncrono
# ============================================================
engine: AsyncEngine = create_async_engine(
    settings.database_url_async,
    echo=settings.DB_ECHO,
    connect_args=_connect_args,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    future=True,
)


# ============================================================
# Fábrica de sesiones
# ============================================================
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provee una sesión asíncrona por request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise