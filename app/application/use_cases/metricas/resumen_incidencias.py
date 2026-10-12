"""Caso de uso: resumen de incidencias."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.dtos import ResumenIncidenciasDTO
from app.domain.entities import TipoIncidencia
from app.domain.repositories import IncidenciaRepository


class ResumenIncidenciasUseCase:
    def __init__(self, incidencia_repo: IncidenciaRepository) -> None:
        self._incidencia_repo = incidencia_repo

    async def execute(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> ResumenIncidenciasDTO:
        todas = await self._incidencia_repo.list(
            desde=desde, hasta=hasta, limit=10000
        )
        abiertas = sum(1 for i in todas if not i.resuelta)
        resueltas = sum(1 for i in todas if i.resuelta)

        por_tipo: dict[TipoIncidencia, int] = {t: 0 for t in TipoIncidencia}
        for inc in todas:
            por_tipo[inc.tipo] = por_tipo.get(inc.tipo, 0) + 1

        return ResumenIncidenciasDTO(
            total=len(todas),
            abiertas=abiertas,
            resueltas=resueltas,
            por_tipo=por_tipo,
        )