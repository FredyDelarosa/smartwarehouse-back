"""Caso de uso: iniciar una búsqueda de producto."""

from __future__ import annotations

from app.application.dtos import (
    IniciarBusquedaDTO,
    ProductoReadDTO,
    ResultadoBusquedaDTO,
    UbicacionConStockDTO,
)
from app.domain.entities import Busqueda
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories import (
    BusquedaRepository,
    InventarioRepository,
    ProductoRepository,
    UbicacionRepository,
)


class IniciarBusquedaUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        inventario_repo: InventarioRepository,
        ubicacion_repo: UbicacionRepository,
        busqueda_repo: BusquedaRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._inventario_repo = inventario_repo
        self._ubicacion_repo = ubicacion_repo
        self._busqueda_repo = busqueda_repo

    async def execute(
        self, dto: IniciarBusquedaDTO, usuario_id: int
    ) -> ResultadoBusquedaDTO:
        # 1. Determinar el producto a buscar
        if dto.producto_id is not None:
            producto = await self._producto_repo.get_by_id(dto.producto_id)
        else:
            coincidencias = await self._producto_repo.search(
                dto.termino_busqueda, limit=1
            )
            producto = coincidencias[0] if coincidencias else None

        if producto is None or producto.id is None:
            raise ProductoNoEncontradoError(
                details={"termino": dto.termino_busqueda}
            )

        # 2. Distribución de stock por ubicación
        inventarios = await self._inventario_repo.list_by_producto(producto.id)
        ubicaciones: list[UbicacionConStockDTO] = []
        stock_total = 0
        for inv in inventarios:
            ubicacion = await self._ubicacion_repo.get_by_id(inv.ubicacion_id)
            if ubicacion is None:
                continue
            stock_total += inv.cantidad
            ubicaciones.append(
                UbicacionConStockDTO(
                    ubicacion_id=ubicacion.id or 0,
                    codigo_ubicacion=ubicacion.codigo_ubicacion,
                    pasillo=ubicacion.pasillo,
                    estante=ubicacion.estante,
                    nivel=ubicacion.nivel,
                    cantidad=inv.cantidad,
                )
            )
        ubicaciones.sort(key=lambda u: u.codigo_ubicacion)

        # 3. Abrir el registro de búsqueda
        busqueda = Busqueda(
            usuario_id=usuario_id,
            termino_busqueda=dto.termino_busqueda,
            producto_id=producto.id,
        )
        busqueda.iniciar()
        guardada = await self._busqueda_repo.create(busqueda)

        # 4. Armar la respuesta
        return ResultadoBusquedaDTO(
            busqueda_id=guardada.id,
            producto=ProductoReadDTO.model_validate(producto),
            stock_total=stock_total,
            ubicaciones=ubicaciones,
        )