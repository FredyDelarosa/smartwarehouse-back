"""Caso de uso: listar ubicaciones."""

from __future__ import annotations

from typing import Optional

from app.application.dtos import UbicacionReadDTO
from app.domain.repositories import UbicacionRepository


class ListarUbicacionesUseCase:
    def __init__(self, ubicacion_repo: UbicacionRepository) -> None:
        self._ubicacion_repo = ubicacion_repo

    async def execute(
        self,
        *,
        almacen_id: Optional[int] = None,
        solo_activas: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> list[UbicacionReadDTO]:
        if almacen_id is not None:
            ubicaciones = await self._ubicacion_repo.list_by_almacen(
                almacen_id, solo_activas=solo_activas
            )
            ubicaciones = ubicaciones[skip : skip + limit]
        else:
            ubicaciones = await self._ubicacion_repo.list(
                skip=skip, limit=limit
            )
        return [UbicacionReadDTO.model_validate(u) for u in ubicaciones]