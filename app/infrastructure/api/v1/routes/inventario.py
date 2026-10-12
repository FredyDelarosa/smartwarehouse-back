"""Endpoints de inventario."""

from __future__ import annotations

from fastapi import APIRouter

from app.application.dtos import (
    ProductoStockBajoDTO,
    StockTotalProductoDTO,
)
from app.application.use_cases.inventario import (
    AlertasStockBajoUseCase,
    ConsultarStockUseCase,
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
