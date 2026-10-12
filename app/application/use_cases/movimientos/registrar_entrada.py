"""Caso de uso: registrar una entrada de producto a una ubicación."""

from __future__ import annotations

from app.application.dtos import MovimientoCreateDTO, MovimientoReadDTO
from app.domain.entities import Movimiento, TipoMovimiento
from app.domain.exceptions import (
    EntidadNoEncontradaError,
    MovimientoInvalidoError,
    ProductoNoEncontradoError,
    UbicacionNoEncontradaError,
)
from app.domain.repositories import (
    InventarioRepository,
    MovimientoRepository,
    ProductoRepository,
    UbicacionRepository,
)


class RegistrarEntradaUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        ubicacion_repo: UbicacionRepository,
        inventario_repo: InventarioRepository,
        movimiento_repo: MovimientoRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._ubicacion_repo = ubicacion_repo
        self._inventario_repo = inventario_repo
        self._movimiento_repo = movimiento_repo

    async def execute(
        self, dto: MovimientoCreateDTO, usuario_id: int
    ) -> MovimientoReadDTO:
        if dto.tipo != TipoMovimiento.ENTRADA:
            raise MovimientoInvalidoError(
                "Este caso de uso solo acepta movimientos de tipo ENTRADA"
            )
        if dto.ubicacion_destino_id is None:
            raise MovimientoInvalidoError("Una ENTRADA requiere ubicación destino")

        # 1. Validar producto
        producto = await self._producto_repo.get_by_id(dto.producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(
                details={"producto_id": dto.producto_id}
            )
        if not producto.esta_activo():
            raise EntidadNoEncontradaError(
                "Producto inactivo", details={"producto_id": dto.producto_id}
            )

        # 2. Validar ubicación destino
        ubicacion = await self._ubicacion_repo.get_by_id(dto.ubicacion_destino_id)
        if ubicacion is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": dto.ubicacion_destino_id}
            )

        # 3. Incrementar stock
        await self._inventario_repo.upsert(
            producto_id=dto.producto_id,
            ubicacion_id=dto.ubicacion_destino_id,
            delta_cantidad=dto.cantidad,
        )

        # 4. Registrar movimiento
        movimiento = Movimiento(
            tipo=TipoMovimiento.ENTRADA,
            producto_id=dto.producto_id,
            cantidad=dto.cantidad,
            usuario_id=usuario_id,
            ubicacion_origen_id=None,
            ubicacion_destino_id=dto.ubicacion_destino_id,
            referencia=dto.referencia,
            observaciones=dto.observaciones,
        )
        errores = movimiento.validar()
        if errores:
            raise MovimientoInvalidoError(errores=errores)

        creado = await self._movimiento_repo.create(movimiento)
        return MovimientoReadDTO.model_validate(creado)