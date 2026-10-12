"""Endpoints de health check y verificación de autenticación."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.core.config import get_settings
from app.infrastructure.api.dependencies import CurrentUserDep, SessionDep

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


@router.get("", summary="Liveness probe")
async def health() -> dict:
    """Verifica que la API responde. No toca base de datos."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/db", summary="Readiness probe (verifica conexión a BD)")
async def health_db(session: SessionDep) -> dict:
    result = await session.execute(text("SELECT 1"))
    result.scalar()
    return {"status": "ok", "database": "reachable"}


@router.get("/me", summary="Devuelve el usuario autenticado")
async def health_me(current_user: CurrentUserDep) -> dict:
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.nombre_rol,
    }