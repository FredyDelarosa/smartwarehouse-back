"""Caso de uso: crear un producto."""

from __future__ import annotations

from app.application.dtos import ProductoCreateDTO, ProductoReadDTO
from app.domain.entities import Producto
from app.domain.exceptions import (
    CodigoProductoDuplicadoError,
    EntidadNoEncontradaError,
    ValidacionError,
)
from app.domain.repositories import CategoriaRepository, ProductoRepository
from app.domain.value_objects import CodigoProducto


class CrearProductoUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        categoria_repo: CategoriaRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._categoria_repo = categoria_repo

    async def execute(
        self, dto: ProductoCreateDTO, almacen_id: int
    ) -> ProductoReadDTO:
        # 1. Validar y normalizar el código con el value object
        try:
            codigo_vo = CodigoProducto(dto.codigo)
        except ValueError as exc:
            raise ValidacionError(str(exc), errores=[str(exc)]) from exc

        # 2. Verificar unicidad del código
        if await self._producto_repo.get_by_codigo(codigo_vo.valor) is not None:
            raise CodigoProductoDuplicadoError(
                details={"codigo": codigo_vo.valor}
            )

        # 3. Verificar categoría si se especifica
        if dto.categoria_id is not None:
            categoria = await self._categoria_repo.get_by_id(dto.categoria_id)
            if categoria is None:
                raise EntidadNoEncontradaError(
                    "Categoría no encontrada",
                    details={"categoria_id": dto.categoria_id},
                )

        # 4. Construir la entidad y validarla
        producto = Producto(
            # Sin esto, la entidad caía al valor por defecto y TODO producto
            # creado acababa en el almacén 1: quien notificaba desde el
            # almacén 2 escribía dentro del almacén 1 sin enterarse. Con el
            # índice único por almacén, eso además salía como un 500 de
            # "Duplicate entry" al crear un E001 que ya existía allí.
            almacen_id=almacen_id,
            codigo=codigo_vo.valor,
            nombre=dto.nombre.strip(),
            descripcion=dto.descripcion,
            categoria_id=dto.categoria_id,
            unidad_medida=dto.unidad_medida,
            stock_minimo=dto.stock_minimo,
            foto_url=dto.foto_url,
            activo=dto.activo,
        )
        errores = producto.validar()
        if errores:
            raise ValidacionError(errores=errores)

        # 5. Persistir
        creado = await self._producto_repo.create(producto)
        return ProductoReadDTO.model_validate(creado)