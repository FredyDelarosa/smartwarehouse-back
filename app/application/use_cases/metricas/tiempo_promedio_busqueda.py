"""Caso de uso: tiempo promedio de búsqueda en un rango."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.dtos import TiempoPromedioBusquedaDTO
from app.domain.repositories import BusquedaRepository


class TiempoPromedioBusquedaUseCase:
    def __init__(self, busqueda_repo: BusquedaRepository) -> None:
        self._busqueda_repo = busqueda_repo

    async def execute(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> TiempoPromedioBusquedaDTO:
        promedio = await self._busqueda_repo.tiempo_promedio(
            desde=desde, hasta=hasta
        )
        total = await self._busqueda_repo.count(desde=desde, hasta=hasta)
        exitosas = await self._busqueda_repo.count(
            desde=desde, hasta=hasta, exito=True
        )
        fallidas = await self._busqueda_repo.count(
            desde=desde, hasta=hasta, exito=False
        )

        promedio_min = round(promedio / 60.0, 2) if promedio is not None else None

        return TiempoPromedioBusquedaDTO(
            desde=desde,
            hasta=hasta,
            total_busquedas=total,
            promedio_segundos=round(promedio, 2) if promedio is not None else None,
            promedio_minutos=promedio_min,
            exitosas=exitosas,
            fallidas=fallidas,
        )