"""Caso de uso: resumen de movimientos."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.dtos import ResumenMovimientosDTO
from app.domain.entities import TipoMovimiento
from app.domain.repositories import MovimientoRepository


class ResumenMovimientosUseCase:
    def __init__(self, movimiento_repo: MovimientoRepository) -> None:
        self._movimiento_repo = movimiento_repo

    async def execute(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> ResumenMovimientosDTO:
        # Traemos todos los movimientos del rango y agregamos en memoria.
        # Con los volúmenes actuales es perfectamente aceptable; si en el
        # futuro crece mucho, se refactoriza con SUM agrupado en el repo.
        movimientos = await self._movimiento_repo.list(
            desde=desde, hasta=hasta, limit=10000
        )

        por_tipo: dict[TipoMovimiento, int] = {t: 0 for t in TipoMovimiento}
        total_piezas = 0
        for mov in movimientos:
            por_tipo[mov.tipo] = por_tipo.get(mov.tipo, 0) + 1
            total_piezas += mov.cantidad

        return ResumenMovimientosDTO(
            total=len(movimientos),
            por_tipo=por_tipo,
            total_piezas_movidas=total_piezas,
        )