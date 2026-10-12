"""Caso de uso: comparar dos periodos de búsquedas."""

from __future__ import annotations

from datetime import datetime

from app.application.dtos import ComparativaBusquedaDTO
from app.domain.repositories import BusquedaRepository


class CompararBusquedasUseCase:
    def __init__(self, busqueda_repo: BusquedaRepository) -> None:
        self._busqueda_repo = busqueda_repo

    async def execute(
        self,
        *,
        desde_anterior: datetime,
        hasta_anterior: datetime,
        desde_actual: datetime,
        hasta_actual: datetime,
    ) -> ComparativaBusquedaDTO:
        from app.application.use_cases.metricas.tiempo_promedio_busqueda import (
            TiempoPromedioBusquedaUseCase,
        )

        tp = TiempoPromedioBusquedaUseCase(self._busqueda_repo)
        anterior = await tp.execute(desde=desde_anterior, hasta=hasta_anterior)
        actual = await tp.execute(desde=desde_actual, hasta=hasta_actual)

        mejora_segundos = None
        mejora_porcentaje = None
        if (
            anterior.promedio_segundos is not None
            and actual.promedio_segundos is not None
            and anterior.promedio_segundos > 0
        ):
            mejora_segundos = round(
                anterior.promedio_segundos - actual.promedio_segundos, 2
            )
            mejora_porcentaje = round(
                (mejora_segundos / anterior.promedio_segundos) * 100.0, 2
            )

        return ComparativaBusquedaDTO(
            periodo_actual=actual,
            periodo_anterior=anterior,
            mejora_segundos=mejora_segundos,
            mejora_porcentaje=mejora_porcentaje,
        )