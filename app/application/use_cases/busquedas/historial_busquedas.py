"""Caso de uso: historial de búsquedas de un usuario."""

from __future__ import annotations

from app.application.dtos import BusquedaReadDTO
from app.domain.repositories import BusquedaRepository


class HistorialBusquedasUseCase:
    def __init__(self, busqueda_repo: BusquedaRepository) -> None:
        self._busqueda_repo = busqueda_repo

    async def execute(
        self, usuario_id: int, *, skip: int = 0, limit: int = 50
    ) -> list[BusquedaReadDTO]:
        busquedas = await self._busqueda_repo.list_by_usuario(
            usuario_id, skip=skip, limit=limit
        )
        return [BusquedaReadDTO.model_validate(b) for b in busquedas]