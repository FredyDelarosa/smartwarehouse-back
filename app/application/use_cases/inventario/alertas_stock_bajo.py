"""Caso de uso: listar productos con stock por debajo del mínimo."""

from __future__ import annotations

from app.application.dtos import ProductoStockBajoDTO
from app.domain.repositories import InventarioRepository


class AlertasStockBajoUseCase:
    def __init__(self, inventario_repo: InventarioRepository) -> None:
        self._inventario_repo = inventario_repo

    async def execute(self) -> list[ProductoStockBajoDTO]:
        filas = await self._inventario_repo.list_stock_bajo()
        resultado: list[ProductoStockBajoDTO] = []
        for producto, stock_total in filas:
            if producto.id is None:
                continue
            faltante = max(0, producto.stock_minimo - stock_total)
            resultado.append(
                ProductoStockBajoDTO(
                    producto_id=producto.id,
                    codigo=producto.codigo,
                    nombre=producto.nombre,
                    unidad_medida=producto.unidad_medida,
                    stock_total=stock_total,
                    stock_minimo=producto.stock_minimo,
                    faltante=faltante,
                )
            )
        return resultado