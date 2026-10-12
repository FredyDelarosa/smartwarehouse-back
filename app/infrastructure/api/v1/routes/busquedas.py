"""Endpoints de búsquedas."""

from __future__ import annotations

from fastapi import APIRouter, Query, status

from app.application.dtos import (
    BusquedaFinalizadaDTO,
    BusquedaReadDTO,
    FinalizarBusquedaDTO,
    IniciarBusquedaDTO,
    ResultadoBusquedaDTO,
)
from app.application.use_cases.busquedas import (
    FinalizarBusquedaUseCase,
    HistorialBusquedasUseCase,
    IniciarBusquedaUseCase,
)
from app.infrastructure.api.dependencies import (
    BusquedaRepoDep,
    CurrentUserDep,
    InventarioRepoDep,
    ProductoRepoDep,
    SessionDep,
    UbicacionRepoDep,
)

router = APIRouter(prefix="/busquedas", tags=["busquedas"])


# ============================================================
# POST /busquedas/iniciar
# ============================================================
@router.post(
    "/iniciar",
    response_model=ResultadoBusquedaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar una búsqueda de producto",
)
async def iniciar_busqueda(
    payload: IniciarBusquedaDTO,
    current_user: CurrentUserDep = None,
    producto_repo: ProductoRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    busqueda_repo: BusquedaRepoDep = None,
    session: SessionDep = None,
) -> ResultadoBusquedaDTO:
    use_case = IniciarBusquedaUseCase(
        producto_repo, inventario_repo, ubicacion_repo, busqueda_repo
    )
    resultado = await use_case.execute(payload, current_user.id or 0)
    await session.commit()
    return resultado


# ============================================================
# POST /busquedas/{busqueda_id}/finalizar
# ============================================================
@router.post(
    "/{busqueda_id}/finalizar",
    response_model=BusquedaFinalizadaDTO,
    summary="Finalizar una búsqueda",
)
async def finalizar_busqueda(
    busqueda_id: int,
    payload: FinalizarBusquedaDTO,
    busqueda_repo: BusquedaRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    session: SessionDep = None,
) -> BusquedaFinalizadaDTO:
    use_case = FinalizarBusquedaUseCase(busqueda_repo, ubicacion_repo)
    resultado = await use_case.execute(busqueda_id, payload)
    await session.commit()
    return resultado


# ============================================================
# GET /busquedas/historial
# ============================================================
@router.get(
    "/historial",
    response_model=list[BusquedaReadDTO],
    summary="Historial de búsquedas del usuario",
)
async def historial_busquedas(
    current_user: CurrentUserDep = None,
    busqueda_repo: BusquedaRepoDep = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[BusquedaReadDTO]:
    use_case = HistorialBusquedasUseCase(busqueda_repo)
    return await use_case.execute(
        current_user.id or 0, skip=skip, limit=limit
    )
