"""Caso de uso: listar incidencias con filtros."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.dtos import IncidenciaReadDTO
from app.domain.entities import TipoIncidencia
from app.domain.repositories import IncidenciaRepository


class ListarIncidenciasUseCase:
    def __init__(self, incidencia_repo: IncidenciaRepository) -> None:
        self._incidencia_repo = incidencia_repo

    async def execute(
        self,
        *,
        tipo: Optional[TipoIncidencia] = None,
        resuelta: Optional[bool] = None,
        producto_id: Optional[int] = None,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[IncidenciaReadDTO]:
        incidencias = await self._incidencia_repo.list(
            tipo=tipo,
            resuelta=resuelta,
            producto_id=producto_id,
            desde=desde,
            hasta=hasta,
            skip=skip,
            limit=limit,
        )
        return [IncidenciaReadDTO.model_validate(i) for i in incidencias]