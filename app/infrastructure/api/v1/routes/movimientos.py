"""Endpoints de movimientos de inventario."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.application.dtos import MovimientoCreateDTO, MovimientoReadDTO
from app.application.use_cases.movimientos import (
    RegistrarEntradaUseCase,
    RegistrarSalidaUseCase,
    RegistrarTrasladoUseCase,
)
from app.domain.entities import TipoMovimiento
from app.infrastructure.api.dependencies import (
    CurrentUserDep,
    InventarioRepoDep,
    MovimientoRepoDep,
    ProductoRepoDep,
    UbicacionRepoDep,
    require_role,
)

router = APIRouter(prefix="/movimientos", tags=["movimientos"])


# ============================================================
# POST /movimientos/entrada
# ============================================================
@router.post(
    "/entrada",
    response_model=MovimientoReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una entrada de producto",
    dependencies=[Depends(require_role("Almacenero", "Supervisor"))],
)
async def registrar_entrada(
    payload: MovimientoCreateDTO,
    current_user: CurrentUserDep = None,
    producto_repo: ProductoRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    movimiento_repo: MovimientoRepoDep = None,
) -> MovimientoReadDTO:
    use_case = RegistrarEntradaUseCase(
        producto_repo, ubicacion_repo, inventario_repo, movimiento_repo
    )
    return await use_case.execute(payload, current_user.id or 0)


# ============================================================
# POST /movimientos/salida
# ============================================================
@router.post(
    "/salida",
    response_model=MovimientoReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una salida de producto",
    dependencies=[Depends(require_role("Almacenero", "Supervisor"))],
)
async def registrar_salida(
    payload: MovimientoCreateDTO,
    current_user: CurrentUserDep = None,
    producto_repo: ProductoRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    movimiento_repo: MovimientoRepoDep = None,
) -> MovimientoReadDTO:
    use_case = RegistrarSalidaUseCase(
        producto_repo, ubicacion_repo, inventario_repo, movimiento_repo
    )
    return await use_case.execute(payload, current_user.id or 0)


# ============================================================
# POST /movimientos/traslado
# ============================================================
@router.post(
    "/traslado",
    response_model=MovimientoReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un traslado entre ubicaciones",
    dependencies=[Depends(require_role("Almacenero", "Supervisor"))],
)
async def registrar_traslado(
    payload: MovimientoCreateDTO,
    current_user: CurrentUserDep = None,
    producto_repo: ProductoRepoDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    movimiento_repo: MovimientoRepoDep = None,
) -> MovimientoReadDTO:
    use_case = RegistrarTrasladoUseCase(
        producto_repo, ubicacion_repo, inventario_repo, movimiento_repo
    )
    return await use_case.execute(payload, current_user.id or 0)


# ============================================================
# GET /movimientos
# ============================================================
@router.get(
    "/",
    response_model=list[MovimientoReadDTO],
    summary="Listar movimientos con filtros",
)
async def listar_movimientos(
    movimiento_repo: MovimientoRepoDep = None,
    producto_id: int = Query(None),
    ubicacion_id: int = Query(None),
    usuario_id: int = Query(None),
    tipo: TipoMovimiento = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[MovimientoReadDTO]:
    movimientos = await movimiento_repo.list(
        producto_id=producto_id,
        ubicacion_id=ubicacion_id,
        usuario_id=usuario_id,
        tipo=tipo,
        skip=skip,
        limit=limit,
    )
    return [MovimientoReadDTO.model_validate(m) for m in movimientos]
