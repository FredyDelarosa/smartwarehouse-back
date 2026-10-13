"""Endpoints de inventario."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.application.dtos import (
    ProductoStockBajoDTO,
    StockTotalProductoDTO,
    UbicacionStockDTO,
)
from app.application.use_cases.inventario import (
    AlertasStockBajoUseCase,
    ConsultarStockUseCase,
    StockPorUbicacionUseCase,
)
from app.infrastructure.api.dependencies import (
    InventarioRepoDep,
    ProductoRepoDep,
    UbicacionRepoDep,
)

router = APIRouter(prefix="/inventario", tags=["inventario"])


# ============================================================
# GET /inventario/producto/{producto_id}
# ============================================================
@router.get(
    "/producto/{producto_id}",
    response_model=StockTotalProductoDTO,
    summary="Consultar stock consolidado de un producto",
)
async def consultar_stock(
    producto_id: int,
    producto_repo: ProductoRepoDep,
    inventario_repo: InventarioRepoDep,
    ubicacion_repo: UbicacionRepoDep,
) -> StockTotalProductoDTO:
    use_case = ConsultarStockUseCase(
        producto_repo, inventario_repo, ubicacion_repo
    )
    return await use_case.execute(producto_id)


# ============================================================
# GET /inventario/alertas
# ============================================================
@router.get(
    "/alertas",
    response_model=list[ProductoStockBajoDTO],
    summary="Listar productos con stock bajo",
)
async def alertas_stock_bajo(
    inventario_repo: InventarioRepoDep,
) -> list[ProductoStockBajoDTO]:
    use_case = AlertasStockBajoUseCase(inventario_repo)
    return await use_case.execute()


# ============================================================
# GET /inventario/ubicaciones
# ============================================================
# No hay conflicto de orden con "/producto/{producto_id}": los prefijos de
# ruta son distintos ("producto/" frente a "ubicaciones"), así que "/ubicaciones"
# nunca casa con el {producto_id}. La ruta puede declararse en cualquier orden.
@router.get(
    "/ubicaciones",
    response_model=list[UbicacionStockDTO],
    summary="Listar ubicaciones con los productos que contienen",
)
async def stock_por_ubicacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    solo_activas: bool = Query(True),
    inventario_repo: InventarioRepoDep = None,
) -> list[UbicacionStockDTO]:
    """
    Vista inversa del inventario, para el listado de ubicaciones.

    No devuelve solo las ubicaciones con existencias, sino únicamente aquellas
    que tienen al menos una fila en `inventario`. Es lo que se pinta: un
    estante vacío no aporta nada en la columna de productos.
    """
    use_case = StockPorUbicacionUseCase(inventario_repo)
    return await use_case.execute(skip=skip, limit=limit, solo_activas=solo_activas)
