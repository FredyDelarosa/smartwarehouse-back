"""Caso de uso: qué productos hay en cada ubicación."""

from __future__ import annotations

from app.application.dtos import (
    ProductoEnUbicacionResumenDTO,
    UbicacionStockDTO,
)
from app.domain.repositories import InventarioRepository


class StockPorUbicacionUseCase:
    """
    Vista inversa del inventario: en lugar de "este producto, dónde está",
    responde "esta ubicación, qué tiene".

    Es lo que necesita el listado de ubicaciones. Componerlo con las rutas
    existentes no sirve: `/inventario/producto/{id}` es por producto y
    `/ubicaciones/qr/{código}` es por ubicación, así que pintar 20 filas de la
    tabla costaría 20 peticiones.
    """

    def __init__(self, inventario_repo: InventarioRepository) -> None:
        self._inventario_repo = inventario_repo

    async def execute(
        self, *, skip: int = 0, limit: int = 50, solo_activas: bool = True
    ) -> list[UbicacionStockDTO]:
        filas = await self._inventario_repo.listar_con_productos(
            skip=skip, limit=limit, solo_activas=solo_activas
        )

        resultado: list[UbicacionStockDTO] = []
        for ubicacion, productos in filas:
            if ubicacion.id is None:
                continue

            resumen: list[ProductoEnUbicacionResumenDTO] = []
            total = 0
            for producto, cantidad in productos:
                if producto.id is None:
                    continue
                resumen.append(
                    ProductoEnUbicacionResumenDTO(
                        producto_id=producto.id,
                        codigo=producto.codigo,
                        nombre=producto.nombre,
                        cantidad=cantidad,
                    )
                )
                total += cantidad

            resultado.append(
                UbicacionStockDTO(
                    ubicacion_id=ubicacion.id,
                    codigo_ubicacion=ubicacion.codigo_ubicacion,
                    pasillo=ubicacion.pasillo,
                    estante=ubicacion.estante,
                    nivel=ubicacion.nivel,
                    productos=resumen,
                    total_unidades=total,
                )
            )
        return resultado