"""Casos de uso de búsquedas."""

from app.application.use_cases.busquedas.finalizar_busqueda import (
    FinalizarBusquedaUseCase,
)
from app.application.use_cases.busquedas.historial_busquedas import (
    HistorialBusquedasUseCase,
)
from app.application.use_cases.busquedas.iniciar_busqueda import (
    IniciarBusquedaUseCase,
)

__all__ = [
    "FinalizarBusquedaUseCase",
    "HistorialBusquedasUseCase",
    "IniciarBusquedaUseCase",
]