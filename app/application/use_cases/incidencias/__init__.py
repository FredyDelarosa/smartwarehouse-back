"""Casos de uso de incidencias."""

from app.application.use_cases.incidencias.crear_incidencia import (
    CrearIncidenciaUseCase,
)
from app.application.use_cases.incidencias.listar_incidencias import (
    ListarIncidenciasUseCase,
)
from app.application.use_cases.incidencias.resolver_incidencia import (
    ResolverIncidenciaUseCase,
)

__all__ = [
    "CrearIncidenciaUseCase",
    "ListarIncidenciasUseCase",
    "ResolverIncidenciaUseCase",
]