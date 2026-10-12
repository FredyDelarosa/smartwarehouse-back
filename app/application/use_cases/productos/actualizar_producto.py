"""Caso de uso: actualizar un producto existente."""

from __future__ import annotations

from app.application.dtos import ProductoReadDTO, ProductoUpdateDTO
from app.domain.exceptions import (
    CodigoProductoDuplicadoError,
    EntidadNoEncontradaError,
    ProductoNoEncontradoError,
    ValidacionError,
)
from app.domain.repositories import CategoriaRepository, ProductoRepository
from app.domain.value_objects import CodigoProducto


class ActualizarProductoUseCase:
    def __init__(
        self,
        producto_repo: ProductoRepository,
        categoria_repo: CategoriaRepository,
    ) -> None:
        self._producto_repo = producto_repo
        self._categoria_repo = categoria_repo

    async def execute(
        self, producto_id: int, dto: ProductoUpdateDTO
    ) -> ProductoReadDTO:
        # 1. Recuperar producto
        producto = await self._producto_repo.get_by_id(producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(
                details={"producto_id": producto_id}
            )

        # 2. Si cambia el código, validar VO + unicidad
        if dto.codigo is not None:
            try:
                codigo_vo = CodigoProducto(dto.codigo)
            except ValueError as exc:
                raise ValidacionError(str(exc), errores=[str(exc)]) from exc

            if codigo_vo.valor != producto.codigo:
                existente = await self._producto_repo.get_by_codigo(
                    codigo_vo.valor
                )
                if existente is not None and existente.id != producto.id:
                    raise CodigoProductoDuplicadoError(
                        details={"codigo": codigo_vo.valor}
                    )
                producto.codigo = codigo_vo.valor

        # 3. Si cambia la categoría, verificar que exista
        if dto.categoria_id is not None:
            categoria = await self._categoria_repo.get_by_id(dto.categoria_id)
            if categoria is None:
                raise EntidadNoEncontradaError(
                    "Categoría no encontrada",
                    details={"categoria_id": dto.categoria_id},
                )
            producto.categoria_id = dto.categoria_id

        # 4. Copiar el resto de campos provistos
        if dto.nombre is not None:
            producto.nombre = dto.nombre.strip()
        if dto.descripcion is not None:
            producto.descripcion = dto.descripcion
        if dto.unidad_medida is not None:
            producto.unidad_medida = dto.unidad_medida
        if dto.stock_minimo is not None:
            producto.stock_minimo = dto.stock_minimo
        if dto.foto_url is not None:
            producto.foto_url = dto.foto_url
        if dto.activo is not None:
            producto.activo = dto.activo

        # 5. Validación de negocio de la entidad
        errores = producto.validar()
        if errores:
            raise ValidacionError(errores=errores)

        # 6. Persistir
        actualizado = await self._producto_repo.update(producto)
        return ProductoReadDTO.model_validate(actualizado)