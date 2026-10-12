"""Endpoints de métricas e indicadores."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from app.application.dtos import (
    ComparativaBusquedaDTO,
    DashboardResumenDTO,
    ResumenIncidenciasDTO,
    ResumenMovimientosDTO,
    TiempoPromedioBusquedaDTO,
)
from app.application.use_cases.metricas import (
    CompararBusquedasUseCase,
    DashboardResumenUseCase,
    ResumenIncidenciasUseCase,
    ResumenMovimientosUseCase,
    TiempoPromedioBusquedaUseCase,
)
from app.infrastructure.api.dependencies import (
    BusquedaRepoDep,
    IncidenciaRepoDep,
    InventarioRepoDep,
    MovimientoRepoDep,
    ProductoRepoDep,
    UbicacionRepoDep,
)

router = APIRouter(prefix="/metricas", tags=["metricas"])


# ============================================================
# GET /metricas/tiempo-promedio
# ============================================================
@router.get(
    "/tiempo-promedio",
    response_model=TiempoPromedioBusquedaDTO,
    summary="Tiempo promedio de búsqueda",
)
async def tiempo_promedio(
    busqueda_repo: BusquedaRepoDep = None,
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
) -> TiempoPromedioBusquedaDTO:
    use_case = TiempoPromedioBusquedaUseCase(busqueda_repo)
    return await use_case.execute(desde=desde, hasta=hasta)


# ============================================================
# GET /metricas/comparativa
# ============================================================
@router.get(
    "/comparativa",
    response_model=ComparativaBusquedaDTO,
    summary="Comparar dos periodos de búsquedas",
)
async def comparativa(
    busqueda_repo: BusquedaRepoDep = None,
    desde_anterior: datetime = Query(...),
    hasta_anterior: datetime = Query(...),
    desde_actual: datetime = Query(...),
    hasta_actual: datetime = Query(...),
) -> ComparativaBusquedaDTO:
    use_case = CompararBusquedasUseCase(busqueda_repo)
    return await use_case.execute(
        desde_anterior=desde_anterior,
        hasta_anterior=hasta_anterior,
        desde_actual=desde_actual,
        hasta_actual=hasta_actual,
    )


# ============================================================
# GET /metricas/incidencias
# ============================================================
@router.get(
    "/incidencias",
    response_model=ResumenIncidenciasDTO,
    summary="Resumen de incidencias",
)
async def resumen_incidencias(
    incidencia_repo: IncidenciaRepoDep = None,
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
) -> ResumenIncidenciasDTO:
    use_case = ResumenIncidenciasUseCase(incidencia_repo)
    return await use_case.execute(desde=desde, hasta=hasta)


# ============================================================
# GET /metricas/movimientos
# ============================================================
@router.get(
    "/movimientos",
    response_model=ResumenMovimientosDTO,
    summary="Resumen de movimientos",
)
async def resumen_movimientos(
    movimiento_repo: MovimientoRepoDep = None,
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
) -> ResumenMovimientosDTO:
    use_case = ResumenMovimientosUseCase(movimiento_repo)
    return await use_case.execute(desde=desde, hasta=hasta)


# ============================================================
# GET /metricas/dashboard
# ============================================================
@router.get(
    "/dashboard",
    response_model=DashboardResumenDTO,
    summary="Dashboard con indicadores clave",
)
async def dashboard(
    producto_repo: ProductoRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    incidencia_repo: IncidenciaRepoDep = None,
    busqueda_repo: BusquedaRepoDep = None,
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
) -> DashboardResumenDTO:
    use_case = DashboardResumenUseCase(
        producto_repo,
        ubicacion_repo,
        inventario_repo,
        incidencia_repo,
        busqueda_repo,
    )
    return await use_case.execute(desde=desde, hasta=hasta)
