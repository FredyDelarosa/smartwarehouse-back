"""Caso de uso: consultar stock consolidado de un producto."""

from __future__ import annotations

from app.application.dtos import StockPorUbicacionDTO, StockTotalProductoDTO
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories import (
    InventarioRepository,
    ProductoRepository,
    UbicacionRepository,
)


class ConsultarStockUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        inventario_repo: InventarioRepository,
        ubicacion_repo: UbicacionRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._inventario_repo = inventario_repo
        self._ubicacion_repo = ubicacion_repo

    async def execute(self, producto_id: int) -> StockTotalProductoDTO:
        # 1. Recuperar producto
        producto = await self._producto_repo.get_by_id(producto_id)
        if producto is None or producto.id is None:
            raise ProductoNoEncontradoError(details={"producto_id": producto_id})

        # 2. Traer los registros de inventario de ese producto
        inventarios = await self._inventario_repo.list_by_producto(producto.id)

        # 3. Armar la distribución por ubicación
        distribucion: list[StockPorUbicacionDTO] = []
        stock_total = 0
        for inv in inventarios:
            ubicacion = await self._ubicacion_repo.get_by_id(inv.ubicacion_id)
            if ubicacion is None:
                continue
            stock_total += inv.cantidad
            distribucion.append(
                StockPorUbicacionDTO(
                    ubicacion_id=ubicacion.id or 0,
                    codigo_ubicacion=ubicacion.codigo_ubicacion,
                    pasillo=ubicacion.pasillo,
                    estante=ubicacion.estante,
                    nivel=ubicacion.nivel,
                    cantidad=inv.cantidad,
                )
            )

        # Orden estable: por código de ubicación
        distribucion.sort(key=lambda d: d.codigo_ubicacion)

        return StockTotalProductoDTO(
            producto_id=producto.id,
            codigo=producto.codigo,
            nombre=producto.nombre,
            unidad_medida=producto.unidad_medida,
            stock_minimo=producto.stock_minimo,
            stock_total=stock_total,
            requiere_alerta=producto.requiere_alerta_por(stock_total),
            distribucion=distribucion,
        )