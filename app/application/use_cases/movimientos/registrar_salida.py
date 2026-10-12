"""Caso de uso: registrar una salida de producto desde una ubicación."""

from __future__ import annotations

from app.application.dtos import MovimientoCreateDTO, MovimientoReadDTO
from app.domain.entities import Movimiento, TipoMovimiento
from app.domain.exceptions import (
    EntidadNoEncontradaError,
    MovimientoInvalidoError,
    ProductoNoEncontradoError,
    StockInsuficienteError,
    UbicacionNoEncontradaError,
)
from app.domain.repositories import (
    InventarioRepository,
    MovimientoRepository,
    ProductoRepository,
    UbicacionRepository,
)


class RegistrarSalidaUseCase:
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
        if dto.tipo != TipoMovimiento.SALIDA:
            raise MovimientoInvalidoError(
                "Este caso de uso solo acepta movimientos de tipo SALIDA"
            )
        if dto.ubicacion_origen_id is None:
            raise MovimientoInvalidoError("Una SALIDA requiere ubicación origen")

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

        # 2. Validar ubicación origen
        ubicacion = await self._ubicacion_repo.get_by_id(dto.ubicacion_origen_id)
        if ubicacion is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": dto.ubicacion_origen_id}
            )

        # 3. Verificar stock suficiente en ESA ubicación
        actual = await self._inventario_repo.get_by_producto_y_ubicacion(
            dto.producto_id, dto.ubicacion_origen_id
        )
        disponible = actual.cantidad if actual is not None else 0
        if disponible < dto.cantidad:
            raise StockInsuficienteError(
                message=(
                    f"Stock insuficiente en {ubicacion.codigo_ubicacion}: "
                    f"disponible {disponible}, solicitado {dto.cantidad}"
                ),
                disponible=disponible,
                solicitado=dto.cantidad,
            )

        # 4. Decrementar stock
        await self._inventario_repo.upsert(
            producto_id=dto.producto_id,
            ubicacion_id=dto.ubicacion_origen_id,
            delta_cantidad=-dto.cantidad,
        )

        # 5. Registrar movimiento
        movimiento = Movimiento(
            tipo=TipoMovimiento.SALIDA,
            producto_id=dto.producto_id,
            cantidad=dto.cantidad,
            usuario_id=usuario_id,
            ubicacion_origen_id=dto.ubicacion_origen_id,
            ubicacion_destino_id=None,
            referencia=dto.referencia,
            observaciones=dto.observaciones,
        )
        errores = movimiento.validar()
        if errores:
            raise MovimientoInvalidoError(errores=errores)

        creado = await self._movimiento_repo.create(movimiento)
        return MovimientoReadDTO.model_validate(creado)