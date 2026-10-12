"""Endpoints de ubicaciones."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.application.dtos import (
    UbicacionCreateDTO,
    UbicacionQRReadDTO,
    UbicacionReadDTO,
)
from app.application.use_cases.ubicaciones import (
    BuscarUbicacionPorQRUseCase,
    CrearUbicacionUseCase,
    ListarUbicacionesUseCase,
)
from app.domain.exceptions import UbicacionNoEncontradaError
from app.infrastructure.api.dependencies import (
    AlmacenRepoDep,
    InventarioRepoDep,
    ProductoRepoDep,
    UbicacionRepoDep,
    require_role,
)

router = APIRouter(prefix="/ubicaciones", tags=["ubicaciones"])


# ============================================================
# GET /ubicaciones
# ============================================================
@router.get(
    "/",
    response_model=list[UbicacionReadDTO],
    summary="Listar ubicaciones",
)
async def listar_ubicaciones(
    ubicacion_repo: UbicacionRepoDep = None,
    almacen_id: int = Query(None),
    solo_activas: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[UbicacionReadDTO]:
    use_case = ListarUbicacionesUseCase(ubicacion_repo)
    return await use_case.execute(
        almacen_id=almacen_id,
        solo_activas=solo_activas,
        skip=skip,
        limit=limit,
    )


# ============================================================
# GET /ubicaciones/{id}
# ============================================================
@router.get(
    "/{ubicacion_id}",
    response_model=UbicacionReadDTO,
    summary="Obtener una ubicación por ID",
)
async def obtener_ubicacion(
    ubicacion_id: int,
    ubicacion_repo: UbicacionRepoDep = None,
) -> UbicacionReadDTO:
    ubicacion = await ubicacion_repo.get_by_id(ubicacion_id)
    if ubicacion is None:
        raise UbicacionNoEncontradaError(
            details={"ubicacion_id": ubicacion_id}
        )
    return UbicacionReadDTO.model_validate(ubicacion)


# ============================================================
# POST /ubicaciones
# ============================================================
@router.post(
    "/",
    response_model=UbicacionReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva ubicación",
    dependencies=[Depends(require_role("Administrador"))],
)
async def crear_ubicacion(
    payload: UbicacionCreateDTO,
    ubicacion_repo: UbicacionRepoDep = None,
    almacen_repo: AlmacenRepoDep = None,
) -> UbicacionReadDTO:
    # Validar unicidad de codigo_qr (PET-2)
    if payload.codigo_qr:
        existente = await ubicacion_repo.get_by_qr(payload.codigo_qr)
        if existente is not None:
            from app.domain.exceptions import UbicacionDuplicadaError
            raise UbicacionDuplicadaError(
                "Ya existe una ubicación con ese código QR",
                details={"codigo_qr": payload.codigo_qr},
            )
    use_case = CrearUbicacionUseCase(ubicacion_repo, almacen_repo)
    return await use_case.execute(payload)


# ============================================================
# GET /ubicaciones/qr/{codigo}
# ============================================================
@router.get(
    "/qr/{codigo_qr}",
    response_model=UbicacionQRReadDTO,
    summary="Escanear QR de ubicación",
)
async def escanear_qr(
    codigo_qr: str,
    ubicacion_repo: UbicacionRepoDep = None,
    inventario_repo: InventarioRepoDep = None,
    producto_repo: ProductoRepoDep = None,
) -> UbicacionQRReadDTO:
    use_case = BuscarUbicacionPorQRUseCase(
        ubicacion_repo, inventario_repo, producto_repo
    )
    return await use_case.execute(codigo_qr)


# ============================================================
# GET /ubicaciones/almacen/{almacen_id}
# ============================================================
@router.get(
    "/almacen/{almacen_id}",
    response_model=list[UbicacionReadDTO],
    summary="Listar ubicaciones de un almacén",
)
async def listar_por_almacen(
    almacen_id: int,
    ubicacion_repo: UbicacionRepoDep = None,
    solo_activas: bool = Query(True),
) -> list[UbicacionReadDTO]:
    use_case = ListarUbicacionesUseCase(ubicacion_repo)
    return await use_case.execute(
        almacen_id=almacen_id,
        solo_activas=solo_activas,
    )
