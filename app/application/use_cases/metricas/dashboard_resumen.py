"""Caso de uso: dashboard con los indicadores clave."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.application.dtos import DashboardResumenDTO
from app.domain.repositories import (
    BusquedaRepository,
    IncidenciaRepository,
    InventarioRepository,
    ProductoRepository,
    UbicacionRepository,
)


class DashboardResumenUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        ubicacion_repo: UbicacionRepository,
        inventario_repo: InventarioRepository,
        incidencia_repo: IncidenciaRepository,
        busqueda_repo: BusquedaRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._ubicacion_repo = ubicacion_repo
        self._inventario_repo = inventario_repo
        self._incidencia_repo = incidencia_repo
        self._busqueda_repo = busqueda_repo

    async def execute(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> DashboardResumenDTO:
        # Productos (activos)
        total_productos = await self._producto_repo.count(solo_activos=True)

        # Ubicaciones: contamos en memoria (150 filas hoy)
        ubicaciones = await self._ubicacion_repo.list(skip=0, limit=10000)
        total_ubicaciones = len(ubicaciones)

        # Alertas de stock
        stock_bajo = await self._inventario_repo.list_stock_bajo()
        productos_stock_bajo = len(stock_bajo)

        # Incidencias abiertas
        abiertas = await self._incidencia_repo.list(
            resuelta=False, limit=10000
        )
        total_incidencias_abiertas = len(abiertas)

        # Métricas de búsqueda
        promedio = await self._busqueda_repo.tiempo_promedio(
            desde=desde, hasta=hasta
        )
        total_busquedas = await self._busqueda_repo.count(
            desde=desde, hasta=hasta
        )

        return DashboardResumenDTO(
            total_productos=total_productos,
            total_ubicaciones=total_ubicaciones,
            productos_stock_bajo=productos_stock_bajo,
            total_incidencias_abiertas=total_incidencias_abiertas,
            tiempo_promedio_busqueda_segundos=(
                round(promedio, 2) if promedio is not None else None
            ),
            tiempo_promedio_busqueda_minutos=(
                round(promedio / 60.0, 2) if promedio is not None else None
            ),
            total_busquedas=total_busquedas,
        )