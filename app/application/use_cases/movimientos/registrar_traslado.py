"""Caso de uso: registrar un traslado entre dos ubicaciones."""

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


class RegistrarTrasladoUseCase:
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
        if dto.tipo != TipoMovimiento.TRASLADO:
            raise MovimientoInvalidoError(
                "Este caso de uso solo acepta movimientos de tipo TRASLADO"
            )
        if dto.ubicacion_origen_id is None or dto.ubicacion_destino_id is None:
            raise MovimientoInvalidoError(
                "Un TRASLADO requiere ubicación origen y destino"
            )
        if dto.ubicacion_origen_id == dto.ubicacion_destino_id:
            raise MovimientoInvalidoError(
                "Origen y destino no pueden ser la misma ubicación"
            )

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

        # 2. Validar ubicaciones
        origen = await self._ubicacion_repo.get_by_id(dto.ubicacion_origen_id)
        if origen is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": dto.ubicacion_origen_id}
            )
        destino = await self._ubicacion_repo.get_by_id(dto.ubicacion_destino_id)
        if destino is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": dto.ubicacion_destino_id}
            )

        # 3. Verificar stock en origen
        actual = await self._inventario_repo.get_by_producto_y_ubicacion(
            dto.producto_id, dto.ubicacion_origen_id
        )
        disponible = actual.cantidad if actual is not None else 0
        if disponible < dto.cantidad:
            raise StockInsuficienteError(
                message=(
                    f"Stock insuficiente en {origen.codigo_ubicacion}: "
                    f"disponible {disponible}, solicitado {dto.cantidad}"
                ),
                disponible=disponible,
                solicitado=dto.cantidad,
            )

        # 4. Decrementar en origen y luego incrementar en destino.
        #    Si el segundo falla, el rollback del test/endpoint deshace todo.
        await self._inventario_repo.upsert(
            producto_id=dto.producto_id,
            ubicacion_id=dto.ubicacion_origen_id,
            delta_cantidad=-dto.cantidad,
        )
        await self._inventario_repo.upsert(
            producto_id=dto.producto_id,
            ubicacion_id=dto.ubicacion_destino_id,
            delta_cantidad=dto.cantidad,
        )

        # 5. Registrar movimiento
        movimiento = Movimiento(
            tipo=TipoMovimiento.TRASLADO,
            producto_id=dto.producto_id,
            cantidad=dto.cantidad,
            usuario_id=usuario_id,
            ubicacion_origen_id=dto.ubicacion_origen_id,
            ubicacion_destino_id=dto.ubicacion_destino_id,
            referencia=dto.referencia,
            observaciones=dto.observaciones,
        )
        errores = movimiento.validar()
        if errores:
            raise MovimientoInvalidoError(errores=errores)

        creado = await self._movimiento_repo.create(movimiento)
        return MovimientoReadDTO.model_validate(creado)