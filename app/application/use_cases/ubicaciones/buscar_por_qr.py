"""Caso de uso: escanear un QR de ubicación y ver qué debería haber ahí."""

from __future__ import annotations

from app.application.dtos import (
    ProductoEnUbicacionDTO,
    UbicacionQRReadDTO,
    UbicacionReadDTO,
)
from app.domain.exceptions import UbicacionNoEncontradaError
from app.domain.repositories import (
    InventarioRepository,
    ProductoRepository,
    UbicacionRepository,
)


class BuscarUbicacionPorQRUseCase:
    def __init__(
        self,
        ubicacion_repo: UbicacionRepository,
        inventario_repo: InventarioRepository,
        producto_repo: ProductoRepository,
    ) -> None:
        self._ubicacion_repo = ubicacion_repo
        self._inventario_repo = inventario_repo
        self._producto_repo = producto_repo

    async def execute(self, codigo_qr: str) -> UbicacionQRReadDTO:
        # 1. Localizar la ubicación por QR
        ubicacion = await self._ubicacion_repo.get_by_qr(codigo_qr)
        if ubicacion is None:
            raise UbicacionNoEncontradaError(
                "Ubicación no encontrada para el QR escaneado",
                details={"codigo_qr": codigo_qr},
            )
        if ubicacion.id is None:
            raise UbicacionNoEncontradaError(
                "La ubicación no tiene id asignado"
            )

        # 2. Traer los registros de inventario de esa ubicación
        inventarios = await self._inventario_repo.list_by_ubicacion(ubicacion.id)

        # 3. Cargar cada producto referenciado y armar el DTO
        productos: list[ProductoEnUbicacionDTO] = []
        for inv in inventarios:
            producto = await self._producto_repo.get_by_id(inv.producto_id)
            if producto is None:
                continue
            productos.append(
                ProductoEnUbicacionDTO(
                    producto_id=producto.id if producto.id is not None else 0,
                    codigo=producto.codigo,
                    nombre=producto.nombre,
                    cantidad=inv.cantidad,
                )
            )

        # Ordenar por nombre para que la lectura sea estable
        productos.sort(key=lambda p: p.nombre)

        return UbicacionQRReadDTO(
            ubicacion=UbicacionReadDTO.model_validate(ubicacion),
            productos=productos,
        )