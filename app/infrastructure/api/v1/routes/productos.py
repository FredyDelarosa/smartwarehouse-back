"""Endpoints de productos."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.application.dtos import (
    ProductoCreateDTO,
    ProductoReadDTO,
    ProductoUpdateDTO,
)
from app.application.use_cases.productos import (
    ActualizarProductoUseCase,
    CrearProductoUseCase,
    EliminarProductoUseCase,
    ListarProductosUseCase,
    ObtenerProductoUseCase,
)
from app.infrastructure.api.dependencies import (
    CategoriaRepoDep,
    ProductoRepoDep,
    require_role,
)

router = APIRouter(prefix="/productos", tags=["productos"])


# ============================================================
# GET /productos
# ============================================================
@router.get(
    "/",
    response_model=list[ProductoReadDTO],
    summary="Listar productos con paginación",
)
async def listar_productos(
    producto_repo: ProductoRepoDep = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    categoria_id: Optional[int] = Query(None),
    solo_activos: bool = Query(False),
) -> list[ProductoReadDTO]:
    use_case = ListarProductosUseCase(producto_repo)
    productos, _ = await use_case.execute(
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
        solo_activos=solo_activos,
    )
    return productos


# ============================================================
# GET /productos/buscar
# ============================================================
@router.get(
    "/buscar",
    response_model=list[ProductoReadDTO],
    summary="Buscar productos por nombre o código",
)
async def buscar_productos(
    producto_repo: ProductoRepoDep = None,
    termino: str = Query(..., min_length=1, max_length=150),
    limit: int = Query(20, ge=1, le=100),
) -> list[ProductoReadDTO]:
    productos = await producto_repo.search(termino, limit=limit)
    return [ProductoReadDTO.model_validate(p) for p in productos]


# ============================================================
# GET /productos/{id}
# ============================================================
@router.get(
    "/{producto_id}",
    response_model=ProductoReadDTO,
    summary="Obtener un producto por ID",
)
async def obtener_producto(
    producto_id: int,
    producto_repo: ProductoRepoDep = None,
) -> ProductoReadDTO:
    use_case = ObtenerProductoUseCase(producto_repo)
    return await use_case.execute(producto_id)


# ============================================================
# POST /productos
# ============================================================
@router.post(
    "/",
    response_model=ProductoReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    dependencies=[Depends(require_role("Administrador", "Supervisor"))],
)
async def crear_producto(
    payload: ProductoCreateDTO,
    producto_repo: ProductoRepoDep = None,
    categoria_repo: CategoriaRepoDep = None,
) -> ProductoReadDTO:
    use_case = CrearProductoUseCase(producto_repo, categoria_repo)
    return await use_case.execute(payload)


# ============================================================
# PATCH /productos/{id}
# ============================================================
@router.patch(
    "/{producto_id}",
    response_model=ProductoReadDTO,
    summary="Actualizar un producto existente",
    dependencies=[Depends(require_role("Administrador", "Supervisor"))],
)
async def actualizar_producto(
    producto_id: int,
    payload: ProductoUpdateDTO,
    producto_repo: ProductoRepoDep = None,
    categoria_repo: CategoriaRepoDep = None,
) -> ProductoReadDTO:
    use_case = ActualizarProductoUseCase(producto_repo, categoria_repo)
    return await use_case.execute(producto_id, payload)


# ============================================================
# DELETE /productos/{id}
# ============================================================
@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Dar de baja un producto (baja lógica)",
    dependencies=[Depends(require_role("Administrador"))],
)
async def eliminar_producto(
    producto_id: int,
    producto_repo: ProductoRepoDep = None,
) -> None:
    use_case = EliminarProductoUseCase(producto_repo)
    await use_case.execute(producto_id)
