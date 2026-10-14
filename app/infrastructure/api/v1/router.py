"""Router agregador de la API v1."""

from __future__ import annotations

from fastapi import APIRouter

from app.infrastructure.api.v1.routes import (
    configuracion,
    auth,
    busquedas,
    categorias,
    health,
    incidencias,
    inventario,
    metricas,
    movimientos,
    productos,
    ubicaciones,
)

api_v1_router = APIRouter()

api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(productos.router)
api_v1_router.include_router(categorias.router)
api_v1_router.include_router(ubicaciones.router)
api_v1_router.include_router(inventario.router)
api_v1_router.include_router(movimientos.router)
api_v1_router.include_router(busquedas.router)
api_v1_router.include_router(incidencias.router)
api_v1_router.include_router(metricas.router)
api_v1_router.include_router(configuracion.router)

__all__ = ["api_v1_router"]
