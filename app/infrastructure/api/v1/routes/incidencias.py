"""Endpoints de incidencias."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.application.dtos import (
    IncidenciaCreateDTO,
    IncidenciaReadDTO,
)
from app.application.use_cases.incidencias import (
    CrearIncidenciaUseCase,
    ListarIncidenciasUseCase,
    ResolverIncidenciaUseCase,
)
from app.domain.entities import TipoIncidencia
from app.infrastructure.api.dependencies import (
    SessionDep,
    CurrentUserDep,
    IncidenciaRepoDep,
    ProductoRepoDep,
    UbicacionRepoDep,
    require_role,
)

router = APIRouter(prefix="/incidencias", tags=["incidencias"])


# ============================================================
# GET /incidencias
# ============================================================
@router.get(
    "/",
    response_model=list[IncidenciaReadDTO],
    summary="Listar incidencias con filtros",
)
async def listar_incidencias(
    incidencia_repo: IncidenciaRepoDep = None,
    tipo: Optional[TipoIncidencia] = Query(None),
    resuelta: Optional[bool] = Query(None),
    producto_id: Optional[int] = Query(None),
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[IncidenciaReadDTO]:
    use_case = ListarIncidenciasUseCase(incidencia_repo)
    return await use_case.execute(
        tipo=tipo,
        resuelta=resuelta,
        producto_id=producto_id,
        desde=desde,
        hasta=hasta,
        skip=skip,
        limit=limit,
    )


# ============================================================
# POST /incidencias
# ============================================================
@router.post(
    "/",
    response_model=IncidenciaReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una incidencia",
)
async def crear_incidencia(
    payload: IncidenciaCreateDTO,
    current_user: CurrentUserDep,
    incidencia_repo: IncidenciaRepoDep,
    producto_repo: ProductoRepoDep,
    ubicacion_repo: UbicacionRepoDep,
    session: SessionDep = None,
) -> IncidenciaReadDTO:
    use_case = CrearIncidenciaUseCase(
        incidencia_repo, producto_repo, ubicacion_repo
    )
    dto = await use_case.execute(payload, current_user.id or 0)

    # Sin commit la incidencia no se guardaba: 201 con un id que luego no
    # aparecía en el listado.
    await session.commit()
    return dto


# ============================================================
# POST /incidencias/{incidencia_id}/resolver
# ============================================================
@router.post(
    "/{incidencia_id}/resolver",
    response_model=IncidenciaReadDTO,
    summary="Resolver una incidencia",
    dependencies=[Depends(require_role("Administrador", "Almacenero", "Supervisor"))],
)
async def resolver_incidencia(
    incidencia_id: int,
    incidencia_repo: IncidenciaRepoDep,
    session: SessionDep = None,
) -> IncidenciaReadDTO:
    use_case = ResolverIncidenciaUseCase(incidencia_repo)
    dto = await use_case.execute(incidencia_id)

    # Sin commit la incidencia seguía apareciendo como abierta.
    await session.commit()
    return dto
